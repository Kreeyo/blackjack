from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import time

app = Flask(__name__)

# Secret key for signing licenses - KEEP THIS PRIVATE!
SECRET_KEY = b"m:B.+$=e&1]915iMp.QW.}Fmy*31!:L"  # Use your own secure key here

def validate_license_key(key):
    """
    Validate license key string.
    Returns (True, expiry_timestamp) if valid and not expired,
    or (False, reason_string) if invalid or expired.
    """
    try:
        payload_b64, signature_b64 = key.split(".")
        payload = base64.urlsafe_b64decode(payload_b64.encode())
        signature = base64.urlsafe_b64decode(signature_b64.encode())
    except Exception:
        return False, "Malformed license key"

    expected_sig = hmac.new(SECRET_KEY, payload, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_sig, signature):
        return False, "Invalid license signature"

    expiry_timestamp = int(payload.decode())
    if expiry_timestamp != 0 and time.time() > expiry_timestamp:
        return False, "License key expired"

    return True, expiry_timestamp

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify({"valid": False, "error": "No license key provided"}), 400
    valid, result = validate_license_key(key)
    if valid:
        return jsonify({"valid": True, "expiry": result})
    else:
        return jsonify({"valid": False, "error": result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
