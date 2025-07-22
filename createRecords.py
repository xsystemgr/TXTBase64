import base64
import textwrap

# === Ρυθμίσεις ===
image_path = "logo.png"                     # 🖼 Βάλε το αρχείο εικόνας σου εδώ
record_prefix = "photo"                     # π.χ. photo.0.example.com
domain = "example.com."                     # Με τελεία στο τέλος
output_file = "dns_records.txt"             # Εξαγόμενο αρχείο
chunk_size = 255                            # Το όριο του DNS TXT string

def encode_image_to_base64_chunks(path, chunk_size):
    with open(path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode('ascii')
    return textwrap.wrap(b64_data, chunk_size)

def generate_txt_records(chunks, prefix, domain):
    records = []
    for i, chunk in enumerate(chunks):
        record_name = f"{prefix}.{i}.{domain}"
        # Αν χρειαστεί split σε πολλαπλά strings (π.χ. για BIND-style multiline TXT)
        string_parts = textwrap.wrap(chunk, chunk_size)
        txt_lines = ' '.join(f'"{part}"' for part in string_parts)
        records.append(f'{record_name} IN TXT {txt_lines}')
    return records

def save_records_to_file(records, filename):
    with open(filename, "w") as f:
        f.write("\n".join(records))
    print(f"✅ DNS records αποθηκεύτηκαν στο {filename}")

if __name__ == "__main__":
    chunks = encode_image_to_base64_chunks(image_path, chunk_size)
    records = generate_txt_records(chunks, record_prefix, domain)
    save_records_to_file(records, output_file)
