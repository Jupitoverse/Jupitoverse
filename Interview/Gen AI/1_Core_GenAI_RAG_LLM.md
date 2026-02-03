# 1. Core Gen AI, RAG & LLM – Interview Guide

---

## 📋 Quick Reference

| Concept | One-Liner |
|---------|-----------|
| RAG | Retrieve relevant docs → inject as context → LLM generates answer (reduces hallucination) |
| LLM | Large Language Model; autoregressive, trained on massive text; good at next-token prediction |
| Embedding | Dense vector representing semantic meaning of text (e.g. 384–1536 dims) |
| Vector DB | Store embeddings; search by similarity (cosine/dot product) for retrieval |
| Similarity metrics | Cosine (angle), dot product (same as cosine if normalized), L2 distance (smaller = more similar) |
| Chunking | Split docs before embedding; size 256–512 tokens typical; overlap 10–20% for continuity; recursive/section/semantic by doc type |
| Fine-tuning | Update model weights on domain data; costly, needs data + compute |
| Prompt engineering | Designing system/user prompts to get consistent, safe, task-specific outputs |

---

## 🔑 Core Concepts

### 1. What is RAG (Retrieval-Augmented Generation)?

```
User Query → Embed Query → Vector Search → Retrieve Top-K Docs → Build Context → LLM(Prompt + Context) → Answer
```

Why RAG over fine-tuning (for many use cases)?
- No retraining; update knowledge by updating the retrieval store.
- Reduces hallucination by grounding answers in retrieved facts.
- Lower cost and faster to iterate than fine-tuning.
- Good when you have a knowledge base (docs, tickets, manuals) that changes.

### 2. Embeddings & Semantic Search

- Embedding: A fixed-size vector (e.g. 384, 768, 1536 dimensions) that captures meaning.
- Semantic similarity: "Server crashed" and "Backend failure" have close vectors; keyword search would miss this.
- Typical flow: Encode query and documents with the same model → compare via cosine similarity or dot product → return top-K.

```python
# Conceptual
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
emb = model.encode("your text")  # e.g. 384-dim vector
```

### 3. Semantic Search Methods: Similarity & Distance

After encoding query and documents into vectors, we need a way to compare them. The choice of metric affects ranking and sometimes which index the vector DB uses. All of these operate on dense vectors (embedding space).

---

**Cosine similarity**

- Formula: \( \text{cosine}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_i A_i B_i}{\sqrt{\sum_i A_i^2} \sqrt{\sum_i B_i^2}} \)
- Range: -1 to 1. 1 = same direction (most similar), 0 = orthogonal, -1 = opposite.
- Interpretation: Measures the angle between two vectors; ignores magnitude (length).
- When to use: Default choice for semantic search when document/query lengths vary. Long and short texts with the same meaning get similar scores because length is normalized out.
- Pros: Invariant to vector magnitude; well-suited to text embeddings; most embedding models assume cosine (or normalized dot product) in training.
- Cons: Does not reflect magnitude; if magnitude carried meaning (e.g. confidence), that is lost.
- In code (NumPy): `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`. Or pre-normalize vectors and use dot product.

---

**Dot product (inner product)**

- Formula: \( A \cdot B = \sum_i A_i B_i \)
- Range: Unbounded (depends on vector length and dimension).
- When normalized: If both vectors are L2-normalized (unit length), dot product equals cosine similarity.
- When to use: When vectors are already normalized (many embedding APIs return unit vectors); then dot product is equivalent to cosine but one fewer operation. When magnitude is meaningful (e.g. relevance score encoded in length), unnormalized dot product can be used.
- Pros: Fast (single multiply-add loop); equivalent to cosine when vectors are normalized; some indexes (e.g. FAISS) optimize for dot product on normalized vectors.
- Cons: Unnormalized dot product is sensitive to length—longer documents can score higher even if less relevant.

---

**Euclidean distance (L2 distance)**

- Formula: \( \|A - B\|_2 = \sqrt{\sum_i (A_i - B_i)^2} \)
- Range: 0 to infinity. 0 = identical vectors; larger = less similar.
- Interpretation: Straight-line distance between two points. Minimizing L2 distance is equivalent to maximizing (negative squared L2) or, for normalized vectors, related to cosine (since \( \|A-B\|^2 = 2(1 - \cos(A,B)) \) when \(\|A\|=\|B\|=1\)).
- When to use: When the index or library expects a distance (e.g. k-NN by L2). Many vector DBs support L2; for normalized embeddings, L2 and cosine give the same ranking (monotonic relationship).
- Pros: Intuitive; many ANN algorithms (e.g. HNSW, IVF) support L2 natively.
- Cons: Sensitive to magnitude unless vectors are normalized; "similarity" is inverse of distance (smaller distance = more similar).

---

**Squared L2 distance**

- Formula: \( \|A - B\|_2^2 = \sum_i (A_i - B_i)^2 \)
- Used in practice to avoid the square root; same ranking as L2, cheaper to compute. Often what is implemented under the hood.

