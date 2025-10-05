#!/usr/bin/env python3
"""
iPhone Webcam Server - Single File Edition
A complete wireless webcam solution in one file!

Just run this file and scan the QR code with your iPhone camera.
No additional files or complex setup required.

Author: nightfury3128
License: MIT
Version: 2.0.0
"""

# ============================================================================
# EMBEDDED HTML TEMPLATE
# ============================================================================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>iPhone Webcam Streamer</title>
  <style>
    body { text-align: center; font-family: sans-serif; background: #f0f0f0; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; background: white; border-radius: 10px; margin-top: 20px; }
    video { width: 90vw; max-width: 480px; border: 2px solid #333; border-radius: 8px; }
    button { margin: 10px; padding: 12px 24px; font-size: 1.1em; border: none; border-radius: 5px; cursor: pointer; }
    .start-btn { background: #4CAF50; color: white; }
    .stop-btn { background: #f44336; color: white; }
    select { margin: 5px; padding: 8px; border-radius: 5px; border: 1px solid #ddd; }
    .status { margin: 10px; padding: 10px; border-radius: 5px; }
    .status.good { background: #d4edda; color: #155724; }
    .status.warning { background: #fff3cd; color: #856404; }
    .status.error { background: #f8d7da; color: #721c24; }
    .metrics { display: flex; justify-content: space-around; margin: 10px 0; }
    .metric { text-align: center; }
    .metric-value { font-size: 1.2em; font-weight: bold; }
    .metric-label { font-size: 0.9em; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <h2>📱 iPhone Webcam Streamer</h2>
    <video id="video" autoplay playsinline></video><br>
    
    <div>
      <label for="camera">📷 Camera:</label>
      <select id="camera">
        <option value="">Loading cameras...</option>
      </select>
    </div>
    
    <div>
      <label for="resolution">📐 Resolution:</label>
      <select id="resolution">
        <option value="1280x720" selected>1280x720 (HD)</option>
        <option value="960x540">960x540 (QHD)</option>
        <option value="640x360">640x360 (SD)</option>
        <option value="3840x2160">3840x2160 (4K)</option>
      </select>
    </div>
    
    <div>
      <label for="quality">⚙️ Quality:</label>
      <select id="quality">
        <option value="high">High (0.8)</option>
        <option value="medium" selected>Medium (0.7)</option>
        <option value="low">Low (0.5)</option>
        <option value="auto">🤖 Auto (Adaptive)</option>
      </select>
    </div>
    
    <div>
      <label for="maxFps">🎬 Max FPS:</label>
      <select id="maxFps">
        <option value="30" selected>30 FPS</option>
        <option value="24">24 FPS</option>
        <option value="15">15 FPS</option>
        <option value="10">10 FPS</option>
      </select>
    </div>
    
    <button id="start" class="start-btn">🚀 Start Streaming</button>
    
    <div id="status" class="status">Ready to stream</div>
    
    <div class="metrics">
      <div class="metric">
        <div id="fpsValue" class="metric-value">--</div>
        <div class="metric-label">FPS</div>
      </div>
      <div class="metric">
        <div id="latencyValue" class="metric-value">--</div>
        <div class="metric-label">Latency (ms)</div>
      </div>
      <div class="metric">
        <div id="qualityValue" class="metric-value">--</div>
        <div class="metric-label">Quality (%)</div>
      </div>
      <div class="metric">
        <div id="sizeValue" class="metric-value">--</div>
        <div class="metric-label">Size (KB)</div>
      </div>
    </div>
  </div>

  <script>
    const video = document.getElementById('video');
    const startBtn = document.getElementById('start');
    const status = document.getElementById('status');
    const resolutionSelect = document.getElementById('resolution');
    const cameraSelect = document.getElementById('camera');
    const qualitySelect = document.getElementById('quality');
    const maxFpsSelect = document.getElementById('maxFps');
    
    // Metric displays
    const fpsValue = document.getElementById('fpsValue');
    const latencyValue = document.getElementById('latencyValue');
    const qualityValue = document.getElementById('qualityValue');
    const sizeValue = document.getElementById('sizeValue');
    
    let streaming = false;
    let cameraStarted = false;
    let uploading = false;
    let lastFrameTime = 0;
    let frameCount = 0;
    
    // Network efficiency variables
    let adaptiveQuality = 0.7;
    let targetFPS = 30;
    let networkLatency = 0;
    let frameDropCount = 0;
    let lastSuccessTime = Date.now();
    let frameSkipCounter = 0;
    let compressionLevel = 0.7;
    let dynamicResolution = false;
    let currentWidth = 1280;
    let currentHeight = 720;
    let useWebP = false;
    let wakeLock = null;

    // Server URL
    const SERVER_URL = window.location.href.replace(/\\/$/, '') + '/upload';
    
    // Network monitoring
    function monitorNetworkPerformance(responseTime) {
      networkLatency = responseTime;
      latencyValue.textContent = Math.round(responseTime);
      
      if (qualitySelect.value === 'auto') {
        if (responseTime > 1000) {
          adaptiveQuality = Math.max(0.3, adaptiveQuality - 0.1);
          targetFPS = Math.max(10, targetFPS - 2);
          compressionLevel = Math.max(0.3, compressionLevel - 0.1);
        } else if (responseTime < 200) {
          adaptiveQuality = Math.min(0.8, adaptiveQuality + 0.05);
          targetFPS = Math.min(30, targetFPS + 1);
          compressionLevel = Math.min(0.8, compressionLevel + 0.05);
        }
        
        if (responseTime > 2000 && !dynamicResolution) {
          dynamicResolution = true;
          currentWidth = Math.max(320, Math.floor(currentWidth * 0.7));
          currentHeight = Math.max(240, Math.floor(currentHeight * 0.7));
        } else if (responseTime < 300 && dynamicResolution) {
          dynamicResolution = false;
          const [w, h] = resolutionSelect.value.split('x').map(Number);
          currentWidth = w;
          currentHeight = h;
        }
      }
      
      qualityValue.textContent = Math.round(adaptiveQuality * 100);
    }

    // Wake lock
    async function requestWakeLock() {
      try {
        if ('wakeLock' in navigator) {
          wakeLock = await navigator.wakeLock.request('screen');
          console.log('Wake Lock active');
        }
      } catch (err) {
        console.error('Wake Lock failed:', err);
      }
    }

    async function releaseWakeLock() {
      if (wakeLock) {
        try {
          await wakeLock.release();
          wakeLock = null;
        } catch (err) {
          console.error('Wake Lock release failed:', err);
        }
      }
    }

    // Get cameras
    async function getCameras() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const cameras = devices.filter(device => device.kind === 'videoinput');
        cameraSelect.innerHTML = cameras.map(camera => 
          `<option value="${camera.deviceId}">${camera.label || `Camera ${cameras.indexOf(camera) + 1}`}</option>`
        ).join('');
      } catch (err) {
        console.error('Camera enumeration failed:', err);
        updateStatus('Error loading cameras', 'error');
      }
    }

    // Request permissions and get cameras
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        stream.getTracks().forEach(track => track.stop());
        getCameras();
      })
      .catch(() => {
        updateStatus('Camera permission denied', 'error');
      });

    // WebP support check
    async function checkWebPSupport() {
      return new Promise(resolve => {
        const img = new Image();
        img.onload = () => resolve(img.width === 1);
        img.onerror = () => resolve(false);
        img.src = "data:image/webp;base64,UklGRiIAAABXRUJQVlA4TAYAAAAvAAAAAAfQ//73v/+BiOh/AAA=";
      });
    }

    // Update status with styling
    function updateStatus(message, type = 'good') {
      status.textContent = message;
      status.className = `status ${type}`;
    }

    // Start camera
    async function startCamera() {
      try {
        const [w, h] = resolutionSelect.value.split('x').map(Number);
        currentWidth = w;
        currentHeight = h;
        
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: w },
            height: { ideal: h },
            deviceId: { exact: cameraSelect.value }
          },
          audio: false
        });
        
        video.srcObject = stream;
        cameraStarted = true;
        updateStatus(`Camera started at ${w}x${h}. Ready to stream.`, 'good');
      } catch (err) {
        console.error('Camera start failed:', err);
        updateStatus('Camera access denied or not available', 'error');
      }
    }

    // Send frame
    async function sendFrame() {
      if (!streaming || !cameraStarted || uploading) return;
      if (video.videoWidth === 0 || video.videoHeight === 0) {
        updateStatus('Waiting for camera...', 'warning');
        setTimeout(sendFrame, 100);
        return;
      }
      
      // Frame rate control
      const frameInterval = 1000 / targetFPS;
      const timeSinceLastFrame = Date.now() - lastSuccessTime;
      if (timeSinceLastFrame < frameInterval) {
        setTimeout(sendFrame, frameInterval - timeSinceLastFrame);
        return;
      }
      
      // Skip frames if struggling
      frameSkipCounter++;
      if (networkLatency > 500 && frameSkipCounter % 2 === 0) {
        setTimeout(sendFrame, 50);
        return;
      }
      
      const canvas = document.createElement('canvas');
      canvas.width = currentWidth;
      canvas.height = currentHeight;
      const ctx = canvas.getContext('2d');
      
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      
      // Handle rotation
      if (video.videoHeight > video.videoWidth) {
        ctx.save();
        ctx.translate(currentWidth / 2, currentHeight / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.drawImage(video, -currentHeight / 2, -currentWidth / 2, currentHeight, currentWidth);
        ctx.restore();
      } else {
        ctx.drawImage(video, 0, 0, currentWidth, currentHeight);
      }
      
      uploading = true;
      const startTime = Date.now();
      
      let blob;
      if (useWebP) {
        blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/webp', adaptiveQuality));
      } else {
        blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', compressionLevel));
      }
      
      if (!blob) {
        updateStatus('No frame to send', 'warning');
        uploading = false;
        setTimeout(sendFrame, 100);
        return;
      }
      
      try {
        const response = await fetch(SERVER_URL, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/octet-stream',
            'Connection': 'keep-alive'
          },
          body: blob,
          signal: AbortSignal.timeout(5000)
        });
        
        const responseTime = Date.now() - startTime;
        monitorNetworkPerformance(responseTime);
        lastSuccessTime = Date.now();
        frameDropCount = Math.max(0, frameDropCount - 1);
        
        // Update metrics
        sizeValue.textContent = Math.round(blob.size / 1024);
        updateStatus(`Streaming... (${Math.round(blob.size/1024)}KB, ${responseTime}ms)`, 'good');
        
        // FPS calculation
        frameCount++;
        const now = performance.now();
        if (!lastFrameTime) lastFrameTime = now;
        if (now - lastFrameTime >= 1000) {
          fpsValue.textContent = frameCount;
          frameCount = 0;
          lastFrameTime = now;
        }
        
      } catch (e) {
        frameDropCount++;
        if (e.name === 'TimeoutError') {
          updateStatus('Connection timeout - reducing quality', 'warning');
          monitorNetworkPerformance(5000);
        } else {
          updateStatus(`Failed to send frame (${frameDropCount} drops)`, 'error');
          const backoffDelay = Math.min(1000, 100 * Math.pow(2, Math.min(frameDropCount, 5)));
          uploading = false;
          if (streaming) {
            setTimeout(sendFrame, backoffDelay);
          }
          return;
        }
      }
      
      uploading = false;
      if (streaming) {
        const nextFrameDelay = Math.max(16, 1000 / targetFPS);
        setTimeout(sendFrame, nextFrameDelay);
      }
    }

    // Event handlers
    qualitySelect.onchange = () => {
      const qualityValue = qualitySelect.value;
      if (qualityValue !== 'auto') {
        const qualityMap = { 'high': 0.8, 'medium': 0.7, 'low': 0.5 };
        adaptiveQuality = qualityMap[qualityValue] || 0.7;
        compressionLevel = adaptiveQuality;
      }
    };

    maxFpsSelect.onchange = () => {
      targetFPS = parseInt(maxFpsSelect.value);
    };

    resolutionSelect.onchange = async () => {
      if (streaming) {
        streaming = false;
        startBtn.textContent = '🚀 Start Streaming';
        startBtn.className = 'start-btn';
        updateStatus('Restarting camera...', 'warning');
        await startCamera();
        streaming = true;
        startBtn.textContent = '🛑 Stop Streaming';
        startBtn.className = 'stop-btn';
        sendFrame();
      }
    };

    cameraSelect.onchange = async () => {
      if (streaming) {
        streaming = false;
        startBtn.textContent = '🚀 Start Streaming';
        startBtn.className = 'start-btn';
        updateStatus('Restarting camera...', 'warning');
        await startCamera();
        streaming = true;
        startBtn.textContent = '🛑 Stop Streaming';
        startBtn.className = 'stop-btn';
        sendFrame();
      }
    };

    startBtn.onclick = async () => {
      if (!streaming) {
        if (!cameraStarted) {
          updateStatus('Requesting camera access...', 'warning');
          await startCamera();
          if (!cameraStarted) return;
        }
        
        streaming = true;
        startBtn.textContent = '🛑 Stop Streaming';
        startBtn.className = 'stop-btn';
        await requestWakeLock();
        sendFrame();
        
      } else {
        streaming = false;
        startBtn.textContent = '🚀 Start Streaming';
        startBtn.className = 'start-btn';
        updateStatus('Stopped', 'warning');
        await releaseWakeLock();
        
        // Reset metrics
        fpsValue.textContent = '--';
        latencyValue.textContent = '--';
        qualityValue.textContent = '--';
        sizeValue.textContent = '--';
      }
    };

    // Initialize
    (async () => {
      useWebP = await checkWebPSupport();
      console.log('WebP support:', useWebP);
    })();
  </script>
