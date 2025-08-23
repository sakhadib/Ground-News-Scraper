import os
import json
from collections import defaultdict

# Path to the folder containing the JSON files
folder_path = 'json/'

def analyze_json_files(folder_path):
    total_sources = 0
    non_null_text_sources = 0
    null_text_sources = 0
    bias_counts = defaultdict(int)  # To store the count of each bias value
    
    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Only process JSON files
        if file_name.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    sources = data.get("sources", [])

                    # Count sources and check 'text' attribute
                    total_sources += len(sources)

                    for source in sources:
                        text = source.get("text")
                        bias = source.get("bias")
                        
                        # Counting text values
                        if text:
                            non_null_text_sources += 1
                        else:
                            null_text_sources += 1
                        
                        # Counting bias values
                        if bias:
                            bias_counts[bias] += 1

                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_name}")
    
    # Calculate the percentage of sources with non-null text
    if total_sources > 0:
        non_null_percentage = (non_null_text_sources / total_sources) * 100
    else:
        non_null_percentage = 0

    # Display the results
    print(f"Total sources: {total_sources}")
    print(f"Sources with non-null 'text': {non_null_text_sources}")
    print(f"Sources with null 'text': {null_text_sources}")
    print(f"Percentage of sources with non-null 'text': {non_null_percentage:.2f}%")

    # Display bias counts
    print("\nBias counts:")
    for bias, count in bias_counts.items():
        print(f"{bias}: {count}")


if __name__ == "__main__":
    analyze_json_files(folder_path)