---

**Manhattan distance (L1)**

- Formula: \( \|A - B\|_1 = \sum_i |A_i - B_i| \)
- Less common for dense text embeddings. Used in some specialized or sparse settings. Not the default for semantic search.

---

**When to use which (summary)**

- Default for text RAG: Cosine similarity, or dot product on L2-normalized vectors (same ranking).
- If the system expects a distance: Use L2 (or squared L2) on normalized embeddings; ranking aligns with cosine.
- Always use the same metric at index time and query time; many embedding models are trained with cosine in mind.

---

**Quick code reference**

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def dot_product_normalized(a, b):
    # Same as cosine if a, b are unit vectors
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    return np.dot(a_norm, b_norm)

def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def l2_squared(a, b):
    return np.sum((np.array(a) - np.array(b)) ** 2)

# For normalized vectors: higher cosine = lower L2 (more similar)
# cos(A,B) = 1 - (L2_squared(A,B) / 2)  when |A|=|B|=1
```

---

### 4. Vector Databases

- Role: Store embeddings and support fast similarity search (ANN: approximate nearest neighbor).
- Examples: ChromaDB, Pinecone, Weaviate, FAISS, pgvector, Azure AI Search.
- ChromaDB: Embedded, persistent, good for prototyping and mid-scale; no separate server.
- Cosine similarity: `cos(θ) = (A·B)/(|A||B|)`; 1 = same direction, 0 = unrelated.

### 5. LLM Basics

- Decoder-only (e.g. GPT, LLaMA): Predict next token; good for generation and instruction following.
- Key knobs: Temperature (creativity vs determinism), max_tokens, top_p.
- Hallucination: Model generates plausible but false content; mitigated by RAG, lower temperature, and "say I don't know" instructions.

### 6. Prompt Engineering

- System prompt: Sets role, rules, format (e.g. "You are a support analyst. Answer only from the context.").
- User prompt: Task + context (e.g. retrieved chunks) + actual question.
- Few-shot: Include 1–3 examples in the prompt to steer format and behavior.
- Chain-of-thought (CoT): Ask model to "think step by step" for reasoning tasks.

---

## RAG Pipeline – Chunking Strategy (Detailed)

Chunking is how you split documents into smaller pieces before embedding and storing. It directly affects retrieval quality, context coherence, and cost. Poor chunking is a common cause of bad RAG.

---
 
### Why chunking matters

- Embedding models have a max input length (e.g. 512–8K tokens). Long documents must be split to fit.
- Smaller chunks → more precise retrieval (the right snippet is found) but risk losing surrounding context.
- Larger chunks → more context per chunk but noisier retrieval and fewer chunks that exactly match the query.
- Overlap between chunks can reduce “cut in the middle of a sentence” and preserve continuity at boundaries.

---

### Chunk size: trade-offs and typical values

**Small chunks (e.g. 128–256 tokens, ~100–200 words)**  
- Pros: Precise retrieval; query often matches one chunk well; less irrelevant text in context; more chunks = finer granularity.  
- Cons: May split a thought across chunks; LLM gets less surrounding context; more chunks = more embeddings and storage.  
- When to use: Factual Q&A, exact phrase or entity lookup, when answers are local to a short passage.

**Medium chunks (e.g. 256–512 tokens, ~200–400 words)**  
- Pros: Good balance of precision and context; works well for many docs (articles, tickets, docs).  
- Cons: Not ideal for very long paragraphs or for answers that span multiple sections.  
- When to use: Default choice for general RAG (support docs, knowledge bases, mixed content).
 g
**Large chunks (e.g. 512–1024+ tokens, ~400–800+ words)**  
- Pros: More context per chunk; good when the answer needs a full section or paragraph.  
- Cons: Retrieval is noisier; irrelevant parts of the chunk can dilute the answer; fewer, coarser chunks.  
- When to use: Long-form explanations, legal/contract clauses, or when the document has long coherent sections.

**Rule of thumb:** Start with 256–512 tokens (or 200–400 words). Tune using a small set of real queries: if answers are cut off or lack context, try larger chunks or overlap; if retrieval returns too much noise, try smaller chunks.

---

### Overlap: what it is and when to use it

**What is overlap?**  
Overlap is the number of characters (or tokens) shared between two consecutive chunks. Example: chunk size 100, overlap 20 → first chunk [0:100], second chunk [80:180], so positions 80–99 appear in both.

**Pros of overlap:**  
- Reduces the chance that a key sentence is split across a boundary (one chunk has the full sentence).  
- Improves recall for queries that land near a boundary.  
- Smoother context when you concatenate retrieved chunks.

**Cons of overlap:**  
- Duplicate content in the vector store and in the prompt → more storage and tokens.  
- Slightly more complex to implement (sliding window with step = size - overlap).  
- Too much overlap (e.g. 50%+) wastes tokens and can make chunks too similar.

**Typical values:**  
- Overlap 0: Simple, no redundancy; use when documents have clear boundaries (e.g. one paragraph per chunk).  
- Overlap 10–20% of chunk size (e.g. 50 chars for 500-char chunks): Common default; good for sentence continuity.  
- Overlap 50–100 tokens: Alternative when thinking in tokens; e.g. size 512, overlap 50.  
- Large overlap (e.g. 30–50%): Only when boundaries are very unclear or answers often span two chunks.

**When to use overlap:**  
- Use overlap when using fixed-size or token-based chunking (so boundaries are arbitrary).  
- Use little or no overlap when chunking by paragraph, section, or sentence (boundaries are already natural).

---

### Chunking types: comparison and when to use what

**1. Fixed-size (character or token)**  
- How it works: Split every N characters or every N tokens. Optional overlap (sliding window).  
- Pros: Simple, fast, predictable; easy to tune (one number: size).  
- Cons: Can split mid-word or mid-sentence; no respect for document structure.  
- When to use: Quick prototyping; unstructured or plain text; when other strategies are not worth the complexity.  
- Typical size: 256–512 tokens or 200–500 chars; overlap 0–20%.

**2. Sentence-based**  
- How it works: Split on sentence boundaries (e.g. `. `, `!`, `?`); then optionally group N sentences per chunk or cap by token size.  
- Pros: No mid-sentence cuts; sentences are natural units for meaning.  
- Cons: Sentence length varies a lot; need a good sentence splitter (language-dependent).  
- When to use: Prose, articles, support text; when you want readable, coherent chunks.  
- Typical size: 3–10 sentences per chunk or max 256–512 tokens per chunk.

**3. Paragraph-based**  
- How it works: Split on paragraph boundaries (e.g. `\n\n` or double newline). Optionally merge small paragraphs or split large ones by token cap.  
- Pros: Respects author structure; paragraphs are often one idea.  
- Cons: Paragraph length can be very uneven (one line vs long block).  
- When to use: Docs with clear paragraphs (blogs, docs, tickets with structured text).  
- Typical size: 1–3 paragraphs per chunk or max 512 tokens; little or no overlap.
*  
- How it works: Try to split by first separator (e.g. `\n\n`), then if a piece is still too big, split by `\n`, then by space, etc. Keeps chunk size under a max.  
- Pros: Respects hierarchy (paragraph > line > word); one algorithm for many doc types.  
- Cons: Behavior depends on separator order; can still get uneven chunks.  
- When to use: Mixed content (markdown, plain text, code); default in LangChain `RecursiveCharacterTextSplitter`.  
- Typical size: 500–1000 chars or 256–512 tokens; overlap 0–100 chars.

**5. Section / heading-based (structure-aware)**  
- How it works: Split by document structure: markdown headers (`#`, `##`), HTML headings, or XML sections. Each chunk = one section (or subsection) or a small set of sections.  
- Pros: Chunks align with “topics”; retrieval returns a full section; good for long-form docs.  
- Cons: Requires structured input (markdown, HTML, or tagged content); not all docs have clear headings.  
- When to use: Documentation, wikis, long articles with headers; when “section” is the right unit of retrieval.  
- Typical size: One section or N subsections; cap very long sections by tokens if needed.

