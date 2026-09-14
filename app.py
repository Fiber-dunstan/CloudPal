"""Streamlit UI for CloudPal."""

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

st.set_page_config(
    page_title="CloudPal",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
);

html,
body,
[class*="css"] {
    font-family: 'Inter', sans-serif;
}

body {
    overflow-x: hidden;
}

.block-container {
    max-width: 1180px !important;
    margin: 0 auto !important;
    padding-top: 6.5rem !important;
    padding-left: 3.5rem !important;
    padding-right: 3.5rem !important;
    padding-bottom: 8rem !important;
}

.fixed-brand {
    position: fixed !important;
    top: 1rem !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 999999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.35rem !important;
    padding: 0.45rem 0.9rem !important;
    margin: 0 !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    letter-spacing: -0.035em !important;
    color: var(--text-color, inherit) !important;
    white-space: nowrap !important;
    pointer-events: none !important;
    width: max-content !important;
    max-width: none !important;
}

.cloud-icon {
    font-size: 1.45rem !important;
    line-height: 1 !important;
}

.cloudpal-logo {
    font-weight: 700 !important;
    line-height: 1 !important;
}

.main-intro {
    max-width: 680px;
    margin: 0 auto 2.2rem auto;
    text-align: center;
    font-size: 0.94rem;
    line-height: 1.6;
    color: var(--text-color, inherit);
    opacity: 0.58;
}

section[data-testid="stSidebar"] {
    border-right: 1px solid
        var(--border-color, rgba(128, 128, 128, 0.18));
}

[data-testid="stSidebarUserContent"] {
    padding-top: 1.2rem !important;
    padding-left: 1.4rem !important;
    padding-right: 1.4rem !important;
    padding-bottom: 2rem !important;
}

.sidebar-title {
    margin: 0 0 0.3rem 0;
    font-size: 1.18rem;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: -0.025em;
}

.sidebar-subtitle {
    margin: 0 0 1.25rem 0;
    font-size: 0.8rem;
    line-height: 1.5;
    color: var(--text-color, inherit);
    opacity: 0.56;
}

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 0.5rem;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 46px;
    padding: 0.65rem 0.8rem;
    border-radius: 11px;
    border: 1px solid
        var(--border-color, rgba(128, 128, 128, 0.23));
    background: transparent;
    color: var(--text-color, inherit);
    text-align: left;
    font-size: 0.82rem;
    font-weight: 400;
    line-height: 1.35;
    transition:
        background-color 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: var(
        --secondary-background-color,
        rgba(128, 128, 128, 0.07)
    );
    border-color: var(
        --primary-color,
        rgba(128, 128, 128, 0.45)
    );
    transform: translateY(-1px);
}

[data-testid="stChatMessage"] {
    border: 1px solid
        var(--border-color, rgba(128, 128, 128, 0.17));
    border-radius: 15px;
    padding: 0.95rem 1.1rem;
    margin-bottom: 0.85rem;
    background: transparent;
}

.source-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.75rem;
}

.source-chip {
    border: 1px solid
        var(--border-color, rgba(128, 128, 128, 0.25));
    border-radius: 999px;
    padding: 0.22rem 0.62rem;
    font-size: 0.69rem;
    color: var(--text-color, inherit);
    opacity: 0.62;
    background: transparent;
}

[data-testid="stChatInput"] {
    max-width: 860px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-bottom: 1rem !important;
}

[data-testid="stChatInput"] > div {
    border-radius: 18px !important;
    border: 1px solid
        var(--border-color, rgba(128, 128, 128, 0.24)) !important;
    background: var(
        --background-color,
        transparent
    ) !important;
    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.08) !important;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color:
        var(--primary-color, rgba(128, 128, 128, 0.48))
        !important;
    box-shadow:
        0 10px 32px rgba(0, 0, 0, 0.12) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text-color, inherit) !important;
    border: none !important;
    box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.5 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-color, inherit) !important;
    opacity: 0.42 !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background-color: transparent !important;
}

[data-testid="stChatInput"] button {
    border-radius: 10px !important;
    transition:
        background-color 0.18s ease,
        transform 0.18s ease !important;
}

[data-testid="stChatInput"] button:hover {
    transform: scale(1.04);
}

