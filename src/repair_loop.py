import json
from jsonschema import validate, ValidationError
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from eval_set import evaluation_set
from json_schema import extraction_schema
from llm_extract import tokenizer, pipe

MAX_REPAIR_ATTEMPTS = 2

def validate_output(text):
    
    try:
        data = json.loads(text.strip())
        validate(instance=data, schema=extraction_schema)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, f"Помилка парсингу JSON: {str(e)}"
    except ValidationError as e:
        return False, None, f"Помилка валідації схеми: {e.message}"
    except Exception as e:
        return False, None, f"Непередбачена помилка: {str(e)}"


def run_extraction_with_repair(initial_messages):
    
    current_messages = list(initial_messages)
    attempt = 0
    
    while attempt <= MAX_REPAIR_ATTEMPTS:
        prompt = tokenizer.apply_chat_template(
            current_messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        outputs = pipe(
            prompt, 
            max_new_tokens=256, 
            do_sample=False, 
            return_full_text=False
        )
        
        generated_text = outputs[0]["generated_text"].strip()
        
        is_valid, data, error_msg = validate_output(generated_text)
        
        if is_valid:
            print(f"Успішно на спробі {attempt}")
            return {"status": "success", "data": data, "attempts": attempt}
        
        print(f"Спроба {attempt} провалена: {error_msg}")
        
        if attempt < MAX_REPAIR_ATTEMPTS:
            current_messages.append({"role": "assistant", "content": generated_text})
            
            repair_instruction = (
                f"Your previous result contains an error: {error_msg}. "
                f"Please fix the error and return ONLY a valid JSON object that "
                f"matches to the schema."
            )
            current_messages.append({"role": "user", "content": repair_instruction})
            
        attempt += 1

    return {
        "status": "failed", 
        "last_output": generated_text, 
        "error": error_msg, 
        "attempts": MAX_REPAIR_ATTEMPTS
    }

results_repair = []

for item in evaluation_set[:10]:
    messages = [
      {"role": "system", "content": "You are a precise information extraction system. Respond ONLY with valid JSON."},
      {"role": "user", "content": f"""Extract data from the text below. 
      
    Rules:
    - If missing → null
    - Use YYYY-MM-DD for dates if possible
    - Amount must be a number
    - Extract only the core brand name
    - event_type must be one of ["acquisition", "investment", "partnership", "launch", "sanctions", "other"]
    - Normalize currency (e.g., "доларів" → USD, "€" -> EUR, "$" -> USD)
    - Choose the main company which mentioned first if multiple are mentioned


    Output schema:
    {{
      "company": string,
      "event_type": lowercase string,
      "amount": number or null,
      "currency": string or null,
      "date": string or null,
      "location": string or null
    }}

    Text: {item['text']}"""}
    ]
    
    final_result = run_extraction_with_repair(messages)
    results_repair.append(final_result)