**6. Semantic chunking**  
- How it works: Use embeddings or a model to detect “topic” or meaning change; split when similarity drops or when a new topic is detected. E.g. embed consecutive sentences and split when cosine similarity to previous drops below a threshold.  
- Pros: Chunks follow meaning, not arbitrary length; can improve retrieval when topics vary within a doc.  
- Cons: More compute (embed or score every segment); threshold is tunable; can be brittle on noisy text.  
- When to use: Long, multi-topic documents; when fixed-size or paragraph chunking leaves mixed-topic chunks.  
- Typical size: Variable; often used with a max token cap to avoid huge chunks.

**7. Sliding window with overlap**  
- How it works: Fixed-size chunks with a step smaller than size (e.g. size 512, step 384 → overlap 128).  
- Pros: Same as fixed-size + overlap; every span of text is “covered” by at least one chunk.  
- Cons: Redundancy; more chunks and tokens.  
- When to use: When you want fixed-size simplicity but also continuity at boundaries (e.g. narrative or technical docs).  
- Typical size: 256–512 tokens; overlap 10–25% of size.

**8. Token-based with model-specific limit**  
- How it works: Split by token count (using the same tokenizer as your embedding model) so no chunk exceeds the model’s max (e.g. 512 or 8192).  
- Pros: No embedding truncation; safe for API limits.  
- Cons: Token boundaries can split words (BPE); need to run tokenizer.  
- When to use: When embedding model has a strict token limit; production pipelines that must not exceed limits.  
- Typical size: Just under model max (e.g. 510 tokens for 512-max models); overlap optional.

---

### Chunking strategy: when to use what (summary)