[data-testid="stTextInput"] input {
    border-radius: 11px !important;
    color: var(--text-color, inherit) !important;
    background: var(
        --secondary-background-color,
        rgba(128, 128, 128, 0.06)
    ) !important;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .block-container {
        max-width: 100% !important;
        padding-top: 5.25rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 7rem !important;
    }

    .fixed-brand {
        top: 0.75rem !important;
        font-size: 1.35rem !important;
        padding: 0.4rem 0.7rem !important;
    }

    .cloud-icon {
        font-size: 1.25rem !important;
    }

    .main-intro {
        font-size: 0.87rem;
        margin-bottom: 1.5rem;
    }

    [data-testid="stChatInput"] {
        max-width: calc(100% - 0.5rem) !important;
    }
}

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


GREETINGS = {
    "hi",
    "hello",
    "hey",
    "yo",
    "sup",
    "howdy",
    "greetings",
    "good morning",
    "good afternoon",
    "good evening",
    "hiya",
    "hey there",
    "hello there",
}


def is_greeting(text: str) -> bool:
    normalized = text.strip().lower().rstrip("!.,? ")
    return normalized in GREETINGS


GREETING_RESPONSE = (
    "Hey! I'm CloudPal — ask me anything about AWS: EC2, S3, IAM, containers, "
    "databases, CI/CD, or generative AI services, and I'll answer from a curated "
    "knowledge base. Type a question or use the mic to get started."
)


def render_fixed_brand():
    st.markdown(
        """
        <div class="fixed-brand">
            <span class="cloud-icon">☁️</span>
            <span class="cloudpal-logo">CloudPal</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_main_intro():
    st.markdown(
        """
        <div class="main-intro">
            Ask about AWS and get answers grounded in a curated knowledge base.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sources(retrieved):
    labels = sorted(
        {
            SOURCE_LABELS.get(
                r["source"],
                r["source"]
            )
            for r in retrieved
        }
    )

    chips = "".join(
        f'<span class="source-chip">{label}</span>'
        for label in labels
    )

    st.markdown(
        f"""
        <div class="source-chip-row">
            {chips}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">
                Explore CloudPal
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-subtitle">
                Try one of these, or ask your own question.
            </div>
            """,
            unsafe_allow_html=True,
        )

        for q in SUGGESTED_QUESTIONS:
            if st.button(
                q,
                key=f"suggest_{q}",
                use_container_width=True,
            ):
                st.session_state.pending_query = q


def main():
    embedder = get_embedder()
    index, chunks, sources = get_index_and_chunks()

    render_fixed_brand()
    render_sidebar()
    render_main_intro()

    api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Groq API key (free at console.groq.com)",
            type="password",
        )

    if not api_key:
        st.info("Add a free Groq API key above to start chatting.")
        st.stop()

    client = Groq(api_key=api_key)

    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        avatar = (
            "🧑‍💻"
            if msg["role"] == "user"
            else "☁️"
        )

        with st.chat_message(
            msg["role"],
            avatar=avatar,
        ):
            st.markdown(msg["content"])

            if (
                msg["role"] == "assistant"
                and msg.get("sources")
            ):
                render_sources(msg["sources"])

    chat_submission = st.chat_input(
        "Ask about EC2, S3, IAM, containers, AI/ML services...",
        accept_audio=True,
        audio_sample_rate=16000,
        key="cloudpal_chat_input",
    )

    query = None

    if chat_submission is not None:
        if chat_submission.text:
            query = chat_submission.text.strip()

        elif chat_submission.audio is not None:
            audio_bytes = chat_submission.audio.getvalue()

            with st.spinner("Transcribing your question..."):
                transcript = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=(
                        "recording.wav",
                        audio_bytes,
                    ),
                )

            query = transcript.text.strip()

    if "pending_query" in st.session_state:
        query = st.session_state.pop("pending_query")

    if query:
        st.session_state.history.append(
            {
                "role": "user",
                "content": query,
            }
        )

        with st.chat_message(
            "user",
            avatar="🧑‍💻",
        ):
            st.markdown(query)

        if is_greeting(query):
            answer = GREETING_RESPONSE

            with st.chat_message(
                "assistant",
                avatar="☁️",
            ):
                st.markdown(answer)

            st.session_state.history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        else:
            retrieved = retrieve(
                query,
                embedder,
                index,
                chunks,
                sources,
            )

            prompt = build_prompt(
                query,
                retrieved,
            )

            with st.chat_message(
                "assistant",
                avatar="☁️",
            ):
                with st.spinner(
                    "Retrieving context and generating an answer..."
                ):
                    answer = generate_answer(
                        client,
                        prompt,
                    )

                st.markdown(answer)
                render_sources(retrieved)

            st.session_state.history.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": retrieved,
                }
            )


if __name__ == "__main__":
    main()