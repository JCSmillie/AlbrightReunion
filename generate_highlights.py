#!/usr/bin/env python3
import os

LIGHTBOX_CSS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css"
LIGHTBOX_JS = "https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"

ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_STYLE = "../style.css"
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

def generate_downloadable_html(year, images, relative_style="../style.css"):
    items = "\n".join(
        f'<div style="margin-bottom: 20px;">'
        f'<img src="{img}" width="300"><br>'
        f'<a href="{img}" download class="download-link">Download the Photo Above</a>'
        f'</div>'
        for img in images
    )
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>{year}th Reunion - All Photos</title>
  <link rel="stylesheet" href="{relative_style}">
</head>
<body>
  <h1>{year}th Reunion - Full Photo Set</h1>
  <div class="photo-header">Browse and Download Any Memory</div>
  {items}
  <p><a href="../highlights.html">← Back to Highlights</a></p>
</body>
</html>"""

def generate_highlights_html(year, images):
    image_blocks = "\n".join(
        f'<div style="margin-bottom: 25px;">'
        f'<a href="gallery/{img}" data-lightbox="{year}th" data-title="Right-click to save">'
        f'<img src="gallery/{img}" width="300"></a><br>'
        f'<a href="gallery/{img}" download class="download-link">Download the Photo Above</a>'
        f'</div>'
        for img in images
    )
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>{year}th Reunion Highlights</title>
  <link rel="stylesheet" href="../style.css">
  <link rel="stylesheet" href="{LIGHTBOX_CSS}">
</head>
<body>
  <h1>{year}th Albright Reunion - Highlights</h1>
  <div class="photo-header">Memories Worth a Thousand Words</div>
  {image_blocks}
  <p><a href="gallery/index.html">View all photos from the {year}th Reunion</a></p>
  <p><a href="../index.html">← Back to Home</a></p>
  <script src="{LIGHTBOX_JS}"></script>
</body>
</html>"""

def generate_index_html(valid_years, intro_html, attention_html, pdf_html):
    links = "\n".join(
        f'<li><a href="{year}/highlights.html">{year}th Reunion Photos and Other Highlights</a></li>'
        for year in sorted(valid_years, reverse=True)
    )
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>Albright Reunion Gallery</title>
  <link rel="stylesheet" href="style.css">
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

        all_images = sorted([
            img for img in os.listdir(gallery_path)
            if img.lower().endswith(".jpg")
        ])
        highlights = [img for img in all_images if img.startswith("highlight")]
        if "family_group.jpg" in all_images:
            highlights.insert(0, "family_group.jpg")

        if not highlights:
            continue

        # Generate highlights.html
        with open(highlights_path, "w") as f:
            f.write(generate_highlights_html(year, highlights))

        # Generate gallery index.html
        gallery_index_path = os.path.join(gallery_path, "index.html")
        with open(gallery_index_path, "w") as f:
            f.write(generate_downloadable_html(year, all_images, relative_style="../../style.css"))

        print(f"Generated highlights and gallery index for {year} ({len(highlights)} highlights, {len(all_images)} total)")
        valid_years.append(year)

    # Update homepage index.html
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

