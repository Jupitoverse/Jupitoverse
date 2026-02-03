"""
Demo Script for Feedback Storage System
Demonstrates how to use the feedback system programmatically
"""

from feedback_storage import WorkaroundFeedbackStorage
from pathlib import Path


def demo_basic_operations():
    """Demo: Basic vote recording and retrieval"""
    print("=" * 80)
    print("DEMO 1: Basic Operations")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    # Simulate user feedback for different SRs
    print("\n[*] Recording votes for SR-001...")
    storage.upvote("SR-001", "ai", "Check PS config, update ipAddressRange field, and retry task")
    storage.upvote("SR-001", "ai", "Check PS config, update ipAddressRange field, and retry task")
    storage.upvote("SR-001", "ai", "Check PS config, update ipAddressRange field, and retry task")
    storage.downvote("SR-001", "ai", "Check PS config, update ipAddressRange field, and retry task")
    
    print("[*] Recording votes for SR-001 original workaround...")
    storage.downvote("SR-001", "original", "Manual fix required - contact L3 support")
    storage.downvote("SR-001", "original", "Manual fix required - contact L3 support")
    
    # Get and display votes
    ai_votes = storage.get_votes("SR-001", "ai")
    original_votes = storage.get_votes("SR-001", "original")
    
    print(f"\n[Results] SR-001 AI Workaround:")
    print(f"  Upvotes: {ai_votes['upvotes']}")
    print(f"  Downvotes: {ai_votes['downvotes']}")
    print(f"  Score: {ai_votes['score']:+d}")
    
    print(f"\n[Results] SR-001 Original Workaround:")
    print(f"  Upvotes: {original_votes['upvotes']}")
    print(f"  Downvotes: {original_votes['downvotes']}")
    print(f"  Score: {original_votes['score']:+d}")


def demo_multiple_srs():
    """Demo: Multiple SRs with different vote patterns"""
    print("\n" + "=" * 80)
    print("DEMO 2: Multiple SRs with Different Vote Patterns")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    # SR-002: Highly validated AI workaround
    print("\n[*] SR-002: Highly validated solution")
    for _ in range(10):
        storage.upvote("SR-002", "ai", "Clear cache in OSO, restart service, verify in logs")
    storage.downvote("SR-002", "ai", "Clear cache in OSO, restart service, verify in logs")
    
    # SR-003: Mixed feedback
    print("[*] SR-003: Mixed feedback")
    for _ in range(3):
        storage.upvote("SR-003", "ai", "Update VLAN configuration in PS")
    for _ in range(3):
        storage.downvote("SR-003", "ai", "Update VLAN configuration in PS")
    
    # SR-004: Problematic solution
    print("[*] SR-004: Problematic solution")
    storage.upvote("SR-004", "ai", "Delete and recreate project")
    for _ in range(5):
        storage.downvote("SR-004", "ai", "Delete and recreate project")
    
    # Display all
    print("\n[Results] Vote Summary:")
    for sr_id in ["SR-002", "SR-003", "SR-004"]:
        votes = storage.get_votes(sr_id, "ai")
        
        # Determine emoji
        if votes['score'] > 5:
            emoji = "🔥"
            label = "HIGHLY VALIDATED"
        elif votes['score'] > 0:
            emoji = "✅"
            label = "VALIDATED"
        elif votes['score'] == 0:
            emoji = "⚖️"
            label = "MIXED"
        else:
            emoji = "⚠️"
            label = "PROBLEMATIC"
        
        print(f"\n  {sr_id}: 👍 {votes['upvotes']} | 👎 {votes['downvotes']} | Score: {votes['score']:+d} {emoji} {label}")


def demo_top_workarounds():
    """Demo: Get top-rated workarounds"""
    print("\n" + "=" * 80)
    print("DEMO 3: Top Rated Workarounds")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    top_workarounds = storage.get_top_workarounds(limit=5, min_votes=1)
    
    if top_workarounds:
        print(f"\n[*] Top {len(top_workarounds)} Workarounds:")
        for idx, w in enumerate(top_workarounds, 1):
            print(f"\n{idx}. {w['sr_id']} ({w['workaround_type']})")
            print(f"   Score: {w['score']:+d} (👍 {w['upvotes']} | 👎 {w['downvotes']})")
            print(f"   Text: {w['workaround_text'][:100]}...")
    else:
        print("\n[*] No workarounds have been rated yet.")


def demo_bottom_workarounds():
    """Demo: Get lowest-rated workarounds"""
    print("\n" + "=" * 80)
    print("DEMO 4: Lowest Rated Workarounds (Need Improvement)")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    bottom_workarounds = storage.get_bottom_workarounds(limit=5)
    
    if bottom_workarounds:
        print(f"\n[*] Bottom {len(bottom_workarounds)} Workarounds:")
        for idx, w in enumerate(bottom_workarounds, 1):
            print(f"\n{idx}. {w['sr_id']} ({w['workaround_type']})")
            print(f"   Score: {w['score']:+d} (👍 {w['upvotes']} | 👎 {w['downvotes']})")
            print(f"   Text: {w['workaround_text'][:100]}...")
            print(f"   ⚠️ This solution needs review and improvement!")
    else:
        print("\n[*] No workarounds have negative feedback.")


