# backend/model_client.py
import requests
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_DEVICE = os.getenv("MODEL_DEVICE", "cpu")
MODEL_MAX_NEW_TOKENS = int(os.getenv("MODEL_MAX_NEW_TOKENS"))
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE"))

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if MODEL_DEVICE == "cuda" else torch.float32,
    low_cpu_mem_usage=True,
)
model.to(MODEL_DEVICE)
model.eval()
print("Model loaded.")


def ask_model(messages):
    prompt = ""
    for m in messages:
        role = m["role"]
        content = m["content"]
        if role == "system":
            prompt += f"[SYSTEM] {content}\n"
        elif role == "assistant":
            prompt += f"[ASSISTANT] {content}\n"
        else:
            prompt += f"[USER] {content}\n"
    prompt += "[ASSISTANT] "

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(MODEL_DEVICE)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MODEL_MAX_NEW_TOKENS,
            do_sample=True,
            temperature=MODEL_TEMPERATURE,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = output_ids[0][inputs["input_ids"].shape[-1]:]
    reply = tokenizer.decode(generated, skip_special_tokens=True)
    return reply.strip()
