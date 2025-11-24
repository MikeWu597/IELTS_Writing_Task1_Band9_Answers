import pandas as pd
import json
import os
from collections import defaultdict
import shutil

def load_data(jsonl_file):
    """
    Load data from JSONL file
    """
    data = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def group_by_image(data):
    """
    Group data by image URL
    """
    grouped = defaultdict(list)
    for item in data:
        image_url = item.get('image', '')
        grouped[image_url].append(item)
    return grouped

def categorize_pdfs(source_dir, categorized_dir, data):
    """
    Categorize PDFs based on their topic type
    """
    # Create the main categorized directory
    os.makedirs(categorized_dir, exist_ok=True)
    
    # Group data by image URL to get topic information
    grouped_data = group_by_image(data)
    
    # Create topic directories
    topics = set()
    for items in grouped_data.values():
        topic = items[0].get('topic', 'Unknown')
        topics.add(topic)
    
    for topic in topics:
        topic_dir = os.path.join(categorized_dir, topic)
        os.makedirs(topic_dir, exist_ok=True)
    
    # Move PDF files to their respective topic directories
    for i, (image_url, question_data) in enumerate(grouped_data.items(), 1):
        topic = question_data[0].get('topic', 'Unknown')
        source_file = os.path.join(source_dir, f"question_{i}.pdf")
        dest_dir = os.path.join(categorized_dir, topic)
        dest_file = os.path.join(dest_dir, f"question_{i}.pdf")
        
        # Check if source file exists
        if os.path.exists(source_file):
            # Move the file
            shutil.move(source_file, dest_file)
            print(f"Moved {source_file} to {dest_file}")
        else:
            print(f"Source file not found: {source_file}")

def main():
    # Load data
    data_file = 'high_score_results.jsonl'
    if not os.path.exists(data_file):
        print(f"Data file {data_file} not found!")
        return
    
    data = load_data(data_file)
    print(f"Loaded {len(data)} records")
    
    # Categorize PDFs
    source_dir = 'ielts_task1_improved_pdfs'  # Directory where PDFs were created
    categorized_dir = 'categorized_pdfs'
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} not found!")
        return
    
    categorize_pdfs(source_dir, categorized_dir, data)
    print(f"PDFs have been categorized into '{categorized_dir}' directory")

if __name__ == "__main__":
    main()