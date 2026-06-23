#!/usr/bin/env python3

import sys
import os
import re
import pandas as pd
from typing import Tuple, List

def validate_submission(csv_path: str) -> Tuple[bool, List[str]]:
    """Validate submission format"""
    errors = []
    warnings = []
    
    try:
        if not os.path.exists(csv_path):
            return False, [f"File not found: {csv_path}"]
        
        df = pd.read_csv(csv_path)
    except Exception as e:
        return False, [f"Could not read CSV: {e}"]
    
    # Check columns
    required = ['candidate_id', 'rank', 'score', 'reasoning']
    missing = set(required) - set(df.columns)
    if missing:
        errors.append(f"Missing columns: {missing}")
    
    # Check number of rows
    if len(df) != 100:
        errors.append(f"Expected exactly 100 rows, got {len(df)}")
    
    # Check candidate IDs
    pattern = re.compile(r'^CAND_[0-9]{7}$')
    invalid = df[~df['candidate_id'].astype(str).str.match(pattern)]
    if not invalid.empty:
        errors.append(f"Invalid candidate IDs: {invalid['candidate_id'].tolist()}")
    
    # Check duplicates
    if df['candidate_id'].duplicated().any():
        errors.append("Duplicate candidate IDs found")
    
    # Check ranks
    if df['rank'].duplicated().any():
        errors.append("Duplicate ranks found")
    
    if not all(df['rank'].between(1, 100)):
        errors.append("Ranks must be between 1 and 100")
    
    # Check ranks 1-100
    missing_ranks = set(range(1, 101)) - set(df['rank'])
    if missing_ranks:
        errors.append(f"Missing ranks: {sorted(missing_ranks)}")
    
    # Check score non-increasing
    scores = df['score'].tolist()
    for i in range(len(scores)-1):
        if scores[i] < scores[i+1]:
            errors.append(f"Score decreased at rank {i+1}")
            break
    
    # Check score range
    if df['score'].min() < 0 or df['score'].max() > 1:
        errors.append("Scores should be between 0 and 1")
    
    # Check reasoning
    empty = df[df['reasoning'].isna() | (df['reasoning'].astype(str).str.strip() == '')]
    if not empty.empty:
        errors.append(f"Empty reasoning for {len(empty)} candidates")
    
    # Print warnings
    if warnings:
        print("\n⚠️ Warnings:")
        for w in warnings:
            print(f"  - {w}")
    
    return len(errors) == 0, errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py submission.csv")
        print("       python validate_submission.py outputs\\ultimate_submission.csv")
        sys.exit(1)
    
    is_valid, errors = validate_submission(sys.argv[1])
    
    print("\n" + "="*60)
    print("VALIDATION RESULTS")
    print("="*60)
    
    if is_valid:
        print("✅ Submission is valid!")
        sys.exit(0)
    else:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)