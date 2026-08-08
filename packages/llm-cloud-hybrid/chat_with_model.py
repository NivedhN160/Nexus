from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load fine-tuned model and tokenizer from local folder
model_path = "./fine_tuned_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to('cpu')  # change to 'cuda' if you have GPU

def generate_response(question, max_length=150):
    # Format prompt with special tokens matching training format
    prompt = f" {question} "

    inputs = tokenizer.encode_plus(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128,
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
        top_k=30,
        top_p=0.9,
        temperature=0.6
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract answer between <answer> tags if present
    start_tag = "<answer>"
    end_tag = "</answer>"
    start = response.find(start_tag)
    end = response.find(end_tag)
    if start != -1 and end != -1 and end > start:
        return response[start + len(start_tag):end].strip()
    else:
        # Fallback if tags not found
        if response.lower().startswith(question.lower()):
            return response[len(question):].strip()
        return response.strip()

if __name__ == "__main__":
    print("Chat with your fine-tuned AI (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        answer = generate_response(user_input)
        print("AI:", answer)
