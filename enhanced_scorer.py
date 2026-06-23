import profile

import numpy as np
from typing import Dict, Tuple, List
from datetime import datetime
import re

class EnhancedCandidateScorer:
    def __init__(self, jd_parser):
        self.jd_parser = jd_parser
        self.jd_analysis = None
        
        # Consulting firms for detection
        self.consulting_firms = {
            'tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini',
            'hcl', 'tech mahindra', 'mindtree', 'lti', 'mphasis', 'hexaware',
            'genpact', 'deloitte', 'pwc', 'ey', 'kpmg'
        }
        
        # Non-tech titles for trap detection
        self.non_tech_titles = {
            'accountant', 'hr manager', 'hr generalist', 'sales executive',
            'sales manager', 'graphic designer', 'ui designer', 'ux designer',
            'civil engineer', 'mechanical engineer', 'electrical engineer',
            'operations manager', 'customer support', 'marketing manager',
            'content writer', 'project manager', 'business analyst'
        }
        
        # Impact keywords
        self.impact_keywords = [
            'improved', 'increased', 'reduced', 'delivered', 'launched',
            'shipped', 'led', 'built', 'created', 'optimized', 'designed',
            'architected', 'implemented', 'developed', 'scaled', 'deployed'
        ]
        
    def set_jd(self, jd_text: str):
        """Set job description and parse it"""
        self.jd_analysis = self.jd_parser.parse(jd_text)
        
    def score_candidate(self, candidate: Dict) -> Tuple[float, Dict]:
        """Score candidate with all components"""
        components = {}
        
        # 1. Skill Match (25%)
        components['skill_match'] = self._score_skills(candidate)
        
        # 2. Title/Headline Match (18%)
        components['title_match'] = self._score_title_match(candidate)
        
        # 3. Experience Quality (15%)
        components['experience_quality'] = self._score_experience_quality(candidate)
        
        # 4. Career Trajectory (12%)
        components['career_trajectory'] = self._score_career_trajectory(candidate)
        
        # 5. Behavioral Signals (15%)
        components['behavioral'] = self._score_behavioral(candidate)
        
        # 6. Education (5%)
        components['education'] = self._score_education(candidate)
        
        # 7. Location/Culture Fit (5%)
        components['location_fit'] = self._score_location(candidate)
        
        # 8. Honeypot Detection (5%)
        components['honeypot_risk'] = self._score_honeypot_risk(candidate)
        
        # Weighted combination
        weights = {
            'skill_match': 0.25,
            'title_match': 0.18,
            'experience_quality': 0.15,
            'career_trajectory': 0.12,
            'behavioral': 0.15,
            'education': 0.05,
            'location_fit': 0.05,
            'honeypot_risk': 0.05,
        }
        
        # Weighted combination
        final_score = sum(
            weights[k] * components.get(k, 0)
            for k in weights
        )

        final_score = max(0, min(1, final_score))

        return final_score, components

    def _score_skills(self, candidate: Dict) -> float:
        """Score candidate skills against JD requirements"""
        if not self.jd_analysis:
            return 0.5
        
        required_skills = self.jd_analysis.get('required_skills', {})
        if not required_skills:
            return 0.5
        
        candidate_skills = set()
        skill_details = {}
        
        for skill in candidate.get('skills', []):
            name = skill.get('name', '').lower()
            candidate_skills.add(name)
            # Add variations
            candidate_skills.add(name.replace(' ', '_'))
            candidate_skills.add(name.replace(' ', ''))
            
            # Store proficiency
            proficiency = skill.get('proficiency', '')
            proficiency_weights = {'expert': 1.0, 'advanced': 0.8, 
                                  'intermediate': 0.5, 'beginner': 0.3}
            skill_details[name] = proficiency_weights.get(proficiency, 0.5)
        
        total_importance = 0
        matched_importance = 0
        proficiency_score = 0
        
        for skill, info in required_skills.items():
            importance = info.get('importance', 0.5)
            total_importance += importance
            
            # Direct match
            if skill in candidate_skills:
                matched_importance += importance
                proficiency_score += importance * skill_details.get(skill, 0.5)
                continue
            
            # Check synonyms
            synonyms = info.get('synonyms', [])
            matched_synonym = None
            for syn in synonyms:
                syn_lower = syn.lower()
                if syn_lower in candidate_skills:
                    matched_synonym = syn_lower
                    break
            
            if matched_synonym:
                matched_importance += importance * 0.8
                proficiency_score += importance * 0.8 * skill_details.get(matched_synonym, 0.5)
        
        if total_importance == 0:
            return 0.5
        
        match_score = matched_importance / total_importance
        prof_score = proficiency_score / max(total_importance, 0.01)
        
        # Combine match and proficiency
        return 0.6 * match_score + 0.4 * min(prof_score, 1.0)
    
    def _score_title_match(self, candidate: Dict) -> float:
    
        profile = candidate.get('profile', {})

        title = profile.get(
            'current_title',
            ''
        ).lower()

        headline = profile.get(
            'headline',
            ''
        ).lower()

        combined = f"{title} {headline}"

        if not combined.strip():
            return 0.0

        # Hard negative titles (likely irrelevant to AI Retrieval role)
        non_ai_titles = [
            'hr',
            'human resources',
            'recruiter',
            'talent acquisition',
            'civil engineer',
            'mechanical engineer',
            'electrical engineer',
            'sales',
            'marketing',
            'accountant',
            'finance',
            'operations manager'
        ]

        if any(
            t in combined
            for t in non_ai_titles
        ):
            return 0.0

        # AI/ML title weights
        ai_keywords = {
            'ml engineer': 1.0,
            'machine learning': 1.0,
            'ai engineer': 1.0,
            'search engineer': 1.0,
            'ranking engineer': 1.0,
            'recommendation': 1.0,
            'nlp engineer': 0.9,
            'applied scientist': 0.9,
            'data scientist': 0.8,
            'data engineer': 0.8,
            'backend engineer': 0.7,
            'software engineer': 0.6,
            'full stack': 0.5
        }

        title_score = 0.0

        for keyword, weight in ai_keywords.items():
            if keyword in combined:
                title_score = max(
                    title_score,
                    weight
                )

        # Bonus for JD-required skills appearing in title/headline
        if self.jd_analysis:

            required_skills = self.jd_analysis.get(
                'required_skills',
                {}
            )

            skill_hits = sum(
                1
                for skill in required_skills
                if skill in combined
          )

            if required_skills:
                title_score = max(
                    title_score,
                    0.3 + 0.7 * (
                        skill_hits /
                        len(required_skills)
                    )
                )

        return min(title_score, 1.0)

    def _score_experience_quality(self, candidate: Dict) -> float:
        """Score quality of experience"""
        career_history = candidate.get('career_history', [])
        
        if not career_history:
            return 0.0
        
        # Check for product company experience
        product_months = 0
        consulting_months = 0
        total_months = 0
        leadership_count = 0
        
        for job in career_history:
            company = job.get('company', '').lower()
            duration = job.get('duration_months', 0)
            title = job.get('title', '').lower()
            desc = job.get('description', '').lower()
            
            total_months += duration
            
            
            # Better consulting company detection
            is_consulting = any(
                firm.lower() in company
                for firm in self.consulting_firms
            )

            if is_consulting:
                consulting_months += duration
            else:
                product_months += duration
            
            # Leadership signals
            if any(word in title for word in ['lead', 'senior', 'staff', 'principal', 'manager']):
                leadership_count += 1
            
            # Impact statements
            if any(kw in desc for kw in self.impact_keywords):
                leadership_count += 0.5
        
        if total_months == 0:
            return 0.0
        
        product_ratio = product_months / total_months
        leadership_score = min(leadership_count / 3, 1.0)
        
        # If all consulting, penalty
        if consulting_months > 0 and product_months == 0:
            product_ratio = 0.2
        
        # Check for AI-related experience
        ai_experience = 0
        for job in career_history:
            desc = job.get('description', '').lower()
            if any(kw in desc for kw in ['machine learning', 'ai', 'nlp', 'retrieval', 'ranking']):
                ai_experience += job.get('duration_months', 0)
        
        ai_ratio = min(ai_experience / max(total_months, 1), 1.0)
        
        return 0.35 * product_ratio + 0.35 * leadership_score + 0.3 * ai_ratio
    
    def _score_career_trajectory(self, candidate: Dict) -> float:
        """Score career progression and growth"""
        career_history = candidate.get('career_history', [])
        
        if len(career_history) < 2:
            return 0.5
        
        # Check for promotions
        titles = [job.get('title', '').lower() for job in career_history]
        seniority_levels = ['intern', 'junior', 'associate', 'engineer', 
                           'senior', 'lead', 'staff', 'principal']
        
        level_scores = []
        for title in titles:
            level = 0
            for i, word in enumerate(seniority_levels):
                if word in title:
                    level = max(level, i)
            level_scores.append(level)
        
        # Progression
        if len(level_scores) >= 2:
            progression = sum(1 for i in range(1, len(level_scores)) 
                            if level_scores[i] > level_scores[i-1])
            progression_ratio = progression / (len(level_scores) - 1)
        else:
            progression_ratio = 0.5
        
        # Tenure analysis
        tenures = [job.get('duration_months', 0) for job in career_history]
        avg_tenure = sum(tenures) / len(tenures) if tenures else 0
        
        # Prefer 18-36 months, penalize < 12 months
        if avg_tenure >= 36:
            tenure_score = 0.7
        elif avg_tenure >= 18:
            tenure_score = 1.0
        elif avg_tenure >= 12:
            tenure_score = 0.6
        else:
            tenure_score = 0.3
        
        # Check for growth in company size
        company_sizes = [job.get('company_size', '') for job in career_history]
        size_weights = {
            '1-10': 1, '11-50': 2, '51-200': 3, '201-500': 4,
            '501-1000': 5, '1001-5000': 6, '5001-10000': 7, '10001+': 8
        }
        
        size_growth = 0
        if len(company_sizes) >= 2:
            prev_size = size_weights.get(company_sizes[0], 0)
            for size in company_sizes[1:]:
                curr_size = size_weights.get(size, 0)
                if curr_size > prev_size:
                    size_growth += 1
                prev_size = curr_size
            size_growth_ratio = size_growth / (len(company_sizes) - 1)
        else:
            size_growth_ratio = 0.5
        
        return 0.5 * progression_ratio + 0.3 * tenure_score + 0.2 * size_growth_ratio
    
    def _score_behavioral(self, candidate: Dict) -> float:
        """Enhanced behavioral scoring with all signals"""
        signals = candidate.get('redrob_signals', {})
        score = 0.0
        details = {}
        
        # 1. Recruiter Response Rate (25%)
        response_rate = signals.get('recruiter_response_rate', 0)
        details['response_rate'] = response_rate
        score += 0.25 * response_rate
        
        # 2. Interview Completion Rate (20%)
        interview_rate = signals.get('interview_completion_rate', 0)
        if interview_rate >= 0:
            details['interview_rate'] = interview_rate
            score += 0.20 * interview_rate
        
        # 3. Open to Work (15%)
        if signals.get('open_to_work_flag', False):
            details['open_to_work'] = True
            score += 0.15
        
        # 4. Recent Activity (15%)
        last_active = signals.get('last_active_date')
        if last_active:
            try:
                last_date = datetime.strptime(last_active, '%Y-%m-%d')
                days_inactive = (datetime.now() - last_date).days
                if days_inactive < 7:
                    score += 0.15
                    details['activity'] = 'very_recent'
                elif days_inactive < 30:
                    score += 0.12
                    details['activity'] = 'recent'
                elif days_inactive < 90:
                    score += 0.08
                    details['activity'] = 'moderate'
                elif days_inactive < 180:
                    score += 0.04
                    details['activity'] = 'stale'
                else:
                    details['activity'] = 'inactive'
            except:
                pass
        
        # 5. Profile Completeness (10%)
        completeness = signals.get('profile_completeness_score', 0)
        details['completeness'] = completeness
        score += 0.10 * (completeness / 100)
        
        # 6. GitHub Activity (10%)
        github_score = signals.get('github_activity_score', -1)
        if github_score >= 0:
            details['github'] = github_score
            score += 0.10 * (github_score / 100)
        else:
            score += 0.02  # No GitHub not a penalty
        
        # 7. Recruiter Saves (5%)
        saves = signals.get('saved_by_recruiters_30d', 0)
        details['saves'] = saves
        score += 0.05 * min(saves / 20, 1.0)
        
        return min(score, 1.0)
    
    def _score_education(self, candidate: Dict) -> float:
        """Score education with tier and relevance"""
        education = candidate.get('education', [])
        
        if not education:
            return 0.3
        
        tier_weights = {
            'tier_1': 1.0, 'tier_2': 0.8, 'tier_3': 0.5, 'tier_4': 0.3, 'unknown': 0.4
        }
        
        best_tier = 0.3
        relevant_fields = ['computer science', 'data science', 'machine learning',
                          'artificial intelligence', 'statistics', 'mathematics',
                          'information technology', 'software engineering']
        
        field_match = 0
        highest_degree = ''
        
        for edu in education:
            tier = edu.get('tier', 'unknown')
            best_tier = max(best_tier, tier_weights.get(tier, 0.3))
            
            field = edu.get('field_of_study', '').lower()
            if any(rf in field for rf in relevant_fields):
                field_match = 1.0
            
            degree = edu.get('degree', '').lower()
            if 'phd' in degree or 'ph.d' in degree:
                highest_degree = 'phd'
            elif 'master' in degree or 'm.s' in degree or 'm.tech' in degree:
                if highest_degree == '':
                    highest_degree = 'master'
            elif 'bachelor' in degree or 'b.tech' in degree or 'b.e' in degree:
                if highest_degree == '':
                    highest_degree = 'bachelor'
        
        degree_weights = {'phd': 1.0, 'master': 0.9, 'bachelor': 0.7}
        degree_score = degree_weights.get(highest_degree, 0.5)
        
        return 0.4 * best_tier + 0.3 * field_match + 0.3 * degree_score
    
    def _score_location(self, candidate: Dict) -> float:
        """Score location fit"""
        profile = candidate.get('profile', {})
        country = profile.get('country', '').lower()
        location = profile.get('location', '').lower()
        
        if not self.jd_analysis:
            return 0.5
        
        jd_locations = self.jd_analysis.get('locations', [])
        
        # Check for India preference
        if 'india' in country:
            # Check specific cities
            for loc in jd_locations:
                if loc.lower() in location:
                    return 1.0
            # In India but not preferred city
            return 0.7
        else:
            # Outside India
            return 0.3
    
    def _score_honeypot_risk(self, candidate: Dict) -> float:
        """Comprehensive honeypot detection"""
        risk = 0.0
        details = []
        
        skills = candidate.get('skills', [])
        profile = candidate.get('profile', {})
        
        # 1. Expert skills without duration
        expert_skills = [s for s in skills if s.get('proficiency') == 'expert']
        
        for skill in expert_skills:
            duration = skill.get('duration_months', 0)
            if duration < 12:
                risk += 0.08
                details.append(f"expert in {skill.get('name')} with only {duration}m")
        
        if len(expert_skills) > 6:
            risk += 0.15
            details.append(f"{len(expert_skills)} expert skills")
        
        # 2. Non-tech title with heavy AI skills
        title = profile.get('current_title', '').lower()
        if any(nt in title for nt in self.non_tech_titles):
            ai_skills = sum(1 for s in skills 
                          if s.get('name', '').lower() in 
                          {'llm', 'pytorch', 'tensorflow', 'nlp', 'embeddings', 
                           'rag', 'faiss', 'pinecone', 'qdrant'})
            if ai_skills >= 4:
                risk += 0.25
                details.append(f"non-tech title with {ai_skills} AI skills")
        
        # 3. Suspicious company names
        for job in candidate.get('career_history', []):
            company = job.get('company', '').lower()
            if company in {'wayne enterprises', 'stark industries', 'hooli', 
                          'pied piper', 'dunder mifflin', 'globe inc'}:
                risk += 0.05
                details.append(f"suspicious company: {company}")
        
        # 4. Inconsistent experience
        total_experience = profile.get('years_of_experience', 0)
        career_months = sum(job.get('duration_months', 0) 
                           for job in candidate.get('career_history', []))
        
        if career_months > 0 and abs(total_experience * 12 - career_months) > 24:
            risk += 0.1
            details.append("experience inconsistency")
        
        # 5. Too many skills
        if len(skills) > 20:
            risk += 0.05
            details.append(f"{len(skills)} skills (too many)")
        
        return min(risk, 1.0)