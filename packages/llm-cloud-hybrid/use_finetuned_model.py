from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Path to your fine-tuned model directory
model_path = "./fine_tuned_model"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to('cpu')  # Change to 'cuda' if GPU available

def generate_response(prompt, max_length=100):
    inputs = tokenizer.encode_plus(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128,
        add_special_tokens=True,
        return_attention_mask=True
    )
    input_ids = inputs["input_ids"].to('cpu')
    attention_mask = inputs["attention_mask"].to('cpu')

    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example usage:
if __name__ == "__main__":
    question = "Explain polymorphism in simple terms."
    answer = generate_response(question)
    print("Q:", question)
    print("A:", answer)
