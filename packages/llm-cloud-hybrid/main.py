# main.py

from retrieval_qa_with_websearch import answer_question

def main():
    print("Welcome to the Neural GPT Retrieval-QA Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = answer_question(user_input)
        print("AI:", response)

if __name__ == "__main__":
    main()
