from google import genai
from google.genai import types
import os
import argparse
import pathlib
import re
import mimetypes
from dotenv import load_dotenv

def csv_blocks(response: types.GenerateContentResponse):
    blocks = re.findall(r"```csv\n(.*?)\n```", response.text, re.DOTALL)
    if not blocks:
        raise ValueError(f"no CSV blocks found in response: '{response.text}'")
    return blocks

def generate_content(client: genai.Client, prompt_path: str, file_paths: list[str], model: str = "gemini-3-pro-preview") -> types.GenerateContentResponse:
    """
    Generates content using the Gemini API with a prompt and arbitrary files.
    Args:
        client: Gemini Client.
        prompt_path: Path to prompt text file.
        file_paths: List of file paths to include in the request.
        model: Model name to use (default: gemini-3-pro-preview).
    """
    contents = [types.Part.from_text(text = pathlib.Path(prompt_path).read_text())]
    for file_path in file_paths:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            # Fallback to application/octet-stream if type cannot be determined
            mime_type = 'application/octet-stream'
        file_part = types.Part.from_bytes(
            data=pathlib.Path(file_path).read_bytes(),
            mime_type=mime_type
        )
        contents.append(file_part)
    return client.models.generate_content(
        model=model,
        contents=contents
    )

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Extract tables from files using the Gemini API.")
    parser.add_argument("page", help="zero-padded page number (e.g., 036)")
    args = parser.parse_args()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key, vertexai=True)
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please create a .env file with your API key or set the environment variable.")
        return
    prompt_file = "prompt.md"
    pdf_file = f"pages/page-{args.page}.pdf"
    jpg_file = f"pages/page-{args.page}.jpg"
    response = generate_content(client, prompt_file, [pdf_file, jpg_file])
    for i, block in enumerate(csv_blocks(response)):
        file_name = f"result/page-{args.page}-{i+1}.csv"
        with open(file_name, "w") as f:
            f.write(block)
        print(f"Saved table to {file_name}")

if __name__ == "__main__":
    main()