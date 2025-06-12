import cv2
import numpy as np
from flask import Flask, request, Response, make_response, send_from_directory
import threading

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

if __name__ == '__main__':
    threading.Thread(target=show_frames, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
