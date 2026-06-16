#!/usr/bin/env python3
"""
NEXUS AI RECRUITER - Professional Intelligence Platform
"""

import json
import time
import re
import http.server
import socketserver
import threading
import webbrowser
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class JobRequirement:
    category: str
    skill: str
    importance: float
    semantic_variants: List[str] = field(default_factory=list)
    years_required: Optional[float] = None
    context: str = ""


@dataclass
class CareerSignal:
    signal_type: str
    value: float
    evidence: str
    recency_weight: float


@dataclass
class CandidateScore:
    candidate_id: str
    total_score: float
    rank: int
    technical_score: float
    semantic_fit_score: float
    experience_score: float
    behavioral_score: float
    culture_score: float
    growth_trajectory_score: float
    score_breakdown: Dict[str, Any]
    strengths: List[str]
    gaps: List[str]
    hire_recommendation: str
    recommendation_class: str
    confidence: float
    interview_focus_areas: List[str]


# ============================================================
# SEMANTIC ENGINE
# ============================================================

class SemanticKnowledgeEngine:
    def __init__(self):
        self.skill_taxonomy = self._build_skill_taxonomy()
        self.semantic_clusters = self._build_semantic_clusters()

    def _build_skill_taxonomy(self):
        return {
            "python": {
                "family": "programming",
                "related": ["django", "flask", "fastapi", "pandas", "numpy", "scikit-learn", "pytorch", "tensorflow", "pyspark"],
                "transfers_from": ["ruby", "javascript", "java"],
                "synonyms": ["python3", "python programming"]
            },
            "machine learning": {
                "family": "ai_ml",
                "related": ["deep learning", "neural networks", "nlp", "computer vision", "reinforcement learning", "feature engineering", "model deployment"],
                "transfers_from": ["statistics", "data analysis", "research"],
                "synonyms": ["ml", "ai", "artificial intelligence", "predictive modeling"]
            },
            "kubernetes": {
                "family": "devops",
                "related": ["docker", "helm", "istio", "k8s", "container orchestration", "microservices", "cloud native"],
                "transfers_from": ["docker", "linux administration"],
                "synonyms": ["k8s", "container orchestration"]
            },
            "react": {
                "family": "frontend",
                "related": ["javascript", "typescript", "redux", "next.js", "graphql", "html", "css", "webpack"],
                "transfers_from": ["vue", "angular", "svelte"],
                "synonyms": ["react.js", "reactjs"]
            },
            "leadership": {
                "family": "soft_skills",
                "related": ["team management", "mentoring", "stakeholder management", "strategic thinking", "decision making"],
                "transfers_from": [],
                "synonyms": ["people management", "team lead"]
            },
            "distributed systems": {
                "family": "systems",
                "related": ["kafka", "rabbitmq", "microservices", "event driven", "scalability", "high availability", "fault tolerance"],
                "transfers_from": ["backend engineering", "systems programming"],
                "synonyms": ["distributed computing", "large scale systems"]
            },
            "data engineering": {
                "family": "data",
                "related": ["etl", "data pipeline", "spark", "airflow", "dbt", "data warehouse", "data lake", "streaming"],
                "transfers_from": ["software engineering", "data analysis"],
                "synonyms": ["data pipelines", "etl engineering"]
            },
            "mlops": {
                "family": "ai_ml",
                "related": ["model serving", "experiment tracking", "mlflow", "kubeflow", "model monitoring", "feature store", "ci/cd for ml"],
                "transfers_from": ["devops", "data engineering"],
                "synonyms": ["ml operations", "ml infrastructure", "ml platform"]
            },
            "nlp": {
                "family": "ai_ml",
                "related": ["transformers", "bert", "gpt", "llm", "text classification", "named entity recognition", "sentiment analysis", "language models"],
                "transfers_from": ["machine learning", "linguistics"],
                "synonyms": ["natural language processing", "text mining"]
            },
            "spark": {
                "family": "data",
                "related": ["pyspark", "scala", "hadoop", "data pipeline", "big data", "databricks", "distributed computing"],
                "transfers_from": ["data engineering", "python"],
                "synonyms": ["apache spark", "pyspark"]
            }
        }

    def _build_semantic_clusters(self):
        return {
            "cloud_expertise": {
                "terms": ["aws", "gcp", "azure", "cloud", "serverless", "lambda", "ec2", "s3", "cloud functions", "bigquery", "redshift"],
                "weight": 0.85
            },
            "scale_experience": {
                "terms": ["millions of users", "high traffic", "distributed", "scalable", "performance optimization", "load balancing", "caching", "petabyte"],
                "weight": 0.9
            },
            "product_impact": {
                "terms": ["launched", "shipped", "deployed", "production", "users", "revenue impact", "reduced latency", "improved", "built"],
                "weight": 0.8
            },
            "leadership_signals": {
                "terms": ["led", "managed", "mentored", "architected", "designed", "founded", "established", "grew team", "hired", "principal"],
                "weight": 0.75
            },
            "innovation_signals": {
                "terms": ["patent", "open source", "conference", "published", "speaker", "contributed", "created", "invented", "novel", "first"],
                "weight": 0.7
            }
        }

    def compute_semantic_similarity(self, text1: str, text2: str) -> float:
        t1, t2 = text1.lower(), text2.lower()
        score = 0.0
        w1 = set(re.findall(r'\b\w+\b', t1))
        w2 = set(re.findall(r'\b\w+\b', t2))
        if w1 and w2:
            score += len(w1 & w2) / len(w1 | w2) * 0.3
        cs, cm = 0.0, 0
        for cd in self.semantic_clusters.values():
            if any(t in t1 for t in cd["terms"]) and any(t in t2 for t in cd["terms"]):
                cs += cd["weight"]; cm += 1
        if cm:
            score += min(cs / cm * 0.4, 0.4)
        ts = sum(0.1 for s, d in self.skill_taxonomy.items()
                 if any(t in t1 for t in [s] + d.get("synonyms", []) + d.get("related", []))
                 and any(t in t2 for t in [s] + d.get("synonyms", []) + d.get("related", [])))
        score += min(ts, 0.3)
        return min(score, 1.0)

    def expand_skill_semantically(self, skill: str) -> List[str]:
        variants = [skill]
        for ts, d in self.skill_taxonomy.items():
            if ts in skill.lower() or skill.lower() in ts:
                variants.extend(d.get("synonyms", []))
                variants.extend(d.get("related", []))
                variants.extend(d.get("transfers_from", []))
        return list(set(variants))

    def infer_skill_from_context(self, text: str, skill: str) -> float:
        score = 0.0
        tl = text.lower()
        for ts, d in self.skill_taxonomy.items():
            if ts == skill.lower():
                rf = [r for r in d.get("related", []) if r in tl]
                if rf:
                    score += 0.6 * (len(rf) / max(len(d.get("related", [])), 1))
                tf = [t for t in d.get("transfers_from", []) if t in tl]
                if tf:
                    score += 0.3
        return min(score, 0.85)


# ============================================================
# JOB ANALYZER
# ============================================================

