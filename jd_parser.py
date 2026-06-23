import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field

@dataclass
class SkillRequirement:
    name: str
    importance: float
    synonyms: List[str] = field(default_factory=list)
    years_required: float = 0.0
    context: str = ""

class AdvancedJDParser:
    def __init__(self):
        self.skill_patterns = {
            'embeddings': {
                'synonyms': ['embedding', 'sentence-transformers', 'bge', 'e5', 'text-embedding'],
                'category': 'core_ml'
            },
            'retrieval': {
                'synonyms': ['retrieval', 'information retrieval', 'hybrid search', 'semantic search'],
                'category': 'core_ml'
            },
            'ranking': {
                'synonyms': ['ranking', 'learning to rank', 'ltr', 'ndcg', 'mrr', 'map', 'relevance'],
                'category': 'core_ml'
            },
            'vector_db': {
                'synonyms': ['faiss', 'pinecone', 'weaviate', 'qdrant', 'milvus', 'opensearch', 'elasticsearch'],
                'category': 'infrastructure'
            },
            'llm': {
                'synonyms': ['llm', 'large language model', 'rag', 'fine-tuning', 'lora', 'qlora', 'peft'],
                'category': 'advanced_ml'
            },
            'python': {
                'synonyms': ['python', 'pytorch', 'tensorflow', 'keras', 'numpy', 'pandas'],
                'category': 'programming'
            },
            'production': {
                'synonyms': ['production', 'deployed', 'scale', 'latency', 'serving', 'real users'],
                'category': 'experience'
            },
            'evaluation': {
                'synonyms': ['evaluation', 'offline', 'online', 'a/b test', 'experiment', 'metrics'],
                'category': 'experience'
            },
            'mlops': {
                'synonyms': ['mlops', 'model serving', 'experiment tracking', 'mlflow', 'kubeflow'],
                'category': 'infrastructure'
            }
        }
        
        self.hidden_patterns = {
            'product_company': ['product company', 'product team', 'startup', 'series a'],
            'production_experience': ['production', 'real users', 'scale', 'millions'],
            'async_work': ['async', 'remote-first', 'distributed team', 'write a lot'],
            'fast_paced': ['fast-paced', 'move fast', 'agile', 'quickly'],
            'ownership': ['ownership', 'autonomous', 'self-starter', 'independent'],
            'collaboration': ['cross-functional', 'collaborate', 'team', 'stakeholder'],
        }
        
        self.importance_signals = {
            'critical': 1.0,
            'required': 0.9,
            'must have': 0.9,
            'essential': 0.9,
            'strongly preferred': 0.75,
            'highly desired': 0.75,
            'preferred': 0.6,
            'desired': 0.6,
            'ideally': 0.55,
            'nice to have': 0.3,
            'bonus': 0.25,
            'plus': 0.25
        }

    def parse(self, jd_text: str) -> Dict:
        """Parse job description with advanced NLP"""
        jd_lower = jd_text.lower()
        
        result = {
            'raw_text': jd_text,
            'required_skills': {},
            'preferred_skills': {},
            'hidden_requirements': {},
            'seniority_level': self._detect_seniority(jd_lower),
            'experience_range': self._extract_experience_range(jd_lower),
            'locations': self._extract_locations(jd_lower),
            'culture_signals': self._extract_culture(jd_lower),
            'disqualifiers': self._extract_disqualifiers(jd_lower),
            'company_stage': self._detect_company_stage(jd_lower),
            'role_archetype': self._detect_archetype(jd_lower),
        }
        
        # Extract skills with importance
        for skill, info in self.skill_patterns.items():
            importance = self._get_skill_importance(jd_lower, skill, info['synonyms'])
            if importance > 0.3:
                result['required_skills'][skill] = {
                    'importance': importance,
                    'synonyms': info['synonyms'],
                    'category': info['category'],
                    'matched': [s for s in info['synonyms'] if s in jd_lower]
                }
        
        # Extract hidden requirements
        for req, patterns in self.hidden_patterns.items():
            detected = [p for p in patterns if p in jd_lower]
            if detected:
                result['hidden_requirements'][req] = {
                    'detected': True,
                    'patterns': detected,
                    'strength': len(detected) / len(patterns)
                }
        
        return result

    def _detect_seniority(self, text: str) -> str:
        levels = {
            'junior': ['junior', 'entry', '0-2', '1-3'],
            'mid': ['mid', '3-5', '3+', '4+', 'software engineer'],
            'senior': ['senior', '5-9', '5+', '7+', 'lead', 'sr.'],
            'staff': ['staff', 'principal', '10+', 'architect'],
        }
        for level, patterns in levels.items():
            if any(p in text for p in patterns):
                return level
        return 'mid'

    def _extract_experience_range(self, text: str) -> Tuple[float, float]:
        patterns = [
            (r'(\d+)-(\d+)\s*years?', 'range'),
            (r'(\d+)\+\s*years?', 'min'),
            (r'(\d+)\s*years?\s*experience', 'min'),
        ]
        for pattern, ptype in patterns:
            matches = re.findall(pattern, text)
            if matches:
                if ptype == 'range':
                    return float(matches[0][0]), float(matches[0][1])
                elif ptype == 'min':
                    val = float(matches[0]) if isinstance(matches[0], str) else float(matches[0][0])
                    return val, val + 3
        return 5.0, 9.0

    def _get_skill_importance(self, text: str, skill: str, synonyms: List[str]) -> float:
        base_importance = 0.5
        skill_lower = skill.lower()
        
        # Check for explicit mentions
        for syn in [skill_lower] + [s.lower() for s in synonyms]:
            if syn in text:
                idx = text.find(syn)
                context = text[max(0, idx-120):min(len(text), idx+120)]
                
                for signal, weight in self.importance_signals.items():
                    if signal in context:
                        return weight
                
                # Check if in list/bullet
                if '\n' in context[:30]:
                    return 0.85
        
        return base_importance

    def _extract_locations(self, text: str) -> List[str]:
        locations = []
        loc_patterns = ['Pune', 'Noida', 'Hyderabad', 'Mumbai', 'Delhi', 
                        'Bangalore', 'Chennai', 'Gurgaon', 'NCR']
        for loc in loc_patterns:
            if loc.lower() in text:
                locations.append(loc)
        
        # Check for country preferences
        if 'india' in text:
            locations.append('India')
        if 'remote' in text:
            locations.append('Remote')
        
        return locations

    def _extract_culture(self, text: str) -> Dict[str, float]:
        culture_signals = {
            'fast_paced': ['fast-paced', 'move fast', 'agile', 'dynamic', 'quickly'],
            'impact_driven': ['impact', 'drive', 'outcome', 'results', 'mission'],
            'innovation': ['innovative', 'cutting-edge', 'state-of-the-art', 'novel'],
            'collaborative': ['collaborate', 'team', 'cross-functional', 'together'],
            'ownership': ['ownership', 'autonomous', 'self-starter', 'independent'],
            'data_driven': ['data-driven', 'metrics', 'experiment', 'a/b test'],
            'growth_mindset': ['learn', 'grow', 'development', 'curious'],
        }
        
        result = {}
        for key, patterns in culture_signals.items():
            matches = sum(1 for p in patterns if p in text)
            result[key] = min(matches / len(patterns) * 2, 1.0)
        
        return {k: v for k, v in result.items() if v > 0.3}

    def _extract_disqualifiers(self, text: str) -> List[str]:
        disqualifiers = []
        
        if any(x in text for x in ['consulting', 'services', 'tcs', 'infosys', 'wipro']):
            disqualifiers.append('consulting_background')
        
        if 'research-only' in text or 'academic' in text:
            disqualifiers.append('research_only')
        
        if 'title-chaser' in text or 'title chasing' in text:
            disqualifiers.append('title_chaser')
        
        if 'framework enthusiast' in text:
            disqualifiers.append('framework_enthusiast')
        
        return disqualifiers

    def _detect_company_stage(self, text: str) -> str:
        if any(x in text for x in ['series a', 'series b', 'seed', 'early-stage']):
            return 'early_startup'
        if any(x in text for x in ['series c', 'series d', 'growth stage']):
            return 'growth_startup'
        if any(x in text for x in ['fortune 500', 'enterprise', 'global']):
            return 'enterprise'
        return 'growth_startup'

    def _detect_archetype(self, text: str) -> str:
        archetypes = {
            'ml_engineer': ['machine learning', 'model', 'training', 'inference', 'ml pipeline'],
            'data_scientist': ['data science', 'statistical', 'experiment', 'analysis'],
            'backend_engineer': ['backend', 'api', 'server', 'database', 'microservice'],
            'data_engineer': ['data engineering', 'pipeline', 'etl', 'data warehouse'],
            'devops_sre': ['devops', 'sre', 'infrastructure', 'reliability'],
            'research_engineer': ['research', 'novel', 'phd', 'publication'],
            'full_stack': ['full stack', 'frontend', 'backend'],
        }
        
        scores = {}
        for arch, patterns in archetypes.items():
            scores[arch] = sum(1 for p in patterns if p in text)
        
        if not scores:
            return 'ml_engineer'
        
        return max(scores, key=scores.get)