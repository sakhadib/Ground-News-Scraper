import os
import json
import pandas as pd
import re
import unicodedata

# Define the folder containing the JSON files
folder_path = 'json/'

# Create 'dataset' folder if it doesn't exist
output_dir = 'dataset'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Data containers
story_data = []
source_data = []
perspective_data = []
seen_links = set()  # for removing duplicate source links

# Clean and normalize text
def clean_text(text):
    if text is None:
        return ""

    # Normalize Unicode to preserve characters like é, ü, etc.
    text = unicodedata.normalize('NFKD', text)

    # Replace newlines and carriage returns with space
    text = re.sub(r'[\r\n]+', ' ', text)

    # Replace curly quotes and other punctuation
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-")

    # Remove non-printable characters
    text = ''.join(c if c.isprintable() else ' ' for c in text)

    # Replace ? (possibly from decoding errors) with space
    text = text.replace('?', ' ')

    # Collapse multiple spaces and trim
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Process each JSON file
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                story = json.load(file)

                # Story metadata
                story_id = story.get("story_id", "")
                timestamp = story.get("metadata", {}).get("timestamp", "")
                title = clean_text(story.get("metadata", {}).get("title", ""))

                bias = story.get("bias_distribution", {})
                total_sources = bias.get("total_sources", 0)
                leaning_left = bias.get("leaning_left", 0)
                center = bias.get("center", 0)
                leaning_right = bias.get("leaning_right", 0)

                story_data.append({
                    'story_id': story_id,
                    'fetch_timestamp': timestamp,
                    'gn_title': title,
                    'total_sources': total_sources,
                    'leaning_left_count': leaning_left,
                    'center_count': center,
                    'leaning_right_count': leaning_right
                })

                # Perspective summaries
                left = clean_text(' '.join(story.get("perspective_summaries", {}).get("left", [])))
                center_p = clean_text(' '.join(story.get("perspective_summaries", {}).get("center", [])))
                right = clean_text(' '.join(story.get("perspective_summaries", {}).get("right", [])))

                perspective_data.append({
                    'story_id': story_id,
                    'left_perspective': left,
                    'center_perspective': center_p,
                    'right_perspective': right
                })

                # Source articles
                for src in story.get("sources", []):
                    link = src.get("news_link", "")
                    if not link or link in seen_links:
                        continue

                    source_text = clean_text(src.get("text", ""))
                    if not source_text:
                        continue  # skip empty articles

                    seen_links.add(link)
                    source_data.append({
                        'story_id': story_id,
                        'source_news_title': clean_text(src.get("news_title", "")),
                        'source_news_link': link,
                        'source_text': source_text,
                        'source_bias': clean_text(src.get("bias", ""))
                    })

            except json.JSONDecodeError:
                print(f"⚠️ JSON decode error in file: {filename}")
            except Exception as e:
                print(f"⚠️ Error processing file {filename}: {e}")

# Convert to DataFrames
story_df = pd.DataFrame(story_data)
source_df = pd.DataFrame(source_data)
perspective_df = pd.DataFrame(perspective_data)

# Filter out rows where source_text is empty
source_df = source_df[source_df['source_text'].notna() & (source_df['source_text'] != "")]

# Filter known biases
known_bias_df = source_df[source_df['source_bias'].str.lower() != 'unknown']

# Export CSVs
story_df.to_csv(os.path.join(output_dir, 'stories.csv'), index=False, encoding='utf-8')
source_df.to_csv(os.path.join(output_dir, 'sources.csv'), index=False, encoding='utf-8')
perspective_df.to_csv(os.path.join(output_dir, 'perspectives.csv'), index=False, encoding='utf-8')
known_bias_df.to_csv(os.path.join(output_dir, 'known_bias.csv'), index=False, encoding='utf-8')

print("✅ CSV files generated successfully in 'dataset/'")
