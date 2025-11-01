#!/usr/bin/env python3
"""
Example script demonstrating how to use the batch processing functions.

Usage:
  # Create a batch job
  python batch_example.py create pages/page-*.pdf

  # Check batch job status and retrieve results
  python batch_example.py check <batch_job_name>
"""

import os
import sys
import glob
from dotenv import load_dotenv
from extract_tables import create_batch_job, check_and_save_batch_results

load_dotenv()

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please create a .env file with your API key or set the environment variable.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Error: Please provide PDF file pattern")
            print("Example: python batch_example.py create pages/page-*.pdf")
            sys.exit(1)

        # Expand glob patterns
        pdf_patterns = sys.argv[2:]
        pdf_files = []
        for pattern in pdf_patterns:
            pdf_files.extend(glob.glob(pattern))

        if not pdf_files:
            print(f"Error: No PDF files found matching the patterns: {pdf_patterns}")
            sys.exit(1)

        print(f"Found {len(pdf_files)} PDF files to process")

        # Create batch job
        batch_job_name = create_batch_job(
            api_key=api_key,
            prompt_path="prompt.md",
            pdf_file_paths=pdf_files
        )

        print(f"\n{'='*60}")
        print(f"Batch job created successfully!")
        print(f"Job name: {batch_job_name}")
        print(f"\nTo check status and retrieve results, run:")
        print(f"  python batch_example.py check {batch_job_name}")
        print(f"{'='*60}")

    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: Please provide batch job name")
            print("Example: python batch_example.py check <batch_job_name>")
            sys.exit(1)

        batch_job_name = sys.argv[2]

        # Check status and retrieve results
        result = check_and_save_batch_results(
            api_key=api_key,
            batch_job_name=batch_job_name
        )

        print(f"\n{'='*60}")
        if result['completed']:
            if result['success']:
                print(f"SUCCESS! Extracted {result['total_tables']} tables")
            else:
                print(f"Job completed with state: {result['state']}")
        else:
            print(f"Job still processing: {result['state']}")
            print("\nPlease check again later.")
        print(f"{'='*60}")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
