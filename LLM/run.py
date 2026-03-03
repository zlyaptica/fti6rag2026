import torch
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

class QwenLLM:
    def __init__(self, model_path="./Qwen3-0.6B"):
        self.model_path = os.path.abspath(model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.SYSTEM_PROMPT = (
            "Сформируй осмысленный и точный ответ."
            "Учитывай как содержание источников, так и формулировку запроса."
        )
        self._load_model()
    
    def _load_model(self):
        print(f"Загрузка модели из {self.model_path} на устройство {self.device}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Папка с моделью не найдена: {self.model_path}")
        
        print(f"Содержимое папки модели: {os.listdir(self.model_path)}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path, 
            local_files_only=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,  
            device_map="auto",
            dtype=torch.bfloat16,
            local_files_only=True
        )
        print("Модель успешно загружена!")
    
    def ask(self, user_text: str, max_new_tokens: int = 2048) -> str:
        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_text
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        content = self.tokenizer.decode(output_ids[0:], skip_special_tokens=True).strip("\n")

        return content

def ask_llm(user_text: str, top_k: int = 5) -> str:
    llm = QwenLLM() 
    return llm.ask(user_text)
_global_llm_instance = None

def get_llm_instance():
    global _global_llm_instance
    if _global_llm_instance is None:
        _global_llm_instance = QwenLLM()
    return _global_llm_instance
__all__ = ['ask_llm', 'QwenLLM', 'get_llm_instance']

if __name__ == "__main__":
    print("Тестирование модели...")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Проверка наличия папки Qwen3-0.6B: {os.path.exists('./Qwen3-0.6B')}")
    if os.path.exists('./Qwen3-0.6B'):
        print(f"Содержимое папки Qwen3-0.6B: {os.listdir('./Qwen3-0.6B')}")
    
    try:
        test = ask_llm("Как починить мою машину марки Lada?")
        print(f"Ответ: {test}")
    except Exception as e:
        print(f"ОШИБКА: {e}")
        print(f"Тип ошибки: {type(e)}")