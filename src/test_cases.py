test_cases = [
  {
    "case_id": "case_001", 
    "case_type": "simple_case", 
    "top_words": ["НАТО", "альянс", "оборона", "саміт", "Брюссель"], 
    "top_docs": ["Лідери НАТО зібралися на саміт у Брюсселі", "Питання колективної оборони обговорено на зустрічі альянсу"], 
    "expected": {"classification": "politics", "quality": "good", "is_noise": False, "noise_words": []}
  },
  {
    "case_id": "case_002", 
    "case_type": "missing_data", 
    "top_words": [], 
    "top_docs": ["Ціни на нафту зросли на 5%", "Барель марки Brent торгується за новою ціною"], 
    "expected": {"classification": "economy", "quality": "mixed/bad", "is_noise": False, "noise_words": []}
  },
  {
    "case_id": "case_003", 
    "case_type": "noisy_text", 
    "top_words": ["та", "що", "сказав", "це", "року", "воно", "їх", "було"], 
    "top_docs": ["Компанія X-Corp (колишня Twitter) уклала угоду з приватною фірмою в ОАЕ", "В Україні торік зареєстрували 267 видавців і книгарень"], 
    "expected": {"classification": "economy/culture", "quality": "bad", "is_noise": True, "noise_words": ["та", "що", "сказав", "це", "року", "воно", "їх", "було"]}
  },
  {
    "case_id": "case_004", 
    "case_type": "empty_tool_result", 
    "top_words": ["qwe12", "xyz_4", "10101", "err_log", "як"], 
    "top_docs": ["Системне повідомлення qwe12", "Лог помилок 10101"], 
    "expected": {"classification": "-", "quality": "bad", "is_noise": True, "noise_words": ["як"]}
  },
  {
    "case_id": "case_005", 
    "case_type": "no_redundant_tools", 
    "top_words": ["футбол", "чемпіонат", "гол", "стадіон", "ФІФА"], 
    "top_docs": ["Фінал чемпіонату світу", "Забитий гол на стадіоні"], 
    "expected": {"classification": "sports", "quality": "good", "is_noise": False, "noise_words": []}
  },
  {
    "case_id": "case_006", 
    "case_type": "ambiguity", 
    "top_words": ["ядро", "процесор", "клітина", "біологія", "Intel", "синтез"], 
    "top_docs": ["Новий процесор Intel має 16 ядер", "Ядро клітини містить генетичний код"], 
    "expected": {"classification": "technology/biology/science", "quality": "mixed", "is_noise": False, "noise_words": []}
  },
  {
    "case_id": "case_007", 
    "case_type": "sequential_tools", 
    "top_words": ["гривня", "НБУ", "інфляція", "курс", "долар"], 
    "top_docs": ["НБУ встановив офіційний курс", "Інфляція в Україні сповільнилася"], 
    "expected": {"classification": "economy", "quality": "good", "is_noise": False, "noise_words": []}
  },
  {
    "case_id": "case_008", 
    "case_type": "validator_issue", 
    "top_words": ["вакцина", "щеплення", "вірус", "пандемія", "МОЗ"], 
    "top_docs": ["Нова партія вакцини прибула", "Рецепт смачного борщу з пампушками"], 
    "expected": {"classification": "health", "quality": "mixed", "is_noise": False, "noise_words": []} 
  },
  {
    "case_id": "case_009", 
    "case_type": "reference_to_output", 
    "top_words": ["Марс", "NASA", "висадка", "космос", "запуск"],
    "top_docs": ["NASA запускає найбільше дослідження центру Чумацького Шляху", "Перший крок до висадки людини на Місяць"], 
    "expected": {"classification": "science", "quality": "good", "is_noise": False, "noise_words": []} 
  },
  {
    "case_id": "case_010", 
    "case_type": "agent_error_correction", 
    "top_words": ["Apple", "смартфон", "iPhone", "iOS", "садівництво"], 
    "top_docs": ["Як виростити яблука в саду", "Обрізка дерев восени"], 
    "expected": {"classification": "technology/gardening", "quality": "mixed", "is_noise": False, "noise_words": []} 
  }
]