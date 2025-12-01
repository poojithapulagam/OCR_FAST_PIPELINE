import ollama

class LLMExtractor:

    def __init__(self, model="qwen2.5"):
        self.model = model

    def extract_name_address_pairs(self, text):
        prompt = f"""
Extract the recipient name and address from this text:
{text}

Return JSON:
[
  {{"input_name": "...", "input_address": "..."}}
]
"""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            import json
            return json.loads(response["response"])
        except Exception:
            return []
