import json
from copy import deepcopy
from functools import lru_cache
from venv import logger
from services.ai_prompt import single_prompt_answer

sys_prompt_business_strategy = """
You are a corporate strategy analyst.

Analyze the following text from a company's annual report.

Extract ONLY information related to:
- what the company is trying to achieve
- its business focus
- its positioning
- its strategic direction
- how it differentiates itself

Ignore risks, financial figures, and general background.

Return ONLY a JSON object that fits this schema:

{
  "summary": "string or null",
  "core_focus": ["string"],
  "competitive_advantages": ["string"],
  "strategic_direction": "string or null"
}

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
Do NOT return explanations.
"""

sys_prompt_risk_analysis = """
You are a risk and compliance analyst.

Analyze the following text from a company's annual report.

Extract ONLY:
- risks
- uncertainties
- exposures
- weaknesses
- how the company discusses managing those risks

Return ONLY a JSON object that fits:

{
  "risk_posture": "Low | Moderate | High | Unknown",
  "key_risks": ["string"],
  "risk_management_approach": "string or null",
  "tone": "Proactive | Defensive | Vague | Transparent | Mixed | Unknown"
}

Do not include strategy, growth, or financial metrics.
Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
Do NOT return explanations.
"""

sys_prompt_market_sentiment = """
You are a market sentiment analyst.

Analyze the tone and confidence expressed in this text.

Extract:
- how positive or negative management sounds
- how confident they appear about the future
- signals of optimism, caution, or uncertainty

Return ONLY a JSON object that fits:

{
  "sentiment": "Positive | Neutral | Negative | Mixed | Unknown",
  "confidence_level": "High | Medium | Low | Unknown",
  "supporting_signals": ["string"]
}

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
Do NOT return explanations.
"""

sys_prompt_qualitative_performance = """
You are an operations and execution analyst.

Analyze the text for how well the company describes:
- its operations
- execution
- stability
- efficiency
- ability to deliver

Ignore strategy, growth plans, and risks.

Return ONLY a JSON object that fits:

{
  "operational_strength": "Strong | Stable | Weak | Unknown",
  "business_stability": "Stable | Volatile | Declining | Unknown",
  "execution_capability": "High | Medium | Low | Unknown",
  "summary": "string or null"
}

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
Do NOT return explanations.
"""

sys_prompt_growth_potential = """
You are a growth and opportunity analyst.

Analyze the text for:
- future expansion
- demand
- opportunities
- market size
- constraints on growth

Return ONLY a JSON object that fits:

{
  "level": "High | Medium | Low | Unknown",
  "growth_drivers": ["string"],
  "constraints": ["string"],
  "summary": "string or null"
}

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
Do NOT return explanations.
"""

@lru_cache
def __cache_signals():
    return {
        'business_strategy',
        'growth_potential',
        'risk_analysis',
        'qualitative_performance',
        'market_sentiment'
    }

@lru_cache
def __cache_mapping():
    return {
        'business_strategy': sys_prompt_business_strategy,
        'growth_potential': sys_prompt_growth_potential,
        'risk_analysis': sys_prompt_risk_analysis,
        'qualitative_performance': sys_prompt_qualitative_performance,
        'market_sentiment': sys_prompt_market_sentiment
    }

def group_signals(data):
    signals = __cache_signals()
    res = {}

    for signal in signals:
        res[signal] = {'text': '', 'sources': []}

    for page_no, info in data.items():
        signal_list = info.get('category', {}).get('market_signals')
        for signal in signal_list:
            if signal not in res:
                continue
            res[signal]['text'] += info.get('text', '')
            res[signal]['sources'].append(int(page_no))

    return res


def extract_text_signal(data):
    # logger.info('debug before group')
    groupped_data = group_signals(data)
    # logger.info('debug after group')
    mapping = __cache_mapping()
    for signal, info in groupped_data.items():
        text = info['text']
        # logger.info(f'debug signal: {signal}')
        if signal not in mapping:
            continue
        sys_prompt = mapping[signal]
        data_str = single_prompt_answer(sys_prompt, text)
        if not data_str: data_str = ''
        info['data'] = json.loads(data_str)
    return groupped_data

