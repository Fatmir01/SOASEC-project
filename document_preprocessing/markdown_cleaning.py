import re

def clean_marker_md(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_len = sum(len(l) for l in lines)
    cleaned = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip image references: ![...](...) 
        if re.match(r'^!\[.*?\]\(.*?\)$', stripped):
            continue
        
        # Skip footnote block lines starting with <sup> patterns
        if re.match(r'^<sup>', stripped):
            continue
        if re.match(r'^<sup>&</sup>', stripped):
            continue
        if re.match(r'^\$?<sup>', stripped):
            continue
            
        # Skip standalone URLs (footnote leftovers)
        if re.match(r'^https?://\S+\.?$', stripped):
            continue
        
        # Skip lines that are just a dash/underscore (page artifacts)
        if stripped in ['-', '_', '\_']:
            continue
            
        # Skip "EN EN" language marker
        if stripped in ['**EN EN**', 'EN EN']:
            continue
            
        # Skip orphaned footnote fragments
        if stripped in ['Fundamental Rights.', 'pornography.', 
                        'and men in the European Union in 2014-2015.']:
            continue

        # Skip lines that are ONLY a footnote reference number + text starting with
        # a known footnote pattern (number followed by space and typical footnote content)
        # But be very specific: only match lines where the number is clearly a footnote
        # (preceded by nothing, and the content looks like a citation/reference)
        if re.match(r'^\d{2,}\s+(In particular|Eurostat|For instance|For existing|This includes|One of|Maldonado|Relevant|Positive|Regulation|Recent|See,|See )', stripped):
            continue
        
        # Remove inline footnote markers: <sup>13</sup> etc.
        line = re.sub(r'<sup>\d+</sup>', '', line)
        # Remove remaining <sup>...</sup> inline
        line = re.sub(r'<sup>.*?</sup>', '', line)
        
        # Remove LaTeX artifacts
        line = re.sub(r'\$<sup>.*?\$', '', line)
        line = re.sub(r'\$\^?\{?\d+\}?\$', '', line)
        
        # Remove image refs that might be inline (not on their own line)
        line = re.sub(r'!\[.*?\]\(.*?\)', '', line)
        
        # Clean bold markers around headings: ## **Title** -> ## Title  
        line = re.sub(r'^(#{1,6})\s+\*\*(.*?)\*\*\s*$', r'\1 \2\n', line)
        
        # Strip trailing whitespace
        line = line.rstrip() + '\n'
        
        cleaned.append(line)
    
    text = ''.join(cleaned)
    
    # Consolidate multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove page separator lines
    text = re.sub(r'^\s*-{3,}\s*$', '', text, flags=re.MULTILINE)
    
    text = text.strip() + '\n'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    cleaned_len = len(text)
    reduction = (1 - cleaned_len / original_len) * 100
    
    # Count sections
    sections = re.findall(r'^#{1,3}\s+', text, re.MULTILINE)
    
    print(f"Original:  {original_len:,} chars")
    print(f"Cleaned:   {cleaned_len:,} chars")
    print(f"Reduction: {reduction:.1f}%")
    print(f"Sections:  {len(sections)} headings found")
    print(f"Saved to:  {output_path}")

clean_marker_md('/home/claude/input.md', '/home/claude/regulation_cleaned_v2.md')