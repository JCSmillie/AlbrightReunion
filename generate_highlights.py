#!/usr/bin/env python3
import os

LIGHTBOX_CSS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css"
LIGHTBOX_JS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"

ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_STYLE = "style.css"
INTRO_FILENAME = "intro.txt"
ATTENTION_IMAGE = "Attention.png"

def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def read_intro():
    intro_path = os.path.join(ROOT_DIR, INTRO_FILENAME)
    if not os.path.isfile(intro_path):
        return ""
    with open(intro_path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
        text = html_escape(raw)
        text = text.replace("\\\\n", "<br>").replace("\\r\\n", "<br>").replace("\\r", "<br>").replace("\\\\", "\\").replace("\n", "<br>")
        return f"<p class='intro'>{text}</p>"

def get_attention_image_html():
    attention_path = os.path.join(ROOT_DIR, ATTENTION_IMAGE)
    if os.path.isfile(attention_path):
        return (
            f'<div class="attention-box">'
            f'<img src="{ATTENTION_IMAGE}" alt="Important Announcement" class="attention-img">'
            f'</div>'
        )
    return ""

def get_pdf_links_html():
    pdfs = [f for f in os.listdir(ROOT_DIR) if f.lower().endswith(".pdf")]
    if not pdfs:
        return ""
    links = "".join(
        f'<li><a href="{pdf}" target="_blank">{pdf}</a></li>' for pdf in sorted(pdfs)
    )
    return (
        '<h2>Related Document Files</h2>'
        '<ul class="pdf-list">'
        f'{links}'
        '</ul>'
    )

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
  <link rel="stylesheet" href="../{TEMPLATE_STYLE}">
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

def generate_index_html(valid_years, intro_html, attention_html, pdf_html):
    links = "\n".join(
        f'<li><a href="{year}/highlights.html">{year}th Reunion Highlights</a></li>'
        for year in sorted(valid_years, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>Albright Reunion Gallery</title>
  <link rel="stylesheet" href="{TEMPLATE_STYLE}">
</head>
<body>
  <h1>Welcome to the Albright Family Reunion Gallery</h1>
  {attention_html}
  {intro_html}
  <ul class="reunion-links">
    {links}
  </ul>
  {pdf_html}
</body>
</html>"""

def generate_all_highlights():
    valid_years = []
    for year in os.listdir(ROOT_DIR):
        year_path = os.path.join(ROOT_DIR, year)
        gallery_path = os.path.join(year_path, "gallery")
        highlights_path = os.path.join(year_path, "highlights.html")

        if not os.path.isdir(year_path) or not os.path.isdir(gallery_path):
            continue

        all_images = os.listdir(gallery_path)
        highlights = [img for img in sorted(all_images) if img.startswith("highlight") and img.lower().endswith(".jpg")]
        if "family_group.jpg" in all_images:
            highlights.insert(0, "family_group.jpg")

        if not highlights:
            continue

        with open(highlights_path, "w") as f:
            f.write(generate_highlights_html(year, highlights))
        print(f"Generated highlights.html for {year} ({len(highlights)} images)")
        valid_years.append(year)

    # Write updated index.html
    if valid_years:
        intro_html = read_intro()
        attention_html = get_attention_image_html()
        pdf_html = get_pdf_links_html()
        index_path = os.path.join(ROOT_DIR, "index.html")
        with open(index_path, "w") as f:
            f.write(generate_index_html(valid_years, intro_html, attention_html, pdf_html))
        print(f"Updated index.html with {len(valid_years)} reunion year(s).")

if __name__ == "__main__":
    generate_all_highlights()

