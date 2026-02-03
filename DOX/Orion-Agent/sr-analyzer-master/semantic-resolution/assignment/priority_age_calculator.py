"""
Priority and Age Calculator for SR Assignment
Calculates business days excluding US holidays and weekends
Provides priority weighting for assignment ordering
"""

from datetime import datetime, timedelta
from typing import Optional
import math

# Try to import holidays, but provide fallback if not available
try:
    import holidays
    HOLIDAYS_AVAILABLE = True
except ImportError:
    HOLIDAYS_AVAILABLE = False
    print("WARNING: holidays library not installed - age calculation will include US federal holidays")
    print("   Install with: pip install holidays")


class PriorityAgeCalculator:
    """
    Calculates SR priority weights and age in business days
    """
    
    def __init__(self):
        # US Federal Holidays: New Year, Memorial Day, Independence Day, 
        # Labor Day, Thanksgiving, Christmas
        if HOLIDAYS_AVAILABLE:
            self.us_holidays = holidays.US(years=range(2020, 2030))
        else:
            # Fallback: Use empty set (will only exclude weekends)
            self.us_holidays = set()
        
    def calculate_business_days(self, created_date, current_date: Optional[datetime] = None) -> int:
        """
        Calculate age in business days excluding weekends and US federal holidays
        
        Args:
            created_date: When the SR was created (datetime or string)
            current_date: Current date (defaults to now)
            
        Returns:
            int: Number of business days
        """
        try:
            # Handle None or NaN values
            if created_date is None or (isinstance(created_date, float) and math.isnan(created_date)):
                return 0
            
            # Parse created_date if it's a string
            if isinstance(created_date, str):
                # Clean the string
                created_date = str(created_date).strip()
                if not created_date or created_date.lower() in ['nan', 'nat', 'none', '']:
                    return 0
                
                # Try multiple date formats including timezone-aware formats
                date_formats = [
                    '%Y-%m-%d',
                    '%m/%d/%Y',
                    '%Y-%m-%d %H:%M:%S',
                    '%m/%d/%Y %H:%M:%S',
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%d %H:%M:%S.%f',
                    '%d-%m-%Y',
                    '%d/%m/%Y',
                    '%Y%m%d'
                ]
                
                parsed = False
                for fmt in date_formats:
                    try:
                        created_date = datetime.strptime(created_date, fmt)
                        parsed = True
                        break
                    except ValueError:
                        continue
                
                if not parsed:
                    # Try pandas to_datetime as a fallback (handles more formats)
                    try:
                        import pandas as pd
                        created_date = pd.to_datetime(created_date)
                        if hasattr(created_date, 'to_pydatetime'):
                            created_date = created_date.to_pydatetime()
                    except:
                        return 0
            
            # Handle pandas Timestamp
            if hasattr(created_date, 'to_pydatetime'):
                created_date = created_date.to_pydatetime()
            
            # Ensure we have a datetime object
            if not isinstance(created_date, datetime):
                return 0
            
            # Default to current date if not provided
            if current_date is None:
                current_date = datetime.now()
            elif isinstance(current_date, str):
                # Try multiple date formats (same as created_date)
                parsed_end = False
                for fmt in date_formats:
                    try:
                        current_date = datetime.strptime(current_date.strip(), fmt)
                        parsed_end = True
                        break
                    except ValueError:
                        continue
                
                if not parsed_end:
                    # Try pandas to_datetime as fallback
                    try:
                        import pandas as pd
                        current_date = pd.to_datetime(current_date)
                        if hasattr(current_date, 'to_pydatetime'):
                            current_date = current_date.to_pydatetime()
                        parsed_end = True
                    except:
                        current_date = datetime.now()
            elif hasattr(current_date, 'to_pydatetime'):
                current_date = current_date.to_pydatetime()
            
            # Ensure created_date is before current_date
            if created_date > current_date:
                return 0
            
            # If dates are the same, return 0
            if created_date.date() == current_date.date():
                return 0
            
            business_days = 0
            current = created_date
            
            # Iterate through each day and count business days
            while current.date() < current_date.date():
                # Skip weekends (Saturday=5, Sunday=6)
                if current.weekday() < 5:  # Monday=0 through Friday=4
                    # Skip US federal holidays
                    if current.date() not in self.us_holidays:
                        business_days += 1
                current += timedelta(days=1)
            
            return business_days
            
        except Exception as e:
            print(f"⚠️ Error calculating business days for {created_date}: {e}")
            return 0
    
    def get_priority_weight(self, priority_str: str) -> int:
        """
        Convert priority string (P0-P4) to numeric weight
        Higher weight = higher priority
        
        Args:
            priority_str: Priority level (P0, P1, P2, P3, P4)
            
        Returns:
            int: Priority weight (5=P0 highest, 1=P4 lowest, 0=unknown)
        """
        if not priority_str:
            return 0
        
        # Normalize the priority string
        priority_str = str(priority_str).strip().upper()
        
        # Priority mapping: P0 is most critical
        priority_map = {
            'P0': 5,
            'P1': 4,
            'P2': 3,
            'P3': 2,
            'P4': 1,
            'CRITICAL': 5,
            'HIGH': 4,
            'MEDIUM': 3,
            'LOW': 2,
            'URGENT': 5
        }
        
        return priority_map.get(priority_str, 0)
    
    def is_high_priority(self, priority_str: str) -> bool:
        """
        Check if priority is P0, P1, or P2 (requires expert assignment)
        
        Args:
            priority_str: Priority level
            
        Returns:
            bool: True if P0/P1/P2
        """
        weight = self.get_priority_weight(priority_str)
        return weight >= 3  # P2 or higher
    
    def get_priority_label(self, priority_str: str) -> str:
        """
        Get human-readable priority label
        
        Args:
            priority_str: Priority level
            
        Returns:
            str: Priority label
        """
        weight = self.get_priority_weight(priority_str)
        
        labels = {
            5: 'CRITICAL (P0)',
            4: 'HIGH (P1)',
            3: 'ELEVATED (P2)',
            2: 'MEDIUM (P3)',
            1: 'LOW (P4)',
            0: 'UNKNOWN'
        }
        
        return labels.get(weight, 'UNKNOWN')

