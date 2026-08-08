from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    # Load your book text
    loader = TextLoader("book.txt", encoding="utf-8")
    documents = loader.load()

    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create vector store
    vectorstore = FAISS.from_documents(texts, embedding_model)

    # Create local transformers pipeline for text generation
    local_pipe = pipeline(
        "text-generation",
        model="gpt2",
        tokenizer="gpt2",
        device=-1,
        max_length=150,
        temperature=0.7,
        do_sample=True,
    )

    # Wrap pipeline as LangChain LLM
    llm = HuggingFacePipeline(pipeline=local_pipe)

    # Use updated RetrievalQA constructor
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff")

    print("AI Assistant ready. Type 'exit' or 'quit' to stop.")

    while True:
        query = input("\nAsk me anything: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer = qa.run(query)
        print("\nAnswer:", answer)

if __name__ == "__main__":
    main()
