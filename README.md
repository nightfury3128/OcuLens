# iPhone Webcam Streamer

Use your iPhone as a high-quality wireless webcam for your Windows PC, streaming directly into OBS or any app that supports virtual cameras.

## Features
- Stream video from your iPhone camera to your PC over Wi-Fi
- Choose from 4K, 720p, 540p, or 360p resolutions
- Real-time performance with minimal lag
- No coding required for setup
- Docker support for easy background running
- Secure HTTPS connection (self-signed certs)

## Quick Start (No Coding Required)

### 1. Download and Install
- Download this folder to your PC.
- Make sure you have [Python 3.11+](https://www.python.org/downloads/) installed (if not using Docker).

### 2. (Recommended) Run with Docker
1. Open PowerShell in this folder.
2. Build the Docker image:
   ```powershell
   docker build -t iphone-webcam .
   ```
3. Run the server:
   ```powershell
   docker run -d -p 5000:5000 --name iphone-webcam iphone-webcam
   ```

### 3. Or Run with Python
1. Install dependencies:
   ```powershell
   pip install flask numpy opencv-python pyvirtualcam
   ```
2. Start the server:
   ```powershell
   python main.py
   ```

### 4. Connect Your iPhone
1. On your iPhone, connect to the same Wi-Fi as your PC.
2. Open Safari and go to:
   ```
   https://<YOUR_PC_IP>:5000/iphone.html
   ```
   - Example: `https://192.168.1.100:5000/iphone.html`
   - Accept the self-signed certificate warning.
3. Select your desired resolution and click **Start Streaming**.

### 5. Use in OBS or Any App
- Open OBS or your preferred app.
- Add a Video Capture Device and select the virtual camera (usually "OBS Virtual Camera" or "pyvirtualcam").

## FAQ

### Do I need to edit any files or create CRED.json?
**No!**
- By default, the web page will use the server's IP address automatically if you open `iphone.html` from the server (PC) itself.
- If you want to hardcode or customize the server address, you can create a `CRED.json` file, but it's not required for most users.

### How do I find my PC's IP address?
- Open PowerShell and run:
  ```powershell
  ipconfig
  ```
- Look for the `IPv4 Address` under your Wi-Fi adapter.

### Security
- The server uses HTTPS with self-signed certificates for local network security.
- For public/Internet use, use trusted certificates and firewall rules.

### Troubleshooting
- If you change resolution and the video stops, restart the server and the virtual camera in OBS.
- Make sure your firewall allows incoming connections on port 5000.
- If you see a certificate warning, accept it (it's safe for local use).

## Credits
- Built with Flask, OpenCV, pyvirtualcam, and modern browser APIs.
