import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import List, Dict, Tuple

class CrossEncoderReranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        """Initialize cross-encoder for re-ranking"""
        print(f"Loading cross-encoder: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.model = self.model.to('cpu')
        self.model_name = model_name
        
    def rerank(self, query: str, candidates: List[Dict], top_k: int = 200) -> List[Dict]:
        """
        Re-rank candidates using cross-encoder
        """
        if not candidates:
            return []
        
        print(f"  Re-ranking {len(candidates)} candidates...")
        
        # Prepare pairs - FIXED: pairs is defined here
        pairs = []
        for c in candidates:
            cand_text = self._prepare_text(c.get('candidate', c))
            pairs.append((query[:512], cand_text[:512]))
        
        # Score in batches
        scores = []
        batch_size = 32
        
        for i in range(0, len(pairs), batch_size):
            batch = pairs[i:i+batch_size]
            batch_scores = self._score_batch(batch)
            scores.extend(batch_scores)
        
        # Combine with initial scores
        for i, c in enumerate(candidates):
            if i < len(scores):
                c['cross_encoder_score'] = scores[i]
                # Blend with initial score
                initial = c.get('initial_score', 0.5)
                c['final_rerank_score'] = 0.5 * scores[i] + 0.5 * initial
            else:
                c['cross_encoder_score'] = 0.5
                c['final_rerank_score'] = c.get('initial_score', 0.5)
        
        # Sort by final score
        candidates.sort(key=lambda x: x.get('final_rerank_score', 0), reverse=True)
        
        return candidates[:top_k]
    
    def _prepare_text(self, candidate: Dict) -> str:
        """Prepare candidate text for cross-encoder"""
        parts = []
        
        if 'profile' in candidate:
            profile = candidate.get('profile', {})
            parts.append(profile.get('headline', ''))
            parts.append(profile.get('summary', ''))
            parts.append(f"{profile.get('current_title', '')} at {profile.get('current_company', '')}")
        
        # Skills
        skills = candidate.get('skills', [])[:10]
        parts.extend([s.get('name', '') for s in skills])
        
        # Experience
        for job in candidate.get('career_history', [])[:2]:
            parts.append(job.get('description', ''))
        
        # Education
        for edu in candidate.get('education', [])[:1]:
            parts.append(f"{edu.get('degree', '')} in {edu.get('field_of_study', '')}")
        
        return ' '.join(parts)[:512]
    
    def _score_batch(self, pairs: List[Tuple[str, str]]) -> List[float]:
        """Score a batch of query-candidate pairs"""
        # Tokenize
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        )
        
        inputs = {k: v.to('cpu') for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            scores = torch.sigmoid(logits).squeeze()
            
            if scores.dim() == 0:
                scores = scores.unsqueeze(0)
            scores = scores.tolist()
            if isinstance(scores, float):
                scores = [scores]
        
        return scores