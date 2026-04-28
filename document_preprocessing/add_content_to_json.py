import json
import re
import os

def parse_markdown_by_chunks(filepath):
    """
    Parses a markdown file into chunks based on specific delimiters.
    Extracts chunk number, page number, titles, subtitles, and content for each.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return None
    except Exception as e:
        print(f"Error reading input file '{filepath}': {e}")
        return None
    
    delimiter_pattern = r"^-{3,}\s*Chunk\s+(\d+)\s+\(page\s+(\d+),\s*starts at line\s+\d+\)\s*-{3,}\s*$"
    delimiters = list(re.finditer(delimiter_pattern, text, flags=re.MULTILINE))
    results = []

    if not delimiters:
        print("Warning: No chunk delimiters found. Processing file as a single chunk (Chunk 1).")
        chunk_text = text.strip()
        if chunk_text:
            chunk_num = 1
            page_num = None 
            headers = re.findall(r"^(#{1,4})\s+(.*)", chunk_text, re.MULTILINE)
            title_list = [h_text.strip() for level, h_text in headers if len(level) <= 2]
            subtitle_list = [h_text.strip() for level, h_text in headers if len(level) > 2]
            content_body = re.sub(r"^#{1,4}\s+.*", "", chunk_text, flags=re.MULTILINE).strip()
            content_body = "\n".join(line for line in content_body.splitlines() if line.strip())
            if content_body:
                results.append({
                    "chunk": chunk_num,
                    "page_number": page_num,
                    "titles": title_list,
                    "subtitles": subtitle_list,
                    "content": content_body
                })
        return results
    
    for i, match in enumerate(delimiters):
        if i == 0:
            continue

        prev_delimiter_match = delimiters[i-1]
        prev_delimiter_end = prev_delimiter_match.span()[1]
        
        chunk_text = text[prev_delimiter_end:match.span()[0]].strip()
        
        prev_chunk_num = int(prev_delimiter_match.group(1))
        prev_page_num = int(prev_delimiter_match.group(2))

        if chunk_text:
            headers = re.findall(r"^(#{1,4})\s+(.*)", chunk_text, re.MULTILINE)
            title_list = [h_text.strip() for level, h_text in headers if len(level) <= 2]
            subtitle_list = [h_text.strip() for level, h_text in headers if len(level) > 2]
            content_body = re.sub(r"^#{1,4}\s+.*", "", chunk_text, flags=re.MULTILINE).strip()
            content_body = "\n".join(line for line in content_body.splitlines() if line.strip())
            if content_body:
                results.append({
                    "chunk": prev_chunk_num,
                    "page_number": prev_page_num,
                    "titles": title_list,
                    "subtitles": subtitle_list,
                    "content": content_body
                })
    
    if delimiters:
        last_delimiter_match = delimiters[-1]
        last_delimiter_end = last_delimiter_match.span()[1]
        last_chunk_num = int(last_delimiter_match.group(1))
        last_page_num = int(last_delimiter_match.group(2))

        chunk_text = text[last_delimiter_end:].strip()
        if chunk_text:
            headers = re.findall(r"^(#{1,4})\s+(.*)", chunk_text, re.MULTILINE)
            title_list = [h_text.strip() for level, h_text in headers if len(level) <= 2]
            subtitle_list = [h_text.strip() for level, h_text in headers if len(level) > 2]
            content_body = re.sub(r"^#{1,4}\s+.*", "", chunk_text, flags=re.MULTILINE).strip()
            content_body = "\n".join(line for line in content_body.splitlines() if line.strip())
            if content_body:
                results.append({
                    "chunk": last_chunk_num,
                    "page_number": last_page_num,
                    "titles": title_list,
                    "subtitles": subtitle_list,
                    "content": content_body
                })

    results.sort(key=lambda x: x['chunk'])
    return results


import json



# if __name__ == "__main__":
#     # Percorsi dei file
#     input_md_path = "./documents/gender-equality-strategy-2020-2025_chunked.md"
#     input_json_path = "./documents/gender-equality-strategy-2020-2025_chunked_qa.json"
#     output_json_path = "./documents/gender-equality-strategy-2020-2025_qa.json"

#     # 1. Caricamento del contenuto dal Markdown (usando la tua funzione)
#     parsed_chunks_content = parse_markdown_by_chunks(input_md_path)

#     # 2. Creazione della Tabella di Lookup { numero_chunk: contenuto_testuale }
#     # Usiamo 'chunk' come chiave perché è il nome del campo nel tuo parser markdown
#     content_lookup = {item['chunk']: item['content'] for item in parsed_chunks_content}

#     # 3. Caricamento del JSON originale
#     with open(input_json_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     # 4. Iterazione e Merging dei dati
#     # Creiamo una nuova lista per i chunk aggiornati
#     updated_chunks = []

#     for chunk_metadata in data.get('chunks', []):
#         num = chunk_metadata.get("chunk_number")
        
#         # Creiamo una copia per non modificare l'originale durante l'iterazione
#         chunk_completo = chunk_metadata.copy()
        
#         # Cerchiamo il contenuto corrispondente nel lookup
#         # Se non trovato, mettiamo un valore di default o None
#         chunk_completo["content"] = content_lookup.get(num, None)
        
#         updated_chunks.append(chunk_completo)

#     # 5. Aggiornamento dell'oggetto principale e salvataggio
#     data['chunks'] = updated_chunks

#     with open(output_json_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

#     print(f"Merge completato. Creato file: {output_json_path}")


#     # Ora final_processed_chunks contiene gli oggetti completi di testo, 
#     # indipendentemente dall'ordine originale.

if __name__ == "__main__":
    # Percorso del file JSON con la nuova struttura (multi-source)
    input_json_path = "./legends/legends_all_chunked_qa.json"
    output_json_path = "./legends/legends_all_qa.json"
    
    # Directory dove si trovano i file markdown (.md) elencati in "source_file"
    md_directory = "./legends/chunked/"

    # 1. Carichiamo il JSON principale
    with open(input_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 2. Processiamo ogni sorgente
    for source in data.get('sources', []):
        file_name = source.get('source_file')
        md_path = os.path.join(md_directory, file_name)
        
        print(f"Processing source: {file_name}...")

        if not os.path.exists(md_path):
            print(f"Warning: File {file_name} not found in {md_directory}. Skipping.")
            continue

        # 3. Leggiamo il markdown specifico per questa sorgente
        # parse_markdown_by_chunks è la tua funzione definita in precedenza 
        parsed_content = parse_markdown_by_chunks(md_path)
        
        # 4. Creiamo il lookup table per i chunk di questo specifico file
        content_lookup = {item['chunk']: item['content'] for item in parsed_content}

        # 5. Inseriamo il contenuto in ogni chunk della sorgente attuale
        for chunk_data in source.get('chunks', []):
            num = chunk_data.get("chunk_number")
            
            # Mappatura sicura tramite ID
            if num in content_lookup:
                chunk_data["content"] = content_lookup[num]
            else:
                chunk_data["content"] = None
                print(f"  ! No content found for Chunk {num} in {file_name}")

    # 6. Salvataggio finale mantenendo la struttura originale
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nProcessing complete. Final file saved at: {output_json_path}")