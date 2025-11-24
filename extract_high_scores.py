import pandas as pd
import json
import sys

def extract_rows_with_score_9(parquet_file_path, output_file_path):
    """
    Extract rows where overall_band_score is 9 from a parquet file.
    
    Args:
        parquet_file_path (str): Path to the input parquet file
        output_file_path (str): Path to the output file (JSON lines format)
    """
    # Read the parquet file
    df = pd.read_parquet(parquet_file_path)
    
    # Filter rows where overall_band_score is 9
    filtered_df = df[df['overall_band_score'] == "9"]
    
    # Write each row as a JSON object to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for _, row in filtered_df.iterrows():
            # Convert the row to a dictionary and then to JSON
            row_dict = row.to_dict()
            # Handle any NaN values that might cause serialization issues
            for key, value in row_dict.items():
                if pd.isna(value):
                    row_dict[key] = None
            json.dump(row_dict, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Extracted {len(filtered_df)} rows with overall_band_score = 9")
    print(f"Results saved to {output_file_path}")

def extract_from_csv_if_parquet_fails(csv_file_path, output_file_path):
    """
    Alternative method to extract from CSV if parquet reading fails.
    This assumes the data structure based on the sample provided.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        output_file_path (str): Path to the output file (JSON lines format)
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Assuming the last column contains the band score information
    # Based on the samples, we need to parse the 'evaluation' column to extract scores
    
    # Filter rows with overall band score of 9
    # This is a simplified approach - you might need to adjust based on actual data structure
    high_score_rows = []
    
    for idx, row in df.iterrows():
        evaluation_text = row['evaluation']
        if 'Overall Band Score: 9' in evaluation_text or 'Overall Band Score: [9]' in evaluation_text:
            high_score_rows.append(row)
    
    # Write results to output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for row in high_score_rows:
            row_dict = row.to_dict()
            # Handle any NaN values that might cause serialization issues
            for key, value in row_dict.items():
                if pd.isna(value):
                    row_dict[key] = None
            json.dump(row_dict, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Extracted {len(high_score_rows)} rows with overall_band_score = 9")
    print(f"Results saved to {output_file_path}")

if __name__ == "__main__":
    # Try to process the parquet file first
    try:
        extract_rows_with_score_9('train-00000-of-00001.parquet', 'high_score_results.jsonl')
    except Exception as e:
        print(f"Failed to read parquet file: {e}")
        print("Trying to process CSV file instead...")
        try:
            extract_from_csv_if_parquet_fails('train.csv', 'high_score_results.jsonl')
        except Exception as e2:
            print(f"Failed to read CSV file: {e2}")
            print("Please check your file paths and data format.")