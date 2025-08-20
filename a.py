import json
import os
from collections import defaultdict

def process_json_files(directory_path):
    total_bias_dist = defaultdict(int)
    source_bias_counts = defaultdict(int)
    total_sources_count = 0
    processed_files = 0

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            try:
                # Try different encodings to handle the file
                for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            data = json.load(f)
                            
                            # Process bias distribution (from the bias_distribution field)
                            if 'bias_distribution' in data:
                                bias_dist = data['bias_distribution']
                                for key, value in bias_dist.items():
                                    if key != 'total_sources' and isinstance(value, (int, str)):
                                        # Convert string values to integers
                                        try:
                                            total_bias_dist[key] += int(value)
                                        except ValueError:
                                            pass  # Skip non-numeric values
                            
                            # Process sources (from the sources array)
                            if 'sources' in data:
                                sources = data['sources']
                                total_sources_count += len(sources)
                                for source in sources:
                                    if 'bias' in source:
                                        bias = source['bias']
                                        source_bias_counts[bias] += 1
                            
                            processed_files += 1
                            break  # Break out of encoding loop if successful
                    except UnicodeDecodeError:
                        continue  # Try next encoding
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {filename}")
                        break
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

    return total_bias_dist, source_bias_counts, total_sources_count, processed_files

def main():
    directory = input("Enter the directory path containing JSON files: ")
    
    if not os.path.isdir(directory):
        print("Invalid directory path")
        return

    bias_dist, source_counts, total_sources, processed_files = process_json_files(directory)
    
    print(f"\nProcessed {processed_files} files")
    
    print("\n1. Total Bias Distribution (from bias_distribution field):")
    for bias_type, count in bias_dist.items():
        print(f"  {bias_type}: {count}")
    
    print("\n2. Source Bias Counts (from sources array):")
    for bias, count in source_counts.items():
        print(f"  {bias}: {count}")
    
    print(f"\n3. Total Sources Count: {total_sources}")

if __name__ == "__main__":
    main()