# iPhone Webcam Streamer

Use your iPhone as a high-quality wireless webcam for your Windows PC, streaming directly into OBS or any app that supports virtual cameras.

## Features
- Stream video from your iPhone camera to your PC over Wi-Fi
- Choose from 4K, 720p, 540p, or 360p resolutions
- Real-time performance with minimal lag
- Zero setup - just double-click and go!
- Automatic virtual camera setup
- Secure HTTPS connection (self-signed certs)

## Quick Start (No Coding Required)

### 1. Install Required Software
These are one-time installations:
- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Install [OBS Studio](https://obsproject.com/)

### 2. Run the Webcam Server
1. Download this folder to your PC
2. Double-click `start.bat`
3. Follow the instructions shown in the window

That's it! The script will:
- Start the server automatically
- Show you exactly what to do on your iPhone
- Tell you how to use it in OBS
- Keep running in the background

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
