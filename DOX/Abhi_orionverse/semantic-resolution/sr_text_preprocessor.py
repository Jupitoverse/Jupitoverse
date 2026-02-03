#!/usr/bin/env python3
"""
SR Text Preprocessor
Cleans unstructured SR text for semantic search by removing customer/project metadata
while preserving technical content like activity names and error descriptions
"""

import re
from typing import Optional


class SRTextPreprocessor:
    """Preprocess SR text for semantic search - optimized for unstructured data"""
    
    @staticmethod
    def clean_for_semantic_search(text: str, keep_activity_label: bool = True) -> str:
        """
        Main preprocessing function for SR data
        
        Removes:
        - Customer names/IDs
        - Project names/IDs
        - Plan names/IDs
        - Activity IDs (but keeps activity names)
        - Site information
        - Timestamps/dates
        - Proposal IDs
        - Metadata labels (Summary:, Description:, etc.)
        
        Keeps:
        - Activity names (CW8, CWMA, CWMB, etc.)
        - Technical terms (CMFS, CRTE, CWM, UTI, etc.)
        - Problem descriptions
        - Error messages
        - Status information
        
        Args:
            text: Raw SR description/summary text
            keep_activity_label: Whether to keep "Activity:" label (default: True)
        
        Returns:
            Cleaned text focusing on technical content
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Store original for quality check
        original_length = len(text)
        original_text = text
        
        # Step 1: Extract and preserve activity name (important technical context)
        activity_match = re.search(r'Activity:\s*([A-Z0-9]{2,8})\b', text, re.IGNORECASE)
        activity_name = activity_match.group(1) if activity_match else ""
        
        # Step 2: Remove customer information
        text = re.sub(r'(?i)(customer|client|user)(\s+name|\s+id)?:?\s*[^\n,;]+', '', text)
        text = re.sub(r'(?i)(reported\s+by|submitted\s+by|contact):?\s+[A-Z][a-z]+\s+[A-Z][a-z]+', '', text)
        
        # Step 3: Remove project information
        text = re.sub(r'(?i)project(\s+name|\s+id)?:?\s*[^\n,;]+', '', text)
        
        # Step 4: Remove plan information  
        text = re.sub(r'(?i)plan(\s+name|\s+id)?:?\s*[^\n,;]+', '', text)
        
        # Step 5: Remove site information
        text = re.sub(r'(?i)site(\s+name|\s+id)?:?\s*[^\n,;]+', '', text)
        
        # Step 6: Remove various IDs (but keep short codes like CW8, CWMA)
        # Remove long alphanumeric IDs
        text = re.sub(r'(?i)(proposal|plan|customer|site)\s*id:?\s*[A-Za-z0-9\-_]+', '', text)
        text = re.sub(r'(?i)activity\s*id:?\s*[A-Za-z0-9\-_]+', '', text)  # Remove activity ID only
        text = re.sub(r'\bid:?\s*[A-Za-z0-9\-_]{8,}', '', text)  # Remove generic long IDs (8+ chars)
        
        # Step 7: Remove timestamps and dates
        text = re.sub(r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}(:\d{2})?', '', text)  # ISO format
        text = re.sub(r'\d{2}/\d{2}/\d{4}', '', text)  # MM/DD/YYYY
        text = re.sub(r'\d{2}-\d{2}-\d{4}', '', text)  # DD-MM-YYYY
        text = re.sub(r'(?i)(timestamp|date|time|created|modified):?\s*[^\n,;]+', '', text)
        
        # Step 8: Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Step 9: Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        text = re.sub(r'\b\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b', '[PHONE]', text)
        
        # Step 10: Clean metadata field labels
        # Remove labels at start of text
        text = re.sub(r'^(summary|description|notes|issue|problem|activity):\s*', '', text, flags=re.IGNORECASE)
        # Remove labels within text
        text = re.sub(r'\n(summary|description|notes|issue|problem):\s*', ' ', text, flags=re.IGNORECASE)
        
        # Step 11: Keep Activity label with value (important context)
        if keep_activity_label and activity_name:
            # Clean any existing activity references first
            text = re.sub(r'(?i)activity:\s*', '', text)
            # Add clean activity reference at start if not already there
            if activity_name.upper() not in text.upper():
                text = f"Activity {activity_name} {text}"
        
        # Step 12: Normalize whitespace
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = text.replace('\n', ' ').replace('\t', ' ')  # Convert newlines/tabs to spaces
        
        # Step 13: Clean punctuation
        text = re.sub(r'\.{2,}', '.', text)  # Multiple dots to single dot
        text = re.sub(r'\s+([.,!?;])', r'\1', text)  # Remove space before punctuation
        text = re.sub(r'([.,!?;])\1+', r'\1', text)  # Remove duplicate punctuation
        
        # Step 14: Remove empty brackets and extra separators
        text = re.sub(r'\[\s*\]', '', text)
        text = re.sub(r'\(\s*\)', '', text)
        text = re.sub(r'[,;]\s*[,;]+', ',', text)  # Multiple commas/semicolons
        text = re.sub(r'\s*[,;]\s*$', '', text)  # Trailing comma/semicolon
        
        # Step 15: Final cleanup
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # One more whitespace normalization
        
        # Step 16: Quality check - if we removed too much, use simpler approach
        if len(text) < 10 and original_length > 30:
            # Too aggressive - use lighter preprocessing
            text = original_text
            # Just remove obvious customer/project info
            text = re.sub(r'(?i)(customer|project|plan):\s*[^\n,;]+', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def preprocess_batch(texts: list) -> list:
        """
        Preprocess a batch of texts
        
        Args:
            texts: List of raw text strings
        
        Returns:
            List of preprocessed text strings
        """
        preprocessor = SRTextPreprocessor()
        return [preprocessor.clean_for_semantic_search(text) for text in texts]


# Standalone function for easy import
def preprocess_sr_text(text: str) -> str:
    """Convenience function for preprocessing SR text"""
    preprocessor = SRTextPreprocessor()
    return preprocessor.clean_for_semantic_search(text)


if __name__ == '__main__':
    # Test cases
    print("=" * 80)
    print("SR TEXT PREPROCESSOR - TEST CASES")
    print("=" * 80)
    
    test_cases = [
        "Summary: Customer: ABC Corp - Project: XYZ - Activity: CW8 - CW8 Object completed but the CWM Show is at 0 Obj",
        "Customer Name: John Smith, Project ID: PROJ-12345, Plan: Test Plan, Summary: CMFS Batch Load errors in CRTE",
        "Activity ID: ACT-9999, Activity: CWMA, Task Status: Failed-Canceled, Description: Infact Change on CMFS Activity",
        "2024-11-25 14:30:00 - Customer: Tech Industries - Proposal ID: PROP-456 - UTI CM is completed but the CWM is 0",
    ]
    
    preprocessor = SRTextPreprocessor()
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}:")
        print(f"{'='*80}")
        print(f"BEFORE: {test}")
        cleaned = preprocessor.clean_for_semantic_search(test)
        print(f"AFTER:  {cleaned}")
        print(f"Length: {len(test)} → {len(cleaned)} chars")
    
    print(f"\n{'='*80}")
    print("✅ Preprocessing tests complete!")
    print("=" * 80)

