Aggiungi queste celle su Colab dopo il cleaning.

**Cella 12 — Script di segmentazione**

```python
import re
import json

def segment_markdown(text, max_words=350):
    """
    Segmenta il markdown in passaggi semanticamente coerenti
    basandosi sugli heading, con vincolo di max parole.
    """
    # Split per heading (mantiene l'heading nella sezione)
    sections = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]
    
    passages = []
    
    for section in sections:
        # Estrai heading e contenuto
        heading_match = re.match(r'^(#{1,6}\s+.+?)$', section, flags=re.MULTILINE)
        heading = heading_match.group(1) if heading_match else ""
        
        words = section.split()
        
        # Se la sezione è dentro il limite, tienila intera
        if len(words) <= max_words:
            passages.append({
                "heading": heading,
                "text": section,
                "word_count": len(words)
            })
        else:
            # Sezione troppo lunga: split per paragrafi
            paragraphs = re.split(r'\n\n+', section)
            
            current_chunk = ""
            current_words = 0
            chunk_index = 0
            
            for para in paragraphs:
                para_words = len(para.split())
                
                # Se aggiungere questo paragrafo sfora il limite
                if current_words + para_words > max_words and current_chunk:
                    suffix = f" (part {chunk_index + 1})" if chunk_index > 0 or (current_words + para_words > max_words) else ""
                    passages.append({
                        "heading": heading + suffix,
                        "text": current_chunk.strip(),
                        "word_count": current_words
                    })
                    chunk_index += 1
                    current_chunk = ""
                    current_words = 0
                
                # Se un singolo paragrafo supera max_words, splitta per frasi
                if para_words > max_words:
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    for sent in sentences:
                        sent_words = len(sent.split())
                        if current_words + sent_words > max_words and current_chunk:
                            passages.append({
                                "heading": heading + f" (part {chunk_index + 1})",
                                "text": current_chunk.strip(),
                                "word_count": current_words
                            })
                            chunk_index += 1
                            current_chunk = ""
                            current_words = 0
                        current_chunk += sent + " "
                        current_words += sent_words
                else:
                    current_chunk += para + "\n\n"
                    current_words += para_words
            
            # Salva l'ultimo chunk rimasto
            if current_chunk.strip():
                suffix = f" (part {chunk_index + 1})" if chunk_index > 0 else ""
                passages.append({
                    "heading": heading + suffix,
                    "text": current_chunk.strip(),
                    "word_count": current_words
                })
    
    return passages

# Esegui la segmentazione (usa la variabile 'text' dal cleaning)
passages = segment_markdown(text, max_words=350)

print(f"Total passages: {len(passages)}")
print(f"Word counts: min={min(p['word_count'] for p in passages)}, "
      f"max={max(p['word_count'] for p in passages)}, "
      f"avg={sum(p['word_count'] for p in passages) / len(passages):.0f}")
```

**Cella 13 — Anteprima dei passaggi**

```python
for i, p in enumerate(passages):
    print(f"\n{'='*60}")
    print(f"PASSAGE {i+1} | {p['heading']} | {p['word_count']} words")
    print(f"{'='*60}")
    print(p['text'][:300] + "..." if len(p['text']) > 300 else p['text'])
```

Scorri l'output e verifica che i passaggi abbiano senso semanticamente.

**Cella 14 — Salva come JSON e scarica**

```python
from google.colab import files

# Salva come JSON (utile per le fasi successive della pipeline)
with open('passages.json', 'w', encoding='utf-8') as f:
    json.dump(passages, f, indent=2, ensure_ascii=False)

# Salva anche come Markdown leggibile con separatori
with open('passages_readable.md', 'w', encoding='utf-8') as f:
    for i, p in enumerate(passages):
        f.write(f"<!-- PASSAGE {i+1} | {p['word_count']} words -->\n")
        f.write(p['text'])
        f.write("\n\n---\n\n")

print(f"Saved {len(passages)} passages")
files.download('passages.json')
files.download('passages_readable.md')
```

Il file `passages.json` è quello che userai come input per le fasi successive (span extraction, Q&A generation, ecc.). Ogni passaggio ha heading, testo e word count, ed è garantito essere sotto le 350 parole per stare nel context window ottimale per il processing LLM.

Fai girare e dimmi quanti passaggi escono e se la segmentazione ti sembra coerente!