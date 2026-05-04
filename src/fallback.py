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


def run_fallback_repair(user_input, previous_extraction, issues):
    formatted_issues = "\n".join([f"- Field '{i['field']}': {i['problem']}" for i in issues])
 
    system_msg = f"""You are Extractor in REPAIR mode. 
    Your task is to fix the previous extraction based on the Reviewer's comments.
 
    ORIGINAL TEXT: {user_input}
    PREVIOUS VARIANT: {json.dumps(previous_extraction, ensure_ascii=False)}
    
    ERRORS FOUND:
    {formatted_issues}
 
    RULES:
    1. Return ONLY corrected, complete, valid JSON. 
    2. Fix the errors listed above based on the original text. 
    3. If the Reviewer pointed out a hallucination, replace this field with the correct value or null. 
    4. Do not add any text and fields other than JSON.
    5. Keep all other uncommented fields as they are.

    Output format example:
    {{
      "status": "failed",
      "reason": "required field amount is missing",
      "corrected_fields": {
          {
            "amount": 1800000000,
          }
      },
      "needs_manual_review": true
    }}"""

    repair_prompt = "Provide the corrected JSON according to the instructions."
    response = ask_agent(repair_prompt, system_msg)
 
    try:
        fixed_json = json.loads(response)
        return fixed_json
    except json.JSONDecodeError:
        print("CRITICAL: Repair returned invalid JSON format.")
        return previous_extraction
