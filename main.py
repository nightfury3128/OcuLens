import cv2
import numpy as np
from flask import Flask, request, Response, make_response, send_from_directory
import threading
import pyvirtualcam
import platform
import os
import subprocess
import time
import socket
from contextlib import closing

app = Flask(__name__)
frame = None
frame_event = threading.Event()
virtual_cam = None
last_shape = None

def find_available_port(start_port=5000, max_tries=100):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_tries):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except socket.error:
                continue
    raise RuntimeError(f"Could not find an available port after {max_tries} attempts")

def start_obs_virtual_camera():
    """Try to start OBS Virtual Camera using obs-cli"""
    try:
        obs_cli_path = r"C:\Program Files\obs-studio\bin\64bit\obs-cli.exe"
        if os.path.exists(obs_cli_path):
            subprocess.run([obs_cli_path, "startVirtualCam"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            print("Started OBS Virtual Camera")
            # Give it a moment to initialize
            time.sleep(2)
            return True
    except Exception as e:
        print(f"Error starting OBS virtual camera: {e}")
    return False

def init_virtual_camera(width, height):
    """Initialize or reinitialize the virtual camera"""
    global virtual_cam, last_shape
    try:
        if virtual_cam is not None:
            try:
                virtual_cam.close()
            except:
                pass
            virtual_cam = None

        # Try different virtual camera backends on Windows
        if platform.system() == 'Windows':
            # First try to ensure OBS Virtual Camera is started
            start_obs_virtual_camera()
            
            # Try different backends
            backends = ['obs', 'unitycapture', 'windows']
            for backend in backends:
                try:
                    print(f"Trying virtual camera with backend: {backend}")
                    virtual_cam = pyvirtualcam.Camera(width=width, height=height, fps=30, backend=backend)
                    print(f"Successfully initialized virtual camera using {backend} backend")
                    break
                except Exception as e:
                    print(f"Failed with backend {backend}: {e}")
                    continue
            
            if virtual_cam is None:
                raise Exception("No working virtual camera backend found")
        else:
            virtual_cam = pyvirtualcam.Camera(width=width, height=height, fps=30)
            
        last_shape = (width, height)
        print(f"Virtual camera initialized at {width}x{height}")
        return True
    except Exception as e:
        print(f"Failed to initialize virtual camera: {e}")
        print("\nPlease ensure that:")
        print("1. OBS Studio is installed")
        print("2. You've started OBS at least once")
        print("3. OBS Virtual Camera is installed (Tools -> Virtual Camera -> Start)")
        virtual_cam = None
        return False

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    global frame, virtual_cam, last_shape
    if request.method == 'OPTIONS':
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
    
    # If not running in Docker, update virtual camera
    if not os.path.exists('/.dockerenv'):
        height, width = frame.shape[:2]
        
        # Initialize or reinitialize camera if needed
        if virtual_cam is None or last_shape != (width, height):
            if not init_virtual_camera(width, height):
                # If initialization failed, try starting OBS Virtual Camera and retry
                print("\nRetrying with OBS Virtual Camera...")
                if start_obs_virtual_camera():
                    time.sleep(2)  # Give it time to start
                    if not init_virtual_camera(width, height):
                        print("\nVirtual camera initialization failed. Please:")
                        print("1. Open OBS Studio")
                        print("2. Go to Tools -> Virtual Camera")
                        print("3. Click 'Start'")
                        print("4. Restart this application")
                        return ('Failed to initialize virtual camera', 500)
                else:
                    print("\nCouldn't start OBS Virtual Camera automatically.")
                    print("Please start it manually:")
                    print("1. Open OBS Studio")
                    print("2. Go to Tools -> Virtual Camera")
                    print("3. Click 'Start'")
                    return ('Failed to initialize virtual camera', 500)
        
        try:
            # Convert BGR to RGB for pyvirtualcam
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            virtual_cam.send(frame_rgb)
            virtual_cam.sleep_until_next_frame()
        except Exception as e:
            print(f"\nError sending frame to virtual camera: {e}")
            print("\nVirtual camera connection lost. Please:")
            print("1. Open OBS Studio")
            print("2. Go to Tools -> Virtual Camera")
            print("3. Click 'Stop' then 'Start'")
            virtual_cam = None
            return ('Virtual camera error', 500)
    
    return ('', 204)

@app.route('/')
def index():
    return send_from_directory('.', 'iphone.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\nStarting iPhone Webcam Server...")
    if os.path.exists('/.dockerenv'):
        print("Running in Docker container - virtual camera will be managed by host")
    else:
        print("Running on host - virtual camera will be initialized when streaming starts")
        print("\nIMPORTANT: Before streaming:")
        print("1. Make sure OBS Studio is installed")
        print("2. Start OBS Studio at least once")
        print("3. Go to Tools -> Virtual Camera -> Start")
    
    port = find_available_port()
    print(f"\nServer will run on port: {port}")
    
    # Write the port to a file so the tray app can read it
    with open('server_port.txt', 'w') as f:
        f.write(str(port))
    
    app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'))
