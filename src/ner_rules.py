import re

def extract_dates(text):
    months_list = (
        r"січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня|"
        r"січні|лютому|березні|квітні|травні|червні|липні|серпні|вересні|жовтні|листопаді|грудні"
    )

    pattern = rf"""
      \b(
          \d{{1,2}}\s+({months_list})\s+\d{{4}}(\s?(року|році|рік))? |
          \d{{1,2}}\s+({months_list}) |
          ({months_list})\s+\d{{4}} |
          \d{{4}}\s?(року|році|рік)
      )\b
    """
    
    results = []
    for match in re.finditer(pattern, text, re.VERBOSE | re.IGNORECASE):
        date_str = match.group(0).strip()
        results.append((date_str, "DATE"))
    
    return results

def extract_money(text):
    pattern = r"\b(\d+\s?(тис|тисяча|тисяч|тисячі|мільярда|мільярд|мільярдів|млрд|мільйонів|мільйон|мільйона|мільйонів гривень|млн|грн|гривень|доларів|євро)|(\$|€)\s?\d+)\b"
    
    results = []
    for match in re.finditer(pattern, text):
        results.append((match.group(), "MONEY"))
    
    return results

def extract_organization(text):
    pattern = r"\b\s?(ООН|НАТО|ЄС|Єврокомісія|Європейська комісія|Верховна Рада|Кабмін|Мінфін|Мінекономіки|СБУ|НБУ|МВФ|Світовий банк|USAID|UNICEF|Google|Microsoft|Apple|Amazon|Meta|Tesla|SpaceX|Warner Bros|Disney|BBC|Netflix|ЮНІДО|Європарламент|БЕБ)\b"
    
    results = []
    for match in re.finditer(pattern, text):
        results.append((match.group(), "ORG"))
    
    return results

def merge_person_entities(entities):
    merged = []
    i = 0
    
    while i < len(entities):
        word, label = entities[i]
        
        if label == "PERS" and i + 1 < len(entities):
            next_word, next_label = entities[i + 1]
            
            if next_label == "PER":
                merged.append((word + " " + next_word, "PERS"))
                i += 2
                continue
        
        merged.append((word, label))
        i += 1
    
    return merged

def apply_hybrid_rules(text, stanza_entities):
    results = list(stanza_entities)
    
    results.extend(extract_dates(text))
    results.extend(extract_money(text))
    results.extend(extract_organization(text))
    
    results = merge_person_entities(results)
    results = list(set(results))
    
    return results