- **Default / mixed content:** Recursive character (LangChain) or paragraph-based; size 256–512 tokens; overlap 10–20% if fixed-size.  
- **Structured docs (headers):** Section/heading-based; chunk = one section or a few; cap long sections.  
- **Prose / articles:** Sentence-based or paragraph-based; group by 3–10 sentences or 1–3 paragraphs; cap by tokens.  
- **Factual Q&A / entity lookup:** Smaller chunks (128–256 tokens); fixed-size or sentence; low or no overlap if boundaries are clear.  
- **Long, multi-topic docs:** Semantic chunking with a max token cap, or section-based if headings exist.  
- **Strict API limits:** Token-based chunking with size just under model max; overlap optional.  
- **Quick prototype:** Fixed-size 512 tokens, overlap 50; tune later with real queries.

---

### Quick reference: chunk size and overlap by use case

- **General knowledge base:** Chunk size 256–512 tokens; overlap 10–20% or ~50 tokens; recursive or paragraph-based.
- **Support tickets / short docs:** 200–400 tokens; overlap 0–20%; paragraph or sentence-based.
- **Long articles / documentation:** 512–1024 tokens; overlap 10–20%; section-based or recursive.
- **Factual Q&A / entity search:** 128–256 tokens; overlap 0–10%; fixed-size or sentence-based.
- **Legal / contracts:** 512–1024 tokens; overlap ~20% or split by section; section or semantic.
- **Code or logs:** 256–512 tokens; overlap 0; by block or line group.
- **Multi-topic long doc:** Variable chunk size; overlap optional; semantic chunking with a max token cap.

---

### Code sketch: common chunking patterns

```python
# Fixed-size with overlap (characters)
def chunk_fixed(text, size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# By paragraphs (split on double newline)
def chunk_paragraphs(text, max_tokens=512):
    paras = text.split("\n\n")
    chunks = []
    current = []
    current_tokens = 0
    for p in paras:
        n = estimate_tokens(p)
        if current_tokens + n > max_tokens and current:
            chunks.append("\n\n".join(current))
            current = []
            current_tokens = 0
        current.append(p)
        current_tokens += n
    if current:
        chunks.append("\n\n".join(current))
    return chunks

# LangChain RecursiveCharacterTextSplitter (conceptual)
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " "])
# chunks = splitter.split_text(text)
```

---

## RAG Pipeline – Embedding Models Comparison

Embedding models turn text into vectors for retrieval. Choice affects retrieval quality, latency, cost, and privacy. For each option: owned by, approximate cost, token limits (API), and who uses it.

**OpenAI text-embedding-3-small** (1536 dims, API)  
- Owned by: OpenAI.  
- Cost: ~$0.02/1M tokens (approx; check current pricing).  
- Tokens: Input up to 8K tokens per request; batch supported.  
- Used by: Widely used in SaaS, support tools, internal RAG; e.g. many YC startups, Notion AI, GitHub Copilot–style tooling.  
- Pros: High quality, easy to use, same vendor as GPT.  
- Cons: Cost per token, data leaves your env, rate limits.  
- When to use: Production when quality and simplicity matter, cloud OK.

**OpenAI text-embedding-3-large** (3072 dims, API)  
- Owned by: OpenAI.  
- Cost: ~$0.13/1M tokens (higher than small; check current pricing).  
- Tokens: Input up to 8K tokens per request.  
- Used by: Enterprises and products where retrieval quality is critical; often alongside GPT-4.  
- Pros: Best quality among OpenAI.  
- Cons: Higher cost, larger vectors = more storage/search cost.  
- When to use: When retrieval quality is critical.

**Sentence-Transformers, e.g. all-MiniLM-L6-v2** (384 dims, open/local)  
- Owned by: Community / Hugging Face (model from Microsoft/sentence-transformers).  
- Cost: Free (compute only; run on your hardware).  
- Tokens: No API limit; limited by model max length (~256–512 tokens typical; longer text chunked).  
- Used by: Startups and enterprises for on-prem RAG, research; LangChain docs, many open-source RAG tutorials.  
- Pros: Free, fast, runs on-prem, no API.  
- Cons: Slightly lower quality than top API models.  
- When to use: Prototyping, privacy, cost-sensitive, mid-scale.

**Sentence-Transformers, e.g. all-mpnet-base-v2** (768 dims, open/local)  
- Owned by: Community / Hugging Face.  
- Cost: Free (compute only).  
- Tokens: No API limit; model max length ~384 tokens.  
- Used by: Teams that need better quality than MiniLM but stay local; common in EU/privacy-first stacks.  
- Pros: Better quality than MiniLM, still local.  
- Cons: Slower and larger than MiniLM.  
- When to use: When you need better quality but stay local.

**Cohere embed-v3** (1024 dims, API)  
- Owned by: Cohere.  
- Cost: Usage-based; free tier available; paid ~$0.10/1M tokens range (check current pricing).  
- Tokens: Input up to 512 tokens per call (longer text chunked).  
- Used by: Enterprises for multilingual and intent-aware search; Cohere’s own RAG/semantic search customers.  
- Pros: Good quality, multilingual, embed with intent (search/doc).  
- Cons: API cost, vendor lock-in.  
- When to use: Multilingual or intent-specific retrieval.

