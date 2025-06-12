import cv2
import numpy as np
from flask import Flask, request, Response, make_response, send_from_directory
import threading
import os

app = Flask(__name__)
frame = None
frame_event = threading.Event()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    global frame
    if request.method == 'OPTIONS':
        # CORS preflight
        resp = make_response('', 204)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    img_bytes = request.data
    if not img_bytes:
        return ('No image data', 400)
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    if img_np.size == 0:
        return ('Empty image buffer', 400)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if img is None:
        return ('Failed to decode image', 400)
    frame = img
    frame_event.set()  # Signal new frame
    return ('', 204)

@app.route('/')
def index():
    return 'Webcam receiver is running.'

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

def show_frames():
    import pyvirtualcam
    global frame
    cam = None
    last_shape = None
    while True:
        frame_event.wait()  # Wait for a new frame
        frame_event.clear()
        if frame is not None:
            height, width = frame.shape[:2]
            # If resolution changes, try to re-create the camera
            if cam is None or last_shape != (height, width):
                if cam is not None:
                    try:
                        cam.close()
                    except Exception:
                        pass
                    cam = None
                try:
                    cam = pyvirtualcam.Camera(width=width, height=height, fps=60, print_fps=False)
                    last_shape = (height, width)
                except Exception as e:
                    print(f"[pyvirtualcam] Failed to re-initialize camera: {e}")
                    cam = None
                    continue  # Skip this frame, wait for next
            if cam is not None:
                cam.send(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if cam is not None:
        cam.close()
    # No cv2.destroyAllWindows() since no window is created

def generate_self_signed_cert(cert_file, key_file):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend
    import datetime

    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Write private key to file
    with open(key_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    # Generate self-signed cert
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"State"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"iPhoneWebcam"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost")
        ]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())
    # Write cert to file
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

if __name__ == '__main__':
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        print('Generating self-signed certificate...')
        generate_self_signed_cert(cert_file, key_file)
    threading.Thread(target=show_frames, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, ssl_context=(cert_file, key_file))