class JobDescriptionAnalyzer:
    def __init__(self, se: SemanticKnowledgeEngine):
        self.semantic = se
        self.importance_signals = {
            "critical": 1.0, "required": 0.9, "must have": 0.9, "essential": 0.9,
            "strongly preferred": 0.75, "highly desired": 0.75,
            "preferred": 0.6, "desired": 0.6, "ideally": 0.55,
            "nice to have": 0.3, "bonus": 0.25, "plus": 0.25
        }

    def analyze(self, jd: str, title: str = "") -> Dict:
        analysis = {
            "title": title, "raw_jd": jd,
            "requirements": self._extract_requirements(jd),
            "culture_signals": self._extract_culture(jd),
            "role_archetype": self._detect_archetype(jd, title),
            "seniority_level": self._detect_seniority(jd, title),
            "hidden_requirements": self._detect_hidden(jd),
            "company_stage": self._detect_stage(jd),
            "impact_scope": self._detect_scope(jd),
        }
        analysis["weighted_requirements"] = self._assign_weights(
            analysis["requirements"], analysis["seniority_level"], analysis["role_archetype"]
        )
        return analysis

    def _extract_requirements(self, jd: str) -> List[JobRequirement]:
        reqs = []
        jl = jd.lower()
        patterns = {
            "python": "technical", "machine learning": "technical", "deep learning": "technical",
            "tensorflow": "technical", "pytorch": "technical", "kubernetes": "technical",
            "docker": "technical", "sql": "technical", "spark": "technical", "kafka": "technical",
            "aws": "technical", "react": "technical", "javascript": "technical", "java": "technical",
            "data pipeline": "technical", "mlops": "technical", "microservices": "technical",
            "distributed systems": "technical", "nlp": "technical", "transformers": "technical",
            "llm": "technical", "leadership": "soft", "communication": "soft",
            "collaboration": "soft", "mentoring": "soft", "cross-functional": "soft",
            "stakeholder": "soft", "ownership": "soft",
        }
        for skill, cat in patterns.items():
            if skill in jl:
                imp = self._get_importance(jl, skill)
                yrs = self._get_years(jl, skill)
                reqs.append(JobRequirement(
                    category=cat, skill=skill, importance=imp,
                    semantic_variants=self.semantic.expand_skill_semantically(skill),
                    years_required=yrs, context=self._get_context(jl, skill)
                ))
        reqs.sort(key=lambda x: x.importance, reverse=True)
        return reqs

    def _get_importance(self, jl: str, skill: str) -> float:
        idx = jl.find(skill)
        if idx == -1: return 0.7
        ctx = jl[max(0, idx-100):idx+100]
        for sig, w in self.importance_signals.items():
            if sig in ctx: return w
        if any(s in ctx for s in ["requirement", "qualification", "must", "need"]): return 0.85
        if any(s in ctx for s in ["prefer", "bonus", "nice", "plus"]): return 0.4
        return 0.7

    def _get_years(self, jl: str, skill: str) -> Optional[float]:
        idx = jl.find(skill)
        if idx == -1: return None
        ctx = jl[max(0, idx-60):idx+60]
        for p in [r'(\d+)\+\s*years?', r'(\d+)\s*-\s*(\d+)\s*years?', r'(\d+)\s*years?\s+of\s+experience']:
            m = re.search(p, ctx)
            if m: return float(m.group(1))
        return None

    def _get_context(self, jl: str, skill: str) -> str:
        idx = jl.find(skill)
        if idx == -1: return ""
        s = max(0, jl.rfind('.', 0, idx) + 1)
        e = jl.find('.', idx)
        return jl[s:e if e != -1 else idx+100].strip()

    def _extract_culture(self, jd: str) -> Dict[str, float]:
        jl = jd.lower()
        patterns = {
            "fast_paced": ["fast-paced", "startup", "move fast", "agile", "dynamic"],
            "impact_driven": ["impact", "make a difference", "mission", "purpose"],
            "innovation_focused": ["innovative", "cutting-edge", "state-of-the-art", "novel"],
            "collaborative": ["team player", "collaborative", "cross-functional", "together"],
            "autonomous": ["self-starter", "independent", "ownership", "autonomous"],
            "data_driven": ["data-driven", "metrics", "a/b test", "experimentation"],
            "growth_mindset": ["learn", "grow", "development", "curious"],
        }
        return {k: min(sum(1 for s in v if s in jl) / len(v) * 2, 1.0)
                for k, v in patterns.items() if any(s in jl for s in v)}

    def _detect_archetype(self, jd: str, title: str) -> str:
        c = (jd + " " + title).lower()
        archetypes = {
            "ml_engineer": ["machine learning", "model", "training", "inference", "ml pipeline"],
            "data_scientist": ["data science", "statistical", "experiment", "analysis"],
            "backend_engineer": ["backend", "api", "server", "database", "microservice"],
            "frontend_engineer": ["frontend", "ui", "ux", "react", "user interface"],
            "devops_sre": ["devops", "sre", "infrastructure", "reliability", "deployment"],
            "engineering_manager": ["engineering manager", "people manager", "team lead"],
            "data_engineer": ["data engineering", "pipeline", "etl", "data warehouse"],
            "research_engineer": ["research", "paper", "publication", "novel", "phd"],
        }
        scores = {a: sum(1 for s in sigs if s in c) for a, sigs in archetypes.items()}
        return max(scores, key=scores.get)

    def _detect_seniority(self, jd: str, title: str) -> str:
        c = (jd + " " + title).lower()
        levels = {
            "principal": ["principal", "distinguished", "fellow", "architect"],
            "senior": ["senior", "sr.", "lead", "staff", "7+ years", "5+ years"],
            "mid": ["mid-level", "3+ years", "2-4 years", "intermediate"],
            "junior": ["junior", "entry level", "0-2 years", "new grad"],
        }
        for level, sigs in levels.items():
            if any(s in c for s in sigs): return level
        return "mid"

    def _detect_hidden(self, jd: str) -> List[str]:
        jl = jd.lower()
        hidden = []
        checks = {
            "production_experience": ["scale", "production", "reliability"],
            "startup_adaptability": ["fast-paced", "startup", "wear many hats"],
            "communication_skills": ["cross-functional", "stakeholder", "present"],
            "system_design_ability": ["architect", "design system", "large scale"],
            "research_aptitude": ["state-of-the-art", "novel", "research"],
        }
        for req, sigs in checks.items():
            if any(s in jl for s in sigs): hidden.append(req)
        return hidden

    def _detect_stage(self, jd: str) -> str:
        jl = jd.lower()
        if any(x in jl for x in ["series a", "series b", "seed"]): return "early_startup"
        if any(x in jl for x in ["series c", "series d", "growth stage"]): return "growth_startup"
        if any(x in jl for x in ["fortune 500", "enterprise", "global"]): return "enterprise"
        return "growth_startup"

    def _detect_scope(self, jd: str) -> str:
        jl = jd.lower()
        if any(x in jl for x in ["company-wide", "org-wide"]): return "organizational"
        if any(x in jl for x in ["individual contributor", "ic"]): return "individual"
        return "team"

    def _assign_weights(self, reqs, seniority, archetype):
        adjustments = {
            "principal": {"leadership": 1.3, "soft": 1.2, "technical": 0.95},
            "senior": {"leadership": 1.1, "technical": 1.0, "soft": 1.0},
            "mid": {"technical": 1.1, "soft": 0.9, "leadership": 0.8},
            "junior": {"technical": 0.9, "soft": 0.8},
        }.get(seniority, {})
        for req in reqs:
            req.importance = min(req.importance * adjustments.get(req.category, 1.0), 1.0)
        return reqs


# ============================================================
# CANDIDATE PROFILE BUILDER
# ============================================================

