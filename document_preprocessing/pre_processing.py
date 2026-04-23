import os
import marker
from marker.convert import convert_single_pdf
from marker.models import load_all_models
from marker.output import save_markdown

def convert_pdf_to_md(input_path, output_folder):
    # 1. Load the necessary AI models
    model_lst = load_all_models()
    
    # 2. Perform the conversion
    # full_text contains the markdown, images is a dict of extracted images
    full_text, images, out_metadata = convert_single_pdf(input_path, model_lst)
    
    # 3. Define output filename based on the input
    base_name = os.path.basename(input_path).replace(".pdf", "")
    
    # 4. Save the results
    save_markdown(output_folder, base_name, full_text, images, out_metadata)
    print(f"Conversion complete! File saved in: {output_folder}/{base_name}.md")

if __name__ == "__main__":
    input_file = "../documents/gender-equality-strategy-2026-2030.pdf"
    output_dir = "./documents/pre_processing_output"
    
    if os.path.exists(input_file):
        convert_pdf_to_md(input_file, output_dir)
    else:
        print(f"Error: {input_file} not found.")