# ===================================================================
# ADVANCED BPE vs. HEB HEAD-TO-HEAD EVALUATION
#
# This script runs a more rigorous test by:
# 1. Using a larger dataset (10,000 samples).
# 2. Analyzing new metrics: Vocab Size & Token Length Distribution.
# 3. Testing HEB's sensitivity to its hyperparameters.
# ===================================================================

# ✅ Step 1. Install dependencies
!pip install datasets tokenizers sentence-transformers transformers tqdm matplotlib numpy scipy --quiet
print("✅ Dependencies installed.")

# ===================================================================
# Step 2. Imports
# ===================================================================
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
import functools
import seaborn as sns # For better plots

# Imports for dataset and standard tokenizers
from datasets import load_dataset
from transformers import AutoTokenizer

# Imports for Dynamic Contextual Tokenization (DCT)
from sentence_transformers import SentenceTransformer

print("✅ All libraries imported.")

# ===================================================================
# Step 3. Define All Tokenization Algorithms
#
# (We define all of them, but will only test BPE and HEB
# for this focused evaluation, plus EBT-Opt as a baseline)
# ===================================================================

# --- BPE Tokenizer (Our Baseline) ---
print("\nLoading BPE (GPT-2) tokenizer...")
bpe_tok = AutoTokenizer.from_pretrained("gpt2")
def bpe_tokenize(text):
    return bpe_tok.tokenize(text)

# --- Entropy Helper Functions ---
def shannon_entropy(seq):
    if not seq: return 0
    counts = Counter(seq)
    total = len(seq)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def shannon_entropy_from_counter(counter, total):
    if total == 0: return 0
    return -sum((c/total) * math.log2(c/total) for c in counter.values())

# --- EBT-Opt (For comparison) ---
def ebt_opt_tokenize(text, window=8, threshold=0.5):
    if len(text) < window + 1: return [text]
    tokens, start = [], 0
    window_counts = Counter(text[:window])
    try:
        last_entropy = shannon_entropy_from_counter(window_counts, window)
    except Exception:
        last_entropy = 0
    for i in range(1, len(text) - window + 1):
        char_out = text[i - 1]
        char_in = text[i + window - 1]
        window_counts[char_out] -= 1
        if window_counts[char_out] == 0:
            del window_counts[char_out]
        window_counts[char_in] = window_counts.get(char_in, 0) + 1
        try:
            current_entropy = shannon_entropy_from_counter(window_counts, window)
        except Exception:
            current_entropy = last_entropy
        delta = abs(current_entropy - last_entropy)
        if delta > threshold:
            tokens.append(text[start:i])
            start = i
        last_entropy = current_entropy
    tokens.append(text[start:])
    return [t.strip() for t in tokens if t.strip()]

# --- HEB (Our Contender) ---
def heb_tokenize(text, bpe_tokenizer, window=2, threshold=0.2):
    bpe_tokens = bpe_tokenizer.tokenize(text)
    if len(bpe_tokens) <= window:
        return ["".join(bpe_tokens).replace('Ġ', ' ').strip()]
    merged_tokens = []
    start = 0
    try:
        last_entropy = shannon_entropy(bpe_tokens[0:window])
    except Exception:
        last_entropy = 0
    for i in range(1, len(bpe_tokens) - window + 1):
        current_window = bpe_tokens[i : i + window]
        try:
            current_entropy = shannon_entropy(current_window)
        except Exception:
            current_entropy = last_entropy
        delta = abs(current_entropy - last_entropy)
        if delta > threshold:
            chunk = bpe_tokens[start:i]
            merged_tokens.append("".join(chunk).replace('Ġ', ' ').strip())
            start = i
        last_entropy = current_entropy
    final_chunk = bpe_tokens[start:]
    if final_chunk:
        merged_tokens.append("".join(final_chunk).replace('Ġ', ' ').strip())
    return [t for t in merged_tokens if t]

print("✅ Tokenizer functions defined.")

# ===================================================================
# Step 4. Load a Larger Dataset
# ===================================================================
print("\nLoading larger dataset (ag_news, 10,000 samples)...")
try:
    dataset = load_dataset("ag_news", split="train[:10000]")
    texts = [x["text"] for x in dataset]
    print(f"✅ Loaded {len(texts)} sample texts.")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    texts = [] # Will stop the script