class CandidateProfileBuilder:
    def __init__(self, se: SemanticKnowledgeEngine):
        self.semantic = se

    def build_profile(self, raw: Dict) -> Dict:
        return {
            **raw,
            "skill_map": self._build_skill_map(raw),
            "career_trajectory": self._analyze_trajectory(raw),
            "impact_signals": self._extract_impact(raw),
            "behavioral_signals": self._extract_behavioral(raw),
            "seniority_reality": self._assess_seniority(raw),
            "candidate_narrative": self._build_narrative(raw),
            "red_flags": self._detect_red_flags(raw),
            "star_qualities": self._detect_star_qualities(raw),
        }

    def _build_skill_map(self, c: Dict) -> Dict[str, float]:
        sm = {}
        for s in c.get("skills", []):
            if isinstance(s, dict): sm[s["name"].lower()] = s.get("level", 0.7)
            else: sm[s.lower()] = 0.7
        ft = self._get_text(c)
        for sn, d in self.semantic.skill_taxonomy.items():
            if sn not in sm:
                rf = [r for r in d.get("related", []) if r in ft.lower()]
                if len(rf) >= 2: sm[sn] = 0.65
                elif len(rf) == 1: sm[sn] = 0.4
        return sm

    def _analyze_trajectory(self, c: Dict) -> Dict:
        exps = c.get("experience", [])
        if not exps: return {"pattern": "unknown", "velocity": 0, "consistency": 0}
        tenures = [e.get("years", 0) for e in exps]
        titles = [e.get("title", "").lower() for e in exps]
        ladder = {"intern": 0, "junior": 1, "engineer": 2, "senior": 3,
                  "staff": 4, "principal": 5, "lead": 4, "manager": 4, "director": 5, "vp": 6}
        scores = [next((v for k, v in ladder.items() if k in t), 2) for t in titles]
        velocity = 0.0
        if len(scores) >= 2:
            gc = sum(1 for i in range(1, len(scores)) if scores[i] > scores[i-1])
            velocity = gc / max(len(scores)-1, 1)
        pattern = "fast_riser" if velocity > 0.6 else "steady_growth" if velocity > 0.3 else "specialist"
        all_desc = " ".join([e.get("description", "") for e in exps]).lower()
        growth_signals = [kw for kw in ["promoted", "promotion", "expanded scope", "led initiative"] if kw in all_desc]
        return {
            "total_years": c.get("total_years_experience", 0),
            "company_count": len(exps),
            "avg_tenure": sum(tenures)/len(tenures) if tenures else 0,
            "velocity": velocity,
            "consistency": 1.0 - len([t for t in tenures if t < 1])/max(len(tenures), 1),
            "growth_signals": growth_signals,
            "pattern": pattern
        }

    def _extract_impact(self, c: Dict) -> List[Dict]:
        impacts = []
        ft = self._get_text(c)
        for pat, typ in [
            (r'(\d+)%\s*(improvement|increase|reduction|decrease|faster)', "percentage_impact"),
            (r'(\$[\d,]+[kmb]?)\s*(revenue|savings|cost)', "financial_impact"),
            (r'(\d+[kmb]?)\s*(users|customers|requests|transactions)', "scale_impact"),
            (r'(\d+)x\s*(improvement|faster|performance|growth)', "multiplier_impact"),
        ]:
            for m in re.findall(pat, ft.lower()):
                impacts.append({"type": typ, "evidence": m[0] if isinstance(m, tuple) else m, "weight": 0.9})
        for typ, kws in {
            "launched_product": ["launched", "shipped", "released to production"],
            "led_major_project": ["led the development", "architected", "spearheaded"],
            "team_impact": ["mentored", "grew the team", "hired", "trained"],
        }.items():
            for kw in kws:
                if kw in ft.lower():
                    impacts.append({"type": typ, "evidence": kw, "weight": 0.7}); break
        return impacts

    def _extract_behavioral(self, c: Dict) -> Dict[str, CareerSignal]:
        sigs = {}
        act = c.get("platform_activity", {})
        if act.get("response_rate", 0) > 0.8:
            sigs["high_engagement"] = CareerSignal("engagement", act["response_rate"],
                f"Responds to {act['response_rate']*100:.0f}% of outreach", 1.0)
        if act.get("profile_completeness", 0) > 0.85:
            sigs["profile_investment"] = CareerSignal("professionalism", act["profile_completeness"],
                "Highly complete profile", 0.8)
        lad = act.get("last_active_days", 999)
        if lad < 7:
            sigs["actively_looking"] = CareerSignal("availability", 1.0-(lad/30),
                f"Active {lad} days ago", 1.0)
        os = c.get("open_source", {})
        if os.get("github_stars", 0) > 100:
            sigs["open_source_impact"] = CareerSignal("innovation",
                min(os["github_stars"]/1000, 1.0), f"{os['github_stars']} GitHub stars", 0.9)
        if os.get("contributions", 0) > 50:
            sigs["community_contributor"] = CareerSignal("community",
                min(os["contributions"]/200, 1.0), f"{os['contributions']} contributions", 0.85)
        rec = c.get("recognition", {})
        if rec.get("publications", 0) > 0:
            sigs["thought_leadership"] = CareerSignal("expertise",
                min(rec["publications"]/5, 1.0), f"{rec['publications']} publications", 0.7)
        if rec.get("conference_talks", 0) > 0:
            sigs["public_speaking"] = CareerSignal("leadership",
                min(rec["conference_talks"]/5, 1.0), f"{rec['conference_talks']} conference talks", 0.75)
        refs = c.get("referrals", [])
        if refs:
            sigs["social_proof"] = CareerSignal("trust",
                sum(r.get("strength", 0.5) for r in refs)/len(refs),
                f"{len(refs)} professional referrals", 0.9)
        return sigs

    def _assess_seniority(self, c: Dict) -> Dict:
        ft = self._get_text(c).lower()
        impacts = self._extract_impact(c)
        impact_score = min(len([i for i in impacts if i["weight"] > 0.8])/5, 1.0)
        leadership_score = sum(1 for kw in ["led", "managed", "architected", "mentored",
            "principal", "technical lead", "founded"] if kw in ft) / 7
        year_score = min(c.get("total_years_experience", 0)/10, 1.0)
        eff = year_score*0.3 + impact_score*0.4 + leadership_score*0.3
        level = "principal" if eff > 0.8 else "senior" if eff > 0.6 else "mid" if eff > 0.4 else "junior"
        return {"effective_level": level, "effective_score": eff,
                "year_score": year_score, "impact_score": impact_score, "leadership_score": leadership_score}

    def _build_narrative(self, c: Dict) -> str:
        exps = c.get("experience", [])
        traj = self._analyze_trajectory(c)
        if not exps: return "No experience data available"
        mr = exps[0]
        parts = [f"{c.get('name','Candidate')} is a {traj['pattern'].replace('_',' ')} professional",
                 f"with {c.get('total_years_experience',0)} years of experience",
                 f"currently at {mr.get('company','unknown')} as {mr.get('title','unknown')}."]
        if traj.get("growth_signals"): parts.append("Shows clear growth trajectory.")
        imp = self._extract_impact(c)
        if imp: parts.append(f"Demonstrated measurable impact ({len(imp)} quantified achievements).")
        return " ".join(parts)

    def _detect_red_flags(self, c: Dict) -> List[str]:
        flags = []
        exps = c.get("experience", [])
        short = [e for e in exps if e.get("years", 2) < 1]
        if len(short) > 2: flags.append(f"Multiple short tenures ({len(short)} roles < 1 year)")
        if c.get("employment_gaps", 0) > 12: flags.append(f"Employment gap of {c['employment_gaps']} months")
        if c.get("platform_activity", {}).get("last_active_days", 0) > 90:
            flags.append("Inactive on platform (>90 days)")
        return flags

    def _detect_star_qualities(self, c: Dict) -> List[str]:
        ft = self._get_text(c).lower()
        sqs = []
        for q, sigs in {
            "Shipped at massive scale": ["million users", "billions", "petabyte", "global scale"],
            "Fast career progression": ["promoted", "youngest", "fast track"],
            "Research impact": ["patent", "published", "cited"],
            "Open source leader": ["open source", "github stars", "maintainer"],
            "Thought leader": ["conference", "speaker", "keynote"],
            "Builder mindset": ["founded", "built from scratch", "0 to 1"],
            "Force multiplier": ["mentored", "grew team", "hired"],
            "Business impact": ["revenue", "cost savings", "roi"],
        }.items():
            if any(s in ft for s in sigs): sqs.append(q)
        return sqs

    def _get_text(self, c: Dict) -> str:
        parts = [c.get("summary", ""), c.get("bio", "")]
        for e in c.get("experience", []):
            parts.extend([e.get("title",""), e.get("description",""), e.get("company","")])
        for p in c.get("projects", []):
            parts.extend([p.get("name",""), p.get("description","")])
        for s in c.get("skills", []):
            parts.append(s.get("name","") if isinstance(s, dict) else str(s))
        return " ".join(parts)


# ============================================================
# SCORING ENGINE
# ============================================================

