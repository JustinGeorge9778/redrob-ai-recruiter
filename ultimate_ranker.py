import json
import profile
import time
import pickle
import os
import sys
from unittest import signals
from urllib import response
import numpy as np
from typing import List, Dict, Tuple

# Check for required modules
try:
    import faiss
except ImportError:
    print("Error: faiss-cpu not installed. Run: pip install faiss-cpu")
    sys.exit(1)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: sentence-transformers not installed. Run: pip install sentence-transformers")
    sys.exit(1)

# Import custom modules
try:
    from jd_parser import AdvancedJDParser
    from enhanced_scorer import EnhancedCandidateScorer
    from cross_encoder_rerank import CrossEncoderReranker
    from ensemble_ranker import EnsembleRanker
except ImportError as e:
    print(f"Error importing custom modules: {e}")
    print("Make sure these files exist: jd_parser.py, enhanced_scorer.py, cross_encoder_rerank.py, ensemble_ranker.py")
    sys.exit(1)

class UltimateRanker:
    def __init__(self, jd_text: str, candidates_path: str = 'data/candidates.jsonl'):
        self.jd_text = jd_text
        self.candidates_path = candidates_path
        
        # Initialize components
        print("="*60)
        print("INITIALIZING ULTIMATE RANKER")
        print("="*60)
        
        print("\n[1/5] Initializing JD Parser...")
        self.jd_parser = AdvancedJDParser()
        self.jd_analysis = self.jd_parser.parse(jd_text)
        print(f"  ✅ Extracted {len(self.jd_analysis['required_skills'])} skills")
        print(f"  ✅ Detected {len(self.jd_analysis['hidden_requirements'])} hidden requirements")
        print(f"  ✅ Identified {len(self.jd_analysis['culture_signals'])} culture signals")
        
        print("\n[2/5] Initializing Scorer...")
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"  ❌ Failed to load embedding model: {e}")
            print("  Try: pip install sentence-transformers")
            sys.exit(1)
            
        self.scorer = EnhancedCandidateScorer(self.jd_parser)
        self.scorer.set_jd(jd_text)
        print("  ✅ Scorer ready")
        
        print("\n[3/5] Loading FAISS index...")
        self.index = None
        self.candidate_ids = None
        self._load_faiss_index()
        
        print("\n[4/5] Loading candidates...")
        self.candidates = []
        self.candidate_map = {}
        self._load_candidates(candidates_path)
        
        print("\n[5/5] Initializing Reranker...")
        try:
            self.reranker = CrossEncoderReranker()
        except Exception as e:
            print(f"  ⚠️  Cross-encoder initialization failed: {e}")
            print("  Continuing without cross-encoder re-ranking...")
            self.reranker = None
            
        self.ensemble = EnsembleRanker()
        print("  ✅ All components ready")
    
    def _load_faiss_index(self):
        """Load FAISS index and candidate IDs"""
        try:
            index_path = 'models/candidate_faiss.index'
            ids_path = 'models/candidate_ids.pkl'
            
            if not os.path.exists(index_path):
                print("  ⚠️  FAISS index not found.")
                print("  Build it first with: python src\\build_faiss_index.py")
                print("  Or run: python src\\embed_candidates.py")
                self.index = None
                self.candidate_ids = []
                return
            
            self.index = faiss.read_index(index_path)
            with open(ids_path, 'rb') as f:
                self.candidate_ids = pickle.load(f)
            print(f"  ✅ Loaded FAISS index with {len(self.candidate_ids)} candidates")
        except Exception as e:
            print(f"  ⚠️  Failed to load FAISS index: {e}")
            self.index = None
            self.candidate_ids = []
    
    def _load_candidates(self, candidates_path: str):
        """Load candidates from JSONL"""
        try:
            if not os.path.exists(candidates_path):
                print(f"  ❌ Candidates file not found: {candidates_path}")
                print("  Make sure the file exists in the correct location")
                sys.exit(1)
                
            with open(candidates_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        candidate = json.loads(line)
                        self.candidates.append(candidate)
                        self.candidate_map[candidate['candidate_id']] = candidate
            print(f"  ✅ Loaded {len(self.candidates)} candidates")
        except Exception as e:
            print(f"  ❌ Failed to load candidates: {e}")
            sys.exit(1)
    
    def rank(self, retrieval_k: int = 5000, top_k: int = 100) -> List[Dict]:
        """Complete ranking pipeline"""
        print("\n" + "="*60)
        print("RUNNING RANKING PIPELINE")
        print("="*60)
        
        start_time = time.time()
        
        # Check if we have everything we need
        if self.index is None:
            print("\n[Stage 1] Semantic Retrieval")
            print("  ❌ FAISS index not available")
            print("  Please build the index first:")
            print("    python src\\embed_candidates.py")
            print("    python src\\build_faiss_index.py")
            return []
        
        if not self.candidates:
            print("\n[Stage 1] Semantic Retrieval")
            print("  ❌ No candidates loaded")
            return []
        
        # Stage 1: Semantic Retrieval
        print("\n[Stage 1] Semantic Retrieval")
        retrieved = self._retrieve_top_k(self.jd_text, retrieval_k)
        print(f"  ✅ Retrieved {len(retrieved)} candidates")
        
        if not retrieved:
            print("  ❌ No candidates retrieved")
            return []
        
        # Stage 2: Initial Scoring
        print("\n[Stage 2] Initial Scoring")
        scored = self._initial_scoring(retrieved)
        print(f"  ✅ Scored {len(scored)} candidates")
        
        # Stage 3: Cross-Encoder Re-ranking (if available)
        if self.reranker:
            print("\n[Stage 3] Cross-Encoder Re-ranking")
            reranked = self.reranker.rerank(self.jd_text, scored, min(200, len(scored)))
            print(f"  ✅ Re-ranked to {len(reranked)} candidates")
        else:
            print("\n[Stage 3] Cross-Encoder Re-ranking")
            print("  ⚠️  Skipped (cross-encoder not available)")
            reranked = scored[:min(200, len(scored))]
        
        # Stage 4: Ensemble Ranking
        print("\n[Stage 4] Ensemble Ranking")

        # Initial hybrid score
        self.ensemble.add_scorer(
            lambda c: c.get('initial_score', 0.5),
            0.30,
            "Initial"
        )

        # Cross encoder relevance
        self.ensemble.add_scorer(
            lambda c: c.get(
                'cross_encoder_score',
                c.get('initial_score', 0.5)
            ),
            0.35,
            "Cross-Encoder"
        )

        # Behavioral hiring signals
        self.ensemble.add_scorer(
            lambda c: c.get(
                'behavioral_score',
                0.5
            ),
            0.10,
            "Behavioral"
        )

        # JD skill alignment
        self.ensemble.add_scorer(
            lambda c: c.get(
                'components',
                {}
            ).get(
                'skill_match',
                0.5
            ),
            0.15,
            "Skill-Match"
        )

        # Experience quality
        self.ensemble.add_scorer(
            lambda c: c.get(
                'components',
                {}
            ).get(
                'experience_quality',
                0.5
            ),
            0.10,
            "Experience"
        )

        final_ranked = self.ensemble.rank(reranked)

        print("  ✅ Generated final ranking")

        # Stage 5: Top K
        top_k_candidates = final_ranked[:top_k]
        
        elapsed = time.time() - start_time
        print(f"\n" + "="*60)
        print(f"✅ Ranking completed in {elapsed:.2f} seconds")
        print(f"📊 Top {len(top_k_candidates)} candidates selected")
        print("="*60)
        
        return top_k_candidates
    
    def _retrieve_top_k(self, query: str, k: int) -> List[Dict]:
        """Retrieve top k candidates using FAISS"""
        if self.index is None:
            return []
        
        try:
            # Encode query
            query_embedding = self.embedding_model.encode(
                [query], convert_to_numpy=True
            ).astype('float32')
            faiss.normalize_L2(query_embedding)
            
            # Search
            k = min(k, len(self.candidate_ids))
            scores, indices = self.index.search(query_embedding, k)
            
            # Build results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.candidate_ids):
                    cid = self.candidate_ids[idx]
                    candidate = self.candidate_map.get(cid)
                    if candidate:
                        results.append({
                            'candidate_id': cid,
                            'candidate': candidate,
                            'semantic_score': float(score),
                            'initial_score': float(score)
                        })
            
            return results
        except Exception as e:
            print(f"  ❌ FAISS search failed: {e}")
            return []
    
    def _initial_scoring(self, candidates: List[Dict]) -> List[Dict]:
        """Apply initial scoring"""
        for c in candidates:
            try:
                score, components = self.scorer.score_candidate(c['candidate'])
                c['initial_score'] = 0.6 * c['semantic_score'] + 0.4 * score
                c['components'] = components
                c['behavioral_score'] = components.get('behavioral', 0.5)
                c['skill_match_score'] = components.get('skill_match', 0.5)
                
                # Prepare for cross-encoder
                c['text'] = self._prepare_text(c['candidate'])
            except Exception as e:
                print(f"  ⚠️  Error scoring {c.get('candidate_id', 'unknown')}: {e}")
                c['initial_score'] = c.get('semantic_score', 0.3)
                c['components'] = {}
                c['behavioral_score'] = 0.5
                c['skill_match_score'] = 0.5
        
        return candidates
    
    def _prepare_text(self, candidate: Dict) -> str:
        """Prepare candidate text"""
        parts = []
        profile = candidate.get('profile', {})
        parts.append(profile.get('headline', ''))
        parts.append(profile.get('summary', ''))
        
        skills = candidate.get('skills', [])[:10]
        parts.extend([s.get('name', '') for s in skills])
        
        for job in candidate.get('career_history', [])[:2]:
            parts.append(job.get('description', ''))
        
        return ' '.join(parts)[:512]
    
    def generate_submission(self, ranked: List[Dict]) -> List[Dict]:
        """Generate submission format"""
        submission = []
        
        for rank, item in enumerate(ranked, 1):
            c = item['candidate']
            reasoning = self._generate_reasoning(c, item)
            
            final_score = item.get('ensemble_score', 
                                  item.get('final_rerank_score',
                                  item.get('initial_score', 0.5)))
            
            submission.append({
                'candidate_id': c['candidate_id'],
                'rank': rank,
                'score': round(float(final_score), 6),
                'reasoning': reasoning
            })
        
        return submission
    
    def _generate_reasoning(self, candidate: Dict, item: Dict) -> str:
        """Generate richer recruiter-style reasoning"""
        profile = candidate.get('profile', {})
        signals = candidate.get('redrob_signals', {})

        title = profile.get('current_title', 'Professional')
        years = profile.get('years_of_experience', 0)

        skills = candidate.get('skills', [])
        skill_names = [s.get('name', '') for s in skills]

        ai_skills = []
        priority_keywords = [
            'faiss', 'pinecone', 'qdrant', 'milvus',
            'weaviate', 'elasticsearch', 'opensearch',
            'retrieval', 'ranking', 'embedding',
            'llm', 'rag', 'lora', 'qlora',
            'recommendation', 'vector'
        ]

        for skill in skill_names:
            skill_lower = skill.lower()

            if any(k in skill_lower for k in priority_keywords):
                ai_skills.append(skill)

        ai_skills = ai_skills[:3]

        response = signals.get('recruiter_response_rate', 0)
        interview = signals.get('interview_completion_rate', 0)
        github = signals.get('github_activity_score', -1)

        reasoning_parts = []

        # Intro
        reasoning_parts.append(
            f"{title} with {years:.1f} years of experience"
        )

        # Skills
        if ai_skills:
            reasoning_parts.append(
                f"demonstrates expertise in {', '.join(ai_skills)}"
            )

        # JD Alignment
        if 'components' in item:

            skill_match = item['components'].get(
                'skill_match', 0
            )

            experience_quality = item['components'].get(
                'experience_quality', 0
            )

            if skill_match >= 0.65:
                reasoning_parts.append(
                    "strong alignment with the job's retrieval, ranking and AI requirements"
                )
        
            elif skill_match >= 0.45:
                reasoning_parts.append(
                    "good alignment with the core technical requirements"
                )

            if experience_quality >= 0.70:
                reasoning_parts.append(
                    "backed by high-quality product-focused experience"
            )

        # Recruiter signals
        if response >= 0.75:
            reasoning_parts.append(
                f"excellent recruiter response rate ({response:.0%})"
            )
        elif response >= 0.50:
            reasoning_parts.append(
                f"healthy recruiter response rate ({response:.0%})"
            )

        if interview >= 0.85:
            reasoning_parts.append(
                f"very strong interview completion rate ({interview:.0%})"
            )
        elif interview >= 0.60:
            reasoning_parts.append(
                f"good interview completion rate ({interview:.0%})"
            )

        # OSS signal
        if github > 30:
            reasoning_parts.append(
                "shows evidence of active technical engagement through GitHub activity"
            )

        # Availability
        if signals.get('open_to_work_flag', False):
            reasoning_parts.append(
                "currently open to new opportunities"
            )

        reasoning = ". ".join(reasoning_parts)

        if not reasoning.endswith("."):
            reasoning += "."

        return reasoning[:300]
