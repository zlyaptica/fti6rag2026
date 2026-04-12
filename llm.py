import torch
import os
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

load_dotenv(".env.local")

@dataclass
class GenerationConfig:
    max_new_tokens: int = 256
    temperature: float = 0.8
    do_sample: bool = True


class LLMClient:
    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        self._model_params_config = GenerationConfig()

        # промпт для генерации ответа с использование базы знаний
        self._prompt_with_fact = """Пользователь хочет получить ответ на этот вопрос: {}.\n 
            Твоя задача - проанализировать вопроса пользователя и найденную информацию,
            исправить ошибки форматирования, удалить иинформацию, которая не относится к теме.
            От себя ничего не придумывай, используй только факты, найденные в базе знаний.
            Используй русский ответ для ответа.
        """

    def db_answer_enhance(self, query: str, answer: str) -> str:
        messages = [
            {"role": "system", "content": "Ты полезный ассистент."},
            {"role": "user", "content": self._prompt_with_fact.format(query)},
            {"role": "assistant", "content": answer},
        ]

        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        return self.generate_llm_answer(text)

    def llm_answer(self, query: str) -> str:
        messages = [
            {"role": "system", "content": "Ответь кратко на вопрос пользователя."},
            {"role": "user", "content": query},
        ]

        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        return self.generate_llm_answer(text)
    
    def generate_llm_answer(self, text: str) -> str:
        model_inputs = self._tokenizer([text], return_tensors="pt").to(self._model.device)

        with torch.inference_mode():
            generated_ids = self._model.generate(
                **model_inputs,
                max_new_tokens=self._model_params_config.max_new_tokens,
                temperature=self._model_params_config.temperature,
                do_sample=self._model_params_config.do_sample,
                pad_token_id=self._tokenizer.eos_token_id
            )

        new_tokens = generated_ids[0][len(model_inputs.input_ids[0]):]

        return self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

llm_client = LLMClient(os.getenv("LLM_MODEL"))