# ☁️ CloudPal

**CloudPal** is an AI-powered AWS learning assistant that answers questions about AWS services using Retrieval-Augmented Generation (RAG) — grounding every answer in a curated knowledge base instead of guessing.

🔗 **Live demo:** [Add your live Streamlit URL here]
💻 **Repository:** [github.com/Fiber-dunstan/CloudPal](https://github.com/Fiber-dunstan/CloudPal)

---

## What it does

Ask CloudPal about AWS — EC2, S3, IAM, Lambda, databases, containers, networking, CI/CD, or AWS's own AI/ML services — and it retrieves the most relevant passages from a curated knowledge base, then uses an LLM to generate a grounded answer. You can type your question or ask it out loud using voice input.

**Note:** CloudPal doesn't cover every AWS service yet — it currently spans 15 domains, listed below, and is still being expanded.

## Features

- 🔍 **Retrieval-Augmented Generation (RAG)** — answers are grounded in real content, not model guesswork
- 🎙️ **Voice input** — ask questions out loud, transcribed via Whisper
- 💬 **Chat interface** — built with Streamlit, with light and dark theme support
- 📎 **Source attribution** — every answer shows which AWS topics it drew from
- ✅ **Automated tests + CI** — GitHub Actions runs the test suite on every push
- 🆓 **100% free stack** — every tool used has a free tier

## How it works

1. **Chunking** — AWS knowledge base articles (markdown files) are split into paragraph-sized chunks.
2. **Embedding** — each chunk is converted into a vector using `sentence-transformers` (`all-MiniLM-L6-v2`).
3. **Indexing** — chunk vectors are stored in a FAISS index for fast similarity search.
4. **Retrieval** — when you ask a question, it's embedded the same way, and FAISS returns the most similar chunks.
5. **Generation** — the retrieved chunks are combined with your question into a prompt, sent to an LLM via Groq, and the response is returned to you.

## Tech stack

| Purpose | Tool |
|---|---|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector search | FAISS |
| LLM inference | Groq (`openai/gpt-oss-120b`) |
| Voice transcription | Groq Whisper (`whisper-large-v3-turbo`) |
| Interface | Streamlit |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Hosting | Streamlit Community Cloud |

## Knowledge base

CloudPal currently answers questions on:

EC2 · S3 · Lambda · CloudWatch · VPC · IAM · RDS · DynamoDB · API Gateway · Containers (ECS/EKS/Fargate) · Load Balancing & Route 53 · DevOps & CI/CD · AI/ML services (Bedrock, SageMaker) · AWS Well-Architected Framework · CloudFront

More domains are being added over time.

## Getting started

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
git clone https://github.com/Fiber-dunstan/CloudPal.git
cd CloudPal
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# or: source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Run locally

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Run tests

```bash
pytest tests/ -v
```

## Project structure

```
CloudPal/
├── app.py                   # Streamlit UI
├── rag_utils.py              # RAG pipeline: chunking, embedding, retrieval, generation
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Light/dark theme configuration
├── data/                     # AWS knowledge base (markdown source files)
│   ├── ec2.md
│   ├── s3.md
│   └── ...
├── tests/
│   └── test_rag.py
└── .github/
    └── workflows/
        └── ci.yml             # Runs tests on every push
```

## Deployment

CloudPal is deployed free on [Streamlit Community Cloud](https://share.streamlit.io). To deploy your own copy:

1. Fork this repository.
2. Go to share.streamlit.io and connect your GitHub account.
3. Create a new app pointing to your fork, branch `main`, main file `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```
   GROQ_API_KEY = "your_key_here"
   ```
5. Deploy.

## Roadmap

- [ ] Broaden AWS service coverage
- [ ] Improve retrieval quality (re-ranking, larger context windows)
- [ ] Add response evaluation/quality metrics
- [ ] Expand voice interaction capabilities

## Author

Built by **Dunstan Banyaa (Hagan)** — Cloud & AI Engineer

- GitHub: [@Fiber-dunstan](https://github.com/Fiber-dunstan)
- LinkedIn: [linkedin.com/in/dunstan-banyaa](https://linkedin.com/in/dunstan-banyaa)

## License

MIT