class MultiSignalScoringEngine:
    def __init__(self, se: SemanticKnowledgeEngine):
        self.semantic = se
        self.weights = {
            "technical": 0.30, "semantic_fit": 0.20, "experience_quality": 0.20,
            "behavioral": 0.15, "culture_fit": 0.10, "growth_trajectory": 0.05,
        }

    def score_candidate(self, cp: Dict, ja: Dict) -> CandidateScore:
        ts, tb = self._score_technical(cp, ja)
        ss, sb = self._score_semantic(cp, ja)
        es, eb = self._score_experience(cp, ja)
        bs, bb = self._score_behavioral(cp, ja)
        cs, cb = self._score_culture(cp, ja)
        gs, gb = self._score_growth(cp, ja)

        total = (ts*self.weights["technical"] + ss*self.weights["semantic_fit"] +
                 es*self.weights["experience_quality"] + bs*self.weights["behavioral"] +
                 cs*self.weights["culture_fit"] + gs*self.weights["growth_trajectory"])
        total = self._apply_multipliers(total, cp, ja)
        total_n = min(total * 100, 100)

        strengths = self._strengths(tb, sb, eb, bb, cp)
        gaps = self._gaps(tb, ja, cp)
        rec, rec_class = self._recommendation(total_n, ts, cp.get("red_flags", []))
        interviews = self._interview_areas(gaps, ja)
        confidence = self._confidence(cp)

        return CandidateScore(
            candidate_id=cp.get("id", "unknown"),
            total_score=round(total_n, 2), rank=0,
            technical_score=round(ts*100, 2), semantic_fit_score=round(ss*100, 2),
            experience_score=round(es*100, 2), behavioral_score=round(bs*100, 2),
            culture_score=round(cs*100, 2), growth_trajectory_score=round(gs*100, 2),
            score_breakdown={"technical": tb, "semantic": sb, "experience": eb,
                             "behavioral": bb, "culture": cb, "growth": gb},
            strengths=strengths, gaps=gaps, hire_recommendation=rec,
            recommendation_class=rec_class, confidence=confidence,
            interview_focus_areas=interviews
        )

    def _score_technical(self, cp, ja):
        reqs = ja.get("weighted_requirements", [])
        sm = cp.get("skill_map", {})
        ft = self._get_text(cp)
        bd = {"matched_skills": [], "inferred_skills": [], "missing_skills": [], "total_weight": 0, "matched_weight": 0}
        tw = sum(r.importance for r in reqs if r.category == "technical")
        mw = 0
        for req in reqs:
            if req.category != "technical": continue
            bd["total_weight"] += req.importance
            if req.skill in sm:
                p = sm[req.skill]; mw += req.importance * p
                bd["matched_skills"].append({"skill": req.skill, "proficiency": p, "importance": req.importance, "match_type": "direct"})
                continue
            matched = False
            for v in req.semantic_variants:
                if v in sm or v in ft.lower():
                    mw += req.importance * 0.85
                    bd["matched_skills"].append({"skill": req.skill, "matched_via": v, "importance": req.importance, "match_type": "semantic"})
                    matched = True; break
            if matched: continue
            inf = self.semantic.infer_skill_from_context(ft, req.skill)
            if inf > 0.4:
                mw += req.importance * inf * 0.7
                bd["inferred_skills"].append({"skill": req.skill, "confidence": inf, "importance": req.importance})
            else:
                bd["missing_skills"].append({"skill": req.skill, "importance": req.importance,
                                              "criticality": "high" if req.importance > 0.7 else "medium"})
        return min(mw/max(tw, 0.01), 1.0), bd

    def _score_semantic(self, cp, ja):
        jd = ja.get("raw_jd", ""); ct = self._get_text(cp)
        bd = {}
        os = self.semantic.compute_semantic_similarity(ct, jd); bd["overall_similarity"] = os
        aa = self._archetype_score(cp, ja.get("role_archetype", "")); bd["archetype_alignment"] = aa
        sm = self._seniority_match(ja.get("seniority_level","mid"), cp.get("seniority_reality",{}).get("effective_level","mid")); bd["seniority_match"] = sm
        ds = self._domain_score(cp, ja); bd["domain_expertise"] = ds
        hr = ja.get("hidden_requirements", []); cl = ct.lower()
        hc = sum(1 for r in hr if r.replace("_"," ") in cl or r in cl)/max(len(hr),1); bd["hidden_coverage"] = hc
        score = os*0.30 + aa*0.25 + sm*0.25 + ds*0.15 + hc*0.05
        return min(score, 1.0), bd

    def _archetype_score(self, cp, arch):
        ft = self._get_text(cp).lower()
        signals = {
            "ml_engineer": ["model training", "ml pipeline", "feature engineering", "model deployment", "inference"],
            "data_scientist": ["statistical", "hypothesis", "insight", "analysis", "visualization"],
            "backend_engineer": ["api", "rest", "graphql", "database", "server", "microservice"],
            "data_engineer": ["pipeline", "etl", "spark", "airflow", "data warehouse"],
            "engineering_manager": ["managed", "led team", "hired", "mentored", "roadmap"],
        }.get(arch, [])
        if not signals: return 0.6
        return min(sum(1 for s in signals if s in ft)/max(len(signals)*0.5,1), 1.0)

    def _seniority_match(self, req, actual):
        order = ["junior", "mid", "senior", "principal"]
        try:
            d = abs(order.index(req) - order.index(actual))
            return [1.0, 0.78, 0.45, 0.2][min(d, 3)]
        except: return 0.7

    def _domain_score(self, cp, ja):
        ft = self._get_text(cp).lower()
        jl = ja.get("raw_jd","").lower()
        terms = [w for w in jl.split() if len(w) > 8 and w.isalpha()]
        if not terms: return 0.6
        return min(sum(1 for t in terms if t in ft)/max(len(terms)*0.3,1), 1.0)

    def _score_experience(self, cp, ja):
        bd = {}
        bd["company_caliber"] = self._company_caliber(cp)
        impacts = cp.get("impact_signals", [])
        qi = [i for i in impacts if i.get("weight",0) > 0.8]
        bd["impact_quality"] = min(len(qi)/5*0.6 + len(impacts)/10*0.4, 1.0)
        ry = self._max_years(ja); ay = cp.get("total_years_experience",0)
        bd["years_match"] = self._years_match(ay, ry)
        bd["industry_relevance"] = self._industry_relevance(cp, ja)
        bd["project_complexity"] = self._project_complexity(cp)
        score = (bd["company_caliber"]*0.20 + bd["impact_quality"]*0.35 +
                 bd["years_match"]*0.20 + bd["industry_relevance"]*0.15 + bd["project_complexity"]*0.10)
        return min(score, 1.0), bd

    def _company_caliber(self, cp):
        t1 = {"google","meta","apple","amazon","microsoft","netflix","openai","deepmind",
              "anthropic","stripe","airbnb","uber","linkedin","spacex","tesla","nvidia"}
        t2 = {"salesforce","adobe","oracle","ibm","intel","shopify","slack","zoom",
              "databricks","snowflake","confluent","cohere","hugging face"}
        ms = 0.5
        for e in cp.get("experience",[]):
            co = e.get("company","").lower()
            if any(t in co for t in t1): ms = max(ms, 1.0)
            elif any(t in co for t in t2): ms = max(ms, 0.85)
        return ms

    def _years_match(self, actual, required):
        if required == 0: return 0.8
        r = actual/required
        if r >= 1.0: return 0.7 if r > 3.0 else 0.8 if r > 2.0 else 1.0
        return 0.75 if r >= 0.7 else 0.5 if r >= 0.5 else 0.3

    def _max_years(self, ja):
        yl = [r.years_required for r in ja.get("requirements",[]) if r.years_required]
        return max(yl) if yl else 0

    def _industry_relevance(self, cp, ja):
        jl = ja.get("raw_jd","").lower(); ct = self._get_text(cp).lower()
        for kws in [["finance","banking","payment"],["health","medical","patient"],
                    ["ecommerce","retail","marketplace"],["saas","b2b","enterprise software"]]:
            if any(k in jl for k in kws):
                return 1.0 if any(k in ct for k in kws) else 0.5
        return 0.7

    def _project_complexity(self, cp):
        ft = self._get_text(cp).lower()
        sigs = ["distributed","real-time","at scale","production","million","architecture","system design"]
        return min(sum(1 for s in sigs if s in ft)/len(sigs)*1.5, 1.0)

    def _score_behavioral(self, cp, ja):
        bsigs = cp.get("behavioral_signals",{}); bd = {}
        if not bsigs: return 0.5, {"note":"No behavioral data"}
        tv, tn = 0.0, 0
        for sn, sig in bsigs.items():
            wv = sig.value * sig.recency_weight; tv += wv; tn += 1
            bd[sn] = {"value": sig.value, "evidence": sig.evidence}
        star_boost = min(len(cp.get("star_qualities",[])) * 0.05, 0.2)
        penalty = min(len(cp.get("red_flags",[])) * 0.08, 0.25)
        base = tv/max(tn,1) if tn > 0 else 0.5
        bd["star_boost"] = star_boost; bd["penalty"] = penalty
        return max(min(base + star_boost - penalty, 1.0), 0.0), bd

    def _score_culture(self, cp, ja):
        jc = ja.get("culture_signals",{}); ct = self._get_text(cp).lower(); bd = {}
        ta, ac = 0.0, 0.0
        evidence = {
            "fast_paced": ["shipped quickly","fast","agile","rapid"],
            "impact_driven": ["impact","drove results","outcome"],
            "innovation_focused": ["innovative","novel","created","invented"],
            "collaborative": ["team","cross-functional","collaborated"],
            "autonomous": ["independently","self-directed","owned"],
            "data_driven": ["data","metrics","measured","experiment"],
            "growth_mindset": ["learned","grew","developed"],
        }
        for trait, imp in jc.items():
            if imp < 0.3: continue
            evs = evidence.get(trait, [])
            ch = sum(1 for e in evs if e in ct)/max(len(evs),1)
            bd[trait] = {"importance": imp, "alignment": ch}
            ta += ch*imp; ac += imp
        return min(ta/max(ac,0.01), 1.0), bd

    def _score_growth(self, cp, ja):
        traj = cp.get("career_trajectory",{}); bd = {}
        bd["velocity"] = traj.get("velocity",0.5)
        bd["consistency"] = traj.get("consistency",0.7)
        ps = {"fast_riser":1.0,"steady_growth":0.8,"specialist":0.7,"stable":0.65,"unknown":0.5}
        bd["pattern"] = ps.get(traj.get("pattern","unknown"),0.5)
        ty = cp.get("total_years_experience",1)
        bd["impact_velocity"] = min(len(cp.get("impact_signals",[]))/max(ty,1)/2, 1.0)
        score = bd["velocity"]*0.30 + bd["consistency"]*0.25 + bd["pattern"]*0.30 + bd["impact_velocity"]*0.15
        return min(score, 1.0), bd

    def _apply_multipliers(self, score, cp, ja):
        m = 1.0
        if ja.get("seniority_level","") == cp.get("seniority_reality",{}).get("effective_level",""): m += 0.05
        if cp.get("open_source",{}).get("github_stars",0) > 500: m += 0.04
        m += min(len(cp.get("star_qualities",[])) * 0.02, 0.08)
        if cp.get("platform_activity",{}).get("last_active_days",999) < 3: m += 0.03
        m -= min(len(cp.get("red_flags",[])) * 0.04, 0.12)
        ay = cp.get("total_years_experience",0); ry = self._max_years(ja)
        if ry > 0 and ay > ry * 2.5: m -= 0.05
        return score * min(max(m, 0.7), 1.2)

    def _max_years(self, ja):
        yl = [r.years_required for r in ja.get("requirements",[]) if r.years_required]
        return max(yl) if yl else 0

    def _strengths(self, tb, sb, eb, bb, cp):
        s = []
        ms = tb.get("matched_skills",[])
        hc = [x for x in ms if x.get("proficiency",0) > 0.8]
        if hc: s.append(f"Expert-level proficiency in {', '.join(x['skill'] for x in hc[:3])}")
        if sb.get("archetype_alignment",0) > 0.75: s.append("Career trajectory perfectly aligned with role archetype")
        if eb.get("impact_quality",0) > 0.7: s.append("Strong track record of quantified, measurable impact")
        if eb.get("company_caliber",0) > 0.85: s.append("Proven in high-bar technical environments")
        bsigs = cp.get("behavioral_signals",{})
        if "open_source_impact" in bsigs: s.append("Significant open source contributions & community presence")
        if "thought_leadership" in bsigs: s.append("Published researcher and recognized thought leader")
        for q in cp.get("star_qualities",[])[:3]: s.append(q)
        return s[:6]

    def _gaps(self, tb, ja, cp):
        gaps = []
        for sg in [x for x in tb.get("missing_skills",[]) if x.get("importance",0) > 0.7][:3]:
            gaps.append(f"Missing critical skill: {sg['skill']} ({sg['importance']:.0%} importance)")
        nc = [x for x in tb.get("missing_skills",[]) if x.get("importance",0) <= 0.7]
        if nc: gaps.append(f"Secondary gaps: {', '.join(x['skill'] for x in nc[:3])}")
        for f in cp.get("red_flags",[]): gaps.append(f"Risk: {f}")
        return gaps

    def _recommendation(self, score, ts, red_flags):
        crf = len([f for f in red_flags if "short tenure" in f.lower()])
        if score >= 85 and ts*100 >= 75 and crf == 0: return "Strong Hire", "strong-hire"
        if score >= 75 and ts*100 >= 65: return "Hire", "hire"
        if score >= 65 and ts*100 >= 55: return "Consider", "consider"
        if score >= 55: return "Maybe", "maybe"
        if score >= 40: return "Pipeline", "pipeline"
        return "Pass", "pass"

    def _interview_areas(self, gaps, ja):
        areas = []
        for g in gaps[:2]:
            if "missing" in g.lower():
                skill = g.split(":")[1].split("(")[0].strip() if ":" in g else g
                areas.append(f"Technical deep-dive: {skill}")
        arch_areas = {
            "ml_engineer": ["System design: ML pipeline at scale", "Model optimization & production deployment"],
            "engineering_manager": ["Leadership scenarios & conflict resolution", "Team building & delivery track record"],
            "backend_engineer": ["Distributed systems design", "Database architecture & scaling"],
        }.get(ja.get("role_archetype",""), [])
        areas.extend(arch_areas)
        return areas[:5]

    def _confidence(self, cp):
        f = [cp.get("platform_activity",{}).get("profile_completeness",0.5),
             sum([len(cp.get("experience",[])) > 0, len(cp.get("skills",[])) > 0, len(cp.get("projects",[])) > 0])/3,
             min(len(cp.get("behavioral_signals",{}))/5, 1.0)]
        return sum(f)/len(f)

    def _get_text(self, cp):
        parts = [cp.get("summary",""), cp.get("bio",""), cp.get("candidate_narrative","")]
        for e in cp.get("experience",[]): parts.extend([e.get("title",""), e.get("description",""), e.get("company","")])
        for p in cp.get("projects",[]): parts.extend([p.get("name",""), p.get("description","")])
        for s in cp.get("skills",[]):
            parts.append(s.get("name","") if isinstance(s, dict) else str(s))
        return " ".join(parts)


