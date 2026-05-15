from tool_logger import log_tool_call

domains = {

    "technology": {
        "intel", "amd", "nvidia", "процесор", "cpu", "gpu",
        "ядро", "сервер", "память", "компьютер",
        "ноутбук", "мережа", "алгоритм", "ai",
        "штучний", "дані", "програмування", "код",
        "python", "java", "linux", "windows",
        "база", "database", "cloud", "кібербезпека",
        "чип", "робот", "автоматизація", "інтернет",
        "веб", "software", "hardware"
    },

    "biology": {
        "клітина", "генетичний", "біологія",
        "днк", "рнк", "ядро", "синтез",
        "організм", "бактерія", "вірус",
        "еволюція", "ген", "мікроб",
        "тканина", "фермент", "мутація",
        "молекула", "екосистема", "фотосинтез",
        "біохімія", "нейрон", "хромосома"
    },

    "science": {
        "дослідження", "синтез",
        "аналіз", "експеримент",
        "теорія", "модель", "фізика",
        "хімія", "математика", "формула",
        "статистика", "лабораторія",
        "спостереження", "гіпотеза",
        "відкриття", "квантовий",
        "енергія", "реакція"
    },

    "economy": {
        "економіка", "ринок", "банк",
        "інфляція", "валюта", "гривня",
        "долар", "євро", "кредит",
        "податок", "інвестиція", "бюджет",
        "фінанси", "акції", "біржа", "нафту",
        "бізнес", "компанія", "прибуток",
        "зарплата", "експорт", "імпорт",
        "торгівля", "капітал", "ціна", "ціни"
    },

    "politics": {
        "уряд", "парламент", "президент",
        "вибори", "закон", "політика",
        "депутат", "міністр", "санкції",
        "нато", "альянс", "влада",
        "конституція", "реформа",
        "дипломатія", "саміт",
        "війна", "оборона", "держава",
        "голосування", "партія"
    },

    "culture": {
        "культура", "мистецтво",
        "музика", "театр", "кіно",
        "фільм", "література", "роман",
        "поезія", "традиція", "музей",
        "виставка", "художник",
        "актор", "концерт", "фестиваль",
        "танець", "пісня", "архітектура",
        "спадщина"
    },

    "sports": {
        "спорт", "футбол", "баскетбол",
        "теніс", "матч", "турнір",
        "олімпіада", "команда",
        "чемпіонат", "гол", "тренер",
        "гравець", "стадіон", "медаль",
        "перемога", "поразка",
        "біг", "фітнес", "рекорд",
        "ліга"
    },

    "health": {
        "здоров’я", "лікар", "хвороба",
        "пацієнт", "медицина", "лікування",
        "вакцина", "вірус", "епідемія",
        "симптом", "діагноз",
        "терапія", "операція",
        "імунітет", "психологія",
        "харчування", "стрес",
        "реабілітація", "клініка",
        "антибіотик"
    },

    "gardening": {
        "сад", "город", "рослина", "квітка",
        "дерево", "кущ", "насіння", "ґрунт",
        "полив", "добриво", "врожай",
        "теплиця", "садівництво", "газон",
        "троянда", "тюльпан", "томат",
        "огірок", "картопля", "бур’ян",
        "лопата", "граблі", "компост",
        "мульча", "саджанці", "пересадка",
        "обрізка", "земля", "овочі",
        "фрукти", "ягоди", "перець",
        "морква", "цибуля", "зелень"
    }
}


@log_tool_call
def detect_noise_words(top_words: list) -> dict:
    if not top_words: 
        raise ValueError("Empty top_words and top_docs lists provided")
    stop_words = {"та", "що", "це", "був", "було", "воно", "їх", "його", "але", "для", "про", "як", "сказав", "року"}
    noise = [word for word in top_words if word.lower() in stop_words or len(word) < 2]
    is_noise = False
    if noise: is_noise = True
    return {"is_noise": is_noise, "noise_words": noise}

@log_tool_call
def suggest_topic_label(top_words: list, top_docs: list) -> dict:
    if not top_words and not top_docs: 
        raise ValueError("Empty top_words and top_docs lists provided")
    
    words_lower = [w.lower() for w in top_words]
    docs_text = " ".join(top_docs).lower()

    domain_scores = {}
    for domain, keywords in domains.items():
        score = 0
        for word in words_lower:
            if word in keywords:
                score += 1
        for kw in keywords:
            if kw in docs_text:
                score += 1
        domain_scores[domain] = score

    active_domains = [
        domain
        for domain, score in domain_scores.items()
        if score > 0
    ]

    if not active_domains:
        classification = "unknown"
    else:
        classification = "/".join(active_domains)

    return {"classification": classification}


@log_tool_call
def score_topic_quality(top_words: list, top_docs: list) -> dict:
    if not top_words or not top_docs:
        return {"quality": "bad", "score": 0.0}

    words_lower = [w.lower() for w in top_words]
    docs_text = " ".join(top_docs).lower()

    domain_scores = {}

    for domain, keywords in domains.items():
        score = 0
        for word in words_lower:
            if word in keywords:
                score += 1
        for kw in keywords:
            if kw in docs_text:
                score += 1
        domain_scores[domain] = score

    active_domains = [
        domain
        for domain, score in domain_scores.items()
        if score > 0
    ]

    if len(active_domains) == 1:
        quality = "good"
    elif len(active_domains) > 1:
        quality = "mixed"
    else:
        quality = "bad"

    return {"quality": quality}


tools_map = {
    "detect_noise_words": detect_noise_words,
    "suggest_topic_label": suggest_topic_label,
    "score_topic_quality": score_topic_quality
}