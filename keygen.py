import hmac
import hashlib
import base64
import time

SECRET_KEY = b"m:B.+$=e&1]915iMp.QW.}Fmy*31!:L"  # Must match your main app secret key

def generate_license_key(expiry_timestamp=0):
    payload = str(expiry_timestamp).encode()
    signature = hmac.new(SECRET_KEY, payload, hashlib.sha256).digest()
    key = base64.urlsafe_b64encode(payload).decode() + "." + base64.urlsafe_b64encode(signature).decode()
    return key

if __name__ == "__main__":
    # Example: generate key that expires in 30 days
    expire_in_seconds = 30 * 24 * 60 * 60
    expiry_timestamp = int(time.time()) + expire_in_seconds
    license_key = generate_license_key(expiry_timestamp)
    print("Generated license key (expires in 30 days):")
    print(license_key)
