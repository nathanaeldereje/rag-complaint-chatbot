# scripts/rag_pipeline.py
import argparse
import os
import logging
from dotenv import load_dotenv

# LangChain Imports
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
# Removed unused import: from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# Setup Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CreditRAG:
    def __init__(self, vector_store_path="vector_store/full_faiss_index"):
        """
        Initializes the RAG pipeline: loads the vector store and sets up the LLM.
        """
        self.vector_store_path = vector_store_path
        self.repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        
        # 1. Initialize Embedding Model
        logger.info("Loading Embedding Model...")
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 2. Load Vector Store
        logger.info(f"Loading Vector Store from {self.vector_store_path}...")
        try:
            self.vector_db = FAISS.load_local(
                self.vector_store_path, 
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})
            logger.info("Vector Store Loaded Successfully.")
        except Exception as e:
            logger.error(f"Failed to load Vector Store: {e}")
            raise

        # 3. Initialize LLM (UPDATED SECTION)
        logger.info("Initializing LLM Endpoint...")

        hf_llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="text-generation",
            max_new_tokens=512,
            temperature=0.1,
            do_sample=True,
            timeout=300,
        )

        self.llm = ChatHuggingFace(llm=hf_llm)


        # 4. Define Prompt Template
        self.prompt_template = PromptTemplate(
            template="""
            You are a financial analyst assistant for CrediTrust. 
            Your task is to answer questions about customer complaints based ONLY on the provided context.
            
            Context:
            {context}
            
            Question: 
            {question}
            
            Instructions:
            1. Answer directly and concisely.
            2. If the answer is not in the context, explicitly state: "I don't have enough information in the provided complaints to answer this."
            3. Do not make up facts.
            
            Answer:
            """,
            input_variables=["context", "question"]
        )

    def retrieve_documents(self, query):
        """Retrieve relevant documents for a query."""
        return self.retriever.invoke(query)

    def answer_question(self, query):
        """
        Full RAG pipeline: Retrieve -> Format -> Generate
        """
        # 1. Retrieve
        docs = self.retrieve_documents(query)
        
        # 2. Combine context
        context_text = "\n\n".join([d.page_content for d in docs])
        
        # 3. Generate
        chain = self.prompt_template | self.llm
        response = chain.invoke({"context": context_text, "question": query})
        
        return {
            "question": query,
            "answer": response.content.strip(),
            "source_documents": docs
        }
def parse_args():
    parser = argparse.ArgumentParser(description="Run the CrediTrust RAG pipeline from CLI.")
    parser.add_argument("--question", type=str, default="What are the common complaints about credit card late fees?",
                        help="The question to ask the RAG system (e.g. 'Why are fees so high?')")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()


    rag = CreditRAG()
    test_q = "What are the common complaints about credit card late fees?"
    result = rag.answer_question(args.question)
    print("-" * 50)
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print("-" * 50)
    print("Sources:")
    for doc in result['source_documents']:
        print(f"- {doc.metadata.get('product', 'N/A')}: {doc.page_content[:100]}...")