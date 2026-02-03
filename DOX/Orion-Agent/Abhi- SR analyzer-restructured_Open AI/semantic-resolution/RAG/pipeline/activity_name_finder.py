"""
Activity Implementation Finder for RAG Pipeline

Queries PostgreSQL database to find activity implementation class path.
Optimized for integration with RAG pipeline processing.
"""

import os
import psycopg2
import xml.etree.ElementTree as ET
from typing import Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActivityFinder:
    """Finds activity implementation details from database for RAG pipeline"""
    
    def __init__(self, db_config: Optional[Dict[str, str]] = None):
        """
        Initialize with database configuration
        
        Args:
            db_config: Dictionary with keys: host, port, database, user, password
                      If None, reads from environment variables
        """
        if db_config is None:
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_NAME', 'paasdb'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD')
            }
        
        self.db_config = db_config
        self._validate_config()
    
    def _validate_config(self):
        """Validate database configuration"""
        if not self.db_config.get('user'):
            raise ValueError("Database user is required (set DB_USER env var)")
        if not self.db_config.get('password'):
            raise ValueError("Database password is required (set DB_PASSWORD env var)")
    
    def get_db_connection(self):
        """Create PostgreSQL database connection"""
        try:
            return psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
        except psycopg2.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def find_activity_implementation(self, activity_name: str) -> Dict:
        """
        Find activity implementation class path and file path
        
        Process:
        1. Query oss_ref_data for ActivityProfileSpec by entity_name
        2. Parse XML payload to find Implementation value (with expiration='NONE')
        3. Query again for ActivityProfileImplementation by entity_id
        4. Parse XML to find Class value (with expiration='NONE')
        5. Construct file path from class path
        
        Args:
            activity_name: Name of the activity to search for
            
        Returns:
            Dictionary containing:
            - impl_path: File path to implementation
            - impl_file_name: Implementation file name
            - class_path: Full Java class path
            - class_name: Simple class name
            - profile_name: Profile name (if available)
            - sequence: Sequence number (if available)
            - implementation_id: UUID of implementation entity
            - entity_id: UUID of activity entity
            - error: Error message (if any)
            - success: Boolean indicating success
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Step 1: Query for ActivityProfileSpec with case-insensitive matching
            query1 = """
                SELECT payload, entity_name, entity_id
                FROM ossdb01ref.oss_ref_data 
                WHERE entity_type = 'ActivityProfileSpec' 
                AND LOWER(entity_name) LIKE LOWER(%s)
            """
            cursor.execute(query1, (f'%{activity_name}%',))
            result1 = cursor.fetchone()
            
            if not result1:
                logger.warning(f"Activity '{activity_name}' not found in database")
                return {
                    "success": False,
                    "error": f"Activity '{activity_name}' not found in database",
                    "activity_name": activity_name
                }
            
            payload1_xml, entity_name, entity_id = result1
            
            # Step 2: Parse XML to find Implementation value
            root1 = ET.fromstring(payload1_xml)
            
            implementation_value = None
            profile_name = None
            sequence = None
            
            for version in root1.findall('.//ActivityProfileSpecVersion'):
                if version.get('expiration') == 'NONE':
                    impl_elem = version.find('Implementation')
                    if impl_elem is not None:
                        implementation_value = impl_elem.get('value')
                    
                    profile_elem = version.find('ProfileName')
                    if profile_elem is not None:
                        profile_name = profile_elem.get('value')
                    
                    seq_elem = version.find('Sequence')
                    if seq_elem is not None:
                        sequence = seq_elem.get('value')
                    
                    break
            
            if not implementation_value:
                logger.warning(f"Implementation value not found for activity '{activity_name}'")
                return {
                    "success": False,
                    "error": "Implementation value not found in XML payload",
                    "activity_name": activity_name
                }
            
            # Step 3: Query for ActivityProfileImplementation
            query2 = """
                SELECT payload 
                FROM ossdb01ref.oss_ref_data 
                WHERE entity_id = %s
            """
            cursor.execute(query2, (implementation_value,))
            result2 = cursor.fetchone()
            
            if not result2:
                logger.warning(f"Implementation '{implementation_value}' not found")
                return {
                    "success": False,
                    "error": f"Implementation '{implementation_value}' not found",
                    "activity_name": activity_name
                }
            
            payload2_xml = result2[0]
            
            # Step 4: Parse XML to find Class value
            root2 = ET.fromstring(payload2_xml)
            
            class_path = None
            
            for version in root2.findall('.//ActivityProfileImplementationVersion'):
                if version.get('expiration') == 'NONE':
                    class_elem = version.find('Class')
                    if class_elem is not None:
                        class_path = class_elem.get('value')
                    break
            
            if not class_path:
                logger.warning(f"Class path not found for activity '{activity_name}'")
                return {
                    "success": False,
                    "error": "Class path not found in XML payload",
                    "activity_name": activity_name
                }
            
            # Step 5: Extract class name and construct impl path
            class_name = class_path.split('.')[-1]
            package_path = class_path.replace('.', '/')
            impl_path = f"customization/src/main/java/{package_path}.java"
            
            cursor.close()
            conn.close()
            
            logger.info(f"Successfully found implementation for '{activity_name}': {impl_path}")
            
            return {
                "success": True,
                "activity_name": entity_name,
                "impl_path": impl_path,
                "impl_file_name": f"{class_name}.java",
                "class_path": class_path,
                "class_name": class_name,
                "profile_name": profile_name or "Unknown",
                "sequence": int(sequence) if sequence else 1,
                "implementation_id": implementation_value,
                "entity_id": entity_id
            }
            
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "activity_name": activity_name
            }
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            return {
                "success": False,
                "error": f"XML parsing error: {str(e)}",
                "activity_name": activity_name
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "activity_name": activity_name
            }
    
    def find_multiple_activities(self, activity_names: List[str]) -> Dict[str, Dict]:
        """
        Find implementation details for multiple activities
        
        Args:
            activity_names: List of activity names to search for
            
        Returns:
            Dictionary mapping activity_name -> result dict
        """
        results = {}
        for activity_name in activity_names:
            results[activity_name] = self.find_activity_implementation(activity_name)
        return results


# Convenience function for RAG pipeline integration
def find_activity(activity_name: str, db_config: Optional[Dict[str, str]] = None) -> Dict:
    """
    Convenience function to find activity implementation
    Designed for easy integration with RAG pipeline
    
    Args:
        activity_name: Name of the activity to search for
        db_config: Optional database configuration. If None, uses environment variables
        
    Returns:
        Dictionary with implementation details or error
        
    Example:
        >>> result = find_activity('ValidateAddress')
        >>> if result['success']:
        ...     print(f"File: {result['impl_path']}")
        ...     print(f"Class: {result['class_path']}")
    """
    finder = ActivityFinder(db_config)
    return finder.find_activity_implementation(activity_name)


def find_multiple_activities(activity_names: List[str], db_config: Optional[Dict[str, str]] = None) -> Dict[str, Dict]:
    """
    Convenience function to find multiple activity implementations
    
    Args:
        activity_names: List of activity names to search for
        db_config: Optional database configuration
        
    Returns:
        Dictionary mapping activity_name -> result dict
    """
    finder = ActivityFinder(db_config)
    return finder.find_multiple_activities(activity_names)


# Example usage in RAG pipeline
if __name__ == '__main__':
    # Test with environment variables
    result = find_activity('ValidateAddress')
    
    if result['success']:
        print("✅ Activity Implementation Found")
        print("=" * 60)
        print(f"Activity Name:      {result['activity_name']}")
        print(f"Implementation File: {result['impl_file_name']}")
        print(f"File Path:          {result['impl_path']}")
        print(f"Class Path:         {result['class_path']}")
        print(f"Class Name:         {result['class_name']}")
        print(f"Profile Name:       {result['profile_name']}")
        print(f"Sequence:           {result['sequence']}")
    else:
        print(f"❌ Error: {result['error']}")


