import re
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cpu"
)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def ask_agent(prompt, system_message):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(text, max_new_tokens=512, do_sample=False, return_full_text=False)
    return outputs[0]["generated_text"].strip()

def safe_parse(text):
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in: {text}")

    return json.loads(match.group(0))


def run_reviewer(user_input, extraction_data):
    system_msg = """You are Agent 3 (Reviewer). Check the Extractor output: compare extraction with input text; check consistency;
    find out if there are missing/hallucinated/contradictory fields.
    Return JSON with fields:
    - verdict (accept / repair_needed / fallback_needed)
    - valid_json (boolean)
    - schema_ok (boolean)
    - consistency_ok (boolean)
    - issues (list of objects with field and problem)
    - recommended_action (what to do next)
    
    Output format example:
    {
      "verdict": "repair_needed",
      "valid_json": true,
      "schema_ok": true,
      "consistency_ok": false,
      "issues": [
        {
        "field": "date",
        "problem": "date not normalized"
        }
      ],
      "recommended_action": "run_repair_with_date_normalization"
    }"""
    
    prompt = f"Input text: {user_input}\nExtraction output: {json.dumps(extraction_data)}"
    response = ask_agent(prompt, system_msg)
    return safe_parse(response) 

