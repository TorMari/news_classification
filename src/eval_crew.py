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


def run_extractor(user_input, triage_data):
    system_msg = f"""You are Agent 2 (Extractor). Your task: extract data from the text according to the schema.
    Schema from Triager: {triage_data['expected_fields']}.
    Rules:
    - Return ONLY valid JSON.
    - Set null if there is no data (fields are missing).
    - Add a 'confidence_note' field with an explanation of the confidence.
    - Don't make up data!
    - Use YYYY-MM-DD for dates if possible.
    - Amount must be a number.
    - Extract only the core brand name.
    - event_type must be one of ["acquisition", "investment", "partnership", "launch", "sanctions", "other"].
    - Normalize currency (e.g., "доларів" → USD, "€" -> EUR, "$" -> USD).
    - Choose the main company which mentioned first if multiple are mentioned.
    
    Output schema:
    {{
      "company": string,
      "event_type": lowercase string,
      "amount": number or null,
      "currency": string or null,
      "date": string or null,
      "location": string or null,
      "confidence_note": string
    }}"""
    
    response = ask_agent(user_input, system_msg)
    return safe_parse(response)