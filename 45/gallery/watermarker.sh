#!/bin/bash

INPUT_DIR="."
OUTPUT_DIR="watermarked"
FONT_PATH="/System/Library/Fonts/Supplemental/Arial.ttf"  # Or another available TTF
TEXT="© Jesse C Smillie 2025"

mkdir -p "$OUTPUT_DIR"

# Loop through *.jpg and *.JPG files
for img in "$INPUT_DIR"/*.[jJ][pP][gG]; do
  [ -e "$img" ] || continue  # skip if no match

  # Normalize output name to lowercase .jpg
  base=$(basename "$img")
  base_no_ext="${base%.*}"
  output="$OUTPUT_DIR/${base_no_ext}.jpg"

  echo "Watermarking: $img → $output"

  magick "$img" \
    -font "$FONT_PATH" \
    -gravity SouthEast \
    -pointsize 36 \
    -fill white \
    -annotate +10+10 "$TEXT" \
    "$output"
done

