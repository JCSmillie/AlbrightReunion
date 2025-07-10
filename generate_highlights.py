#!/usr/bin/env python3
import os

LIGHTBOX_CSS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css"
LIGHTBOX_JS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"

YEARS = ["45", "40", "35", "30"]  # You can adjust this list as needed
ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_STYLE = "../style.css"

def generate_highlights_html(year, images):
    image_tags = "\n".join(
        f'<a href="gallery/{img}" data-lightbox="{year}th" data-title="Right-click to save">'
        f'<img src="gallery/{img}" width="300"></a>'
        for img in images
    )
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>{year}th Reunion Highlights</title>
  <link rel="stylesheet" href="{TEMPLATE_STYLE}">
  <link rel="stylesheet" href="{LIGHTBOX_CSS}">
</head>
<body>
  <h1>{year}th Albright Reunion - Highlights</h1>
  {image_tags}
  <p><a href="gallery/">View all photos from the {year}th Reunion</a></p>
  <p><a href="../index.html">← Back to Home</a></p>
  <script src="{LIGHTBOX_JS}"></script>
</body>
</html>"""

def generate_all_highlights():
    for year in YEARS:
        gallery_path = os.path.join(ROOT_DIR, year, "gallery")
        highlights_path = os.path.join(ROOT_DIR, year, "highlights.html")

        if not os.path.exists(gallery_path):
            print(f"Skipping {year}: gallery folder does not exist.")
            continue

        all_images = os.listdir(gallery_path)
        highlights = [img for img in sorted(all_images) if img.startswith("highlight") and img.lower().endswith(".jpg")]
        if "family_group.jpg" in all_images:
            highlights.insert(0, "family_group.jpg")

        if not highlights:
            print(f"No highlights found for {year}")
            continue

        with open(highlights_path, "w") as f:
            f.write(generate_highlights_html(year, highlights))
        print(f"Generated highlights.html for {year} ({len(highlights)} images)")

if __name__ == "__main__":
    generate_all_highlights()
