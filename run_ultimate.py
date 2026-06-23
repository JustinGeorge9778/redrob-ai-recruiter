#!/usr/bin/env python3
import json
import sys
import os
import argparse
import pandas as pd

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ultimate_ranker import UltimateRanker
except ImportError as e:
    print(f"Error importing UltimateRanker: {e}")
    print("Make sure all required files exist in the current directory")
    print("Required files: ultimate_ranker.py, jd_parser.py, enhanced_scorer.py, cross_encoder_rerank.py, ensemble_ranker.py")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Ultimate Candidate Ranker')
    parser.add_argument('--candidates', default='data/candidates.jsonl',
                       help='Path to candidates.jsonl')
    parser.add_argument('--jd', required=True,
                       help='Path to job description text file')
    parser.add_argument('--output', default='outputs/ultimate_submission.csv',
                       help='Output CSV path')
    parser.add_argument('--retrieve-k', type=int, default=5000,
                       help='Number to retrieve semantically')
    parser.add_argument('--top-k', type=int, default=100,
                       help='Number in final ranking')
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("ULTIMATE RANKING SYSTEM")
    print("="*60)
    
    # Check if candidates file exists
    if not os.path.exists(args.candidates):
        print(f"❌ Candidates file not found: {args.candidates}")
        print("Please make sure you have the candidates.jsonl file in the data folder")
        sys.exit(1)
    
    # Read job description
    print("\n[1] Reading job description...")
    try:
        if not os.path.exists(args.jd):
            print(f"❌ Job description file not found: {args.jd}")
            print("Please create a job_description.txt file in the current directory")
            sys.exit(1)
        
        with open(args.jd, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        print(f"  ✅ JD length: {len(jd_text)} characters")
    except Exception as e:
        print(f"  ❌ Failed to read JD: {e}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  ✅ Created output directory: {output_dir}")
    
    # Rank candidates
    print("\n[2] Running ranking pipeline...")
    try:
        ranker = UltimateRanker(jd_text, args.candidates)
        top_results = ranker.rank(retrieval_k=args.retrieve_k, top_k=args.top_k)
    except Exception as e:
        print(f"  ❌ Ranking failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate submission
    print("\n[3] Generating submission...")
    try:
        submission = ranker.generate_submission(top_results)
    except Exception as e:
        print(f"  ❌ Submission generation failed: {e}")
        sys.exit(1)
    
    # Save as CSV
    print("\n[4] Saving results...")
    try:
        df = pd.DataFrame(submission)
        df.to_csv(args.output, index=False)
        print(f"  ✅ Saved {len(submission)} candidates to {args.output}")
    except Exception as e:
        print(f"  ❌ Failed to save: {e}")
        sys.exit(1)
    
    # Print top 10
    print("\n" + "="*60)
    print("TOP 10 CANDIDATES")
    print("="*60)
    for i, row in enumerate(submission[:10], 1):
        print(f"{i:2}. {row['candidate_id']} score={row['score']:.4f}")
        reasoning_preview = row['reasoning'][:100] + "..." if len(row['reasoning']) > 100 else row['reasoning']
        print(f"    {reasoning_preview}")
    
    print("\n" + "="*60)
    print("✅ Ranking complete!")
    print(f"📁 Output: {args.output}")
    print("="*60)

if __name__ == '__main__':
    main()