# 🖼️ DNS Image Uploader for Cloudflare

Αυτό το εργαλείο μετατρέπει οποιαδήποτε εικόνα (PNG, JPG κ.λπ.) σε **Base64**, τη σπάει σε κομμάτια μεγέθους DNS TXT και τα ανεβάζει αυτόματα ως **DNS TXT records** στο Cloudflare.

## ✨ Χαρακτηριστικά

- Υποστηρίζει οποιαδήποτε εικόνα
- Αυτόματη κωδικοποίηση σε Base64
- Split σε chunks μεγέθους 255 χαρακτήρων (DNS-safe)
- Αυτόματη δημιουργία ή ενημέρωση των TXT records
- Υποστήριξη CLI (Command Line Interface)

---

## 📦 Απαιτήσεις

- Python 3.8+
- Cloudflare API Token με δικαίωμα `Zone.DNS → Edit`
- Εγκατάσταση απαιτούμενων βιβλιοθηκών:
