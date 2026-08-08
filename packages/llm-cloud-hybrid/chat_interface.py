from retrieval_qa_backend import answer_question

def run_chat():
    print("Welcome to your GPT Retrieval-QA Chatbot! (type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = answer_question(user_input)
        print("AI:", response)

if __name__ == "__main__":
    run_chat()
