# convert_excel.py
import pandas as pd
import os

def convert():
    """
    Reads the two sheets from the Excel file and saves them as JSON files
    in a new 'data' directory inside the 'backend'.
    """
    excel_path = r"C:\Users\abhisha3\Desktop\OSO_Automation\OSO_Search_Engine\Abhi_SE_V1.xlsx"
    backend_data_path = os.path.join('backend', 'data')

    print("Starting Excel to JSON conversion...")

    try:
        # Create the data directory if it doesn't exist
        os.makedirs(backend_data_path, exist_ok=True)
        
        # Read the 'SR' sheet
        print("Reading SR sheet...")
        df_sr = pd.read_excel(excel_path, sheet_name='SR')
        df_sr.fillna('', inplace=True) # Replace empty cells with empty strings
        sr_json_path = os.path.join(backend_data_path, 'sr_data.json')
        df_sr.to_json(sr_json_path, orient='records', date_format='iso')
        print(f"✅ Successfully converted SR sheet to {sr_json_path}")

        # Read the 'Defect' sheet
        print("Reading Defect sheet...")
        df_defect = pd.read_excel(excel_path, sheet_name='Defect')
        df_defect.fillna('', inplace=True) # Replace empty cells with empty strings
        defect_json_path = os.path.join(backend_data_path, 'defect_data.json')
        df_defect.to_json(defect_json_path, orient='records', date_format='iso')
        print(f"✅ Successfully converted Defect sheet to {defect_json_path}")
        
        print("\nConversion complete!")

    except FileNotFoundError:
        print(f"❌ ERROR: The Excel file was not found at: {excel_path}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    convert()