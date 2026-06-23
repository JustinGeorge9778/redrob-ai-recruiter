import numpy as np
from typing import List, Dict, Callable

class EnsembleRanker:
    def __init__(self):
        self.scorers = []
        self.weights = []
        self.names = []
    
    def add_scorer(self, scorer: Callable, weight: float, name: str = ""):
        """Add a scoring function with weight"""
        self.scorers.append(scorer)
        self.weights.append(weight)
        self.names.append(name or f"Scorer_{len(self.scorers)}")
        
    def rank(self, candidates: List[Dict]) -> List[Dict]:
        """Rank candidates using ensemble"""
        if not candidates:
            return []
        
        # Get scores from each model
        all_scores = []
        for i, scorer in enumerate(self.scorers):
            try:
                scores = [scorer(c) for c in candidates]
                all_scores.append(scores)
            except Exception as e:
                print(f"Warning: Scorer {self.names[i]} failed: {e}")
                all_scores.append([0.5] * len(candidates))
        
        # Normalize scores
        all_scores = self._normalize_scores(all_scores)
        
        # Weighted combination
        final_scores = np.zeros(len(candidates))
        for i, scores in enumerate(all_scores):
            final_scores += self.weights[i] * np.array(scores)
        
        # Normalize final scores
        if len(final_scores) > 0:
            min_score = np.min(final_scores)
            max_score = np.max(final_scores)
            if max_score > min_score:
                final_scores = (final_scores - min_score) / (max_score - min_score)
        
        # Add to candidates
        for i, candidate in enumerate(candidates):
            candidate['ensemble_score'] = float(final_scores[i])
        
        # Sort
        candidates.sort(key=lambda x: x.get('ensemble_score', 0), reverse=True)
        
        return candidates
    
    def _normalize_scores(self, all_scores: List[List[float]]) -> List[List[float]]:
        """Normalize scores to 0-1 range"""
        normalized = []
        for scores in all_scores:
            if not scores:
                normalized.append([])
                continue
            
            min_score = min(scores)
            max_score = max(scores)
            
            if max_score == min_score:
                normalized.append([0.5] * len(scores))
            else:
                normalized.append([(s - min_score) / (max_score - min_score) 
                                  for s in scores])
        
        return normalized