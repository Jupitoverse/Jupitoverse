"""
Intelligent Java Error Detection System
Multi-Signal Scoring Approach for Accurate Java Error Identification

Uses 5 signals:
1. Explicit Indicators (0-30 points) - Stack traces, exceptions in CURRENT SR
2. Semantic Code Match (0-25 points) - Similarity with actual Java code from comcast_code.db
3. Historical Pattern (0-20 points) - Resolution categories from SIMILAR SRs
4. Resolution Metadata (0-15 points) - Categories + Status Reason from SIMILAR SRs
5. Workaround Analysis (0-10 points) - Java commands/classes in SIMILAR SRs' workarounds

Total: 0-100 points
Threshold: 70+ = Java Error, 50-69 = Probable, <50 = Not Java
"""

import re
from typing import Dict, List, Tuple


class IntelligentJavaErrorDetector:
    """
    Multi-signal Java error detection using intelligent scoring
    NOT just keyword matching - uses contextual analysis
    """
    
    def __init__(self):
        self.evidence = []
        
        # Java exception patterns with required context words
        self.exception_patterns = {
            'NullPointerException': ['null', 'object', 'reference', 'pointer'],
            'SQLException': ['database', 'query', 'sql', 'connection', 'jdbc'],
            'IOException': ['file', 'stream', 'read', 'write', 'input', 'output'],
            'ClassNotFoundException': ['class', 'load', 'jar', 'classpath'],
            'OutOfMemoryError': ['memory', 'heap', 'oom', 'space'],
            'IllegalArgumentException': ['argument', 'parameter', 'invalid'],
            'ConcurrentModificationException': ['thread', 'concurrent', 'iteration'],
            'NumberFormatException': ['number', 'parse', 'format', 'integer'],
            'ArrayIndexOutOfBoundsException': ['array', 'index', 'bounds'],
            'FileNotFoundException': ['file', 'path', 'not found', 'missing'],
        }
        
        # Java-specific commands/patterns in workarounds
        self.java_commands = [
            'mvn clean install', 'mvn build', 'gradle build',
            'restart tomcat', 'restart jboss', 'restart wildfly',
            'systemctl restart', 'service restart',
            '.jar', '.war', '.ear',
            'java -jar', 'java -classpath',
            'tail -f /opt/', '/var/log/',
            'jstack', 'jmap', 'jconsole', 'jvisualvm',
            'catalina.out', 'application.log',
        ]
        
        # Resolution categories
        self.java_categories = {
            'code': 10,
            'application error': 8,
            'backend': 8,
            'system error': 6,
            'service failure': 5,
            'backend error': 8,
            'application': 6,
        }
        
        self.non_java_categories = {
            'data': -8,
            'interface': -6,
            'configuration': -5,
            'network': -7,
            'frontend': -8,
            'user error': -10,
            'ui': -7,
            'web': -5,
        }
    
    def detect_java_error(
        self, 
        sr_data: Dict,
        java_code_matches: List[Dict],
        historical_matches: List[Dict],
        java_metadata_context: str
    ) -> Dict:
        """
        Main detection method - combines all signals
        
        Returns:
            {
                'is_java_error': bool,
                'confidence': float (0.0-1.0),
                'total_score': int (0-100),
                'signals': dict,
                'evidence': list,
                'java_file': str,
                'java_path': str
            }
        """
        self.evidence = []
        
        # Initialize signals
        signals = {
            'explicit_indicators': 0.0,
            'semantic_code_match': 0.0,
            'historical_pattern': 0.0,
            'resolution_metadata': 0.0,
            'workaround_analysis': 0.0,
        }
        
        description = str(sr_data.get('Description', ''))
        notes = str(sr_data.get('Notes', ''))
        
        # SIGNAL 1: Explicit Indicators (from CURRENT SR)
        signals['explicit_indicators'] = self._analyze_explicit_indicators(
            description, notes
        )
        
        # SIGNAL 2: Semantic Code Match (from SIMILAR CODE)
        signals['semantic_code_match'] = self._analyze_code_semantic_match(
            java_code_matches, description, notes
        )
        
        # SIGNAL 3: Historical Pattern (from SIMILAR SRs - categories)
        signals['historical_pattern'] = self._analyze_historical_pattern(
            historical_matches
        )
        
        # SIGNAL 4: Resolution Metadata (from SIMILAR SRs - categories & status)
        signals['resolution_metadata'] = self._analyze_resolution_metadata_from_similar(
            historical_matches
        )
        
        # SIGNAL 5: Workaround Analysis (from SIMILAR SRs - workarounds)
        signals['workaround_analysis'] = self._analyze_workaround_from_similar(
            historical_matches, java_metadata_context
        )
        
        # Calculate total score
        total_score = sum(signals.values())
        
        # Determine if Java error and confidence
        if total_score >= 70:
            is_java_error = True
            confidence = min(1.0, total_score / 100)
            confidence_level = "Very High"
        elif total_score >= 50:
            is_java_error = True
            confidence = 0.7
            confidence_level = "High"
        elif total_score >= 30:
            is_java_error = False
            confidence = 0.6
            confidence_level = "Low - Uncertain"
        else:
            is_java_error = False
            confidence = 1.0 - (total_score / 100)
            confidence_level = "Very Low - Not Java"
        
        # Extract Java class information if detected
        java_file = "N/A"
        java_path = "N/A"
        
        if is_java_error:
            java_file, java_path = self._extract_java_class_info(
                description, notes, java_code_matches, java_metadata_context
            )
        
        return {
            'is_java_error': is_java_error,
            'confidence': confidence,
            'confidence_level': confidence_level,
            'total_score': total_score,
            'signals': signals,
            'evidence': self.evidence,
            'java_file': java_file,
            'java_path': java_path,
        }
    
    def _analyze_explicit_indicators(self, description: str, notes: str) -> float:
        """SIGNAL 1: Analyze explicit Java error patterns with context (0-30 points)"""
        score = 0.0
        text = f"{description} {notes}".lower()
        
        if not text.strip():
            self.evidence.append("⚠ No description or notes provided")
            return 0.0
        
        # Pattern 1: Stack Traces (20 points)
        stack_trace_patterns = [
            r'at\s+[a-zA-Z0-9_.]+\.[a-zA-Z0-9_]+\([a-zA-Z0-9_]+\.java:\d+\)',
            r'caused by:.*exception',
            r'exception in thread',
            r'^\s*at\s+com\.',
            r'^\s*at\s+org\.',
        ]
        
        for pattern in stack_trace_patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                score += 20
                self.evidence.append("✓ Stack trace pattern detected")
                break
        
        # Pattern 2: Java Exceptions with Context (15 points)
        exception_found = False
        for exception, context_words in self.exception_patterns.items():
            if exception.lower() in text:
                # Check if exception has relevant context
                has_context = any(word in text for word in context_words)
                if has_context:
                    score += 10
                    context_found = ', '.join([w for w in context_words if w in text])
                    self.evidence.append(f"✓ {exception} with relevant context ({context_found})")
                    exception_found = True
                    break
                else:
                    score += 3
                    self.evidence.append(f"⚠ {exception} found but no relevant context words")
                    exception_found = True
                    break
        
        # Pattern 3: Java Class/Package Names (10 points)
        java_package_patterns = [
            r'com\.[a-z]+\.[a-z]+\.[A-Z][a-zA-Z0-9]+',
            r'org\.[a-z]+\.[a-z]+\.[A-Z][a-zA-Z0-9]+',
            r'[A-Z][a-zA-Z0-9]*Service\.java',
            r'[A-Z][a-zA-Z0-9]*Controller\.java',
            r'[A-Z][a-zA-Z0-9]*Repository\.java',
            r'[A-Z][a-zA-Z0-9]*Impl\.java',
        ]
        
        java_class_found = False
        for pattern in java_package_patterns:
            if re.search(pattern, text):
                score += 10
                self.evidence.append("✓ Java class/package naming convention detected")
                java_class_found = True
                break
        
        # If no explicit indicators found
        if score == 0:
            self.evidence.append("✗ No explicit Java indicators (stack traces, exceptions, Java classes) found in description/notes")
        
        return min(30, score)
    
    def _analyze_code_semantic_match(self, code_matches: List[Dict], 
                                      description: str, notes: str) -> float:
        """SIGNAL 2: Analyze semantic similarity with actual backend code (0-25 points)"""
        if not code_matches:
            self.evidence.append("✗ No Java code semantic matches found")
            return 0.0
        
        score = 0.0
        best_match = code_matches[0]
        similarity = best_match['similarity']
        
        # High similarity with Java code = likely Java error
        if similarity >= 0.80:
            score += 15
            self.evidence.append(f"✓ Very high code similarity: {similarity:.0%}")
        elif similarity >= 0.65:
            score += 10
            self.evidence.append(f"✓ High code similarity: {similarity:.0%}")
        elif similarity >= 0.50:
            score += 5
            self.evidence.append(f"⚠ Moderate code similarity: {similarity:.0%}")
        
        # Analyze code content for error-prone patterns
        error_pattern_score = 0
        for match in code_matches[:3]:
            code = match['code'].lower()
            
            # Error-prone patterns
            if all(k in code for k in ['if', 'null']):
                error_pattern_score += 2
            if all(k in code for k in ['try', 'catch']):
                error_pattern_score += 2
            if any(k in code for k in ['throw', 'exception']):
                error_pattern_score += 1
        
        if error_pattern_score > 0:
            score += min(5, error_pattern_score)
            self.evidence.append(f"✓ Code contains error-handling patterns")
        
        # Check if matched code files are mentioned in SR
        sr_text = f"{description} {notes}".lower()
        for match in code_matches[:3]:
            file_path = match['metadata'].get('file_path', '').lower()
            if file_path:
                class_name = file_path.split('/')[-1].replace('.java', '')
                if class_name and class_name in sr_text:
                    score += 5
                    self.evidence.append(f"✓ Code file '{class_name}' explicitly mentioned in SR")
                    break
        
        return min(25, score)
    
    def _analyze_historical_pattern(self, historical_matches: List[Dict]) -> float:
        """SIGNAL 3: Analyze category patterns from similar SRs (0-20 points)"""
        if not historical_matches:
            self.evidence.append("⚠ No similar SRs found for pattern analysis")
            return 0.0
        
        score = 0.0
        
        java_related = ['code', 'backend', 'application error', 'system error']
        non_java_related = ['data', 'interface', 'configuration', 'network', 'frontend']
        
        java_count = 0
        non_java_count = 0
        unknown_count = 0
        
        for match in historical_matches[:5]:
            hist_category = match.get('resolution_category', '').lower()
            
            if not hist_category or hist_category in ['unknown', 'nan', 'none']:
                unknown_count += 1
                continue
            
            if any(cat in hist_category for cat in java_related):
                java_count += 1
            elif any(cat in hist_category for cat in non_java_related):
                non_java_count += 1
            else:
                unknown_count += 1
        
        # Calculate pattern ratio
        total_categorized = java_count + non_java_count
        
        if total_categorized == 0:
            self.evidence.append(f"⚠ All {len(historical_matches[:5])} similar SRs have unknown categories")
            return 0.0
        
        if java_count > non_java_count:
            ratio = java_count / total_categorized
            score += ratio * 20
            self.evidence.append(f"✓ {java_count}/{total_categorized} similar SRs were Java-related (categories)")
        elif non_java_count > java_count:
            self.evidence.append(f"✗ {non_java_count}/{total_categorized} similar SRs were NOT Java-related (categories)")
        else:
            self.evidence.append(f"⚠ Similar SRs evenly split: {java_count} Java, {non_java_count} non-Java")
        
        if unknown_count > 0:
            self.evidence.append(f"⚠ {unknown_count} similar SRs had unknown categories")
        
        return min(20, score)
    
    def _analyze_resolution_metadata_from_similar(self, historical_matches: List[Dict]) -> float:
        """SIGNAL 4: Analyze Resolution Category + Status Reason from similar SRs (0-15 points)"""
        if not historical_matches:
            self.evidence.append("⚠ No similar SRs found - cannot analyze metadata")
            return 0.0
        
        score = 0.0
        java_category_count = 0
        non_java_category_count = 0
        customer_approved_code_count = 0
        automation_code_count = 0
        
        for match in historical_matches[:5]:
            category = match.get('resolution_category', '').lower()
            reason = match.get('status_reason', '').lower()
            
            # Skip unknown
            if not category or category in ['unknown', 'nan', 'none', '']:
                continue
            
            # Check Java-indicating categories (POSITIVE points)
            for indicator, points in self.java_categories.items():
                if indicator in category:
                    java_category_count += 1
                    score += points / 5  # Divide by 5 since we check top 5 SRs
                    break
            
            # Check non-Java categories (NO NEGATIVE POINTS - just don't add)
            else:  # Only runs if no Java category matched
                for indicator, points in self.non_java_categories.items():
                    if indicator in category:
                        non_java_category_count += 1
                        # Don't subtract points - just record it
                        break
            
            # Status Reason correlation
            if 'customer approved' in reason or 'customer_approved' in reason:
                if any(cat in category for cat in ['code', 'backend', 'application']):
                    customer_approved_code_count += 1
            
            if 'automation' in reason:
                if 'code' in category:
                    automation_code_count += 1
        
        # Evidence summary
        if java_category_count > 0:
            score += min(5, java_category_count)  # Bonus for multiple Java categories
            self.evidence.append(f"✓ {java_category_count}/5 similar SRs had Java-related categories")
        
        if non_java_category_count > 0:
            self.evidence.append(f"✗ {non_java_category_count}/5 similar SRs had NON-Java categories")
        
        if customer_approved_code_count >= 2:
            score += 3
            self.evidence.append(f"✓ {customer_approved_code_count} similar SRs: customer-approved code fixes")
        
        if automation_code_count >= 2:
            score += 2
            self.evidence.append(f"✓ {automation_code_count} similar SRs: automated code resolutions")
        
        if java_category_count == 0 and non_java_category_count == 0:
            self.evidence.append("⚠ Similar SRs have unclear resolution categories")
        
        # Return only positive scores (0-15 range)
        return max(0, min(15, score))
    
    def _analyze_workaround_from_similar(self, historical_matches: List[Dict], 
                                          java_metadata: str) -> float:
        """SIGNAL 5: Analyze workarounds from similar SRs (0-10 points)"""
        if not historical_matches:
            self.evidence.append("⚠ No similar SRs found - cannot analyze workarounds")
            return 0.0
        
        score = 0.0
        total_java_commands = 0
        total_java_classes = 0
        srs_with_java_indicators = 0
        srs_analyzed = 0
        
        for match in historical_matches[:5]:
            workaround = match.get('workaround', '')
            
            # Skip empty workarounds
            if not workaround or str(workaround).lower() in ['not available', 'nan', 'none', 'n/a', 'na']:
                continue
            
            srs_analyzed += 1
            workaround_lower = str(workaround).lower()
            has_java_indicator = False
            
            # Check for Java-specific commands
            command_count = sum(1 for cmd in self.java_commands if cmd in workaround_lower)
            if command_count > 0:
                total_java_commands += command_count
                has_java_indicator = True
            
            # Check for Java class references
            java_class_pattern = r'\b[A-Z][a-zA-Z0-9]*(Service|Controller|Repository|Manager|Handler|Impl)\b'
            class_matches = len(re.findall(java_class_pattern, str(workaround)))
            if class_matches > 0:
                total_java_classes += class_matches
                has_java_indicator = True
            
            if has_java_indicator:
                srs_with_java_indicators += 1
        
        # Calculate score based on aggregated evidence
        if total_java_commands > 0:
            score += min(5, total_java_commands * 0.5)
            self.evidence.append(f"✓ Similar SRs' workarounds contain {total_java_commands} Java commands")
        
        if total_java_classes > 0:
            score += min(3, total_java_classes * 0.3)
            self.evidence.append(f"✓ Similar SRs' workarounds reference {total_java_classes} Java classes")
        
        if srs_with_java_indicators >= 3:
            score += 2
            self.evidence.append(f"✓ {srs_with_java_indicators}/{srs_analyzed} similar SRs have Java-specific workarounds")
        
        if score == 0 and srs_analyzed > 0:
            self.evidence.append(f"✗ {srs_analyzed} similar SRs' workarounds don't contain Java indicators")
        elif srs_analyzed == 0:
            self.evidence.append("⚠ No workarounds available in similar SRs")
        
        return min(10, score)
    
    def _extract_java_class_info(self, description: str, notes: str,
                                  code_matches: List[Dict],
                                  java_metadata: str) -> Tuple[str, str]:
        """Extract Java class name and path from all available information"""
        text = f"{description} {notes}".lower()
        
        # Try to extract from code matches first (most reliable)
        if code_matches:
            best_match = code_matches[0]
            metadata = best_match.get('metadata', {})
            file_path = metadata.get('file_path', '')
            
            if file_path:
                class_name = file_path.split('/')[-1].replace('.java', '')
                return class_name, file_path
        
        # Try to extract from SR text using patterns
        java_class_pattern = r'([A-Z][a-zA-Z0-9]+(?:Service|Controller|Repository|Impl))(?:\.java)?'
        matches = re.findall(java_class_pattern, f"{description} {notes}")
        
        if matches:
            class_name = matches[0]
            # Try to find path in metadata
            if class_name.lower() in java_metadata.lower():
                # Extract path from metadata (simplified)
                path_pattern = rf'Path:\s*([^\n]+{class_name}\.java)'
                path_match = re.search(path_pattern, java_metadata, re.IGNORECASE)
                if path_match:
                    return class_name, path_match.group(1).strip()
            
            return class_name, f"com/amdocs/oss/comcast/.../{ class_name}.java"
        
        # Try to extract from stack trace
        stack_trace_pattern = r'at\s+([a-zA-Z0-9_.]+)\.([a-zA-Z0-9_]+)\([a-zA-Z0-9_]+\.java'
        stack_match = re.search(stack_trace_pattern, text)
        
        if stack_match:
            full_class = stack_match.group(1)
            class_name = full_class.split('.')[-1]
            path = full_class.replace('.', '/') + '.java'
            return class_name, path
        
        return "N/A", "N/A"
    
    def format_evidence_for_prompt(self) -> str:
        """Format evidence list for inclusion in LLM prompt"""
        if not self.evidence:
            return "No evidence collected"
        
        return "\n".join([f"  {item}" for item in self.evidence])


