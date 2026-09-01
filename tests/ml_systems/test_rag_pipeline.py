from python.ml_systems.rag_pipeline import RAGPipeline


def test_lexical_ranking_and_provenance():
    rag = RAGPipeline(max_context_tokens=20)
    rag.index_document("guide", "Python systems use queues and replicas", {"owner": "team"}, chunk_size=3)
    rag.index_document("other", "Python syntax examples", {"owner": "docs"})
    results = rag.retrieve("python replicas", top_k=5)
    assert results[0].chunk.document_id == "guide"
    assert results[0].citation == "[guide:0]"
    assert results[0].chunk.metadata == {"owner": "team"}


def test_reindex_removes_stale_terms_and_context_obeys_budget():
    rag = RAGPipeline(max_context_tokens=4)
    rag.index_document("doc", "oldword alpha beta gamma", chunk_size=2)
    assert rag.retrieve("oldword")
    rag.index_document("doc", "newword only", chunk_size=2)
    assert rag.retrieve("oldword") == ()
    results = rag.retrieve("newword only")
    context = rag.build_context(results)
    assert context.text == "newword only"
    assert context.citations == ("[doc:0]",)


def test_metadata_and_returned_results_are_isolated():
    metadata = {"source": ["trusted-looking"]}
    rag = RAGPipeline()
    rag.index_document("doc", "untrusted text", metadata)
    metadata["source"].append("mutated")
    result = rag.retrieve("untrusted")[0]
    result.chunk.metadata["source"].append("caller")
    assert rag.retrieve("untrusted")[0].chunk.metadata == {"source": ["trusted-looking"]}
