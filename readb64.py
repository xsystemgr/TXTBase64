import dns.resolver
import base64
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

BASE_DOMAIN = "photo"
DOMAIN_SUFFIX = "example.com"
MAX_PARTS = 10

def get_txt_chunks(base, suffix, max_parts):
    chunks = []
    for i in range(max_parts):
        subdomain = f"{base}.{i}.{suffix}"
        try:
            answers = dns.resolver.resolve(subdomain, 'TXT')
            for r in answers:
                part = ''.join([s.strip('"') for s in r.strings])
                chunks.append(part)
        except dns.resolver.NXDOMAIN:
            break  # Δεν υπάρχει άλλο κομμάτι
        except Exception as e:
            print(f"Σφάλμα στο {subdomain}: {e}")
            break
    return ''.join(chunks)

def show_image_from_base64(base64_data):
    try:
        img_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(img_data))

        root = tk.Tk()
        root.title("Εικόνα από πολλαπλά TXT Records")
        tk_img = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=tk_img)
        label.pack()
        root.mainloop()
    except Exception as e:
        print(f"Σφάλμα κατά την εμφάνιση της εικόνας: {e}")

if __name__ == "__main__":
    b64_combined = get_txt_chunks(BASE_DOMAIN, DOMAIN_SUFFIX, MAX_PARTS)
    if b64_combined:
        show_image_from_base64(b64_combined)
    else:
        print("Δεν βρέθηκαν δεδομένα Base64.")
