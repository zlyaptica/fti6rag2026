import torch
import os
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM

@dataclass
class GenerationConfig:
    max_new_tokens: int = 2048
    temperature: float = 0.7
    do_sample: bool = True


class LLMClient:
    __instance = None

    SYSTEM_PROMPT = (
        "Сформируй осмысленный и точный ответ. "
        "Учитывай как содержание источников, так и формулировку запроса."
    )

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


    def __init__(self, model_path: str = "./Qwen3-0.6B") -> None:
        if hasattr(self, "_model"):
            return

        self.model_path = os.path.abspath(model_path)
        self._validate_model_path()
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._tokenizer = None
        self._model = None
        self._load_model()

    @property
    def model_path(self) -> str:
        return self.__model_path

    @model_path.setter
    def model_path(self, value: str) -> None:
        self.__model_path = value

    def _validate_model_path(self) -> None:
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Директория с моделью не найдена: {self.model_path}")

    def _load_model(self) -> None:
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            local_files_only=True
        )

        self._model.eval()

    def ask(self, user_text: str, config: GenerationConfig | None = None) -> str:
        if not user_text:
            raise ValueError("Запрос не может быть пустым.")

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_text.strip()},
        ]

        config = config or GenerationConfig()

        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        model_inputs = self._tokenizer([text], return_tensors="pt").to(self._model.device)

        with torch.inference_mode():
            generated_ids = self._model.generate(
                **model_inputs,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                do_sample=config.do_sample,
                pad_token_id=self._tokenizer.eos_token_id
            )

        new_tokens = generated_ids[0][len(model_inputs.input_ids[0]):]

        return self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()