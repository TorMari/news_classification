from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from eval_set import evaluation_set

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cpu"  
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

results = []

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


  prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
  outputs = pipe(prompt, max_new_tokens=256, do_sample=False, return_full_text=False)
  generated_text = outputs[0]["generated_text"]
  results.append(generated_text)

  print(generated_text)