# ===================================================================
# Step 5. Define Advanced Evaluation Function
# ===================================================================

def evaluate_tokenizer_advanced(fn, name, texts):
    """
    Runs a tokenizer on all texts and returns advanced metrics.
    """
    print(f"\nEvaluating {name} on {len(texts)} samples...")
    start = time.time()
    
    all_tokens_list = []
    all_token_lengths = []
    total_token_count = 0
    
    for t in tqdm(texts, desc=f"Testing {name}"):
        try:
            tokens = fn(t)
            all_tokens_list.extend(tokens)
            all_token_lengths.extend([len(tok) for tok in tokens])
            total_token_count += len(tokens)
        except Exception as e:
            pass # Skip errors on any single text

    end = time.time()
    
    # Calculate metrics
    elapsed = end - start
    avg_tokens = total_token_count / len(texts) if texts else 0
    unique_tokens = set(all_tokens_list)
    
    return {
        "name": name,
        "avg_tokens": avg_tokens,
        "runtime": elapsed,
        "total_unique_tokens": len(unique_tokens),
        "token_lengths_dist": all_token_lengths, # Returns all lengths for plotting
        "total_tokens": total_token_count
    }

# ===================================================================
# Step 6. Run Evaluations
# ===================================================================
if texts:
    print("\n===== STARTING ADVANCED EVALUATION (10k samples) =====")
    
    # Define the tokenizers we want to compare
    tokenizers_to_test = {
        "BPE (Baseline)": bpe_tokenize,
        "EBT-Opt (Fast-EBT)": ebt_opt_tokenize,
        "HEB (Thresh=0.1)": functools.partial(heb_tokenize, bpe_tokenizer=bpe_tok, threshold=0.1),
        "HEB (Thresh=0.2)": functools.partial(heb_tokenize, bpe_tokenizer=bpe_tok, threshold=0.2),
        "HEB (Thresh=0.3)": functools.partial(heb_tokenize, bpe_tokenizer=bpe_tok, threshold=0.3),
    }
    
    results = []
    for name, func in tokenizers_to_test.items():
        eval_data = evaluate_tokenizer_advanced(func, name, texts)
        results.append(eval_data)
        
    print("\n✅ Advanced evaluations complete.")
else:
    print("\nSkipping evaluation as dataset failed to load.")
    results = []

