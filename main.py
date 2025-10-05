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
from OpenSSL import crypto
from datetime import datetime, timedelta
import gzip
import io
import webbrowser
import qrcode
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
frame = None
frame_event = threading.Event()
virtual_cam = None
last_shape = None

# Network optimization settings
ENABLE_COMPRESSION = True
MAX_FRAME_SIZE = 1024 * 1024  # 1MB max frame size

def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS"""
    print("[Setup] Checking SSL certificates...")
    
    # If certificates already exist, return
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print("[Info] SSL certificates already exist")
        return

    print("[Setup] Generating SSL certificates...")
    
    # Generate key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # Generate certificate
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "City"
    cert.get_subject().O = "iPhone Webcam"
    cert.get_subject().OU = "iPhone Webcam App"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Valid for one year
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # Save certificate
    with open("cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open("key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    print("[Success] SSL certificates generated successfully")

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote server to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def generate_qr_code(url, port):
    """Generate QR code for easy mobile access"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Add text below QR code
        img_with_text = Image.new('RGB', (img.size[0], img.size[1] + 60), 'white')
        img_with_text.paste(img, (0, 0))
        
        draw = ImageDraw.Draw(img_with_text)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = f"iPhone Webcam Server\n{url}"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (img.size[0] - text_width) // 2
        draw.text((text_x, img.size[1] + 10), text, fill="black", font=font)
        
        qr_filename = f"qr_code_port_{port}.png"
        img_with_text.save(qr_filename)
        print(f"[Info] QR code saved as: {qr_filename}")
        
        # Display QR code in terminal
        display_qr_in_terminal(url)
        
        return qr_filename
    except Exception as e:
        print(f"[Warning] Could not generate QR code: {e}")
        return None

def display_qr_in_terminal(url):
    """Display QR code in terminal using ASCII characters"""
    try:
        # Create a simple QR code for terminal display
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Get the QR code matrix
        matrix = qr.get_matrix()
        
        print("\n" + "="*60)
        print("📱 SCAN THIS QR CODE WITH YOUR IPHONE CAMERA:")
        print("="*60)
        
        # Convert matrix to ASCII using block characters
        for row in matrix:
            line = ""
            for cell in row:
                if cell:
                    line += "██"  # Full block for black
                else:
                    line += "  "  # Space for white
            print(line)
        
        print("="*60)
        print(f"📱 Or type this URL in your iPhone browser:")
        print(f"🔗 {url}")
        print("="*60)
        
    except Exception as e:
        print(f"[Warning] Could not display QR code in terminal: {e}")
        print(f"📱 Mobile URL: {url}")

def open_browser_after_delay(url, delay=3):
    """Open browser after a short delay to ensure server is running"""
    def delayed_open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"[Info] Opened browser: {url}")
        except Exception as e:
            print(f"[Warning] Could not open browser: {e}")
    
    threading.Thread(target=delayed_open, daemon=True).start()

def create_desktop_shortcut(url, port):
    """Create a desktop shortcut for easy access"""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, f"iPhone_Webcam_Port_{port}.url")
        
        with open(shortcut_path, 'w') as f:
            f.write(f"[InternetShortcut]\n")
            f.write(f"URL={url}\n")
            f.write(f"IconFile=%SystemRoot%\\system32\\shell32.dll\n")
            f.write(f"IconIndex=0\n")
        
        print(f"[Info] Desktop shortcut created: {shortcut_path}")
        return shortcut_path
    except Exception as e:
        print(f"[Warning] Could not create desktop shortcut: {e}")
        return None

def print_access_info(port):
    """Print comprehensive access information"""
    local_ip = get_local_ip()
    local_url = f"https://localhost:{port}"
    network_url = f"https://{local_ip}:{port}"
    
    print("\n" + "="*60)
    print("🎥 IPHONE WEBCAM SERVER - ACCESS INFORMATION")
    print("="*60)
    print(f"📱 Local Access (same computer):")
    print(f"   {local_url}")
    print(f"\n🌐 Network Access (other devices):")
    print(f"   {network_url}")
    print(f"\n💡 Quick Access Options:")
    print(f"   • Browser will open automatically in 3 seconds")
    print(f"   • Desktop shortcut created")
    print(f"   • QR code generated for mobile scanning")
    print(f"\n📋 Manual Setup Steps:")
    print(f"   1. Open browser on any device")
    print(f"   2. Navigate to: {network_url}")
    print(f"   3. Accept the SSL certificate warning")
    print(f"   4. Allow camera access on your iPhone")
    print(f"   5. Start streaming!")
    print("="*60)
    
    return network_url

def setup_automation(port):
    """Set up all automation features"""
    local_ip = get_local_ip()
    network_url = f"https://{local_ip}:{port}"
    local_url = f"https://localhost:{port}"
    
    # Generate QR code
    qr_file = generate_qr_code(network_url, port)
    
    # Create desktop shortcut
    create_desktop_shortcut(local_url, port)
    
    # Open browser automatically
    open_browser_after_delay(local_url)
    
    # Print access information
    final_url = print_access_info(port)
    
    return final_url, qr_file

# Generate SSL certificate if needed
create_self_signed_cert()

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
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Encoding'
    if ENABLE_COMPRESSION:
        response.headers['Accept-Encoding'] = 'gzip, deflate'
    return response

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    global frame, virtual_cam, last_shape
    if request.method == 'OPTIONS':
        resp = make_response('', 204)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Encoding'
        return resp

    img_bytes = request.data
    if not img_bytes:
        return ('No image data', 400)

    # Check if data is compressed
    if request.headers.get('Content-Encoding') == 'gzip':
        try:
            img_bytes = gzip.decompress(img_bytes)
        except Exception as e:
            print(f"Failed to decompress gzipped data: {e}")
            return ('Invalid compressed data', 400)

    # Limit frame size for network efficiency
    if len(img_bytes) > MAX_FRAME_SIZE:
        print(f"Frame too large: {len(img_bytes)} bytes, max: {MAX_FRAME_SIZE}")
        return ('Frame too large', 413)

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
    print("\n🚀 Starting iPhone Webcam Server...")
    if os.path.exists('/.dockerenv'):
        print("Running in Docker container - virtual camera will be managed by host")
    else:
        print("Running on host - virtual camera will be initialized when streaming starts")
        print("\n📋 IMPORTANT: Before streaming:")
        print("1. Make sure OBS Studio is installed")
        print("2. Start OBS Studio at least once")
        print("3. Go to Tools -> Virtual Camera -> Start")
    
    port = find_available_port()
    print(f"\n⚙️  Network optimizations enabled: Compression={ENABLE_COMPRESSION}, Max frame size={MAX_FRAME_SIZE//1024}KB")
    
    # Write the port to a file so the tray app can read it
    with open('server_port.txt', 'w') as f:
        f.write(str(port))
    
    # Set up automation features
    try:
        network_url, qr_file = setup_automation(port)
        
        # Additional mobile instructions
        print(f"\n📱 For iPhone/Mobile Access:")
        print(f"   • Scan the QR code: {qr_file}")
        print(f"   • Or manually type: {network_url}")
        print(f"   • Accept SSL certificate warning")
        print(f"   • Grant camera permissions")
        
    except Exception as e:
        print(f"\n⚠️  Automation setup failed: {e}")
        print(f"Manual access: https://localhost:{port}")
    
    print(f"\n🌟 Server starting on all interfaces (0.0.0.0:{port})...")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'), 
                threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
    finally:
        print("🧹 Cleaning up...")
        if virtual_cam:
            try:
                virtual_cam.close()
            except:
                pass
