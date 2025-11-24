# IELTS Writing Task 1 High Scoring Essays

This repository contains high-scoring IELTS Writing Task 1 essays (band score 9) extracted from the Hugging Face dataset, organized and formatted for easy study and reference.

## Data Source

The original data is sourced from Hugging Face dataset:
[hai2131/IELTS-essays-task-1](https://huggingface.co/datasets/hai2131/IELTS-essays-task-1)

## Repository Structure

```
├── V1_Raw_Extracted/           # Raw extracted essays with band score 9
├── V2_Categorized/             # Essays organized by topic type
├── downloaded_images/          # Images downloaded from URLs in the dataset
├── ielts_task1_improved_pdfs/  # Generated PDF documents (improved formatting)
├── categorized_pdfs/           # Final categorized PDF documents
├── high_score_results.jsonl    # Extracted high scoring essays in JSONL format
├── train-00000-of-00001.parquet # Original dataset file
├── extract_high_scores.py      # Script to extract high scoring essays
├── download_images_and_generate_pdfs.py  # Script to download images and generate improved PDFs
├── generate_pdfs.py            # Script to generate basic PDFs
└── categorize_pdfs.py          # Script to organize PDFs by topic
```

## Processing Pipeline

1. **Extract High Scores**: [extract_high_scores.py](extract_high_scores.py) extracts essays with band score 9 from the original dataset into [high_score_results.jsonl](high_score_results.jsonl)

2. **Generate Basic PDFs**: [generate_pdfs.py](generate_pdfs.py) creates basic PDF documents from the extracted data

3. **Download Images & Generate Improved PDFs**: [download_images_and_generate_pdfs.py](download_images_and_generate_pdfs.py) downloads images and generates better-formatted PDFs

4. **Categorize PDFs**: [categorize_pdfs.py](categorize_pdfs.py) organizes the generated PDFs into topic-specific folders

## Versions

- **V1 (Raw Extracted)**: Found in [V1_Raw_Extracted](V1_Raw_Extracted/) directory
- **V2 (Categorized)**: Found in [V2_Categorized](V2_Categorized/) directory

See the README files in each directory for more specific information.

## Requirements

To run the processing scripts, you'll need:

```bash
pip install pandas requests reportlab
```

## Usage

1. Run [extract_high_scores.py](extract_high_scores.py) to extract high scoring essays:
   ```
   python extract_high_scores.py
   ```

2. Run [generate_pdfs.py](generate_pdfs.py) to generate basic PDFs:
   ```
   python generate_pdfs.py
   ```

3. Run [download_images_and_generate_pdfs.py](download_images_and_generate_pdfs.py) to generate improved PDFs with images:
   ```
   python download_images_and_generate_pdfs.py
   ```

4. Run [categorize_pdfs.py](categorize_pdfs.py) to organize PDFs by topic:
   ```
   python categorize_pdfs.py
   ```

## License

This repository uses data from [hai2131/IELTS-essays-task-1](https://huggingface.co/datasets/hai2131/IELTS-essays-task-1) on Hugging Face. Please refer to the original dataset for licensing information.