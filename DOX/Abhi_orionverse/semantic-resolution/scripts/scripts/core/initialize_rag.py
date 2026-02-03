#!/usr/bin/env python3
"""
Utility script to initialize and manage the SR RAG system
"""

import sys
import argparse
from scripts.rag.sr_rag_engine import SRRAGEngine, initialize_rag_system

def main():
    parser = argparse.ArgumentParser(description='Initialize SR RAG System')
    parser.add_argument(
        '--force-reindex',
        action='store_true',
        help='Force regeneration of all embeddings'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test queries after initialization'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Test a specific query'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Batch size for embedding generation'
    )
    
    args = parser.parse_args()
    
    print("🚀 SR RAG System Initialization")
    print("=" * 70)
    print()
    
    # Initialize RAG system
    rag = initialize_rag_system(force_reindex=args.force_reindex)
    
    # Run tests if requested
    if args.test or args.query:
        print("\n" + "=" * 70)
        print("🧪 Running Tests")
        print("=" * 70)
        
        if args.query:
            # Test specific query
            print(f"\n🔎 Query: '{args.query}'")
            results = rag.semantic_search(args.query, top_k=5)
            
            if results:
                print(f"\n✅ Found {len(results)} similar SRs:\n")
                for i, result in enumerate(results, 1):
                    metadata = result.get('metadata', {})
                    print(f"{i}. **SR {result['sr_id']}** (Similarity: {result['similarity_score']:.2%})")
                    print(f"   Summary: {metadata.get('summary', 'N/A')[:150]}...")
                    print(f"   Application: {metadata.get('application', 'N/A')}")
                    print(f"   Area: {metadata.get('functional_area', 'N/A')}")
                    print()
            else:
                print("❌ No results found")
        
        if args.test:
            # Run predefined tests
            test_queries = [
                "provisioning issues with new connection",
                "billing errors and invoice problems",
                "scheduling conflicts in order management",
                "customer connectivity issues",
                "decomposition failures"
            ]
            
            print("\n📊 Running test queries...")
            for query in test_queries:
                print(f"\n🔎 '{query}'")
                results = rag.semantic_search(query, top_k=3)
                if results:
                    for i, result in enumerate(results, 1):
                        metadata = result.get('metadata', {})
                        print(f"   {i}. SR {result['sr_id']} ({result['similarity_score']:.1%}) - {metadata.get('summary', 'N/A')[:80]}...")
                else:
                    print("   No results")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("📊 RAG System Statistics")
    print("=" * 70)
    stats = rag.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ RAG system ready for use!")
    print("\n💡 You can now use semantic search in the chatbot interface")
    print("   Try queries like:")
    print("   - 'Find similar tickets to provisioning errors'")
    print("   - 'Show me SRs related to billing issues'")
    print("   - 'What SRs are similar to order scheduling problems?'")
    print()

if __name__ == '__main__':
    main()