def demo_statistics():
    """Demo: Overall statistics"""
    print("\n" + "=" * 80)
    print("DEMO 5: Overall Statistics")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    stats = storage.get_statistics()
    
    print(f"\n[*] Feedback Statistics:")
    print(f"  Total Workarounds with Feedback: {stats['total_workarounds_with_feedback']}")
    print(f"  Total Upvotes: {stats['total_upvotes']}")
    print(f"  Total Downvotes: {stats['total_downvotes']}")
    print(f"  Average Score: {stats['average_score']:.2f}")
    
    if stats['best_workaround']['sr_id']:
        print(f"\n  🏆 Best Workaround:")
        print(f"     SR: {stats['best_workaround']['sr_id']}")
        print(f"     Type: {stats['best_workaround']['type']}")
        print(f"     Score: {stats['best_workaround']['score']:+d}")
    
    if stats['worst_workaround']['sr_id']:
        print(f"\n  ⚠️ Worst Workaround:")
        print(f"     SR: {stats['worst_workaround']['sr_id']}")
        print(f"     Type: {stats['worst_workaround']['type']}")
        print(f"     Score: {stats['worst_workaround']['score']:+d}")


def demo_export():
    """Demo: Export feedback data"""
    print("\n" + "=" * 80)
    print("DEMO 6: Export Feedback Data")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    output_path = Path(__file__).parent.parent / "llm output" / "feedback_export.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        storage.export_to_csv(str(output_path))
        print(f"\n[OK] Feedback data exported to: {output_path}")
        print("[*] You can open this CSV in Excel for analysis")
    except Exception as e:
        print(f"\n[ERROR] Export failed: {e}")


def demo_priority_ranking():
    """Demo: How votes affect priority ranking"""
    print("\n" + "=" * 80)
    print("DEMO 7: Priority Ranking Algorithm")
    print("=" * 80)
    
    storage = WorkaroundFeedbackStorage()
    
    # Simulate historical matches with different vote patterns
    matches = [
        {"sr_id": "SR-001", "similarity": 0.85},
        {"sr_id": "SR-002", "similarity": 0.82},
        {"sr_id": "SR-003", "similarity": 0.80},
        {"sr_id": "SR-004", "similarity": 0.90},
    ]
    
    print("\n[*] Historical Matches (unsorted):")
    for m in matches:
        votes = storage.get_votes(m['sr_id'], 'ai')
        print(f"  {m['sr_id']}: Similarity={m['similarity']:.0%}, Votes={votes['score']:+d}")
    
    # Apply priority ranking (70% similarity + 30% votes)
    def calculate_priority(match):
        votes = storage.get_votes(match['sr_id'], 'ai')
        vote_score = votes['score']
        
        # Normalize vote score from [-10, 10] to [0, 1]
        normalized_vote = (vote_score + 10) / 20.0
        normalized_vote = max(0, min(1, normalized_vote))
        
        # Weighted combination
        priority = (match['similarity'] * 0.7) + (normalized_vote * 0.3)
        
        return priority
    
    matches_sorted = sorted(matches, key=calculate_priority, reverse=True)
    
    print("\n[*] Historical Matches (sorted by priority):")
    for m in matches_sorted:
        votes = storage.get_votes(m['sr_id'], 'ai')
        priority = calculate_priority(m)
        print(f"  {m['sr_id']}: Priority={priority:.2f} (Sim={m['similarity']:.0%}, Votes={votes['score']:+d})")
    
    print("\n[*] Explanation:")
    print("  Priority = (Similarity × 0.7) + (Normalized_Votes × 0.3)")
    print("  Higher priority = Appears first in LLM context = More likely to influence AI response")


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("FEEDBACK STORAGE SYSTEM - DEMO")
    print("=" * 80)
    print("\nThis demo will showcase all features of the feedback storage system.")
    print("All operations are stored in: vector store/workaround_feedback.db\n")
    
    input("Press Enter to start the demo...")
    
    # Run all demos
    demo_basic_operations()
    input("\nPress Enter to continue...")
    
    demo_multiple_srs()
    input("\nPress Enter to continue...")
    
    demo_top_workarounds()
    input("\nPress Enter to continue...")
    
    demo_bottom_workarounds()
    input("\nPress Enter to continue...")
    
    demo_statistics()
    input("\nPress Enter to continue...")
    
    demo_export()
    input("\nPress Enter to continue...")
    
    demo_priority_ranking()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Launch the UI: streamlit run sr_feedback_ui.py")
    print("2. Load an Excel file from 'llm output' folder")
    print("3. Start voting on workarounds!")
    print("4. Run the RAG pipeline again to see improved results")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

