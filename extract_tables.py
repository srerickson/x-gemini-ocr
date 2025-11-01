from google import genai
from google.genai import types
import os
import argparse
import pathlib
import re
import json
from dotenv import load_dotenv

load_dotenv()

def save_csv_blocks_from_response(response_text, pdf_file_path):
    """
    Extracts CSV blocks from a response text and saves them to files.

    Args:
        response_text (str): The response text containing CSV blocks
        pdf_file_path (str): The path to the source PDF file (used for naming)

    Returns:
        int: The number of CSV blocks saved
    """
    csv_blocks = re.findall(r"```csv\n(.*?)\n```", response_text, re.DOTALL)

    if not csv_blocks:
        print(f"No tables found in {pathlib.Path(pdf_file_path).name}")
        return 0

    # Save each CSV block to a file
    for i, block in enumerate(csv_blocks):
        file_name = f"result/{pathlib.Path(pdf_file_path).stem}-{i+1}.csv"
        with open(file_name, "w") as f:
            f.write(block)
        print(f"Saved table to {file_name}")

    return len(csv_blocks)

def extract_and_save_tables(api_key, prompt_path, pdf_file_path):
    """
    Extracts tables from a PDF file using the Gemini API and saves them as CSV files.

    Args:
        api_key (str): Your Google API key for the Gemini API.
        prompt_path: path to prompt text
        pdf_file_path (str): The path to the PDF file.
    """
    client = genai.Client(api_key=api_key)

    prompt = pathlib.Path(prompt_path).read_text()

    # Upload the PDF file
    print(f"Uploading file: {pdf_file_path}")
    uploaded_file = client.files.upload(file=pdf_file_path,
                                        config=dict(mime_type='application/pdf'))
    print(f"Completed upload: {uploaded_file.uri}")

    # Create the Gemini model

    # Generate content
    print("Generating content from the model...")
    response = client.models.generate_content(
        model = "gemini-2.5-pro",
        contents = [uploaded_file, prompt]
    )

    # Save CSV blocks from response
    num_tables = save_csv_blocks_from_response(response.text, pdf_file_path)

    if num_tables > 0:
        print(f"\nSuccessfully extracted {num_tables} tables.")


def create_batch_job(api_key, prompt_path, pdf_file_paths, model="gemini-2.5-pro"):
    """
    Creates a batch job to process multiple PDF files using the Gemini Batch API.

    Args:
        api_key (str): Your Google API key for the Gemini API.
        prompt_path (str): Path to the prompt text file.
        pdf_file_paths (list): List of paths to PDF files to process.
        model (str): The model to use (default: gemini-2.5-pro).

    Returns:
        str: The batch job name/ID for retrieving results later.
    """
    client = genai.Client(api_key=api_key)
    prompt = pathlib.Path(prompt_path).read_text()

    # Upload all PDF files and create batch requests
    print(f"Uploading {len(pdf_file_paths)} PDF files...")
    batch_requests = []

    for pdf_path in pdf_file_paths:
        print(f"  Uploading: {pdf_path}")
        uploaded_file = client.files.upload(
            file=pdf_path,
            config=types.UploadFileConfig(mime_type='application/pdf')
        )

        # Create request for this PDF
        request = {
            "contents": [
                {"parts": [{"file_data": {"file_uri": uploaded_file.uri, "mime_type": "application/pdf"}}]},
                {"parts": [{"text": prompt}], "role": "user"}
            ]
        }

        batch_requests.append({
            "key": pathlib.Path(pdf_path).stem,
            "request": request
        })

    # Create JSONL content
    jsonl_content = "\n".join([json.dumps(req) for req in batch_requests])

    # Upload JSONL file
    print("\nCreating batch job...")
    jsonl_path = "batch_requests.jsonl"
    with open(jsonl_path, "w") as f:
        f.write(jsonl_content)

    uploaded_jsonl = client.files.upload(
        file=jsonl_path,
        config=types.UploadFileConfig(
            display_name='pdf-extraction-batch',
            mime_type='text/plain'
        )
    )

    # Create batch job
    batch_job = client.batches.create(
        model=f"models/{model}",
        src=uploaded_jsonl.name,
        config={'display_name': 'pdf-table-extraction-batch'}
    )

    print(f"\nBatch job created successfully!")
    print(f"Job name: {batch_job.name}")
    print(f"Job state: {batch_job.state.name}")

    # Clean up local JSONL file
    os.remove(jsonl_path)

    return batch_job.name


def check_and_save_batch_results(api_key, batch_job_name):
    """
    Checks the status of a batch job and saves results when complete.

    Args:
        api_key (str): Your Google API key for the Gemini API.
        batch_job_name (str): The batch job name/ID returned from create_batch_job.

    Returns:
        dict: Status information including state and results summary.
    """
    client = genai.Client(api_key=api_key)

    # Get batch job status
    print(f"Checking batch job: {batch_job_name}")
    batch_job = client.batches.get(name=batch_job_name)

    print(f"Current state: {batch_job.state.name}")

    completed_states = {'JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED',
                        'JOB_STATE_CANCELLED', 'JOB_STATE_EXPIRED'}

    if batch_job.state.name not in completed_states:
        print(f"Job is still processing. Current state: {batch_job.state.name}")
        return {
            'state': batch_job.state.name,
            'completed': False
        }

    # Handle failed jobs
    if batch_job.state.name != 'JOB_STATE_SUCCEEDED':
        print(f"Job ended with state: {batch_job.state.name}")
        return {
            'state': batch_job.state.name,
            'completed': True,
            'success': False
        }

    # Process successful results
    print("\nJob completed successfully! Processing results...")

    total_tables = 0

    if batch_job.dest and batch_job.dest.file_name:
        # Results are in a file
        result_file_name = batch_job.dest.file_name
        file_content = client.files.download(file=result_file_name)
        result_lines = file_content.decode('utf-8').strip().split('\n')

        for line in result_lines:
            result = json.loads(line)
            pdf_key = result.get('key')

            if 'response' in result and result['response']:
                response_text = result['response'].get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if response_text:
                    # Use the key as the pseudo-filename for saving
                    num_tables = save_csv_blocks_from_response(response_text, pdf_key + '.pdf')
                    total_tables += num_tables
            elif 'error' in result:
                print(f"Error processing {pdf_key}: {result['error']}")

    elif batch_job.dest and batch_job.dest.inlined_responses:
        # Results are inline
        for inline_response in batch_job.dest.inlined_responses:
            if inline_response.response:
                # Extract the key from somewhere in the response structure
                response_text = inline_response.response.text
                # We don't have the key easily accessible in inline responses
                # So we'll use a generic naming
                num_tables = save_csv_blocks_from_response(response_text, f"batch-result.pdf")
                total_tables += num_tables
            elif inline_response.error:
                print(f"Error in response: {inline_response.error}")

    print(f"\nBatch processing complete! Extracted {total_tables} total tables.")

    return {
        'state': batch_job.state.name,
        'completed': True,
        'success': True,
        'total_tables': total_tables
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from a PDF file using the Gemini API.")
    parser.add_argument("pdf_file", help="The path to the PDF file.")
    parser.add_argument("prompt_file", help="that path to the prompt", default="prompt.md")
    args = parser.parse_args()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please create a .env file with your API key or set the environment variable.")
    else:
        extract_and_save_tables(api_key, args.prompt_file, args.pdf_file)
