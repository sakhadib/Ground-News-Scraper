import os
import json
import pandas as pd

# Define the folder containing the JSON files
folder_path = 'json/'

# Create an empty list to store the data for the CSV
data = []

# Iterate over each JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            # Load the JSON data
            try:
                story = json.load(file)
                
                # Extract metadata
                story_id = story.get("story_id")
                timestamp = story.get("metadata", {}).get("timestamp")
                title = story.get("metadata", {}).get("title")
                
                # Extract source details
                for source in story.get("sources", []):
                    # Handle null text and replace '\n' with a space
                    source_text = source.get("text", "").replace("\n", " ") if source.get("text") else ""
                    
                    # Append each source's information as a new row
                    data.append({
                        'story_id': story_id,
                        'fetch_timestamp': timestamp,
                        'gn_title': title,
                        'source_news_title': source.get("news_title"),
                        'source_news_link': source.get("news_link"),
                        'source_text': source_text,
                        'source_bias': source.get("bias")
                    })
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Convert the list of data into a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('asm.csv', index=False, encoding='utf-8')

print("CSV file 'asm.csv' has been created successfully.")