# ============================================================
# RANKING ENGINE
# ============================================================

class IntelligentRankingEngine:
    def rank(self, scored: List[CandidateScore], top_k: int = 10) -> List[CandidateScore]:
        ranked = sorted(scored, key=lambda x: x.total_score, reverse=True)[:top_k]
        for i, c in enumerate(ranked): c.rank = i + 1
        return ranked


# ============================================================
# DATA
# ============================================================

def get_candidates():
    return [
        {
            "id": "c001", "name": "Aria Chen", "location": "San Francisco, CA",
            "total_years_experience": 7,
            "skills": [
                {"name": "python", "level": 0.95}, {"name": "machine learning", "level": 0.90},
                {"name": "pytorch", "level": 0.88}, {"name": "tensorflow", "level": 0.80},
                {"name": "kubernetes", "level": 0.75}, {"name": "mlops", "level": 0.82},
                {"name": "spark", "level": 0.70}, {"name": "sql", "level": 0.85},
                {"name": "data pipeline", "level": 0.78}, {"name": "distributed systems", "level": 0.65},
                {"name": "nlp", "level": 0.72}, {"name": "transformers", "level": 0.75},
                {"name": "llm", "level": 0.68},
            ],
            "experience": [
                {"title": "Senior ML Engineer", "company": "OpenAI", "years": 2.5,
                 "description": "Led development of production ML pipeline serving 50M+ users daily. Reduced model inference latency by 40% through optimization. Architected distributed training infrastructure processing 1TB+ datasets. Mentored team of 4 engineers. Shipped 3 major model versions to production."},
                {"title": "ML Engineer", "company": "Airbnb", "years": 3,
                 "description": "Built recommendation engine using deep learning, increasing bookings by 12%. Developed real-time fraud detection system handling 100k transactions/minute. Implemented A/B testing framework for ML model evaluation. Python, PyTorch, Spark, Kafka, AWS."},
                {"title": "Data Scientist", "company": "Stripe", "years": 1.5,
                 "description": "Statistical modeling for payment fraud detection. Reduced false positive rate by 23%. Python, scikit-learn, SQL, Redshift."},
            ],
            "projects": [{"name": "FastML", "description": "Open source ML training optimization library. 2.3k GitHub stars, used by 500+ companies."}],
            "summary": "Senior ML Engineer with 7 years building production ML systems at scale. Expert in PyTorch, MLOps, distributed training. Strong track record of measurable business impact.",
            "platform_activity": {"response_rate": 0.85, "profile_completeness": 0.95, "last_active_days": 2},
            "open_source": {"github_stars": 2300, "contributions": 180},
            "recognition": {"publications": 2, "conference_talks": 3},
            "referrals": [{"strength": 0.9}, {"strength": 0.85}],
            "employment_gaps": 0
        },
        {
            "id": "c002", "name": "Marcus Johnson", "location": "New York, NY",
            "total_years_experience": 4,
            "skills": [
                {"name": "python", "level": 0.85}, {"name": "machine learning", "level": 0.75},
                {"name": "pytorch", "level": 0.72}, {"name": "docker", "level": 0.70},
                {"name": "kubernetes", "level": 0.55}, {"name": "sql", "level": 0.80},
                {"name": "nlp", "level": 0.78}, {"name": "transformers", "level": 0.80},
                {"name": "llm", "level": 0.82}, {"name": "data pipeline", "level": 0.60},
                {"name": "aws", "level": 0.65},
            ],
            "experience": [
                {"title": "ML Engineer", "company": "Cohere", "years": 2,
                 "description": "Fine-tuned and deployed large language models for enterprise use cases. Built RAG pipeline serving 1M+ queries/day. Improved model accuracy by 18% through advanced prompt engineering. PyTorch, Transformers, AWS SageMaker, Docker."},
                {"title": "Research Engineer", "company": "Columbia University NLP Lab", "years": 2,
                 "description": "Published 2 papers on transformer architectures at ACL 2023, EMNLP 2022. Implemented novel attention mechanism improving BERT performance by 8%."},
            ],
            "projects": [{"name": "LLM Evaluation Framework", "description": "Open source LLM evaluation. 800+ stars, featured at NeurIPS 2023."}],
            "summary": "ML Engineer specializing in NLP and LLMs. Research background translated to production. Deep expertise in transformer architectures.",
            "platform_activity": {"response_rate": 0.90, "profile_completeness": 0.90, "last_active_days": 1},
            "open_source": {"github_stars": 800, "contributions": 120},
            "recognition": {"publications": 2, "conference_talks": 2},
            "referrals": [{"strength": 0.92}, {"strength": 0.80}],
            "employment_gaps": 0
        },
        {
            "id": "c003", "name": "Priya Patel", "location": "Seattle, WA",
            "total_years_experience": 9,
            "skills": [
                {"name": "python", "level": 0.90}, {"name": "machine learning", "level": 0.70},
                {"name": "tensorflow", "level": 0.68}, {"name": "sql", "level": 0.88},
                {"name": "spark", "level": 0.85}, {"name": "data pipeline", "level": 0.90},
                {"name": "aws", "level": 0.85}, {"name": "kubernetes", "level": 0.80},
                {"name": "data engineering", "level": 0.88},
            ],
            "experience": [
                {"title": "Principal Data Engineer", "company": "Amazon", "years": 4,
                 "description": "Architected company-wide data platform processing 5PB+ daily. Led team of 8 engineers. Reduced data pipeline costs by $2M annually. Mentored 6 junior engineers, 2 promoted to senior."},
                {"title": "Senior Data Engineer", "company": "Databricks", "years": 3,
                 "description": "Built Delta Lake-based lakehouse for Fortune 500 clients. Spark optimization reduced job costs by 45%. Created ML feature store serving 100+ models."},
                {"title": "Data Engineer", "company": "Microsoft", "years": 2,
                 "description": "ETL pipelines for Azure data warehouse. Python, SQL, Azure."},
            ],
            "projects": [],
            "summary": "Principal Data Engineer with 9 years building large-scale data infrastructure. Expert in Spark, AWS, and ML pipeline architecture.",
            "platform_activity": {"response_rate": 0.70, "profile_completeness": 0.85, "last_active_days": 14},
            "open_source": {"github_stars": 150, "contributions": 40},
            "recognition": {"publications": 0, "conference_talks": 1},
            "referrals": [{"strength": 0.88}],
            "employment_gaps": 0
        },
        {
            "id": "c004", "name": "Dr. Wei Zhang", "location": "Boston, MA",
            "total_years_experience": 8,
            "skills": [
                {"name": "python", "level": 0.85}, {"name": "machine learning", "level": 0.98},
                {"name": "deep learning", "level": 0.95}, {"name": "pytorch", "level": 0.92},
                {"name": "nlp", "level": 0.90}, {"name": "computer vision", "level": 0.88},
                {"name": "transformers", "level": 0.95},
            ],
            "experience": [
                {"title": "Research Scientist", "company": "MIT CSAIL", "years": 5,
                 "description": "Published 12 papers in top venues (NeurIPS, ICML, ICLR). H-index 18. Novel transformer architecture cited 500+ times. NSF grant recipient."},
                {"title": "Research Intern", "company": "Google Brain", "years": 0.5,
                 "description": "Research on efficient transformers. 1 publication."},
                {"title": "PhD Student", "company": "MIT", "years": 5,
                 "description": "PhD in Machine Learning. Thesis: Efficient Attention Mechanisms."},
            ],
            "projects": [],
            "summary": "Research scientist with exceptional ML theory depth. 12 publications in top venues. Limited production experience, primarily research-focused.",
            "platform_activity": {"response_rate": 0.60, "profile_completeness": 0.80, "last_active_days": 30},
            "open_source": {"github_stars": 450, "contributions": 60},
            "recognition": {"publications": 12, "conference_talks": 5},
            "referrals": [{"strength": 0.95}],
            "employment_gaps": 0
        },
        {
            "id": "c005", "name": "James O'Brien", "location": "Austin, TX",
            "total_years_experience": 6,
            "skills": [
                {"name": "python", "level": 0.92}, {"name": "java", "level": 0.88},
                {"name": "distributed systems", "level": 0.90}, {"name": "kubernetes", "level": 0.88},
                {"name": "docker", "level": 0.90}, {"name": "kafka", "level": 0.85},
                {"name": "microservices", "level": 0.88}, {"name": "sql", "level": 0.85},
                {"name": "aws", "level": 0.82}, {"name": "machine learning", "level": 0.45},
                {"name": "data pipeline", "level": 0.72},
            ],
            "experience": [
                {"title": "Staff Software Engineer", "company": "Netflix", "years": 3,
                 "description": "Designed streaming infrastructure serving 200M+ users. Led migration to microservices - 99.99% uptime. Reduced infrastructure costs by $3M annually. Technical lead for 6-person team."},
                {"title": "Senior Software Engineer", "company": "Uber", "years": 3,
                 "description": "Real-time dispatch system handling 10M+ rides/day. Designed event-driven architecture with Kafka. Python, Java, Kubernetes."},
            ],
            "projects": [{"name": "StreamBench", "description": "Open source streaming benchmark. 1.2k stars."}],
            "summary": "Staff engineer with deep expertise in distributed systems. Excellent track record of building reliable, scalable infrastructure at Netflix and Uber.",
            "platform_activity": {"response_rate": 0.80, "profile_completeness": 0.88, "last_active_days": 5},
            "open_source": {"github_stars": 1200, "contributions": 90},
            "recognition": {"publications": 0, "conference_talks": 2},
            "referrals": [{"strength": 0.90}, {"strength": 0.85}],
            "employment_gaps": 0
        },
        {
            "id": "c006", "name": "Alex Rivera", "location": "Denver, CO",
            "total_years_experience": 5,
            "skills": [
                {"name": "python", "level": 0.80}, {"name": "machine learning", "level": 0.72},
                {"name": "pytorch", "level": 0.68}, {"name": "docker", "level": 0.75},
                {"name": "sql", "level": 0.70},
            ],
            "experience": [
                {"title": "ML Engineer", "company": "Startup A", "years": 0.8, "description": "ML model development."},
                {"title": "ML Engineer", "company": "Startup B", "years": 0.7, "description": "Recommendation system."},
                {"title": "Data Scientist", "company": "Company C", "years": 1.5, "description": "Predictive analytics, reduced churn by 15%."},
                {"title": "Junior Data Scientist", "company": "Agency D", "years": 1.0, "description": "Client ML projects."},
                {"title": "Data Analyst", "company": "Company E", "years": 1.0, "description": "SQL analysis."},
            ],
            "projects": [],
            "summary": "ML practitioner with broad experience. Multiple short stints at startups.",
            "platform_activity": {"response_rate": 0.75, "profile_completeness": 0.72, "last_active_days": 3},
            "open_source": {"github_stars": 20, "contributions": 10},
            "recognition": {"publications": 0, "conference_talks": 0},
            "referrals": [],
            "employment_gaps": 2
        },
        {
            "id": "c007", "name": "Fatima Al-Rashidi", "location": "Remote",
            "total_years_experience": 4,
            "skills": [
                {"name": "python", "level": 0.88}, {"name": "machine learning", "level": 0.82},
                {"name": "pytorch", "level": 0.80}, {"name": "nlp", "level": 0.85},
                {"name": "transformers", "level": 0.88}, {"name": "llm", "level": 0.85},
                {"name": "mlops", "level": 0.75}, {"name": "docker", "level": 0.72},
                {"name": "aws", "level": 0.68}, {"name": "kubernetes", "level": 0.60},
            ],
            "experience": [
                {"title": "ML Engineer", "company": "Hugging Face", "years": 2.5,
                 "description": "Core contributor to Transformers library (5k+ commits). Implemented 15+ model architectures. Built model hub serving 100M+ monthly downloads."},
                {"title": "Research Engineer", "company": "EleutherAI", "years": 1.5,
                 "description": "Trained GPT-NeoX-20B, first open-source 20B parameter LLM. Distributed training across 96 GPUs."},
            ],
            "projects": [{"name": "Arabic NLP Suite", "description": "Comprehensive Arabic NLP toolkit. 8k GitHub stars, used in 40+ countries."}],
            "summary": "ML Engineer specializing in LLMs and NLP. Core contributor to foundational open-source ML. Trained production LLMs at scale.",
            "platform_activity": {"response_rate": 0.95, "profile_completeness": 0.92, "last_active_days": 1},
            "open_source": {"github_stars": 8000, "contributions": 5000},
            "recognition": {"publications": 1, "conference_talks": 2},
            "referrals": [{"strength": 0.95}, {"strength": 0.90}],
            "employment_gaps": 0
        },
        {
            "id": "c008", "name": "Robert Kim", "location": "Palo Alto, CA",
            "total_years_experience": 15,
            "skills": [
                {"name": "machine learning", "level": 0.85}, {"name": "python", "level": 0.80},
                {"name": "leadership", "level": 0.95}, {"name": "distributed systems", "level": 0.88},
                {"name": "kubernetes", "level": 0.82}, {"name": "mlops", "level": 0.78},
            ],
            "experience": [
                {"title": "VP of Engineering, AI", "company": "Salesforce", "years": 4,
                 "description": "Led 120-person AI engineering org. $50M budget. Launched Einstein AI used by 100k+ companies. Grew team from 30 to 120 engineers."},
                {"title": "Director, ML Platform", "company": "LinkedIn", "years": 5,
                 "description": "Built ML platform serving all LinkedIn recommendation systems. Led 45 engineers. 10x improvement in deployment velocity."},
                {"title": "Senior ML Engineer", "company": "Google", "years": 6,
                 "description": "Core contributor to TensorFlow. Search ranking ML systems."},
            ],
            "projects": [],
            "summary": "Seasoned AI engineering leader, VP-level at Salesforce. 15 years experience with strong technical foundation and extensive people management.",
            "platform_activity": {"response_rate": 0.65, "profile_completeness": 0.90, "last_active_days": 21},
            "open_source": {"github_stars": 200, "contributions": 30},
            "recognition": {"publications": 3, "conference_talks": 8},
            "referrals": [{"strength": 0.95}, {"strength": 0.92}],
            "employment_gaps": 0
        },
        {
            "id": "c009", "name": "Zara Thompson", "location": "San Jose, CA",
            "total_years_experience": 1.5,
            "skills": [
                {"name": "python", "level": 0.80}, {"name": "machine learning", "level": 0.72},
                {"name": "pytorch", "level": 0.75}, {"name": "nlp", "level": 0.70},
                {"name": "transformers", "level": 0.72}, {"name": "sql", "level": 0.68},
            ],
            "experience": [
                {"title": "ML Engineer", "company": "Scale AI", "years": 1.5,
                 "description": "Built data quality ML pipeline improving accuracy by 22%. Fastest promotion to SWE II in team history (8 months)."},
            ],
            "projects": [
                {"name": "Stanford Thesis: Efficient Transformers", "description": "Novel attention optimization reducing inference by 3x. Best thesis award."},
                {"name": "HackMIT Winner", "description": "First place ML track. Real-time sign language translation."},
            ],
            "summary": "Stanford CS graduate (4.0 GPA). Quick riser at Scale AI, exceptional learning velocity. Strong theoretical foundation.",
            "platform_activity": {"response_rate": 0.95, "profile_completeness": 0.88, "last_active_days": 0},
            "open_source": {"github_stars": 300, "contributions": 80},
            "recognition": {"publications": 0, "conference_talks": 0},
            "referrals": [{"strength": 0.90}, {"strength": 0.85}],
            "employment_gaps": 0
        },
        {
            "id": "c010", "name": "David Park", "location": "Chicago, IL",
            "total_years_experience": 5,
            "skills": [
                {"name": "python", "level": 0.75}, {"name": "machine learning", "level": 0.68},
                {"name": "tensorflow", "level": 0.65}, {"name": "sql", "level": 0.78},
                {"name": "docker", "level": 0.70}, {"name": "aws", "level": 0.65},
            ],
            "experience": [
                {"title": "ML Engineer", "company": "Mid-size Startup", "years": 3,
                 "description": "ML models for churn prediction. 14% improvement. Python, TensorFlow, AWS."},
                {"title": "Data Scientist", "company": "Consulting Firm", "years": 2,
                 "description": "Client analytics. SQL, Python, dashboards."},
            ],
            "projects": [],
            "summary": "ML Engineer with solid foundations in standard ML workflows.",
            "platform_activity": {"response_rate": 0.70, "profile_completeness": 0.75, "last_active_days": 7},
            "open_source": {"github_stars": 10, "contributions": 5},
            "recognition": {"publications": 0, "conference_talks": 0},
            "referrals": [],
            "employment_gaps": 0
        },
    ]