</body>
</html>'''

# ============================================================================
# MAIN APPLICATION CODE
# ============================================================================

import sys
import os
import socket
import threading
import time
import webbrowser
import subprocess
from contextlib import closing
from datetime import datetime, timedelta

# Try to import required packages, install if missing
try:
    import cv2
    import numpy as np
    from flask import Flask, request, Response, make_response
    import pyvirtualcam
    from OpenSSL import crypto
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"⚠️  Missing required package: {e}")
    print("📦 Installing required packages...")
    
    packages = [
        "flask", "opencv-python", "numpy", "pyvirtualcam", 
        "pyOpenSSL", "qrcode[pil]", "pillow"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}. Please install manually.")
            sys.exit(1)
    
    print("✅ Packages installed! Please restart the application.")
    sys.exit(0)

# Global variables
app = Flask(__name__)
frame = None
virtual_cam = None
last_shape = None
ENABLE_COMPRESSION = True
MAX_FRAME_SIZE = 1024 * 1024  # 1MB

def get_local_ip():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def find_available_port(start_port=5000, max_tries=100):
    """Find available port"""
    for port in range(start_port, start_port + max_tries):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except socket.error:
                continue
    raise RuntimeError(f"Could not find available port after {max_tries} attempts")

def create_self_signed_cert():
    """Create SSL certificate"""
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        return
    
    print("[Setup] Generating SSL certificates...")
    
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "City"
    cert.get_subject().O = "iPhone Webcam"
    cert.get_subject().OU = "iPhone Webcam App"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    
    with open("cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open("key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def display_qr_in_terminal(url):
    """Display QR code in terminal"""
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        
        matrix = qr.get_matrix()
        
        print("\n" + "="*60)
        print("📱 SCAN THIS QR CODE WITH YOUR IPHONE CAMERA:")
        print("="*60)
        
        for row in matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            print(line)
        
        print("="*60)
        print(f"📱 Or type this URL in your iPhone browser:")
        print(f"🔗 {url}")
        print("="*60)
        
    except Exception as e:
        print(f"📱 Mobile URL: {url}")

def open_browser_after_delay(url, delay=3):
    """Open browser after delay"""
    def delayed_open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"[Info] Browser opened: {url}")
        except Exception:
            pass
    threading.Thread(target=delayed_open, daemon=True).start()

def init_virtual_camera(width, height):
    """Initialize virtual camera"""
    global virtual_cam, last_shape
    try:
        if virtual_cam:
            try:
                virtual_cam.close()
            except:
                pass
            virtual_cam = None
        
        backends = ['obs', 'unitycapture', 'windows'] if os.name == 'nt' else ['v4l2loopback']
        for backend in backends:
            try:
                virtual_cam = pyvirtualcam.Camera(width=width, height=height, fps=30, backend=backend)
                print(f"✅ Virtual camera initialized: {backend}")
                break
            except Exception:
                continue
        
        if virtual_cam is None:
            print("⚠️  Virtual camera failed. Install OBS Studio for best results.")
            return False
        
        last_shape = (width, height)
        return True
    except Exception as e:
        print(f"⚠️  Virtual camera error: {e}")
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
        return make_response('', 204)
    
    img_bytes = request.data
    if not img_bytes or len(img_bytes) > MAX_FRAME_SIZE:
        return ('Invalid frame', 400)
    
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    if img_np.size == 0:
        return ('Empty buffer', 400)
    
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if img is None:
        return ('Decode failed', 400)
    
    frame = img
    
    # Update virtual camera
    if not os.path.exists('/.dockerenv'):
        height, width = frame.shape[:2]
        
        if virtual_cam is None or last_shape != (width, height):
            init_virtual_camera(width, height)
        
        if virtual_cam:
            try:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                virtual_cam.send(frame_rgb)
                virtual_cam.sleep_until_next_frame()
            except Exception:
                virtual_cam = None
    
    return ('', 204)

@app.route('/')
def index():
    return HTML_TEMPLATE

def print_startup_info(port):
    """Print comprehensive startup information"""
    local_ip = get_local_ip()
    local_url = f"https://localhost:{port}"
    network_url = f"https://{local_ip}:{port}"
    
    print("\n" + "🎉" * 20)
    print("📱 iPhone Webcam Server - Single File Edition")
    print("🎉" * 20)
    print(f"\n📡 Server running on port: {port}")
    print(f"🌐 Network URL: {network_url}")
    print(f"💻 Local URL: {local_url}")
    
    # Display QR code
    display_qr_in_terminal(network_url)
    
    print(f"\n🚀 Quick Start:")
    print(f"1. Scan the QR code above with your iPhone camera")
    print(f"2. Tap the notification to open in Safari")
    print(f"3. Accept the SSL certificate warning")
    print(f"4. Allow camera access and start streaming!")
    
    print(f"\n💡 Tips:")
    print(f"• Use 'Auto' quality for best performance")
    print(f"• Close other apps for better performance")
    print(f"• Works on same WiFi network")
    
    print(f"\n⚙️  Features:")
    print(f"• Adaptive quality control")
    print(f"• Real-time performance monitoring")
    print(f"• Multiple resolution options")
    print(f"• Virtual camera integration")
    
    print(f"\n🔧 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Auto-open browser
    open_browser_after_delay(local_url)

def main():
    """Main application function"""
    print("🚀 Starting iPhone Webcam Server...")
    
    # Create SSL certificates
    create_self_signed_cert()
    
    # Find available port
    try:
        port = find_available_port()
    except RuntimeError as e:
        print(f"❌ {e}")
        return
    
    # Print startup info
    print_startup_info(port)
    
    try:
        app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'), 
                threaded=True, use_reloader=False, debug=False)
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

if __name__ == "__main__":
    main()