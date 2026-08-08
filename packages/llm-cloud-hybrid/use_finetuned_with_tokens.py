from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "./fine_tuned_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to('cpu')  # Change to 'cuda' if GPU available

def generate_response(question, max_length=150):
    prompt = f"<question> {question} </question><answer>"

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
        eos_token_id=tokenizer.convert_tokens_to_ids('</answer>'),
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=30,
        top_p=0.9,
        temperature=0.6
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract answer part between <answer> and </answer> tags
    answer_start = response.find("<answer>") + len("<answer>")
    answer_end = response.find("</answer>")
    if answer_start != -1 and answer_end != -1:
        answer_text = response[answer_start:answer_end].strip()
    else:
        answer_text = response

    # Remove repeated question if present at start of answer
    if answer_text.lower().startswith(question.lower()):
        answer_text = answer_text[len(question):].strip()

    return answer_text

# Example usage
if __name__ == "__main__":
    question = "What is inheritance in programming?"
    print("Q:", question)
    print("A:", generate_response(question))