def get_job():
    title = "Senior ML Engineer — Foundation Models"
    jd = """
    About the Role
    We are building next-generation AI infrastructure and need exceptional ML Engineers
    who operate at the intersection of cutting-edge research and production-scale systems.
    You will join our Foundation Models team working on large language models and ML systems
    serving hundreds of millions of users globally.

    What You'll Do
    - Design and build scalable ML training and inference pipelines for large-scale models
    - Develop MLOps infrastructure for continuous model improvement and deployment
    - Collaborate cross-functionally with research scientists to productionize novel models
    - Lead technical architecture decisions for ML systems serving millions of users
    - Mentor junior engineers and drive data pipeline development at petabyte scale

    Required Qualifications
    - 5+ years of software engineering with 3+ years in machine learning (required)
    - Expert-level Python programming (required, essential)
    - PyTorch or TensorFlow in production environments (must have)
    - Strong understanding of distributed systems and ML infrastructure (required)
    - MLOps tools: experiment tracking, model serving, monitoring (must have)
    - Proven track record of shipping ML systems at real-world scale (essential)

    Preferred Qualifications
    - Experience with LLMs, transformers, or NLP (strongly preferred)
    - Distributed training: multi-GPU, multi-node (preferred)
    - Kubernetes and container orchestration (preferred)
    - Open-source ML contributions (nice to have)
    - Research background or publications (nice to have)
    - Kafka, Spark, or large-scale data pipelines (bonus)

    Culture
    We are a fast-paced, impact-driven, innovative team. We value ownership, data-driven
    decisions, and a growth mindset. You will thrive here if you are a builder who ships,
    takes autonomous ownership, and collaborates across functions.
    """
    return jd, title


