#!/bin/bash

PDF_FILE=$1
if [ -z "$PDF_FILE" ]; then
  echo "Usage: $0 <pdf_file>"
  exit 1
fi

if [ ! -f "$PDF_FILE" ]; then
  echo "File not found: $PDF_FILE"
  exit 1
fi

FILENAME=$(basename -- "$PDF_FILE")
DIRNAME="${FILENAME%.*}_pages"
mkdir -p "$DIRNAME"

pdfseparate "$PDF_FILE" "$DIRNAME/page-%d.pdf"

echo "PDF pages extracted to $DIRNAME"
