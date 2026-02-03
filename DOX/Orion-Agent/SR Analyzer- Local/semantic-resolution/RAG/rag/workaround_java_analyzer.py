"""
Workaround-Based Java Error Detection
Analyzes categories and workaround content from similar SRs to determine if issue is Java-related
"""

import re
from typing import Dict, List, Tuple


class WorkaroundJavaAnalyzer:
    """
    Analyzes workarounds and categories from similar SRs to detect Java errors
    Simple, content-based approach (no complex scoring)
    """
    
    def __init__(self):
        self.java_indicators = [
            # Java classes
            r'\b[A-Z][a-zA-Z0-9]*(Service|Controller|Repository|Manager|Handler|Impl|Processor)\b',
            # Java exceptions
            r'(Exception|Error)(?!\s*:)',
            r'NullPointerException|SQLException|IOException|ClassNotFoundException',
            # Java packages
            r'com\.[a-z]+\.[a-z]+',
            r'org\.amdocs',
            r'com\.amdocs',
            r'com\.comcast',
            # Java files
            r'\.java\b',
            # Java commands
            r'mvn\s+(clean\s+)?install',
            r'restart\s+(tomcat|jboss|wildfly)',
            r'systemctl\s+restart',
            # Java tools
            r'\b(jstack|jmap|jconsole|jvisualvm|catalina)\b',
            # Stack traces
            r'at\s+com\.',
            r'at\s+org\.',
            r'at\s+java\.',
        ]
        
        self.java_categories = [
            'code', 'backend', 'application error', 'system error',
            'backend error', 'service failure', 'application'
        ]
        
        self.non_java_categories = [
            'data', 'interface', 'configuration', 'network',
            'frontend', 'user error', 'ui', 'web', 'crm'
        ]
        
        self.customer_issue_indicators = [
            'midmarket customer issue',
            'third party issue',
            'customer issue',
            'third-party'
        ]
        
        self.amdocs_issue_indicators = [
            'midmarket amdocs issue',
            'internal amdocs issue',
            'amdocs issue'
        ]
    
    def analyze(self, sr_data: Dict, similar_srs: List[Dict]) -> Dict:
        """
        Analyze if SR is a Java error based on workaround content and categories
        
        Args:
            sr_data: Current SR data (Description, Notes, Resolution Category, etc.)
            similar_srs: List of similar historical SRs with workarounds
        
        Returns:
            {
                'is_java_error': bool,
                'confidence': str (HIGH/MEDIUM/LOW),
                'category_analysis': dict,
                'workaround_analysis': dict,
                'evidence': list,
                'issue_type': str
            }
        """
        evidence = []
        
        # STEP 1: Analyze Categories
        category_result = self._analyze_categories(similar_srs, sr_data)
        evidence.extend(category_result['evidence'])
        
        # STEP 2: Analyze Semantic Workaround
        semantic_result = self._analyze_semantic_workaround(
            sr_data.get('Semantic Workaround', '')
        )
        evidence.extend(semantic_result['evidence'])
        
        # STEP 3: Analyze AI Workarounds from similar SRs
        ai_result = self._analyze_ai_workarounds(similar_srs)
        evidence.extend(ai_result['evidence'])
        
        # STEP 4: Analyze User Workarounds from similar SRs
        user_result = self._analyze_user_workarounds(similar_srs)
        evidence.extend(user_result['evidence'])
        
        # STEP 5: Analyze Current SR Description/Notes
        current_sr_result = self._analyze_current_sr(sr_data)
        evidence.extend(current_sr_result['evidence'])
        
        # DECISION LOGIC
        votes = {
            'category': category_result['vote'],
            'semantic': semantic_result['vote'],
            'ai_workarounds': ai_result['vote'],
            'user_workarounds': user_result['vote'],
            'current_sr': current_sr_result['vote']
        }
        
        java_votes = sum(1 for v in votes.values() if v == 'JAVA')
        non_java_votes = sum(1 for v in votes.values() if v == 'NON_JAVA')
        unknown_votes = sum(1 for v in votes.values() if v == 'UNKNOWN')
        
        is_java_error = java_votes > non_java_votes
        
        # 🆕 ADAPTIVE CONFIDENCE: Based on ratio of meaningful votes (exclude UNKNOWN)
        meaningful_votes = java_votes + non_java_votes
        total_votes = len(votes)
        
        if meaningful_votes > 0:
            # 🔧 FIX: Calculate confidence based on WINNING side, not always Java
            if is_java_error:
                winning_ratio = java_votes / meaningful_votes
            else:
                winning_ratio = non_java_votes / meaningful_votes
            
            # Confidence based on:
            # 1. Ratio of winning votes among meaningful voters
            # 2. Number of meaningful voters (more = more reliable)
            
            if winning_ratio >= 0.8 and meaningful_votes >= 3:
                confidence = 'HIGH'  # 80%+ agreement with 3+ voters
            elif winning_ratio >= 0.67 and meaningful_votes >= 3:
                confidence = 'MEDIUM'  # 67%+ agreement with 3+ voters
            elif winning_ratio >= 0.6 or (winning_ratio >= 0.5 and meaningful_votes >= 4):
                confidence = 'LOW'  # 60%+ agreement OR 50%+ with 4+ voters
            else:
                confidence = 'VERY_LOW'  # < 60% agreement
            
            confidence_metadata = {
                'winning_ratio': f"{winning_ratio:.1%}",
                'java_votes': java_votes,
                'non_java_votes': non_java_votes,
                'meaningful_votes': meaningful_votes,
                'total_votes': total_votes,
                'unknown_votes': unknown_votes
            }
        else:
            # No meaningful votes available
            confidence = 'UNKNOWN'
            confidence_metadata = {
                'java_ratio': '0.0%',
                'meaningful_votes': 0,
                'total_votes': total_votes,
                'unknown_votes': unknown_votes
            }
        
        # Determine issue type
        if not is_java_error:
            issue_type = category_result.get('suggested_type', 'Data/Interface/Configuration')
        else:
            issue_type = 'Java/Code'
        
        return {
            'is_java_error': is_java_error,
            'confidence': confidence,
            'confidence_metadata': confidence_metadata,
            'votes': votes,
            'java_votes': java_votes,
            'non_java_votes': non_java_votes,
            'unknown_votes': unknown_votes,
            'meaningful_votes': meaningful_votes,
            'category_analysis': category_result,
            'semantic_analysis': semantic_result,
            'ai_workaround_analysis': ai_result,
            'user_workaround_analysis': user_result,
            'current_sr_analysis': current_sr_result,
            'evidence': evidence,
            'issue_type': issue_type
        }
    
    def _analyze_categories(self, similar_srs: List[Dict], sr_data: Dict) -> Dict:
        """Analyze categories from similar SRs with weighted scoring"""
        evidence = []
        java_score = 0.0  # Changed to float for fractional scoring
        non_java_score = 0.0
        customer_issue_count = 0
        amdocs_issue_count = 0
        
        for sr in similar_srs:
            # Resolution Category
            res_cat = str(sr.get('resolution_category', '')).lower()
            
            # SLA Resolution Categorization T1 (if available)
            sla_t1 = str(sr.get('sla_resolution_categorization_t1', '')).lower()
            
            # Check SLA T1 first (strong indicator)
            if any(ind in sla_t1 for ind in self.customer_issue_indicators):
                customer_issue_count += 1
                evidence.append(f"✗ SR {sr.get('sr_id')}: SLA T1 = Customer/Third-Party Issue")
            elif any(ind in sla_t1 for ind in self.amdocs_issue_indicators):
                amdocs_issue_count += 1
                evidence.append(f"✓ SR {sr.get('sr_id')}: SLA T1 = Amdocs Internal Issue")
            
            # 🆕 WEIGHTED CATEGORY SCORING: Analyze each category part separately
            if res_cat and res_cat not in ['nan', 'none', '']:
                category_parts = [part.strip() for part in res_cat.split('|')]
                java_parts = 0
                non_java_parts = 0
                
                for part in category_parts:
                    if any(cat in part for cat in self.java_categories):
                        java_parts += 1
                    elif any(cat in part for cat in self.non_java_categories):
                        non_java_parts += 1
                
                total_parts = java_parts + non_java_parts
                if total_parts > 0:
                    # Fractional scoring based on ratio
                    java_weight = java_parts / total_parts
                    non_java_weight = non_java_parts / total_parts
                    
                    java_score += java_weight
                    non_java_score += non_java_weight
                    
                    if java_weight > 0 and non_java_weight > 0:
                        # Mixed category
                        evidence.append(f"⚖️ SR {sr.get('sr_id')}: Category = '{res_cat}' (Mixed: {java_parts} Java, {non_java_parts} Non-Java → +{java_weight:.2f} Java, +{non_java_weight:.2f} Non-Java)")
                    elif java_weight > 0:
                        evidence.append(f"✓ SR {sr.get('sr_id')}: Category = '{res_cat}' (Java-related → +{java_weight:.2f})")
                    else:
                        evidence.append(f"✗ SR {sr.get('sr_id')}: Category = '{res_cat}' (Non-Java → +{non_java_weight:.2f})")
        
        # 🆕 Input SR category with weighted scoring
        input_category = str(sr_data.get('Resolution Category', '')).lower()
        if input_category and input_category not in ['nan', 'none', '']:
            category_parts = [part.strip() for part in input_category.split('|')]
            java_parts = 0
            non_java_parts = 0
            
            for part in category_parts:
                if any(cat in part for cat in self.java_categories):
                    java_parts += 1
                elif any(cat in part for cat in self.non_java_categories):
                    non_java_parts += 1
            
            total_parts = java_parts + non_java_parts
            if total_parts > 0:
                java_weight = java_parts / total_parts
                non_java_weight = non_java_parts / total_parts
                
                java_score += java_weight
                non_java_score += non_java_weight
                
                if java_weight > 0 and non_java_weight > 0:
                    evidence.append(f"⚖️ Input SR: Category = '{input_category}' (Mixed: {java_parts} Java, {non_java_parts} Non-Java → +{java_weight:.2f} Java, +{non_java_weight:.2f} Non-Java)")
                elif java_weight > 0:
                    evidence.append(f"✓ Input SR: Category = '{input_category}' (Java-related → +{java_weight:.2f})")
                else:
                    evidence.append(f"✗ Input SR: Category = '{input_category}' (Non-Java → +{non_java_weight:.2f})")
        
        # Vote based on weighted scores
        if customer_issue_count > amdocs_issue_count and customer_issue_count > 0:
            vote = 'NON_JAVA'
            evidence.append(f"⚖️ Category Vote: NON-JAVA (Customer/Third-Party issue - {customer_issue_count} indicators)")
        elif java_score > non_java_score:
            vote = 'JAVA'
            evidence.append(f"⚖️ Category Vote: JAVA (score: {java_score:.2f} Java vs {non_java_score:.2f} non-Java)")
        elif non_java_score > java_score:
            vote = 'NON_JAVA'
            evidence.append(f"⚖️ Category Vote: NON-JAVA (score: {non_java_score:.2f} non-Java vs {java_score:.2f} Java)")
        else:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ Category Vote: UNKNOWN (insufficient category data)")
        
        return {
            'vote': vote,
            'java_score': java_score,  # Changed from java_count
            'non_java_score': non_java_score,  # Changed from non_java_count
            'customer_issue_count': customer_issue_count,
            'amdocs_issue_count': amdocs_issue_count,
            'evidence': evidence,
            'suggested_type': self._suggest_issue_type(similar_srs)
        }
    
    def _analyze_semantic_workaround(self, semantic_text: str) -> Dict:
        """Analyze semantic workaround content"""
        evidence = []
        
        if not semantic_text or str(semantic_text).lower() in ['not available', 'nan', 'none', '']:
            evidence.append("⚠️ No semantic workaround provided")
            return {'vote': 'UNKNOWN', 'evidence': evidence, 'java_indicators_found': 0}
        
        java_indicators_found = 0
        found_patterns = []
        
        for pattern in self.java_indicators:
            matches = re.findall(pattern, semantic_text, re.IGNORECASE)
            if matches:
                java_indicators_found += len(matches)
                found_patterns.append(matches[0] if len(matches) == 1 else f"{matches[0]}...")
        
        if found_patterns:
            evidence.append(f"✓ Semantic WA: Found Java indicators: {', '.join(found_patterns[:3])}")
        
        if java_indicators_found >= 3:
            vote = 'JAVA'
            evidence.append(f"⚖️ Semantic WA Vote: JAVA ({java_indicators_found} Java indicators found)")
        elif java_indicators_found > 0:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ Semantic WA Vote: UNKNOWN ({java_indicators_found} weak Java indicators)")
        else:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ Semantic WA Vote: UNKNOWN (No Java indicators found - insufficient data)")
        
        return {'vote': vote, 'evidence': evidence, 'java_indicators_found': java_indicators_found}
    
    def _analyze_ai_workarounds(self, similar_srs: List[Dict]) -> Dict:
        """Analyze AI workarounds from similar SRs"""
        evidence = []
        total_indicators = 0
        srs_with_indicators = 0
        
        for sr in similar_srs:
            workaround = str(sr.get('workaround', ''))
            if 'AI Generated:' in workaround:
                ai_part = workaround.split('AI Generated:')[1]
                indicators = sum(1 for pattern in self.java_indicators 
                               if re.search(pattern, ai_part, re.IGNORECASE))
                if indicators > 0:
                    total_indicators += indicators
                    srs_with_indicators += 1
                    evidence.append(f"✓ SR {sr.get('sr_id')}: AI WA has {indicators} Java indicators")
        
        if srs_with_indicators >= 3:
            vote = 'JAVA'
            evidence.append(f"⚖️ AI WA Vote: JAVA ({srs_with_indicators}/{len(similar_srs)} SRs with Java)")
        elif srs_with_indicators >= 1:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ AI WA Vote: UNKNOWN ({srs_with_indicators} SRs with weak Java signs)")
        else:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ AI WA Vote: UNKNOWN (No Java in AI workarounds - insufficient data)")
        
        return {'vote': vote, 'evidence': evidence, 'srs_with_indicators': srs_with_indicators, 'total_indicators': total_indicators}
    
    def _analyze_user_workarounds(self, similar_srs: List[Dict]) -> Dict:
        """Analyze user workarounds from similar SRs"""
        evidence = []
        total_indicators = 0
        srs_with_indicators = 0
        
        for sr in similar_srs:
            workaround = str(sr.get('workaround', ''))
            if 'Workaround:' in workaround:
                user_part = workaround.split('Workaround:')[1].split('AI Generated:')[0] if 'AI Generated:' in workaround else workaround.split('Workaround:')[1]
                indicators = sum(1 for pattern in self.java_indicators 
                               if re.search(pattern, user_part, re.IGNORECASE))
                if indicators > 0:
                    total_indicators += indicators
                    srs_with_indicators += 1
                    evidence.append(f"✓ SR {sr.get('sr_id')}: User WA has {indicators} Java indicators")
        
        if srs_with_indicators >= 3:
            vote = 'JAVA'
            evidence.append(f"⚖️ User WA Vote: JAVA ({srs_with_indicators}/{len(similar_srs)} SRs with Java)")
        elif srs_with_indicators >= 1:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ User WA Vote: UNKNOWN ({srs_with_indicators} SRs with weak Java signs)")
        else:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ User WA Vote: UNKNOWN (No Java in user workarounds - insufficient data)")
        
        return {'vote': vote, 'evidence': evidence, 'srs_with_indicators': srs_with_indicators, 'total_indicators': total_indicators}
    
    def _analyze_current_sr(self, sr_data: Dict) -> Dict:
        """Analyze current SR description and notes"""
        evidence = []
        text = f"{sr_data.get('Description', '')} {sr_data.get('Notes', '')}"
        
        indicators_found = 0
        found_patterns = []
        
        for pattern in self.java_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators_found += len(matches)
                found_patterns.append(matches[0] if len(matches) == 1 else f"{matches[0]}...")
        
        if found_patterns:
            evidence.append(f"✓ Current SR: Found {', '.join(found_patterns[:3])}")
        
        if indicators_found >= 2:
            vote = 'JAVA'
            evidence.append(f"⚖️ Current SR Vote: JAVA ({indicators_found} Java indicators in description/notes)")
        elif indicators_found == 1:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ Current SR Vote: UNKNOWN ({indicators_found} weak Java indicator)")
        else:
            vote = 'UNKNOWN'
            evidence.append(f"⚖️ Current SR Vote: UNKNOWN (No Java indicators - insufficient data)")
        
        return {'vote': vote, 'evidence': evidence, 'indicators_found': indicators_found}
    
    def _suggest_issue_type(self, similar_srs: List[Dict]) -> str:
        """Suggest issue type based on categories"""
        type_counts = {}
        for sr in similar_srs:
            cat = str(sr.get('resolution_category', '')).lower()
            for non_java_type in self.non_java_categories:
                if non_java_type in cat:
                    type_counts[non_java_type] = type_counts.get(non_java_type, 0) + 1
        
        if type_counts:
            most_common = max(type_counts, key=type_counts.get)
            return most_common.title()
        return 'Unknown'
    
    def extract_activity_names(self, sr_data: Dict, similar_srs: List[Dict]) -> List[str]:
        """Extract activity names from SR and similar workarounds"""
        activity_names = []
        
        # Common activity name patterns
        activity_patterns = [
            r'\b([A-Z][a-zA-Z]+(?:Address|Order|Customer|Account|Service|Payment|Validation|Process|Create|Update|Delete|Validate)[A-Z][a-zA-Z]*)\b',
            r'activity[:\s]+([A-Z][a-zA-Z]+)',
            r'Activity:\s*([A-Z][a-zA-Z]+)',
        ]
        
        # Search in current SR
        text = f"{sr_data.get('Description', '')} {sr_data.get('Notes', '')}"
        for pattern in activity_patterns:
            matches = re.findall(pattern, text)
            activity_names.extend(matches)
        
        # Search in semantic workaround
        semantic = sr_data.get('Semantic Workaround', '')
        if semantic:
            for pattern in activity_patterns:
                matches = re.findall(pattern, semantic)
                activity_names.extend(matches)
        
        # Search in similar SRs workarounds
        for sr in similar_srs[:3]:  # Top 3 similar
            workaround = sr.get('workaround', '')
            for pattern in activity_patterns:
                matches = re.findall(pattern, workaround)
                activity_names.extend(matches)
        
        # Remove duplicates and return
        return list(set(activity_names))