# ============================================================
# WEB DASHBOARD
# ============================================================

def generate_html(results: List[CandidateScore], candidates: List[Dict],
                  job_analysis: Dict, processing_time: float) -> str:

    c_lookup = {c["id"]: c for c in candidates}

    rec_colors = {
        "strong-hire": {"bg": "#0d9488", "text": "#ffffff", "badge": "STRONG HIRE"},
        "hire": {"bg": "#0284c7", "text": "#ffffff", "badge": "HIRE"},
        "consider": {"bg": "#7c3aed", "text": "#ffffff", "badge": "CONSIDER"},
        "maybe": {"bg": "#d97706", "text": "#ffffff", "badge": "MAYBE"},
        "pipeline": {"bg": "#64748b", "text": "#ffffff", "badge": "PIPELINE"},
        "pass": {"bg": "#dc2626", "text": "#ffffff", "badge": "PASS"},
    }

    def score_color(s):
        if s >= 80: return "#0d9488"
        if s >= 70: return "#0284c7"
        if s >= 60: return "#7c3aed"
        if s >= 50: return "#d97706"
        return "#94a3b8"

    def ring(score, size=80, stroke=7):
        r = (size - stroke*2) / 2
        circ = 2 * 3.14159 * r
        dash = circ * score / 100
        gap = circ - dash
        col = score_color(score)
        return f'''
        <svg width="{size}" height="{size}" style="transform:rotate(-90deg)">
          <circle cx="{size/2}" cy="{size/2}" r="{r}"
            fill="none" stroke="#1e293b" stroke-width="{stroke}"/>
          <circle cx="{size/2}" cy="{size/2}" r="{r}"
            fill="none" stroke="{col}" stroke-width="{stroke}"
            stroke-dasharray="{dash:.1f} {gap:.1f}"
            stroke-linecap="round"/>
        </svg>
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
             font-size:15px;font-weight:700;color:{col}">{score:.0f}</div>'''

    def bar(val, color="#0d9488"):
        return f'''<div style="background:#1e293b;border-radius:4px;height:6px;width:100%;overflow:hidden">
          <div style="background:{color};height:6px;width:{val:.0f}%;border-radius:4px;
               transition:width 1s ease"></div></div>'''

    cards_html = ""
    for sc in results:
        c = c_lookup.get(sc.candidate_id, {})
        exps = c.get("experience", [])
        curr_title = exps[0].get("title", "N/A") if exps else "N/A"
        curr_co = exps[0].get("company", "N/A") if exps else "N/A"
        rc = rec_colors.get(sc.recommendation_class, rec_colors["pipeline"])
        rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
        rank_icon = rank_icons.get(sc.rank, f"#{sc.rank}")

        dims = [
            ("Technical", sc.technical_score, "#0d9488"),
            ("Semantic Fit", sc.semantic_fit_score, "#0284c7"),
            ("Experience", sc.experience_score, "#7c3aed"),
            ("Behavioral", sc.behavioral_score, "#d97706"),
            ("Culture", sc.culture_score, "#f43f5e"),
            ("Growth", sc.growth_trajectory_score, "#8b5cf6"),
        ]
        dims_html = "".join([f'''
            <div style="margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em">{n}</span>
                <span style="font-size:11px;font-weight:600;color:{co}">{v:.0f}</span>
              </div>
              {bar(v, co)}
            </div>''' for n, v, co in dims])

        strengths_html = "".join([f'<div style="display:flex;align-items:flex-start;gap:6px;margin-bottom:6px"><span style="color:#0d9488;margin-top:1px;flex-shrink:0">✓</span><span style="font-size:12px;color:#cbd5e1;line-height:1.4">{s}</span></div>' for s in sc.strengths[:4]])
        gaps_html = "".join([f'<div style="display:flex;align-items:flex-start;gap:6px;margin-bottom:6px"><span style="color:#f43f5e;margin-top:1px;flex-shrink:0">!</span><span style="font-size:12px;color:#cbd5e1;line-height:1.4">{g}</span></div>' for g in sc.gaps[:3]])
        interview_html = "".join([f'<div style="font-size:11px;color:#94a3b8;padding:5px 8px;background:#1e293b;border-radius:4px;margin-bottom:4px">→ {a}</div>' for a in sc.interview_focus_areas[:3]])
        stars_html = "".join([f'<span style="font-size:10px;background:#1e2a1a;color:#4ade80;padding:3px 8px;border-radius:20px;margin:2px 2px 2px 0;display:inline-block">{q}</span>' for q in c.get("star_qualities",[])])

        conf_pct = int(sc.confidence * 100)
        os_stars = c.get("open_source", {}).get("github_stars", 0)
        pubs = c.get("recognition", {}).get("publications", 0)
        talks = c.get("recognition", {}).get("conference_talks", 0)
        refs = len(c.get("referrals", []))
        activity_days = c.get("platform_activity", {}).get("last_active_days", 999)
        activity_str = "Today" if activity_days == 0 else f"{activity_days}d ago"
        activity_color = "#4ade80" if activity_days < 3 else "#facc15" if activity_days < 14 else "#94a3b8"

        cards_html += f'''
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;
             overflow:hidden;transition:transform .2s,box-shadow .2s;margin-bottom:16px"
             onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 20px 40px rgba(0,0,0,.4)'"
             onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">

          <!-- Header -->
          <div style="padding:20px 24px 16px;border-bottom:1px solid #1e293b;
               display:flex;align-items:center;justify-content:space-between">
            <div style="display:flex;align-items:center;gap:16px">
              <div style="font-size:24px">{rank_icon}</div>
              <div style="position:relative;width:80px;height:80px;flex-shrink:0">
                {ring(sc.total_score)}
              </div>
              <div>
                <div style="font-size:18px;font-weight:700;color:#f1f5f9">{c.get("name","Unknown")}</div>
                <div style="font-size:13px;color:#64748b;margin-top:2px">{curr_title} @ {curr_co}</div>
                <div style="font-size:12px;color:#475569;margin-top:4px">📍 {c.get("location","N/A")} &nbsp;·&nbsp; 💼 {c.get("total_years_experience",0)} yrs exp</div>
              </div>
            </div>
            <div style="text-align:right">
              <div style="background:{rc['bg']};color:{rc['text']};padding:6px 14px;
                   border-radius:20px;font-size:12px;font-weight:700;letter-spacing:.05em;
                   display:inline-block">{rc['badge']}</div>
              <div style="margin-top:10px;display:flex;gap:12px;justify-content:flex-end">
                <div style="text-align:center">
                  <div style="font-size:14px;font-weight:700;color:#f1f5f9">{"⭐ "+str(os_stars) if os_stars > 0 else "—"}</div>
                  <div style="font-size:10px;color:#475569">GH Stars</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:14px;font-weight:700;color:#f1f5f9">{pubs if pubs > 0 else "—"}</div>
                  <div style="font-size:10px;color:#475569">Papers</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:14px;font-weight:700;color:#f1f5f9">{refs if refs > 0 else "—"}</div>
                  <div style="font-size:10px;color:#475569">Refs</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:14px;font-weight:700;color:{activity_color}">{activity_str}</div>
                  <div style="font-size:10px;color:#475569">Active</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Body -->
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0">

            <!-- Scores -->
            <div style="padding:16px 20px;border-right:1px solid #1e293b">
              <div style="font-size:11px;color:#475569;text-transform:uppercase;
                   letter-spacing:.08em;margin-bottom:12px;font-weight:600">Score Breakdown</div>
              {dims_html}
            </div>

            <!-- Strengths & Gaps -->
            <div style="padding:16px 20px;border-right:1px solid #1e293b">
              <div style="font-size:11px;color:#475569;text-transform:uppercase;
                   letter-spacing:.08em;margin-bottom:10px;font-weight:600">Strengths</div>
              {strengths_html}
              {"" if not sc.gaps else f'<div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:.08em;margin:12px 0 10px;font-weight:600">Gaps & Risks</div>' + gaps_html}
            </div>

            <!-- Interview & Signal -->
            <div style="padding:16px 20px">
              <div style="font-size:11px;color:#475569;text-transform:uppercase;
                   letter-spacing:.08em;margin-bottom:10px;font-weight:600">Interview Focus</div>
              {interview_html}
              {"" if not stars_html else f'<div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:.08em;margin:12px 0 8px;font-weight:600">Star Qualities</div><div>' + stars_html + "</div>"}
              <div style="margin-top:14px;padding:10px;background:#1e293b;border-radius:8px">
                <div style="font-size:10px;color:#475569;margin-bottom:4px">CONFIDENCE</div>
                {bar(conf_pct, "#0284c7")}
                <div style="font-size:11px;color:#94a3b8;margin-top:4px">{conf_pct}% data completeness</div>
              </div>
            </div>

          </div>
        </div>'''

    # Stats
    scores = [r.total_score for r in results]
    avg_score = sum(scores)/len(scores) if scores else 0
    top_score = max(scores) if scores else 0
    strong_hires = len([r for r in results if r.recommendation_class in ["strong-hire","hire"]])

    req_list = "".join([f'''
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
        <div style="width:{int(r.importance*100)}px;max-width:100px;background:#0d9488;
             height:4px;border-radius:2px;flex-shrink:0"></div>
        <span style="font-size:12px;color:#94a3b8">{r.skill}</span>
        <span style="font-size:11px;color:#475569;margin-left:auto">{r.importance:.0%}</span>
      </div>''' for r in job_analysis["requirements"][:8]])

    culture_list = "".join([f'<span style="font-size:11px;background:#1e293b;color:#94a3b8;padding:4px 10px;border-radius:20px;margin:3px 3px 3px 0;display:inline-block">{k.replace("_"," ").title()}</span>'
                             for k, v in job_analysis.get("culture_signals",{}).items() if v > 0.3])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NEXUS AI Recruiter</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
       background:#020617;color:#f1f5f9;min-height:100vh}}
  ::-webkit-scrollbar{{width:6px}}
  ::-webkit-scrollbar-track{{background:#0f172a}}
  ::-webkit-scrollbar-thumb{{background:#334155;border-radius:3px}}
  @keyframes fadeIn{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
  .card{{animation:fadeIn .4s ease forwards}}
</style>
</head>
<body>

<!-- NAV -->
<div style="background:#0a0f1e;border-bottom:1px solid #1e293b;padding:0 32px;
     position:sticky;top:0;z-index:100;backdrop-filter:blur(10px)">
  <div style="max-width:1400px;margin:0 auto;display:flex;align-items:center;
       justify-content:space-between;height:56px">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:32px;height:32px;background:linear-gradient(135deg,#0d9488,#0284c7);
           border-radius:8px;display:flex;align-items:center;justify-content:center;
           font-weight:900;font-size:14px">N</div>
      <span style="font-weight:700;font-size:15px;letter-spacing:.02em">NEXUS AI Recruiter</span>
      <span style="background:#1e293b;color:#64748b;font-size:10px;padding:2px 8px;
           border-radius:10px;font-weight:600">INTELLIGENCE PLATFORM</span>
    </div>
    <div style="display:flex;gap:24px;font-size:12px;color:#475569">
      <span>⚡ {processing_time:.2f}s processing</span>
      <span>📊 {len(results)}/{len(candidates)} shortlisted</span>
      <span style="color:#0d9488">● Live</span>
    </div>
  </div>
</div>

<!-- HERO -->
<div style="background:linear-gradient(135deg,#0a0f1e 0%,#0f172a 50%,#0a0f1e 100%);
     border-bottom:1px solid #1e293b;padding:32px">
  <div style="max-width:1400px;margin:0 auto">
    <div style="font-size:11px;color:#0d9488;text-transform:uppercase;letter-spacing:.1em;
         font-weight:600;margin-bottom:8px">Intelligence Report · {datetime.now().strftime("%B %d, %Y")}</div>
    <h1 style="font-size:28px;font-weight:800;color:#f1f5f9;margin-bottom:4px">{job_analysis["title"]}</h1>
    <div style="font-size:14px;color:#475569">
      {job_analysis["role_archetype"].replace("_"," ").title()} &nbsp;·&nbsp;
      {job_analysis["seniority_level"].title()} Level &nbsp;·&nbsp;
      {job_analysis["company_stage"].replace("_"," ").title()}
    </div>

    <!-- KPI Row -->
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-top:24px">
      {"".join([f'''
      <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:16px 20px">
        <div style="font-size:24px;font-weight:800;color:{col}">{val}</div>
        <div style="font-size:11px;color:#475569;margin-top:2px;text-transform:uppercase;letter-spacing:.05em">{label}</div>
      </div>''' for val, label, col in [
          (len(candidates), "Candidates Analyzed", "#f1f5f9"),
          (len(results), "Shortlisted", "#0d9488"),
          (strong_hires, "Ready to Hire", "#0284c7"),
          (f"{avg_score:.1f}", "Avg Score", score_color(avg_score)),
          (f"{top_score:.1f}", "Top Score", score_color(top_score)),
      ]])}
    </div>
  </div>
</div>

<!-- MAIN -->
<div style="max-width:1400px;margin:0 auto;padding:32px;display:grid;
     grid-template-columns:1fr 280px;gap:24px">

  <!-- LEFT: CANDIDATES -->
  <div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
      <h2 style="font-size:16px;font-weight:700;color:#f1f5f9">Ranked Shortlist</h2>
      <div style="font-size:12px;color:#475569">Sorted by composite intelligence score</div>
    </div>
    {cards_html}
  </div>

  <!-- RIGHT: SIDEBAR -->
  <div>

    <!-- Job Requirements -->
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;
         padding:20px;margin-bottom:16px">
      <div style="font-size:12px;font-weight:700;color:#f1f5f9;margin-bottom:16px;
           text-transform:uppercase;letter-spacing:.05em">Job Requirements</div>
      {req_list}
    </div>

    <!-- Culture DNA -->
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;
         padding:20px;margin-bottom:16px">
      <div style="font-size:12px;font-weight:700;color:#f1f5f9;margin-bottom:12px;
           text-transform:uppercase;letter-spacing:.05em">Culture DNA</div>
      {culture_list}
    </div>

    <!-- Hidden Requirements -->
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;
         padding:20px;margin-bottom:16px">
      <div style="font-size:12px;font-weight:700;color:#f1f5f9;margin-bottom:12px;
           text-transform:uppercase;letter-spacing:.05em">Hidden Requirements</div>
      {"".join([f'<div style="font-size:12px;color:#94a3b8;padding:6px 0;border-bottom:1px solid #1e293b">→ {h.replace("_"," ").title()}</div>' for h in job_analysis.get("hidden_requirements",[])])}
    </div>

    <!-- Score Legend -->
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:20px">
      <div style="font-size:12px;font-weight:700;color:#f1f5f9;margin-bottom:12px;
           text-transform:uppercase;letter-spacing:.05em">Scoring Model</div>
      {"".join([f'''
      <div style="display:flex;justify-content:space-between;align-items:center;
           padding:5px 0;border-bottom:1px solid #1e293b">
        <span style="font-size:11px;color:#94a3b8">{n}</span>
        <span style="font-size:11px;font-weight:600;color:{c}">{w}</span>
      </div>''' for n, w, c in [
          ("Technical Match","30%","#0d9488"),("Semantic Fit","20%","#0284c7"),
          ("Experience Quality","20%","#7c3aed"),("Behavioral Signals","15%","#d97706"),
          ("Culture Fit","10%","#f43f5e"),("Growth Trajectory","5%","#8b5cf6"),
      ]])}
    </div>

  </div>
</div>

<div style="text-align:center;padding:24px;color:#1e293b;font-size:11px;border-top:1px solid #0f172a">
  NEXUS AI Recruiter · Semantic Intelligence Platform · {datetime.now().year}
</div>

</body>
</html>'''


# ============================================================
# MAIN
# ============================================================

class NexusAIRecruiter:
    def __init__(self):
        self.se = SemanticKnowledgeEngine()
        self.jda = JobDescriptionAnalyzer(self.se)
        self.pb = CandidateProfileBuilder(self.se)
        self.scoring = MultiSignalScoringEngine(self.se)
        self.ranking = IntelligentRankingEngine()

    def run(self, jd, title, candidates, top_k=10):
        t0 = time.time()
        print(f"\n  Analyzing job: {title}")
        ja = self.jda.analyze(jd, title)
        print(f"  Building {len(candidates)} candidate profiles...")
        profiles = [self.pb.build_profile(c) for c in candidates]
        print(f"  Scoring across 6 dimensions...")
        scored = [self.scoring.score_candidate(p, ja) for p in profiles]
        ranked = self.ranking.rank(scored, top_k)
        t1 = time.time()
        print(f"  Done in {t1-t0:.2f}s\n")
        return ranked, ja, t1-t0


def main():
    print("\n" + "═"*50)
    print("  NEXUS AI RECRUITER")
    print("  Professional Intelligence Platform")
    print("═"*50)

    recruiter = NexusAIRecruiter()
    jd, title = get_job()
    candidates = get_candidates()

    results, job_analysis, proc_time = recruiter.run(jd, title, candidates, top_k=10)

    print("  Top Candidates:")
    for r in results:
        c = next(x for x in candidates if x["id"] == r.candidate_id)
        print(f"  #{r.rank} {c['name']:<22} {r.total_score:5.1f}/100  {r.hire_recommendation}")

    html = generate_html(results, candidates, job_analysis, proc_time)

    with open("nexus_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\n  Report saved: nexus_report.html")
    print("  Opening in browser...")

    webbrowser.open("nexus_report.html")
    print("\n" + "═"*50)


if __name__ == "__main__":
    main()