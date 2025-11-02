import asyncio
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

async def cross_rerank(query, docs):
    pairs = [[query, d.page_content] for d in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(scores,docs), key=lambda x: -x[0])
    return [d for _, d in ranked]
