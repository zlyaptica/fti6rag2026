import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "./Qwen3-0.6B"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    dtype=torch.bfloat16,
    local_files_only=True
)

SYSTEM_PROMPT = (
    "Сформируй осмысленный и точный ответ."
    "Учитывай как содержание источников, так и формулировку запроса."
)

## MAIN
res = ask_llm("Привет! Как дела?")
print(res)
##

def ask_llm(user_text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_text
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768
    )

    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    content = tokenizer.decode(output_ids[0:], skip_special_tokens=True).strip("\n")

    return content