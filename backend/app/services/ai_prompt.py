import json
from venv import logger
import time
import random
from collections import deque
from datetime import datetime, timezone
from typing import Type
from functools import lru_cache

from app.core.config import settings

from pydantic import BaseModel
from google import genai
from google.genai import types

from pydantic import BaseModel

client = None

class GeminiRateLimitedClient:
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        rpm_limit: int = 60,
        tpm_limit: int = 200_000,
        rpd_limit: int = 10_000,
        max_retries: int = 5,
        base_backoff: float = 1.0,
        max_backoff: float = 30.0,
    ):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY) 
        self.model = model

        # ---- quotas ----
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        self.rpd_limit = rpd_limit

        # ---- retry policy ----
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff

        # ---- state ----
        self.request_times = deque()
        self.token_times = deque()   # (timestamp, tokens)
        self.daily_count = 0
        self.daily_reset = datetime.now(timezone.utc).date()

    # -------------------------
    # Internal helpers
    # -------------------------
    def _reset_daily_if_needed(self):
        today = datetime.now(timezone.utc).date()
        if today != self.daily_reset:
            self.daily_reset = today
            self.daily_count = 0
            logger.info("Daily quota reset")

    def _prune_old_entries(self, now: float):
        while self.request_times and now - self.request_times[0] > 60:
            self.request_times.popleft()

        while self.token_times and now - self.token_times[0][0] > 60:
            self.token_times.popleft()

    def _estimate_tokens(self, text: str) -> int:
        # rough but good enough for throttling
        return max(1, len(text) // 4)

    def _wait_for_quota(self, estimated_tokens: int):
        while True:
            now = time.time()
            self._prune_old_entries(now)

            rpm_used = len(self.request_times)
            tpm_used = sum(t for _, t in self.token_times)

            if rpm_used < self.rpm_limit and tpm_used + estimated_tokens < self.tpm_limit:
                return

            sleep_for = random.uniform(0.5, 1.5)
            logger.debug(
                f"Throttling Gemini calls "
                f"(RPM={rpm_used}/{self.rpm_limit}, "
                f"TPM={tpm_used}/{self.tpm_limit}), "
                f"sleeping {sleep_for:.2f}s"
            )
            time.sleep(sleep_for)

    def _record_usage(self, tokens: int):
        now = time.time()
        self.request_times.append(now)
        self.token_times.append((now, tokens))
        self.daily_count += 1

    def _is_retryable_error(self, exc: Exception) -> bool:
        msg = str(exc).lower()
        return any(
            key in msg
            for key in (
                "429",
                "rate",
                "timeout",
                "unavailable",
                "500",
                "internal",
            )
        )

    # -------------------------
    # Public API
    # -------------------------
    def single_prompt_answer(
        self,
        sys_prompt: str,
        usr_prompt: str,
        response_schema: Type[BaseModel] | None = None,
    ):
        self._reset_daily_if_needed()

        if self.daily_count >= self.rpd_limit:
            logger.error("Gemini daily request quota exceeded (RPD)")
            return None

        estimated_tokens = self._estimate_tokens(sys_prompt + usr_prompt)
        self._wait_for_quota(estimated_tokens)

        response_mime_type = (
            "application/json" if response_schema else None
        )

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=types.Part.from_text(text=usr_prompt),
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt,
                        response_schema=response_schema,
                        response_mime_type=response_mime_type,
                        temperature=0,
                        top_p=0.95,
                        top_k=20,
                    ),
                )

                self._record_usage(estimated_tokens)

                return response.parsed if response_schema else response.text

            except Exception as e:
                if not self._is_retryable_error(e) or attempt == self.max_retries:
                    logger.exception("Gemini request failed permanently")
                    return None

                backoff = min(
                    self.base_backoff * (2 ** (attempt - 1)),
                    self.max_backoff,
                ) + random.uniform(0, 0.5)

                logger.warning(
                    f"Gemini request failed "
                    f"(attempt {attempt}/{self.max_retries}), "
                    f"retrying in {backoff:.2f}s: {e}"
                )
                time.sleep(backoff)

def get_gemini_client():
    global client
    if client: return client
    client = GeminiRateLimitedClient()
    return client