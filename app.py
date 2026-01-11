# app.py
"""
CrediTrust Complaint Analysis App
---------------------------------
Interactive RAG-based assistant for analyzing financial customer complaints.

Tech:
- FAISS Vector Store
- Hugging Face LLM (Mistral-7B)
- Gradio UI
"""

import gradio as gr
import logging
from scripts.rag_pipeline import CreditRAG

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# 1. Initialize the RAG Pipeline (Load Once)
# -------------------------------------------------------------------
print("⏳ Loading CrediTrust RAG System... (This may take a minute)")

try:
    rag_system = CreditRAG(vector_store_path="vector_store/full_faiss_index")
    print("✅ System Loaded Successfully!")
except Exception as e:
    logger.error(f"System initialization failed: {e}")
    rag_system = None
    print("❌ Failed to load system. Check logs.")

# -------------------------------------------------------------------
# 2. Helper Functions
# -------------------------------------------------------------------
def format_sources(docs):
    """
    Format retrieved documents into readable Markdown.
    Displayed below the answer for transparency and trust.
    """
    if not docs:
        return "_No source documents retrieved._"

    formatted = ""
    for i, doc in enumerate(docs, start=1):
        product = doc.metadata.get("product", "Unknown Product")
        issue = doc.metadata.get("issue", "Unknown Issue")
        snippet = doc.page_content[:400]

        formatted += (
            f"**Source {i}: {product}**  \n"
            f"`Issue:` {issue}  \n\n"
            f"> {snippet}...\n\n"
            "---\n"
        )

    return formatted


def query_rag(question, history):
    """
    Main Gradio callback.
    Executes the RAG pipeline and returns:
    - Generated answer
    - Source documents used
    """
    if not question.strip():
        return "", ""

    if rag_system is None:
        return "❌ System unavailable. Please check server logs.", ""

    try:
        result = rag_system.answer_question(question)
        answer = result["answer"]
        sources = format_sources(result["source_documents"])
        return answer, sources

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return "⚠️ An error occurred while processing your request.", ""

# -------------------------------------------------------------------
# 3. Gradio UI
# -------------------------------------------------------------------
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
)

with gr.Blocks(
    theme=theme,
    title="CrediTrust Complaint Assistant"
) as demo:

    # ---------------- Header ----------------
    gr.Markdown(
        """
        # 🏦 CrediTrust Financial AI  
        **Internal Complaint Analysis Tool**

        Ask questions about customer complaints across:
        **Credit Cards, Loans, and Savings Accounts**

        _Retrieval-Augmented Generation (RAG) using FAISS + Mistral-7B_
        """
    )

    # ---------------- Input ----------------
    with gr.Row():
        question_input = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Why are customers upset about overdraft fees?",
            lines=2,
            show_copy_button=True,
        )

    with gr.Row():
        submit_btn = gr.Button("🔍 Analyze", variant="primary")
        clear_btn = gr.ClearButton()

    # ---------------- Output ----------------
    gr.Markdown("### 🤖 AI-Generated Analysis")
    answer_output = gr.Markdown()

    with gr.Accordion("📚 Reference Sources (Click to expand)", open=False):
        sources_output = gr.Markdown()

    # ---------------- Interaction Logic ----------------
    state = gr.State([])  # Dummy state (future-proof)

    submit_btn.click(
        fn=query_rag,
        inputs=[question_input, state],
        outputs=[answer_output, sources_output],
        show_progress=True,   # UX improvement
    )

    question_input.submit(
        fn=query_rag,
        inputs=[question_input, state],
        outputs=[answer_output, sources_output],
        show_progress=True,
    )

    clear_btn.add(
        [question_input, answer_output, sources_output]
    )

    # ---------------- Footer ----------------
    gr.Markdown("---")
    gr.Markdown(
        "*Confidential — For Internal Use Only (CrediTrust Financial)*"
    )

# -------------------------------------------------------------------
# 4. Launch Application
# -------------------------------------------------------------------
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
