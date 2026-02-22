import re
from typing import List, Dict

URL_RE = re.compile(r'https?://[^\s\)\]\}\>,]+')
EMAIL_RE = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b')
PHONE_RE = re.compile(r'\+\d[\d\-\(\) ]{7,}\d')
LONG_ID_RE = re.compile(r'\b\d{8,}\b')
HTML_RE = re.compile(r'<[^>]+>')
HTML_RE = re.compile(
    r'<(?!/?(?:URL|EMAIL|PHONE|ID)\b)[^>]+>',
    re.IGNORECASE
)

ABBREVIATIONS = [
    "м.", "вул.", "р.", "рр.", "т.д.", "т.п.", "ім.", "тис.", "дол."
]

PHOTO_CREDIT_RE = re.compile(
    r'(Фото\s*[^.!\n]*|[^.!\n]*?(Укрінформу|Getty|Reuters)[^.!\n]*купити тут)',
    re.IGNORECASE
)

SOCIAL_CREDIT_RE = re.compile(
    r'(Допис|Повідомлення|Публікація)[^(@\n]+?\(@[^)]+\)',
    re.IGNORECASE
)

HOMOGRAPHS = {
    "a": "а", "e": "е", "o": "о", "i": "і", "y": "у", "p": "р", "c": "с", "x": "х"
}

def replace_homographs(word: str) -> str:
    if re.search(r"[а-яіїєґ]", word, re.IGNORECASE):
        for src, dst in HOMOGRAPHS.items():
            word = word.replace(src, dst)
    return word

def remove_photo_credits(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r'Читайте також:', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\.?\s*Більше фото[^.!\n]*', ' ', text, flags=re.IGNORECASE)
    text = PHOTO_CREDIT_RE.sub(" ", text)
    text = SOCIAL_CREDIT_RE.sub(" ", text)

    return text.strip()


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = HTML_RE.sub(" ", text)
    text = remove_photo_credits(text)
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def normalize_text(text: str) -> str:
    text = re.sub(r'[«»“”„]', '"', text)
    text = re.sub(r"[’`´]", "'", text)
    text = re.sub(r'[–—−]', '-', text)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)

    words = text.split()
    words = [replace_homographs(w) for w in words]
    text = " ".join(words)
    return text.strip()


def mask_pii(text: str) -> str:
    text = URL_RE.sub("<URL>", text)
    text = EMAIL_RE.sub("<EMAIL>", text)
    text = PHONE_RE.sub("<PHONE>", text)
    return text


def sentence_split(text: str) -> List[str]:
    protected = text
    protected = re.sub(r'(\d{1,2}:\d{2})\.', r'\1<DOT_>', text)

    protected = re.sub(
        r'(\d+)\.(?=\s+[A-ZА-ЯІЇЄҐ"])',
        r'\1<DOT>',
        protected
    )
    for abbr in ABBREVIATIONS:
        protected = protected.replace(abbr, abbr.replace(".", "<DOT>"))
   
    protected = protected.replace('<DOT_>', '.')
    sentences = re.split(r'(?<=[.!?])\s+', protected)
    sentences = [s.replace('<DOT>', '.') for s in sentences]
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def preprocess(text: str) -> Dict:
    clean = clean_text(text)
    norm = normalize_text(clean)
    masked = mask_pii(norm)
    sentences = sentence_split(masked)

    return {
        "clean": masked,
        "sentences": sentences
    }