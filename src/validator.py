import json
from jsonschema import validate, ValidationError
from json_schema import extraction_schema
from llm_extract import results

def validate_extraction_output(raw_output):
    print(f"--- Аналіз виходу моделі ---")
    try:
        data = json.loads(raw_output)
        print("Parse Success: Рядок є коректним JSON.")
    except json.JSONDecodeError as e:
        print(f"Parse Fail: Помилка синтаксису JSON: {e}")
        return False
        
    try:
        validate(instance=data, schema=extraction_schema)
        print("Schema Success: Дані повністю відповідають схемі.")
        return True
    except ValidationError as e:
        print(f"Schema Fail: Невідповідність схемі!")
        print(f"{e.message}")
        return False

for item in results:
  validate_extraction_output(item)