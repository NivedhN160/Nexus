# NGPT-Neural GPT

NGPT-Neural GPT is a custom large language model chatbot interface that integrates Meta AI's LLaMA 2 model alongside GPT-Neo retrieval-augmented QA. It combines deep conversational abilities from LLaMA with precise, knowledge-grounded answers from GPT-Neo for versatile AI interactions.

---

## Features and Insights

- **Hybrid Model Integration:** Dynamically routes user queries to LLaMA or GPT-Neo based on domain-specific keywords for optimized responses.
- **Interactive Web GUI:** Modern chat interface built with HTML, CSS, and JavaScript, featuring voice input and text-to-speech for an engaging user experience.
- **Session Context:** Maintains conversation history for coherent multi-turn dialogue leveraging prompt chaining.
- **Response Cleaning:** Extracts the assistant's precise reply from LLaMA outputs, avoiding confusion caused by overlapping role messages.
- **Custom Voice Integration:** Uses browser Web Speech API for microphone input and speech synthesis for voice output.
- **Dark Themed Responsive UI:** Stylish dark gradients and responsive design for desktop and mobile usability.

---

## Execution Instructions

### Prerequisites

- Python 3.8 or newer installed.
- Required Python packages (listed in `requirements.txt`), including:
  - `fastapi`
  - `uvicorn`
  - `langchain`
  - `langchain_community`
  - Other dependencies based on your environment.

### Project Setup

1. Clone or download the repository.
2. Download the LLaMA 2 model file (`llama-2-7b-chat.Q4_K_M.gguf`) and place it in the project directory or update the path in `llama_wrapper.py`.
3. Install Python dependencies:

pip install -r requirements.txt

### Running the Application

1. Start the FastAPI backend server:

uvicorn app:app --host 0.0.0.0 --port 8000

2. Open a modern web browser and navigate to:

http://localhost:8000

3. Interact with NGPT via the chat interface with text or voice input.

---

## Project Structure Overview

- `app.py`: FastAPI backend serving the API and static frontend.
- `main.py`: Core routing logic deciding which model answers a query and managing session conversation history.
- `llama_wrapper.py`: Wrapper for LLaMA 2 model interaction with prompt formatting and output cleaning.
- `retrieval_qa_with_websearch.py`: GPT-Neo retrieval QA setup and invocation.
- `static/index.html`: Frontend HTML file implementing the chat interface with voice features.

---

## Notes and Recommendations

- Properly manage conversation history per user session to avoid cross-user state mixing.
- The LLaMA output cleaning removes unintended role echoes to keep chat natural.
- Consider adding deployment scripts or Dockerfile for environment reproducibility.
- Enhance with user authentication if deploying publicly.
- Monitor model response times; adjust token limits or temperature for performance tuning.

---

## License

Specify your licensing terms here.

---

## Contact

For questions or contributions, open an issue or reach out via contact information here.

---

Thank you for using NGPT-Neural GPT!  
