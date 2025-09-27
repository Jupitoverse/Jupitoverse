import pandas as pd
import json

# Path to the Excel file
excel_file_path = r"C:\Users\abhisha3\Desktop\SR\All_SR_V1.xlsx"

# Read the first sheet of the Excel file
df = pd.read_excel(excel_file_path, sheet_name=0)

# Convert the DataFrame to a list of dictionaries (JSON format)
json_data = df.to_dict(orient='records')

# Print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, save the JSON data to a file
output_json_path = r"C:\Users\abhisha3\Desktop\SR\All_SR_V1.json"
with open(output_json_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON data has been saved to {output_json_path}")
print("The JSON data is quite large, so it has been saved in an organized manner to the specified file.")
print("You can find the JSON file at the specified path for further use.")