**Voyage AI** (1024+ dims, API)  
- Owned by: Voyage AI (startup focused on retrieval).  
- Cost: Usage-based; competitive with OpenAI (check current pricing).  
- Tokens: Domain-specific models; typical input limits in 1K–8K range.  
- Used by: RAG-focused products; often cited in retrieval benchmarks and RAG blogs.  
- Pros: Tuned for RAG, strong retrieval benchmarks.  
- Cons: API, less ecosystem than OpenAI.  
- When to use: RAG-focused apps, willing to use API.

**BGE, e.g. BAAI/bge-base-en-v1.5** (768 dims, open/local)  
- Owned by: BAAI (Beijing Academy of AI); hosted on Hugging Face.  
- Cost: Free (compute only).  
- Tokens: No API limit; max sequence 512 tokens.  
- Used by: Open-source RAG stacks, non-US deployments; strong in MTEB-style benchmarks.  
- Pros: Strong open benchmarks, Hugging Face.  
- Cons: Self-hosted setup.  
- When to use: Open-source stack, good quality/cost.

**E5, e.g. intfloat/e5-base-v2** (768 dims, open/local)  
- Owned by: Microsoft (intfloat); Hugging Face.  
- Cost: Free (compute only).  
- Tokens: No API limit; max 512 tokens.  
- Used by: Research and production RAG where query/passage prefix is controlled; used in Microsoft products.  
- Pros: Query and passage encoding, good for retrieval.  
- Cons: Need to add "query: " / "passage: " prefix.  
- When to use: When you control ingestion and query formatting.

**Jina embeddings** (1024+ dims, API)  
- Owned by: Jina AI.  
- Cost: Free tier; paid usage-based (check jina.ai pricing).  
- Tokens: Long-document support (e.g. 8K); good for full-page embedding.  
- Used by: Long-doc RAG, multimodal use cases; Jina’s own RAG/embedding customers.  
- Pros: Good for long docs, multimodal options.  
- Cons: API cost.  
- When to use: Long-document or multimodal RAG.

**Azure OpenAI Embeddings** (1536 etc., API)  
- Owned by: Microsoft (Azure); same models as OpenAI.  
- Cost: Similar to OpenAI; Azure commitment discounts; check Azure pricing.  
- Tokens: Same as OpenAI (e.g. 8K input).  
- Used by: Enterprises on Azure (banks, healthcare, gov); Microsoft 365 Copilot–style deployments.  
- Pros: Same as OpenAI, Azure compliance/SLA.  
- Cons: Azure ecosystem, cost.  
- When to use: Enterprise on Azure, compliance needs.

**Summary:** Prefer open/local (sentence-transformers, BGE, E5) when data must stay on-prem, zero API cost, or high volume. Prefer API (OpenAI, Cohere, Voyage, Jina) when you want best quality with minimal ops or need multilingual/intent-specific features. Dimension: smaller = faster and cheaper storage/search; larger often = better quality.

---

## RAG Pipeline – Vector Databases Comparison

Vector DBs store embeddings and run approximate nearest neighbor (ANN) search. Choice affects scale, latency, ops, and cost. For each: owned by, approximate cost, typical scale/limits, and who uses it.

**ChromaDB** (embedded / serverless)  
- Owned by: Chroma (open-source; Chroma Inc. offers hosted).  
- Cost: Free (open source); Chroma Cloud has usage-based paid tiers (check chroma.dev).  
- Scale / limits: Single-node; typical up to low millions of vectors; no built-in horizontal scale.  
- Used by: LangChain default for tutorials; many startups and internal tools; rapid prototyping.  
- Pros: Easy start, persistent, no separate server, good for dev and mid-scale.  
- Cons: Scale limits, fewer enterprise features.  
- When to use: Prototyping, small/medium apps, single-node.

**Pinecone** (managed)  
- Owned by: Pinecone (standalone company; AWS-native).  
- Cost: Free tier (1 index, limited size); paid from ~$70/month (serverless) or dedicated pricing; scales with usage (check pinecone.io).  
- Scale / limits: Billions of vectors; serverless or dedicated; managed scaling.  
- Used by: Shopify, Gong, Notion-style products; many production RAG and recommendation systems.  
- Pros: Fully managed, scales well, low ops.  
- Cons: Cost at scale, vendor lock-in.  
- When to use: Production when you want no vector-DB ops.

**Weaviate** (self-hosted / managed)  
- Owned by: Weaviate (company); open-source core; Weaviate Cloud Services (WCS) managed.  
- Cost: Free (self-hosted); WCS usage-based (check weaviate.io).  
- Scale / limits: Horizontal scaling; graph + vector; hybrid search; typical millions of vectors.  
- Used by: Enterprises needing hybrid (keyword + vector); used in telecom, media, and knowledge bases.  
- Pros: Graph + vector, hybrid search, flexible schema.  
- Cons: Heavier to run, learning curve.  
- When to use: When you need hybrid (keyword + vector) or graph.

