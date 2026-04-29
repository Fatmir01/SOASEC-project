import json
import re
import os



import json


# if __name__ == "__main__":
#     # Percorso del file JSON con la nuova struttura (multi-source)
#     factoid_path = "./legends/legends_factoid_qa.json"
#     non_factoid_path = "./legends/legends_non_factoid_qa.json"
    
#     output_json_path = "./legends/legends_qa.json"


#     # 1. Carichiamo il JSON principale
#     with open(factoid_path, 'r', encoding='utf-8') as file:
#         factoid_qa = json.load(file)
        
#     with open(non_factoid_path, 'r', encoding='utf-8') as file:
#         non_factoid_qa = json.load(file)


#     non_factoid_lookup = {item['source_file']: item['chunks'] for item in non_factoid_qa.get('sources', [])}


#     # 2. Processiamo ogni sorgente
#     for source in factoid_qa.get('sources', []):
#         file_name = source.get('source_file')
        
        

#         # 5. Inseriamo il contenuto in ogni chunk della sorgente attuale
#         for chunk_data in source.get('chunks', []):
#             num = chunk_data.get("chunk_number")
            
#             non_factoid_lookup_source = {item['chunk_number']: item['qa_pairs'] for item in non_factoid_lookup[file_name]}
            
            
#             # Mappatura sicura tramite ID
#             if num in non_factoid_lookup_source:
#                 chunk_data["qa_pairs"] = chunk_data["qa_pairs"] + non_factoid_lookup_source[num]
#             else:
#                 print(f"  ! No content found for Chunk {num} in {file_name}")

#     # 6. Salvataggio finale mantenendo la struttura originale
#     with open(output_json_path, 'w', encoding='utf-8') as f:
#         json.dump(factoid_qa, f, indent=2, ensure_ascii=False)

#     print(f"\nProcessing complete. Final file saved at: {output_json_path}")




if __name__ == "__main__":
    # Percorso del file JSON con la nuova struttura (multi-source)
    factoid_path = "./documents/gender-equality-strategy-2020-2025_factoid_qa.json"
    non_factoid_path = "./documents/gender-equality-strategy-2020-2025_non_factoid_qa.json"
    
    output_json_path = "./documents/gender-equality-strategy-2020-2025_qa.json"


    # 1. Carichiamo il JSON principale
    with open(factoid_path, 'r', encoding='utf-8') as file:
        factoid_qa = json.load(file)
        
    with open(non_factoid_path, 'r', encoding='utf-8') as file:
        non_factoid_qa = json.load(file)


    non_factoid_lookup = {item['chunk_number']: item['qa_pairs'] for item in non_factoid_qa.get('chunks', [])}


    # 2. Processiamo ogni sorgente
    for chunk in factoid_qa.get('chunks', []):
        num = chunk.get("chunk_number")
        
        # Mappatura sicura tramite ID
        if num in non_factoid_lookup:
            chunk["qa_pairs"] = chunk["qa_pairs"] + non_factoid_lookup[num]
        else:
            print(f"  ! No content found for Chunk {num}")

    # 6. Salvataggio finale mantenendo la struttura originale
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(factoid_qa, f, indent=2, ensure_ascii=False)

    print(f"\nProcessing complete. Final file saved at: {output_json_path}")