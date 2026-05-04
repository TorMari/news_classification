test_examples = [
  {
    "case_id": "case_001",
    "description": "Простий кейс (Happy Path)",
    "input": "Компанія Apple інвестувала 2 мільярди доларів у розвиток штучного інтелекту 15 травня 2024 року в США.",
    "expected_behavior": "Extract all fields correctly: Apple, investment, 2000000000, USD, 2024-05-15, USA. No repair needed."
  },
  {
    "case_id": "case_002",
    "description": "Missing required field",
    "input": "Стало відомо про інвестицію у розмірі 100 млн євро, яку виділили для стартапу минулого тижня.",
    "expected_behavior": "Validator should flag missing 'company' and 'location'; trigger repair or fail."
  },
  {
    "case_id": "case_003",
    "description": "Ambiguous entity",
    "input": "Amazon купує частину бізнесу своєї дочірньої компанії Amazon Robotics.",
    "expected_behavior": "Extract main company 'Amazon' (mentioned first) and event 'acquisition'; handle naming ambiguity."
  },
  {
    "case_id": "case_004",
    "description": "Relative date",
    "input": "Вчора корпорація Microsoft підписала партнерську угоду на суму 300 млн доларів.",
    "expected_behavior": "Normalize 'Вчора' to a specific YYYY-MM-DD date based on current metadata."
  },
  {
    "case_id": "case_005",
    "description": "Potential Hallucination",
    "input": "Tesla оголосила про запуск нового заводу в Німеччині. Аналітики вважають, що це коштуватиме мільярди.",
    "expected_behavior": "Amount should be 'null' because 'мільярди' is a vague estimate, not a specific number. Prevent model from inventing a digit."
  },
  {
    "case_id": "case_006",
    "description": "Noisy text / Typos",
    "input": "Googlr інвестує 500млн $ у Францію (Париж).",
    "expected_behavior": "Fix typo 'Googlr' -> 'Google'; extract '500000000', 'USD', 'France'."
  },
  {
    "case_id": "case_007",
    "description": "Fallback scenario",
    "input": "У новому звіті йдеться про велику угоду в агросекторі між двома фермерськими господарствами.",
    "expected_behavior": "Extractor fails to find specific names/amounts; system returns empty schema or marks as 'other' for fallback processing."
  },
  {
    "case_id": "case_008",
    "description": "Reviewer rejection",
    "input": "Акції Apple зросли на 5.5% після презентації в Купертіно.",
    "expected_behavior": "Reviewer/Validator should reject this as 'investment' because stock price change is not a corporate investment event."
  },
  {
    "case_id": "case_009",
    "description": "Repair loop helps",
    "input": "Meta виділяє 1 мільярд євро на безпеку.",
    "expected_behavior": "Initial output might miss 'location'. Repair prompt asks for location; model finds context or sets to null/location from metadata."
  },
  {
    "case_id": "case_010",
    "description": "Repair fails / Manual review",
    "input": "Компанія X-Corp (колишня Twitter) уклала угоду з приватною фірмою в ОАЕ.",
    "expected_behavior": "Model confuses X-Corp with SpaceX or fails to extract amount. After 2 repair attempts, flag for manual review."
  }
]