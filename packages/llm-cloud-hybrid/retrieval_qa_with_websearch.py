from ddgs import DDGS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

def web_search(query, max_results=3):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        snippets = []
        for r in results:
            snippet = r.get('body') or r.get('text') or r.get('title') or ""
            if snippet:
                snippets.append(snippet)
        return "\n".join(snippets)

# Load local documents with UTF-8 encoding
loader = TextLoader("book.txt", encoding="utf-8")
documents = loader.load()

# Split documents into smaller chunks to manage input length
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Prepare embeddings and FAISS vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(texts, embedding_model)

# Initialize the generation pipeline with controlled parameters
local_pipe = pipeline(
    "text-generation",
    model="./fine_tuned_neo",
    tokenizer="./fine_tuned_neo",
    max_new_tokens=120,
    do_sample=True,
    temperature=0.7,
    pad_token_id=50256,
    eos_token_id=50256,
)

llm = HuggingFacePipeline(pipeline=local_pipe)

# Define a prompt template with concise answer instruction
template = """
You are a helpful assistant. Use the context below to answer the question concisely and truthfully.
If you don't know the answer, say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# Setup RetrievalQA chain with the custom prompt
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

def clean_response(raw_response: str) -> str:
    # Example cleanup for common repeated prompt fragments
    unwanted_intro = "Use the following pieces of context to answer the question at the end."
    if raw_response.startswith(unwanted_intro):
        # Remove prompt text to leave only final answer
        # Adjust split index based on observed response structure
        parts = raw_response.split("\n\n", 1)
        if len(parts) > 1:
            return parts[1].strip()
    return raw_response.strip()

def answer_question(query: str) -> str:
    web_snippets = web_search(query)
    augmented_query = f"Web search results:\n{web_snippets}\n\nQuestion:\n{query}"
    raw_response = qa.invoke({"query": augmented_query})["result"]
    return clean_response(raw_response)

if __name__ == "__main__":
    print("Chatbot with DuckDuckGo Web Search (type 'exit' to quit)")
    while True:
        query = input("Question: ")
        if query.lower() == "exit":
            break
        answer = answer_question(query)
        print("Answer:", answer)
