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
from reportlab.lib.colors import black, gray
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

def download_images(grouped_data, images_dir):
    """
    Download all images and save them locally
    """
    os.makedirs(images_dir, exist_ok=True)
    
    downloaded_images = {}
    
    for image_url, question_data in grouped_data.items():
        if not image_url:
            continue
            
        # Create a filename from the URL
        parsed_url = urllib.parse.urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = f"image_{hash(image_url)}.jpg"
            
        filepath = os.path.join(images_dir, filename)
        
        # Check if image already exists
        if os.path.exists(filepath):
            print(f"Image already exists: {filename}")
            downloaded_images[image_url] = filepath
            continue
            
        # Download the image
        try:
            print(f"Downloading image: {image_url}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            downloaded_images[image_url] = filepath
            print(f"Saved image: {filepath}")
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")
            downloaded_images[image_url] = None
    
    return downloaded_images

def create_pdf_for_question(question_data, output_path, image_path=None):
    """
    Create a PDF for a single question with all its answers
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4, 
                           leftMargin=50, rightMargin=50,
                           topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=black,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=black,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leading=16,  # Double line spacing
    )
    
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=normal_style,
        fontSize=11,
        spaceAfter=8,
        leading=14,
        textColor=black,
        fontName='Helvetica-Bold'
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
    story.append(Spacer(1, 20))
    
    # Image
    if image_path and os.path.exists(image_path):
        try:
            img = Image(image_path, width=6*inch, height=4*inch)
            img.hAlign = 'CENTER'
            story.append(img)
        except:
            story.append(Paragraph("<b>Image Description:</b>", heading_style))
            story.append(Paragraph(image_description.replace('\n', '<br/>'), normal_style))
    else:
        story.append(Paragraph("<b>Image Description:</b>", heading_style))
        story.append(Paragraph(image_description.replace('\n', '<br/>'), normal_style))
    
    story.append(PageBreak())
    
    # Second page and onwards: Answers and evaluations
    for i, answer_data in enumerate(question_data, 1):
        story.append(Paragraph(f"Model Answer #{i}", heading_style))
        story.append(Spacer(1, 12))
        
        # Content with double line spacing
        content = answer_data.get('content', 'N/A')
        # Process content to preserve line breaks with double spacing
        content_lines = content.split('\n')
        formatted_content = '<br/><br/>'.join(content_lines)  # Double line breaks
        
        story.append(Paragraph(f"<b>Response:</b>", normal_style))
        story.append(Paragraph(formatted_content, normal_style))
        story.append(Spacer(1, 12))
        
        # Scores with bold formatting for score lines
        overall_score = answer_data.get('overall_band_score', 'N/A')
        tr_score = answer_data.get('task_response_score', 'N/A')
        cc_score = answer_data.get('coherence_cohesion_score', 'N/A')
        lr_score = answer_data.get('lexical_resource_score', 'N/A')
        gr_score = answer_data.get('grammatical_range_accuracy_score', 'N/A')
        
        story.append(Paragraph(f"<b>Evaluation:</b>", normal_style))
        story.append(Spacer(1, 6))
        
        story.append(Paragraph(f"<b>Overall Band Score: {overall_score}</b>", bold_style))
        story.append(Paragraph(f"<b>Task Response ({tr_score}):</b> {answer_data.get('task_response_description', '')}", normal_style))
        story.append(Paragraph(f"<b>Coherence & Cohesion ({cc_score}):</b> {answer_data.get('coherence_cohesion_description', '')}", normal_style))
        story.append(Paragraph(f"<b>Lexical Resource ({lr_score}):</b> {answer_data.get('lexical_resource_description', '')}", normal_style))
        story.append(Paragraph(f"<b>Grammatical Range & Accuracy ({gr_score}):</b> {answer_data.get('grammatical_range_accuracy_description', '')}", normal_style))
        
        story.append(Spacer(1, 24))
        
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
    
    # Download images
    images_dir = 'downloaded_images'
    downloaded_images = download_images(grouped_data, images_dir)
    
    # Create output directory
    output_dir = 'ielts_task1_improved_pdfs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create PDFs for each question
    for i, (image_url, question_data) in enumerate(grouped_data.items(), 1):
        output_path = os.path.join(output_dir, f"question_{i}.pdf")
        image_path = downloaded_images.get(image_url)
        print(f"Creating PDF for question {i} with {len(question_data)} answers...")
        create_pdf_for_question(question_data, output_path, image_path)
    
    print(f"All PDFs created in '{output_dir}' directory")

if __name__ == "__main__":
    main()