**Qdrant** (self-hosted / cloud)  
- Owned by: Qdrant (company); open-source; Qdrant Cloud managed.  
- Cost: Free (self-hosted); Qdrant Cloud free tier + usage-based (check qdrant.tech).  
- Scale / limits: Good for millions to hundreds of millions; filtering and payload; HNSW/IVF.  
- Used by: RAG and semantic search in production; used by startups and mid-size companies; strong filtering use cases.  
- Pros: Good performance, filtering, payload storage.  
- Cons: You run/scale it unless cloud.  
- When to use: Performance-sensitive, filter-heavy RAG.

**pgvector (PostgreSQL)** (extension)  
- Owned by: PostgreSQL community; pgvector by pgvector/pgvector.  
- Cost: Free (extension); you pay for Postgres (self-hosted, RDS, Aurora, etc.).  
- Scale / limits: Depends on Postgres; typical millions of vectors; single-node or read replicas; IVFFlat/HNSW indexes.  
- Used by: Teams already on Postgres; Supabase, Neon; many apps that want one DB for relational + vector.  
- Pros: SQL + vector in one DB, ACID, existing Postgres skills.  
- Cons: ANN performance not as tuned as dedicated vector DBs.  
- When to use: Already on Postgres, moderate scale, want one DB.

**FAISS** (library)  
- Owned by: Meta (Facebook AI Research); open-source.  
- Cost: Free (library); you pay for compute/memory.  
- Scale / limits: In-memory; billions of vectors possible with enough RAM; single-node; no persistence by default.  
- Used by: Research; high-throughput in-memory search; used internally at Meta; many ML pipelines.  
- Pros: In-memory, very fast, Facebook research.  
- Cons: No persistence by default, single-node, you build everything.  
- When to use: Research, ultra-low-latency in-memory search.

**Milvus** (distributed)  
- Owned by: LF AI (Linux Foundation); Zilliz (company) drives development; Zilliz Cloud managed.  
- Cost: Free (self-hosted); Zilliz Cloud usage-based (check zilliz.com).  
- Scale / limits: Distributed; billions of vectors; multi-node; strong for very large scale.  
- Used by: Large enterprises and platforms (e.g. Alibaba, JD); very large-scale similarity search.  
- Pros: Scale-out, good for huge vectors.  
- Cons: Complex to operate.  
- When to use: Very large scale, dedicated team.

**Redis (RediSearch)** (in-memory + persistence)  
- Owned by: Redis Ltd.; open-source Redis + RediSearch module.  
- Cost: Free (self-hosted); Redis Cloud has vector support (usage-based).  
- Scale / limits: In-memory first; persistence optional; vector as HNSW; typical millions; you may already use Redis.  
- Used by: Apps that already use Redis for cache/session; add vector in same stack; common in real-time apps.  
- Pros: Fast, you may already use Redis.  
- Cons: Vector support newer, less RAG-specific.  
- When to use: Existing Redis stack, cache + vector in one place.

**Azure AI Search** (managed)  
- Owned by: Microsoft (Azure).  
- Cost: Tier-based (free, basic, standard, etc.); pay for search units and storage (check Azure pricing).  
- Scale / limits: Vector + keyword in one service; integrated with Azure OpenAI; typical enterprise scale.  
- Used by: Enterprises on Azure; Microsoft 365 Copilot, Azure Cognitive Search customers; hybrid search in cloud.  
- Pros: Vector + keyword in one service, Azure integration.  
- Cons: Azure-only, cost.  
- When to use: Azure-first, need hybrid search in cloud.

**Elasticsearch (dense_vector)** (search engine)  
- Owned by: Elastic (company); open-source Elasticsearch.  
- Cost: Free (self-hosted); Elastic Cloud usage-based.  
- Scale / limits: Full-text + vector; horizontal scaling; dense_vector + kNN; typical search-engine scale.  
- Used by: Log search, product search, observability; companies already on ES add vector for hybrid (e.g. e‑commerce, support).  
- Pros: Full-text + vector, mature ecosystem.  
- Cons: Heavier, vector is add-on.  
- When to use: Already using ES for search, add vector on top.

**LanceDB** (embedded)  
- Owned by: LanceDB (open-source project).  
- Cost: Free (embedded/serverless).  
- Scale / limits: Embedded; serverless-friendly; good for edge and mid-scale; Lance format for columnar storage.  
- Used by: Edge and serverless RAG; newer stack; adopted in some startups and OSS projects.  
- Pros: Serverless-friendly, good for edge/dev.  
- Cons: Newer, smaller ecosystem.  
- When to use: Embedded or serverless RAG.

