from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "EleutherAI/gpt-neo-125M"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to('cpu')

def generate_response(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt").to('cpu')
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if response.lower().startswith(prompt.lower()):
        response = response[len(prompt):].strip()
    return response

if __name__ == "__main__":
    print("Chat with GPT-Neo 125M (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        print("AI:", generate_response(user_input))
