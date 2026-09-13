"""Core RAG (Retrieval-Augmented Generation) logic: loading documents, chunking them,
building a searchable vector index, retrieving relevant chunks, and generating an answer."""
import os
import glob
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CHUNK_SIZE = 500
EMBED_MODEL = "all-MiniLM-L6-v2"


def load_and_chunk_docs(data_dir: str = DATA_DIR, chunk_size: int = CHUNK_SIZE):
    """Read every markdown file in data_dir and split it into paragraph-sized chunks."""
    chunks, sources = [], []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        buf = ""
        for p in paragraphs:
            if len(buf) + len(p) < chunk_size:
                buf = f"{buf}\n\n{p}" if buf else p
            else:
                if buf:
                    chunks.append(buf)
                    sources.append(os.path.basename(path))
                buf = p
        if buf:
            chunks.append(buf)
            sources.append(os.path.basename(path))
    return chunks, sources


def load_embedder(model_name: str = EMBED_MODEL) -> SentenceTransformer:
    """Load the embedding model that turns text into numeric vectors."""
    return SentenceTransformer(model_name)


def build_index(embedder: SentenceTransformer, chunks: list[str]):
    """Embed every chunk and build a FAISS index for fast similarity search."""
    embeddings = embedder.encode(chunks, normalize_embeddings=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings, dtype="float32"))
    return index


def retrieve(query: str, embedder: SentenceTransformer, index, chunks, sources, k: int = 3):
    """Embed the user's question and return the k most similar chunks."""
    q_emb = embedder.encode([query], normalize_embeddings=True)
    scores, idxs = index.search(np.array(q_emb, dtype="float32"), k)
    results = []
    for score, idx in zip(scores[0], idxs[0]):
        if idx == -1:
            continue
        results.append({"text": chunks[idx], "source": sources[idx], "score": float(score)})
    return results


def build_prompt(query: str, retrieved: list[dict]) -> str:
    """Combine the retrieved context with the user's question into one prompt for the LLM."""
    context = "\n\n---\n\n".join(f"[Source: {r['source']}]\n{r['text']}" for r in retrieved)
    return (
        "You are a helpful cloud engineering assistant. Answer the question using "
        "ONLY the context below. If the answer isn't in the context, say you don't "
        f"have enough information.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    )


def generate_answer(client, prompt: str, model: str = "openai/gpt-oss-120b") -> str:
    """Send the prompt to Groq's LLM and return the generated answer text."""
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )
    return resp.choices[0].message.content