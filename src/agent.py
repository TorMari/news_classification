import json
import ast
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from tools import tools_map

class TopicAgent:
    def __init__(self, model_name="Qwen/Qwen2.5-1.5B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            torch_dtype="auto", 
            device_map="cpu"
        )
        self.pipe = pipeline(
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer
        )

        self.system_prompt_baseline = """You are a Topic Modeling Assistant. 
        You MUST return ONLY valid JSON with the following fields:
        - classification (topic titles (one, several, "unknown"))
        - quality (one topic -> "good", two or more topic -> "mixed", "unknown" -> "bad")
        - is_noise (one or more noise words -> True, zero noise words -> False), 
        - noise_words (list of noise words)

        Output schema:
        {
          "classification": lowercase string,
          "quality": lowercase string,
          "is_noise": boolean,
          "noise_words": list or null
        }
        """
        
        self.system_prompt_tools = """You are a Topic Modeling Assistant.
        RUN all these 3 tools:
        - detect_noise_words(top_words: list): Returns noise/stop words.
        - suggest_topic_label(top_words: list, top_docs: list): Returns a label.
        - score_topic_quality(top_words: list, top_docs: list): Returns a quality score (0 to 1).

        Format:
        Thought: your reasoning.
        Action: tool_name({"param": "value"})
        Observation: tool output.
        ... (repeat if needed)
        Final Answer: your conclusion.
        """


def safe_parse(text):
   text = re.sub(r"```json\s*", "", text)
   text = re.sub(r"```", "", text).strip()

   match = re.search(r"\{.*\}", text, re.DOTALL)
   if not match:
      raise ValueError(f"No JSON found in: {text}")

   return json.loads(match.group(0))

def run_baseline(self, user_input):
   messages = [
      {"role": "system", "content": self.system_prompt_baseline}, 
      {"role": "user", "content": user_input}
   ]
        
   text = self.tokenizer.apply_chat_template(
      messages, 
      tokenize=False, 
      add_generation_prompt=True
   )
        
   outputs = self.pipe(
      text, 
      max_new_tokens=512, 
      do_sample=False, 
      return_full_text=False
   )
        
   response = outputs[0]["generated_text"].strip()   
   try:
      return safe_parse(response)
   except json.JSONDecodeError:
      return {"error": "Failed to parse JSON", "raw_response": response}

TopicAgent.run_baseline = run_baseline

def run_with_tools(self, user_input):
   messages = [{"role": "system", "content": self.system_prompt_tools}, {"role": "user", "content": user_input}]
        
   for _ in range(1): 
      prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
      output = self.pipe(prompt, max_new_tokens=256, do_sample=False)[0]['generated_text']
      response = output.split("<|im_start|>assistant\n")[-1]
      all_observations = []
      if "Action:" in response:
         try:
            action_lines = [
               line.strip()
               for line in response.splitlines()
               if line.strip().startswith("Action:")
            ]
                    
            current_step_observations = []

            for line in action_lines:
               action_content = line[len("Action:"):].strip()
               tool_name = action_content.split("(", 1)[0].strip()
               args_str = action_content.split("(", 1)[1].rsplit(")", 1)[0]
               parsed_args = ast.literal_eval(args_str)
                        
               if tool_name == "detect_noise_words":
                  observation = tools_map[tool_name](parsed_args)
               else:
                  observation = tools_map[tool_name](*parsed_args)

               obs_entry = {"tool": tool_name, "observation": observation}
               all_observations.append(obs_entry)
               current_step_observations.append(obs_entry)

            messages.append({"role": "assistant", "content": response})
            messages.append({
               "role": "user",
               "content": f"Observations: {json.dumps(current_step_observations, ensure_ascii=False)}"
            })

         except Exception as e:
            messages.append({"role": "user", "content": f"Observation: Error: {e}"})
      if "Final Answer:" in response:
         return response.split("Final Answer:")[-1].strip(), all_observations
   return "Limit reached", all_observations
   
TopicAgent.run_with_tools = run_with_tools