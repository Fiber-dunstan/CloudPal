"""Streamlit UI for CloudPal — theme-aware, ChatGPT-style composer layout."""
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from rag_utils import (
    load_and_chunk_docs,
    load_embedder,
    build_index,
    retrieve,
    build_prompt,
    generate_answer,
)

load_dotenv()

st.set_page_config(page_title="CloudPal", page_icon="☁️", layout="centered")

SOURCE_LABELS = {
    "ec2.md": "EC2",
    "s3.md": "S3",
    "lambda.md": "Lambda",
    "cloudwatch.md": "CloudWatch",
    "vpc.md": "VPC",
    "iam.md": "IAM",
    "rds.md": "RDS",
    "dynamodb.md": "DynamoDB",
    "api-gateway.md": "API Gateway",
    "containers.md": "Containers",
    "networking-elb.md": "Load Balancing",
    "devops-cicd.md": "DevOps & CI/CD",
    "ai-ml.md": "AI/ML",
    "well-architected.md": "Well-Architected",
    "cloudfront.md": "CloudFront",
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2.5rem;
}

.app-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--text-color, inherit);
    letter-spacing: -0.02em;
    margin-bottom: 0.3rem;
}

.app-subtitle {
    font-size: 0.95rem;
    color: var(--text-color, inherit);
    opacity: 0.6;
    margin-bottom: 1.4rem;
}

section[data-testid="stSidebar"] .stButton button {
    background-color: transparent;
    border: 1px solid var(--border-color, rgba(128, 128, 128, 0.3));
    border-radius: 10px;
    text-align: left;
    font-weight: 400;
    font-size: 0.85rem;
    padding: 0.6rem 0.85rem;
    margin-bottom: 0.4rem;
    width: 100%;
    color: var(--text-color, inherit);
    transition: border-color 0.15s ease, opacity 0.15s ease;
}

section[data-testid="stSidebar"] .stButton button:hover {
    border-color: var(--primary-color, currentColor);
    opacity: 0.8;
}

[data-testid="stAppViewBlockContainer"], .block-container {
    padding-top: 3.75rem !important;
}

[data-testid="stSidebarUserContent"] {
    padding-top: 3.75rem !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
}

[data-testid="stChatMessage"] {
    border: 1px solid var(--border-color, rgba(128, 128, 128, 0.25));
    border-radius: 12px;
}

.source-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.7rem;
}

.source-chip {
    border: 1px solid var(--border-color, rgba(128, 128, 128, 0.3));
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    color: var(--text-color, inherit);
    opacity: 0.65;
    background: transparent;
}

footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_embedder():
    return load_embedder()


@st.cache_resource
def get_index_and_chunks():
    chunks, sources = load_and_chunk_docs()
    embedder = get_embedder()
    index = build_index(embedder, chunks)
    return index, chunks, sources


SUGGESTED_QUESTIONS = [
    "What's the difference between EC2 and Lambda pricing?",
    "How does IAM enforce least privilege?",
    "When should I choose ECS over EKS?",
    "What's the difference between an ALB and NLB?",
    "How does Bedrock relate to SageMaker?",
    "What are the six Well-Architected pillars?",
]


def render_header():
    st.markdown(
        """
        <div class="app-title">☁️ CloudPal</div>
        <div class="app-subtitle">Ask about AWS and get answers grounded in a curated knowledge base.</div>
        """,
        unsafe_allow_html=True,
    )


def render_sources(retrieved):
    labels = sorted({SOURCE_LABELS.get(r["source"], r["source"]) for r in retrieved})
    chips = "".join(f'<span class="source-chip">{label}</span>' for label in labels)
    st.markdown(f'<div class="source-chip-row">{chips}</div>', unsafe_allow_html=True)


def main():
    embedder = get_embedder()
    index, chunks, sources = get_index_and_chunks()

    render_header()

    with st.sidebar:
        st.markdown("### Explore CloudPal")
        st.caption("Try one of these, or ask your own question.")
        for q in SUGGESTED_QUESTIONS:
            if st.button(q, key=f"suggest_{q}"):
                st.session_state.pending_query = q

    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Groq API key (free at console.groq.com)", type="password")
    if not api_key:
        st.info("Add a free Groq API key above to start chatting.")
        st.stop()

    client = Groq(api_key=api_key)

    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        avatar = "🧑‍💻" if msg["role"] == "user" else "☁️"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                render_sources(msg["sources"])

    # Unified composer: text input and mic live in the same pinned bottom row
    with st.bottom:
        input_col, mic_col = st.columns([4, 1])
        with input_col:
            typed_query = st.chat_input("Ask about EC2, S3, IAM, containers, AI/ML services...")
        with mic_col:
            audio_value = st.audio_input("Voice question", label_visibility="collapsed")

    query = typed_query
    if audio_value is not None:
        audio_hash = hash(audio_value.getvalue())
        if audio_hash != st.session_state.get("last_audio_hash"):
            st.session_state.last_audio_hash = audio_hash
            with st.spinner("Transcribing your question..."):
                transcript = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=("recording.wav", audio_value.getvalue()),
                )
            query = transcript.text

    if "pending_query" in st.session_state:
        query = st.session_state.pop("pending_query")

    if query:
        st.session_state.history.append({"role": "user", "content": query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(query)

        retrieved = retrieve(query, embedder, index, chunks, sources)
        prompt = build_prompt(query, retrieved)

        with st.chat_message("assistant", avatar="☁️"):
            with st.spinner("Retrieving context and generating an answer..."):
                answer = generate_answer(client, prompt)
            st.markdown(answer)
            render_sources(retrieved)
        st.session_state.history.append(
            {"role": "assistant", "content": answer, "sources": retrieved}
        )


if __name__ == "__main__":
    main()