from rapidfuzz import process, fuzz
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.report import ReportAnalysis


def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("inc", "")
        .replace("ltd", "")
        .replace("corp", "")
        .replace("company", "")
        .replace(".", "")
        .strip()
    )

def find_closest_companies(
    session: Session,
    user_input: str,
    chunk_size: int = 100,
    min_confidence: float = 0.75,
    max_results: int = 5,
):
    """
    Returns up to `max_results` likely company matches based on fuzzy matching.
    """

    normalized_input = normalize(user_input)
    offset = 0
    likely_matches = []

    while True:
        # Fetch next chunk
        companies = (
            session.query(ReportAnalysis.id, ReportAnalysis.company_name)
            .order_by(ReportAnalysis.id)
            .offset(offset)
            .limit(chunk_size)
            .all()
        )

        if not companies:
            break  # No more rows in DB

        # Prepare choices for RapidFuzz
        choices = {
            c.id: normalize(c.company_name)
            for c in companies
        }

        matches = process.extract(
            normalized_input,
            choices,
            scorer=fuzz.WRatio,
            limit=len(choices)
        )

        for _, score, company_id in matches:
            confidence = score / 100.0
            if confidence >= min_confidence:
                company = next(c for c in companies if c.id == company_id)
                likely_matches.append({
                    "id": company.id,
                    "company_name": company.company_name,
                    "confidence": confidence,
                })

        if len(likely_matches) >= max_results:
            break

        offset += chunk_size

    # Sort final results by confidence
    likely_matches.sort(key=lambda x: x["confidence"], reverse=True)

    return likely_matches[:max_results]
