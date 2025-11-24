import pandas as pd
import json
import os
from collections import defaultdict
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import urllib.parse

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

def download_image(url, timeout=30):
    """
    Download image from URL and return as BytesIO object
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return None

def create_pdf_for_question(question_data, output_path):
    """
    Create a PDF for a single question with all its answers
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
    )
    
    # First page: Question and image
    topic = question_data[0].get('topic', 'N/A')
    subject = question_data[0].get('subject', 'N/A')
    image_url = question_data[0].get('image', '')
    image_description = question_data[0].get('image_description', 'N/A')
    
    # Title
    story.append(Paragraph(f"Task 1: {topic}", title_style))
    story.append(Spacer(1, 12))
    
    # Subject
    story.append(Paragraph(f"<b>Subject:</b> {subject}", normal_style))
    story.append(Spacer(1, 12))
    
    # Image
    img_stream = download_image(image_url)
    if img_stream:
        img = Image(img_stream, width=6*inch, height=4*inch)
        img.hAlign = 'CENTER'
        story.append(img)
    else:
        story.append(Paragraph("<b>Image Description:</b>", heading_style))
        story.append(Paragraph(image_description, normal_style))
    
    story.append(PageBreak())
    
    # Second page and onwards: Answers and evaluations
    for i, answer_data in enumerate(question_data, 1):
        story.append(Paragraph(f"Answer #{i}", heading_style))
        
        # Content
        content = answer_data.get('content', 'N/A')
        story.append(Paragraph(f"<b>Response:</b>", normal_style))
        story.append(Paragraph(content.replace('\n', '<br/>'), normal_style))
        story.append(Spacer(1, 12))
        
        # Scores
        overall_score = answer_data.get('overall_band_score', 'N/A')
        tr_score = answer_data.get('task_response_score', 'N/A')
        cc_score = answer_data.get('coherence_cohesion_score', 'N/A')
        lr_score = answer_data.get('lexical_resource_score', 'N/A')
        gr_score = answer_data.get('grammatical_range_accuracy_score', 'N/A')
        
        story.append(Paragraph(f"<b>Scores:</b>", normal_style))
        story.append(Paragraph(f"Overall Band Score: {overall_score}", normal_style))
        story.append(Paragraph(f"Task Response: {tr_score} - {answer_data.get('task_response_description', '')}", normal_style))
        story.append(Paragraph(f"Coherence & Cohesion: {cc_score} - {answer_data.get('coherence_cohesion_description', '')}", normal_style))
        story.append(Paragraph(f"Lexical Resource: {lr_score} - {answer_data.get('lexical_resource_description', '')}", normal_style))
        story.append(Paragraph(f"Grammatical Range & Accuracy: {gr_score} - {answer_data.get('grammatical_range_accuracy_description', '')}", normal_style))
        
        story.append(Spacer(1, 20))
        
        if i < len(question_data):
            story.append(PageBreak())
    
    # Build PDF
    doc.build(story)

def main():
    # Load data
    data_file = 'high_score_results.jsonl'
    if not os.path.exists(data_file):
        print(f"Data file {data_file} not found!")
        return
    
    data = load_data(data_file)
    print(f"Loaded {len(data)} records")
    
    # Group by image
    grouped_data = group_by_image(data)
    print(f"Found {len(grouped_data)} unique questions")
    
    # Create output directory
    output_dir = 'ielts_task1_pdfs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create PDFs for each question
    for i, (image_url, question_data) in enumerate(grouped_data.items(), 1):
        output_path = os.path.join(output_dir, f"question_{i}.pdf")
        print(f"Creating PDF for question {i} with {len(question_data)} answers...")
        create_pdf_for_question(question_data, output_path)
    
    print(f"All PDFs created in '{output_dir}' directory")

if __name__ == "__main__":
    main()