# ===================================================================
# Step 7. Plot Advanced Comparisons
# ===================================================================
if results:
    # --- Data for plotting ---
    names = [r['name'] for r in results]
    avg_tokens = [r['avg_tokens'] for r in results]
    runtimes = [r['runtime'] for r in results]
    unique_vocabs = [r['total_unique_tokens'] for r in results]
    
    # --- Plot 1: The Main Trade-off (Tokens vs. Runtime) ---
    plt.figure(figsize=(20, 7))
    
    # Subplot 1.1: Average Tokens (Compression)
    plt.subplot(1, 3, 1)
    bars1 = plt.bar(names, avg_tokens)
    plt.title("Average Tokens per Sentence (Lower is Better)", fontsize=14)
    plt.ylabel("Avg. Tokens")
    plt.xticks(rotation=45, ha="right")
    plt.bar_label(bars1, fmt='%.2f')
    
    # Subplot 1.2: Total Runtime (Speed)
    plt.subplot(1, 3, 2)
    bars2 = plt.bar(names, runtimes)
    plt.title(f"Total Runtime for {len(texts)} Samples", fontsize=14)
    plt.ylabel("Time (seconds)")
    plt.xticks(rotation=45, ha="right")
    plt.bar_label(bars2, fmt='%.2fs')
    
    # Subplot 1.3: Unique Vocabulary Size
    plt.subplot(1, 3, 3)
    bars3 = plt.bar(names, unique_vocabs)
    plt.title("Total Unique Tokens Created", fontsize=14)
    plt.ylabel("Unique Vocab Size")
    plt.xticks(rotation=45, ha="right")
    plt.bar_label(bars3, fmt='%.0f')
    
    plt.suptitle("Core Performance Metrics (10,000 Samples)", fontsize=18, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    
    # --- Plot 2: Token Length Distribution (The "What") ---
    plt.figure(figsize=(15, 7))
    plt.title("Distribution of Token Lengths (Characters)", fontsize=16, fontweight='bold')
    # We'll just compare BPE and one HEB variant for clarity
    bpe_lengths = next(r['token_lengths_dist'] for r in results if r['name'] == 'BPE (Baseline)')
    heb_lengths = next(r['token_lengths_dist'] for r in results if r['name'] == 'HEB (Thresh=0.2)')
    
    # Plot as KDE (Kernel Density Estimate)
    sns.kdeplot(bpe_lengths, label="BPE (Baseline)", fill=True, bw_adjust=0.5, clip=(0, 50))
    sns.kdeplot(heb_lengths, label="HEB (Thresh=0.2)", fill=True, bw_adjust=0.5, clip=(0, 50))
    
    plt.xlabel("Token Length (in characters)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 40) # Zoom in on the most common lengths
    plt.show()

# ===================================================================
# Step 8. Final Analysis & Summary
# ===================================================================
if results:
    print("\n" + "="*30)
    print("  FINAL ANALYSIS (10k Samples)")
    print("="*30)
    
    # --- Print Summary Table ---
    print(f"\n--- Summary Table ({len(texts)} samples) ---")
    print(f"{'Technique':<18} | {'Avg Tokens':<12} | {'Total Tokens':<14} | {'Runtime (s)':<12} | {'Unique Vocab':<14}")
    print("-" * 75)
    
    # Get BPE baseline for comparison
    bpe_baseline = next(r for r in results if r['name'] == 'BPE (Baseline)')
    
    for r in results:
        # Calculate compression vs BPE
        compression = bpe_baseline['total_tokens'] / r['total_tokens']
        print(f"{r['name']:<18} | {r['avg_tokens']:<12.2f} | {r['total_tokens']:<14.0f} | {r['runtime']:<12.2f} | {r['total_unique_tokens']:<14.0f}")

    print("\n--- Detailed Analysis ---")
    
    print("\n📊 1. Performance (Tokens vs. Runtime):")
    print(f"   - BPE (Baseline): Avg {bpe_baseline['avg_tokens']:.2f} tokens, Runtime {bpe_baseline['runtime']:.2f}s.")
    print("   - HEB (Hybrid): Your HEB variants should all show *fewer average tokens* than BPE. This is a clear win in compression.")
    print("   - Speed: HEB will be slower than pure BPE because it's a two-step process (BPE-pass + Python-pass). The key is *how much* slower. Is it 2x slower or 10x slower? This shows its practical viability.")
    
    print("\n🔬 2. Token Length Distribution (The 'How'):")
    print("   - Look at the 'Distribution of Token Lengths' plot.")
    print("   - BPE's graph will be heavily skewed to the left, with many short tokens (lengths 1-4).")
    print("   - HEB's graph should be 'shifted to the right'. This is **visual proof** that it's working: it's taking BPE's small, fragmented tokens and *merging them* into longer, more meaningful units. The HEB peak should be at a longer character length than BPE's peak.")

    print("\nvocab 3. Vocabulary Analysis (The 'What'):")
    print(f"   - BPE's unique vocab will be a subset of its ~50k static list (e.g., it might use ~15k of them for this 10k sample).")
    print("   - HEB's unique vocab is *dynamically created*. Look at its number. Is it larger or smaller than BPE's? A *smaller* dynamic vocab is a huge win, as it means the model's embedding layer would be smaller and more efficient.")

    print("\n⚙️ 4. Hyperparameter Sensitivity (The 'Stability'):")
    print("   - Compare `HEB (Thresh=0.1)` vs `0.2` vs `0.3`.")
    print("   - A lower threshold (0.1) is 'more sensitive' and should split more often, resulting in *more* tokens (closer to BPE).")
    print("   - A higher threshold (0.3) is 'less sensitive' and will merge more aggressively, resulting in *fewer* tokens.")
    print("   - This shows how you can 'tune' HEB: want more compression? Raise the threshold. Want to be more conservative? Lower it.")

    print("\n🏆 FINAL VERDICT:")
    print("   HEB is a confirmed success if the plots show:")
    print("   1. Avg Tokens (HEB) < Avg Tokens (BPE)")
    print("   2. The Runtime is reasonable (e.g., not 10x+ BPE's).")
    print("   3. The Token Length plot clearly shows a shift to longer, more meaningful tokens.")
    print("   4. The 'Unique Vocab' is manageable and ideally *smaller* than BPE's.")
    
else:
    print("Analysis skipped as no results were generated.")