**Marqo** (open source)  
- Owned by: Marqo (company); open-source.  
- Cost: Free (self-hosted); Marqo Cloud (check marqo.ai).  
- Scale / limits: Multimodal (text + image); built for ML; typical millions of vectors.  
- Used by: Multimodal search and RAG; product catalogs with images; smaller but growing community.  
- Pros: Multimodal, built for ML.  
- Cons: Smaller community.  
- When to use: Multimodal retrieval.

**Summary:** Prototyping/small app → ChromaDB or pgvector. Production, no ops → Pinecone or Azure AI Search. Already on Postgres → pgvector. Need hybrid → Weaviate, Azure AI Search, or Elasticsearch. Max scale → Milvus or Qdrant. In-memory/research → FAISS.

---

## RAG Pipeline – LLMs for Generation (Brief Comparison)

The final step in RAG is generation: LLM takes prompt + retrieved context and produces the answer. For each: owned by, approximate cost, token/context limits, and who uses it.

**OpenAI GPT-4o / GPT-4** (large context, 128K+)  
- Owned by: OpenAI (Microsoft-backed).  
- Cost: GPT-4o ~$2.50/1M input, ~$10/1M output (approx; check openai.com/pricing). GPT-4 more expensive.  
- Tokens: Context 128K (GPT-4o); output limits configurable (e.g. 4K–16K).  
- Used by: ChatGPT, GitHub Copilot, Notion AI, many enterprise RAG and support tools; widely adopted.  
- Pros: Best quality, tool use, vision.  
- Cons: Cost, API, data leaves your env.  
- When to use: When quality and features matter most.

**OpenAI GPT-3.5-turbo** (16K)  
- Owned by: OpenAI.  
- Cost: ~$0.50/1M input, ~$1.50/1M output (approx; cheaper than GPT-4).  
- Tokens: Context 16K; output configurable.  
- Used by: High-volume apps, chatbots, simple extraction; cost-sensitive production RAG.  
- Pros: Cheap, fast.  
- Cons: Weaker than GPT-4.  
- When to use: High volume, simple tasks, cost-sensitive.

**Anthropic Claude** (large context)  
- Owned by: Anthropic.  
- Cost: Varies by model (e.g. Claude 3.5 Sonnet ~$3/1M input, ~$15/1M output; check anthropic.com/pricing).  
- Tokens: Context 200K (Claude 3); long-doc and RAG-friendly.  
- Used by: Enterprise and startups for long-context RAG; used by Notion, others; strong instruction following.  
- Pros: Strong instruction following, long context.  
- Cons: API, cost.  
- When to use: Alternative to GPT-4, long docs.

**Ollama (Llama, Qwen, etc.)** (varies)  
- Owned by: Ollama (company); models from Meta (Llama), Alibaba (Qwen), etc.; run locally.  
- Cost: Free (no API); you pay for GPU/compute.  
- Tokens: Depends on model (e.g. Llama 3 8K–128K context); no API token limit.  
- Used by: Developers and enterprises for on-prem RAG; privacy-first and offline use; many internal tools.  
- Pros: Free, local, no data leaves.  
- Cons: Need GPU/resources, quality varies by model.  
- When to use: Privacy, offline, zero API cost.

**Azure OpenAI** (same as OpenAI)  
- Owned by: Microsoft (Azure); same models as OpenAI.  
- Cost: Similar to OpenAI; Azure commitment discounts; check Azure pricing.  
- Tokens: Same as OpenAI (e.g. 128K for GPT-4o).  
- Used by: Enterprises on Azure (banks, healthcare, gov); Microsoft 365 Copilot, Azure customers.  
- Pros: Same models, Azure SLA/compliance.  
- Cons: Azure ecosystem, cost.  
- When to use: Enterprise on Azure.

**Open-source (vLLM, TGI)** (varies)  
- Owned by: vLLM (UC Berkeley / community); TGI (Hugging Face). Run your own model (Llama, Mistral, etc.).  
- Cost: Free (no API); you pay for GPU/compute and hosting.  
- Tokens: Depends on model (e.g. Llama 128K); no API limit.  
- Used by: On-prem and high-volume deployments; companies that need full control and compliance.  
- Pros: Full control, no API cost.  
- Cons: You run and scale.  
- When to use: On-prem, compliance, cost at scale.

Use smaller/cheaper models (e.g. GPT-3.5, small local) for simple extraction or when cost is critical; use GPT-4/Claude when answer quality and reasoning matter.

---

## 💡 Top 20 Interview Q&A – Gen AI / RAG / LLM

Q1: What is RAG and when do you use it?
> "RAG retrieves relevant documents, adds them as context to the prompt, and lets the LLM generate an answer. I use it when the model needs up-to-date or private knowledge, or when we want to reduce hallucination by grounding answers in a known corpus."

Q2: RAG vs fine-tuning?
> "RAG injects context at inference time; fine-tuning changes model weights. RAG is cheaper, easier to update, and great for knowledge-heavy tasks. Fine-tuning is for changing style, format, or deep domain behavior when you have enough quality data."

