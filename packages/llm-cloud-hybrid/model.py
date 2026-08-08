from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "gpt2"  # Small model suitable for local use
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to('cpu')  # Use 'cuda' if you have GPU

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt").to('cpu')
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    question = "Explain recursion simply."
    print(generate_response(question))
