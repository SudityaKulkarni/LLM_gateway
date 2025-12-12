from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class FlanSanitizer:
    def __init__(self, model_name="google/flan-t5-base", device=None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

        # optional speed boost on GPU
        if self.device == "cuda":
            self.model.half()

    def sanitize(self, prompt: str) -> str:
        # VERY IMPORTANT: instruction tuning
        instruction = (
            "Rewrite the following message to be SAFE, non-harmful, "
            "legal, ethical, and policy-compliant. Preserve meaning "
            "but remove dangerous intent:\n\n"
            f"{prompt}"
        )

        inputs = self.tokenizer(instruction, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=200,
                num_beams=4,
                early_stopping=True,
                do_sample=False,
            )

        safe_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return safe_text.strip()