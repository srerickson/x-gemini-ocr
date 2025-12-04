#!/bin/bash
PDF_FILE="Columbia-FB.pdf"
PAGES_DIR="pages"

if [ ! -f "$PDF_FILE" ]; then
  echo "File not found: $PDF_FILE"
  exit 1
fi

FILENAME=$(basename -- "$PDF_FILE")
mkdir -p "$PAGES_DIR"

pdfseparate -f 6 -l 190 "$PDF_FILE" "$PAGES_DIR/page-%03d.pdf"

echo "PDF pages extracted to $PAGES_DIR/"

# Convert each PDF to JPG
echo "Converting PDFs to JPGs..."
for pdf_file in "$PAGES_DIR"/*.pdf; do
  if [ -f "$pdf_file" ]; then
    # Get the base name without extension
    base_name=$(basename "$pdf_file" .pdf)
    # Convert to JPG using pdftoppm
    pdftoppm -jpeg -singlefile "$pdf_file" "$PAGES_DIR/$base_name"
    echo "Converted $base_name.pdf to $base_name.jpg"
  fi
done

echo "Conversion complete!"
