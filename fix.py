import csv
import uuid
import os
from datetime import datetime

def add_story_id_to_csv():
    """
    Load dataset.csv and add story_id column if it doesn't exist
    """
    csv_filename = 'dataset.csv'
    
    # Check if file exists
    if not os.path.exists(csv_filename):
        print(f"Error: {csv_filename} not found!")
        return
    
    print(f"Found {csv_filename}, checking for story_id column...")
    
    # Read the current CSV data
    rows = []
    fieldnames = []
    
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            
            # Check if fieldnames is None or if story_id column already exists
            if not fieldnames:
                print("Error: Could not read CSV headers!")
                return
                
            if 'story_id' in fieldnames:
                print("✅ story_id column already exists in the CSV!")
                return
            
            print("❌ story_id column not found. Adding it now...")
            
            # Read all existing rows
            for row in reader:
                rows.append(row)
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    print(f"Read {len(rows)} existing rows from CSV")
    
    # Create backup
    backup_filename = f"{csv_filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        os.rename(csv_filename, backup_filename)
        print(f"📁 Created backup: {backup_filename}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
    
    # Add story_id as the first column (fieldnames is guaranteed to be not None at this point)
    if fieldnames:
        new_fieldnames = ['story_id'] + list(fieldnames)
    else:
        print("Error: No fieldnames available!")
        return
    
    # Write the updated CSV
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_fieldnames)
            writer.writeheader()
            
            for i, row in enumerate(rows, 1):
                # Generate unique story ID for each existing row
                story_id = f"GN_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8]}"
                
                # Add story_id to the row
                row['story_id'] = story_id
                writer.writerow(row)
                
                print(f"  Row {i}: Added story_id = {story_id}")
        
        print(f"\n✅ Successfully updated {csv_filename} with story_id column!")
        print(f"📊 Total rows processed: {len(rows)}")
        print(f"📋 New column order: {', '.join(new_fieldnames)}")
        
    except Exception as e:
        print(f"❌ Error writing updated CSV: {e}")
        # Try to restore backup if write failed
        if os.path.exists(backup_filename):
            try:
                os.rename(backup_filename, csv_filename)
                print(f"🔄 Restored original file from backup")
            except:
                print(f"⚠️  Could not restore backup. Original file is at: {backup_filename}")

def main():
    print("=== Story ID Fixer for dataset.csv ===")
    print(f"Working directory: {os.getcwd()}")
    
    add_story_id_to_csv()
    
    print("\n=== Fix completed ===")

if __name__ == "__main__":
    main()