Q3: How do embeddings capture semantic meaning?
> "They’re trained so that semantically similar text gets similar vectors. So 'outage' and 'service down' are close in vector space. That enables meaning-based search instead of exact keyword match."

Q4: Keyword vs semantic search?
> "Keyword matches terms (e.g. 'server error' only). Semantic search uses embeddings so 'backend failure' can match 'server error'. Essential when users phrase the same problem in many ways."

Q5: How do you reduce LLM hallucination?
> "Use RAG to ground in retrieved facts; lower temperature for stability; instruct the model to say 'I don’t know' when unsure; validate critical outputs against a source of truth; collect feedback to improve prompts and retrieval."

Q6: Why use multiple LLM calls instead of one big prompt?
> "Specialized prompts per task often outperform one giant prompt. Benefits: clearer tasks, easier debugging, cacheable intermediate results, and the option to run some calls in parallel."

Q7: What is a vector database and why not use a normal DB?
> "A vector DB is built for similarity search over high-dimensional vectors (e.g. ANN indexes like HNSW). A normal DB can do exact match or simple filters but isn’t optimized for 'find top-K most similar vectors' at scale."

Q8: Cosine similarity vs dot product?
> "Cosine measures angle (ignores magnitude); dot product depends on length too. For normalized embeddings they’re equivalent. Cosine is common when document lengths vary."

Q9: How do you choose chunk size in RAG?
> "Trade-off: small chunks give precise retrieval but may lose context; large chunks keep context but add noise. I typically try 256–512 tokens, consider overlap, and test with real queries. Sometimes use semantic chunking (e.g. by section or paragraph)."

Q10: What is an embedding model and how do you pick one?
> "It’s a model that maps text to a fixed-size vector. I consider: dimension (cost/speed), quality on my domain, latency, and whether it’s open (e.g. sentence-transformers) or API-based (e.g. OpenAI)."

Q11: How do you evaluate RAG?
> "Retrieval: relevance of top-K (e.g. hit rate, MRR). Generation: faithfulness to context, relevance to question, lack of hallucination. I use manual review, LLM-as-judge, or metrics like BLEU/ROUGE where applicable, plus user feedback."

Q12: What is temperature and how do you set it?
> "Temperature controls randomness. Low (e.g. 0–0.3) for factual, deterministic answers; higher for creative or diverse outputs. For RAG/support I usually keep it low."

Q13: What are token limits and why do they matter?
> "LLMs have a max context length (e.g. 8K–128K tokens). Input + output must fit. I keep prompts concise, trim or summarize retrieved chunks, and set max_tokens to cap response length and cost."

Q14: How do you handle long documents in RAG?
> "Chunk the document, embed chunks, store in vector DB. At query time retrieve top-K chunks and optionally re-rank. For very long docs, map-reduce or hierarchical summarization can help."

Q15: What is re-ranking and when do you use it?
> "Re-ranking takes top-N results from vector search and re-scores them with a more accurate (often heavier) model. Use it when you need higher precision and can afford the extra latency and cost."

Q16: Explain attention in transformers (high level).
> "Attention lets each token look at other tokens and weight their importance. So the model can focus on relevant parts of the input when producing each output token, which is key for long-range dependencies."

Q17: What is fine-tuning vs prompt engineering?
> "Prompt engineering shapes behavior via text (system/user prompts, few-shot). Fine-tuning updates model weights on labeled data. Prompting is fast and flexible; fine-tuning is for when you need deeper, consistent behavior change."

Q18: How do you secure LLM inputs/outputs in production?
> "Validate and sanitize inputs; avoid leaking PII in prompts/logs; use output schemas or parsing to constrain format; rate limit and monitor; consider private endpoints or on-prem models for sensitive data."

Q19: What is context window and why does it matter?
> "Context window is the maximum number of tokens the model can take as input. It limits how much retrieval context we can add and how long the conversation history can be. I design RAG and UX around this limit."

Q20: How do you optimize cost for LLM APIs?
> "Cache responses for repeated queries; minimize prompt size (shorter context, concise instructions); use smaller/cheaper models where quality is sufficient; batch where possible; set max_tokens; monitor token usage per use case."

---

## 📊 Key Talking Points

- RAG pipeline: Query → embed → vector search → retrieve → build prompt → LLM → parse/validate answer.
- When to use RAG: Knowledge-heavy apps, private/updated knowledge, need to cite sources, reduce hallucination.
- Vector DB choice: Scale, latency, managed vs self-hosted, cost (e.g. ChromaDB for dev/small scale; Pinecone/Weaviate for large scale).
- Evaluation: Retrieval metrics (recall, MRR) + generation metrics (faithfulness, relevance) + user feedback.

---

## 📁 See Also

- [2_LangChain_LangGraph_Agents_MCP.md](2_LangChain_LangGraph_Agents_MCP.md) – Orchestration and agents  
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index  
- Project Details: SR Analyzer (Ollama/OpenAI) for concrete RAG examples
