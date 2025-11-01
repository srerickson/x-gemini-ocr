from google import genai
# from google.genai import types
import os
import argparse
import pathlib
import re
from dotenv import load_dotenv

load_dotenv()

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

    #print(f"response: ${response.text}")
    # Extract CSV data from the response
    csv_blocks = re.findall(r"```csv\n(.*?)\n```", response.text, re.DOTALL)

    if not csv_blocks:
        print("No tables found in the PDF.")
        return

    # Save each CSV block to a file
    for i, block in enumerate(csv_blocks):
        file_name = f"result/{pathlib.Path(pdf_file_path).name}-{i+1}.csv"
        with open(file_name, "w") as f:
            f.write(block)
        print(f"Saved table to {file_name}")

    print(f"\nSuccessfully extracted {len(csv_blocks)} tables.")


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
