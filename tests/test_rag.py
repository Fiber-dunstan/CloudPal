"""Basic tests for the RAG helper functions (no Streamlit or API key required)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_utils import load_and_chunk_docs, load_embedder, build_index, retrieve


def test_docs_load():
    chunks, sources = load_and_chunk_docs()
    assert len(chunks) > 0, "Expected at least one chunk from data/"
    assert len(chunks) == len(sources)


def test_chunks_reasonable_size():
    chunks, _ = load_and_chunk_docs()
    for chunk in chunks:
        assert 0 < len(chunk) < 2000


def test_all_expected_sources_present():
    _, sources = load_and_chunk_docs()
    unique_sources = set(sources)
    expected = {
        "ec2.md", "s3.md", "lambda.md", "cloudwatch.md", "vpc.md",
        "iam.md", "rds.md", "dynamodb.md", "api-gateway.md", "containers.md",
        "networking-elb.md", "devops-cicd.md", "ai-ml.md", "well-architected.md",
        "cloudfront.md",
    }
    assert expected.issubset(unique_sources)


def test_retrieval_returns_relevant_chunk():
    chunks, sources = load_and_chunk_docs()
    embedder = load_embedder()
    index = build_index(embedder, chunks)
    results = retrieve("How do I store files in the cloud?", embedder, index, chunks, sources, k=1)
    assert len(results) == 1
    assert "s3" in results[0]["source"].lower()


if __name__ == "__main__":
    test_docs_load()
    test_chunks_reasonable_size()
    test_all_expected_sources_present()
    test_retrieval_returns_relevant_chunk()
    print("All tests passed.")