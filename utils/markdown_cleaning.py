import re
import glob
import os

def clean_marker_md(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_len = sum(len(l) for l in lines)

    # ══════════════════════════════════════════
    # PASS 1: LINE-BY-LINE (on raw text, before inline stripping)
    # ══════════════════════════════════════════
    filtered = []
    for line in lines:
        stripped = line.strip()

        # Skip image references: ![...](...)
        if re.match(r'^!\[.*?\]\(.*?\)$', stripped):
            continue

        # Skip footnote blocks: <span id="page-..."> ...
        if re.match(r'^<span id="page-', stripped):
            continue

        # Skip footnote blocks: [](#page-X-Y) or [text](#page-X-Y) ...
        if re.match(r'^\[.*?\]\(#page-\d+-\d+\)', stripped):
            continue

        # Skip footnote blocks starting with <sup>
        if re.match(r'^<sup>', stripped):
            continue
        if re.match(r'^<sup>&</sup>', stripped):
            continue
        if re.match(r'^\$?<sup>', stripped):
            continue

        # Skip standalone URLs
        if re.match(r'^https?://\S+\.?$', stripped):
            continue

        # Skip page artifacts: dashes/underscores
        if re.match(r'^[_\-=\\]{3,}$', stripped):
            continue
        if stripped in ['-', '_', '\\_', '—']:
            continue

        # Skip language markers: "EN EN", "**EN EN**"
        if re.match(r'^\*?\*?[A-Z]{2}\s+[A-Z]{2}\*?\*?$', stripped):
            continue

        # Skip standalone page numbers
        if re.match(r'^\d{1,3}$', stripped):
            continue

        # Skip document reference codes like "10349/19 MC/mz 1"
        if re.match(r'^\d{4,5}/\d{2}\s+\w+/\w+\s+\d+$', stripped):
            continue

        # Skip "LIFE 1.C **EN**" style lines
        if re.match(r'^LIFE\s+\d+\.\w+\s+\*?\*?\w{2}\*?\*?$', stripped):
            continue

        # Skip SWD reference lines: {SWD(2020) 284 final}
        if re.match(r'^\{SWD\(\d{4}\)\s+\d+\s+final\}$', stripped):
            continue

        filtered.append(line)

    text = ''.join(filtered)

    # ══════════════════════════════════════════
    # PASS 2: INLINE CLEANUP (strip markers within kept lines)
    # ══════════════════════════════════════════

    # Images (inline, not on their own line)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    # Footnote inline markers: <sup>13</sup>
    text = re.sub(r'<sup>\d+</sup>', '', text)
    text = re.sub(r'<sup>.*?</sup>', '', text)

    # Footnote links: [1](#page-1-0), [\(](#page-0-0) ), [](#page-0-3) 1 )
    text = re.sub(r'\[\d+\]\(#page-\d+-\d+\)', '', text)
    text = re.sub(r'\[\\?\(?\\?\)?\s*\]\(#page-\d+-\d+\)\s*\(?\s*\d*\s*\)?', '', text)
    text = re.sub(r'\[\s*\]\(#page-\d+-\d+\)\s*\d*\s*\)', '', text)
    text = re.sub(r'\(#page-\d+-\d+\)', '', text)

    # HTML anchors: <span id="page-X-Y"></span>
    text = re.sub(r'<span id="page-\d+-\d+">\s*</span>', '', text)
    # <img> tags
    text = re.sub(r'<img\s+.*?>', '', text)

    # LaTeX artifacts
    text = re.sub(r'\$<sup>.*?\$', '', text)
    text = re.sub(r'\$\^?\{?\d+\}?\$', '', text)

    # Clean bold headings: ## **Title** -> ## Title
    text = re.sub(r'^(#{1,6})\s+\*\*(.*?)\*\*\s*$', r'\1 \2', text, flags=re.MULTILINE)

    # ══════════════════════════════════════════
    # PASS 3: FINAL CLEANUP
    # ══════════════════════════════════════════
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^\s*-{3,}\s*$', '', text, flags=re.MULTILINE)
    text = text.strip() + '\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    cleaned_len = len(text)
    reduction = (1 - cleaned_len / original_len) * 100
    sections = re.findall(r'^#{1,3}\s+', text, re.MULTILINE)

    print(f"  Original:  {original_len:,} chars")
    print(f"  Cleaned:   {cleaned_len:,} chars")
    print(f"  Reduction: {reduction:.1f}%")
    print(f"  Sections:  {len(sections)} headings")
    print(f"  Saved to:  {output_path}")
    print()


if __name__ == "__main__":
    ############################################
    # EDIT THESE PATHS
    ############################################
    input_dir  = "./benchmark/ceb/"       # folder with .md files
    output_dir = "./benchmark/"      # folder for cleaned files
    ############################################

    md_files = sorted(glob.glob(os.path.join(input_dir, '**/*.md'), recursive=True))

    if not md_files:
        print(f"No .md files found in {input_dir}")
    else:
        print(f"Found {len(md_files)} Markdown file(s) in {input_dir}\n")
        os.makedirs(output_dir, exist_ok=True)

        for md in md_files:
            name = os.path.basename(md).replace('.md', '_cleaned.md')
            out = os.path.join(output_dir, name)
            print(f"Cleaning: {md}")
            clean_marker_md(md, out)

        print(f"Done! All cleaned files are in {output_dir}/")
