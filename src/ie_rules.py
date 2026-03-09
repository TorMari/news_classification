import re

months = r"(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)"
DATE_PATTERN = re.compile(rf"\b\d{{1,2}}\s+{months}(?:\s+\d{{4}})?", re.IGNORECASE)
AMOUNT_PATTERN = re.compile(r"\b\d+[.,]?\d*\s?(млн|млрд)?\s?(грн|₴|€|uah|долар(ів)?|usd|eur)\b", re.IGNORECASE) 
SCORE_PATTERN = re.compile(r"(?<!\bо\s)(?<!\bоб\s)(?<!\bз\s)(?<!\bдо\s)(?<!\bпісля\s)\b\d{1,2}[:]\d{1,2}\b", re.IGNORECASE)

def extract_dates(text_id, text):

    results = []

    for m in DATE_PATTERN.finditer(text):

        results.append({
            "text_id": text_id,
            "field_type": "DATE",
            "value": m.group(),
            "start_char": m.start(),
            "end_char": m.end(),
            "method": "regex_date_v1"
        })

    return results


def extract_amounts(text_id, text):

    results = []

    for m in AMOUNT_PATTERN.finditer(text):

        results.append({
            "text_id": text_id,
            "field_type": "AMOUNT",
            "value": m.group(),
            "start_char": m.start(),
            "end_char": m.end(),
            "method": "regex_amount_v1"
        })

    return results


def extract_scores(text_id, text):

    results = []

    for m in SCORE_PATTERN.finditer(text):

        results.append({
            "text_id": text_id,
            "field_type": "SCORE",
            "value": m.group(),
            "start_char": m.start(),
            "end_char": m.end(),
            "method": "regex_score_v1"
        })

    return results


def extract_all(text_id, text):

    return {
        "DATE": extract_dates(text_id, text),
        "AMOUNT": extract_amounts(text_id, text),
        "SCORE": extract_scores(text_id, text)
    }