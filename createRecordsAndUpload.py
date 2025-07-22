import base64
import textwrap
import requests
import os
import argparse

CHUNK_SIZE = 255  # DNS TXT record size limit

def encode_image_to_chunks(path, chunk_size):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode("ascii")
    return textwrap.wrap(b64, chunk_size)

def get_existing_txt_record(zone_id, name, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=TXT&name={name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        if results["success"] and results["result"]:
            return results["result"][0]["id"]
    return None

def create_or_update_txt_record(zone_id, name, content, headers):
    record_id = get_existing_txt_record(zone_id, name, headers)
    if record_id:
        print(f"🔄 Updating existing record: {name}")
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        method = requests.put
    else:
        print(f"🆕 Creating new record: {name}")
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        method = requests.post

    payload = {
        "type": "TXT",
        "name": name,
        "content": content,
        "ttl": 120,
        "proxied": False
    }

    response = method(url, headers=headers, json=payload)
    if response.status_code == 200 and response.json().get("success"):
        print(f"✅ Record saved: {name}")
    else:
        print(f"❌ Failed for {name}: {response.text}")

def upload_image_as_txt(image_path, prefix, domain, zone_id, api_token):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    chunks = encode_image_to_chunks(image_path, CHUNK_SIZE)
    for i, chunk in enumerate(chunks):
        full_record = f"{prefix}.{i}.{domain}"
        create_or_update_txt_record(zone_id, full_record, chunk, headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload an image as DNS TXT records to Cloudflare.")
    parser.add_argument("--file", required=True, help="Path to the image file")
    parser.add_argument("--prefix", required=True, help="Prefix for the DNS TXT records")
    parser.add_argument("--domain", required=True, help="Base domain name")
    parser.add_argument("--zone-id", required=True, help="Cloudflare Zone ID")
    parser.add_argument("--token", required=True, help="Cloudflare API Token")

    args = parser.parse_args()

    upload_image_as_txt(args.file, args.prefix, args.domain, args.zone_id, args.token)
