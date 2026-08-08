from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

# Load documents with UTF-8 encoding to avoid decode errors
loader = TextLoader("book.txt", encoding="utf-8")
documents = loader.load()

# Split documents into smaller chunks to reduce input length
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Create embeddings for retrieval
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(texts, embedding_model)

# Load your fine-tuned GPT-Neo pipeline for generation
local_pipe = pipeline(
    "text-generation",
    model="./fine_tuned_neo",       # Path to your fine-tuned model
    tokenizer="./fine_tuned_neo",
    max_new_tokens=150,             # Only generate up to 150 new tokens
    do_sample=True,
    temperature=0.7,
)

# Wrap Hugging Face pipeline as a LangChain LLM
llm = HuggingFacePipeline(pipeline=local_pipe)

# Create the RetrievalQA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff")

print("Ask questions (type 'exit' to quit):")
while True:
    query = input("Question: ")
    if query.lower() == "exit":
        print("Goodbye!")
        break
    answer = qa.run(query)
    print("Answer:", answer)