if __name__ == "__main__":
    # Test the detector
    print("="*80)
    print("INTELLIGENT JAVA ERROR DETECTOR - TEST")
    print("="*80)
    
    # Test case 1: Clear Java error
    test_sr_1 = {
        'Description': 'NullPointerException in BomOrderServiceImpl when processing order. Stack trace shows error at line 145.',
        'Notes': 'Customer reported order processing failed. Logs show null object reference in processOrder method.',
        'Resolution Category': 'Code',
        'Status Reason': 'Customer Approved',
        'Semantic Workaround': 'Previous fix: Added null check in BomOrderServiceImpl. Restart tomcat service after deployment.'
    }
    
    detector = IntelligentJavaErrorDetector()
    result = detector.detect_java_error(
        test_sr_1,
        [{'similarity': 0.85, 'code': 'public void processOrder(Order order) { if (order == null) throw new NPE', 'metadata': {'file_path': 'com/amdocs/BomOrderServiceImpl.java'}}],
        [{'resolution_category': 'Code', 'status_reason': 'Customer Approved', 'workaround': 'Fixed Java NPE and restarted service'}],
        'BomOrderServiceImpl (Service): com.amdocs.oss.BomOrderServiceImpl\nPath: com/amdocs/oss/BomOrderServiceImpl.java'
    )
    
    print("\nTest Case 1: Clear Java Error")
    print(f"  Decision: {'JAVA ERROR' if result['is_java_error'] else 'NOT JAVA'}")
    print(f"  Confidence: {result['confidence']:.2%} ({result['confidence_level']})")
    print(f"  Total Score: {result['total_score']}/100")
    print(f"  Signals: {result['signals']}")
    print(f"  Java Class: {result['java_file']}")
    print(f"  Java Path: {result['java_path']}")
    print(f"\nEvidence:")
    for evidence in result['evidence']:
        print(f"    {evidence}")
    
    print("\n" + "="*80)
    print("Detector ready for integration!")
    print("="*80)

