# 📱 iPhone Webcam Server

Transform your iPhone into a wireless webcam for your computer with this powerful, network-optimized streaming solution.

![iPhone Webcam Demo](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 📡 **Network Optimized Streaming**
- **Adaptive Quality Control**: Automatically adjusts compression based on network conditions
- **Smart Frame Rate Management**: Dynamic FPS scaling (10-30 FPS) for optimal performance
- **Intelligent Connection Handling**: Exponential backoff, keep-alive connections, and timeout management
- **Real-time Performance Monitoring**: Live FPS, latency, and quality metrics

### 🚀 **Zero-Configuration Automation**
- **Automatic Browser Opening**: No manual URL typing required
- **QR Code Generation**: Instant mobile access via camera scanning
- **Terminal QR Display**: ASCII QR code visible directly in console
- **Desktop Shortcuts**: One-click access for future use
- **System Tray Integration**: Background server management

### 🎥 **Virtual Camera Integration**
- **OBS Studio Support**: Works with OBS Virtual Camera
- **Multiple Backends**: Supports OBS, Unity Capture, Windows backends
- **Auto-initialization**: Virtual camera setup handled automatically
- **Cross-platform Compatibility**: Windows, macOS, and Linux support

### 📱 **Mobile-First Design**
- **iPhone Optimized**: Portrait/landscape rotation handling
- **Camera Selection**: Multiple camera support
- **Resolution Options**: 4K, 1080p, 720p, 540p, 360p
- **Wake Lock**: Prevents screen sleep during streaming

## 🚀 Quick Start

### Option 1: Smart Launcher (Recommended)
```bash
git clone https://github.com/nightfury3128/iphoneWebCam.git
cd iphoneWebCam
python smart_launcher.py
```

### Option 2: Direct Launch
```bash
pip install -r requirements.txt
python main.py
```

### Option 3: System Tray App
```bash
python enhanced_tray_app.py
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OBS Studio (for virtual camera functionality)
- Modern web browser
- iPhone with Safari

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
```
flask>=3.0.0
opencv-python>=4.8.0
numpy>=1.26.0
pyvirtualcam>=0.13.0
pystray>=0.19.0
pillow>=10.0.0
qrcode[pil]>=7.4.2
pyOpenSSL>=23.2.0
cryptography>=41.0.0
```

## 🎛️ Usage

### 1. Start the Server
Run any of these commands:
```bash
python main.py                  # Auto launch with browser
python smart_launcher.py        # Interactive launcher
python enhanced_tray_app.py     # System tray mode
```

### 2. Mobile Access
- **QR Code**: Scan the ASCII QR code displayed in terminal
- **Manual**: Open Safari and navigate to the displayed URL
- **Example**: `https://192.168.1.100:5001`

### 3. Accept SSL Certificate
- Click "Advanced" → "Proceed to localhost" in browser
- This is normal for self-signed certificates

### 4. Configure Camera
- Allow camera access when prompted
- Select camera and resolution
- Choose quality settings (Auto recommended)

### 5. Start Streaming
- Click "Start Streaming"
- Your iPhone camera will appear as a webcam in video applications

## 🔧 Configuration Options

### Quality Settings
- **High (0.8)**: Best quality for fast networks
- **Medium (0.7)**: Balanced quality and performance (default)
- **Low (0.5)**: Optimized for slow connections
- **Auto (Adaptive)**: Automatically adjusts based on network conditions

### Frame Rate Options
- **30 FPS**: Smooth motion for fast networks
- **24 FPS**: Cinematic frame rate
- **15 FPS**: Good balance for most networks
- **10 FPS**: Minimum for slow connections

### Resolution Options
- **4K (3840×2160)**: Ultra-high definition
- **720p (1280×720)**: High definition (recommended)
- **540p (960×540)**: Standard definition
- **360p (640×360)**: Low bandwidth mode

## 📊 Performance Monitoring

The interface displays real-time metrics:
- **Current FPS**: Actual frames per second achieved
- **Target FPS**: Adaptive target based on network conditions
- **Latency**: Round-trip time for frame uploads
- **Frame Size**: Compressed frame size in KB
- **Quality**: Current compression quality percentage
- **Drop Count**: Failed frame transmissions

## 🌐 Network Optimization Features

### Adaptive Quality System
```
Good Connection (<200ms)    → Increase quality gradually
Standard Connection         → Maintain current settings  
Poor Connection (>1000ms)   → Reduce quality and FPS
Very Poor (>2000ms)        → Temporarily reduce resolution
```

### Automatic Adjustments
- **Frame Skipping**: Intelligently skips frames during high latency
- **Compression Scaling**: JPEG/WebP quality adjusts from 30% to 80%
- **Resolution Scaling**: Temporary resolution reduction for poor connections
- **Recovery Logic**: Gradually restores quality when connection improves

## 🛠️ Advanced Usage

### Build Standalone Executable
```bash
python smart_launcher.py
# Select option 5: Build Executable
```

### Custom Launch Script
```python
import subprocess
import webbrowser
import time

# Start server
process = subprocess.Popen(['python', 'main.py'])
time.sleep(3)
webbrowser.open('https://localhost:5001')
```

### System Tray Features
Right-click the tray icon for:
- 🚀 Start/Stop Server
- 🌐 Open Browser
- 📋 Copy URL to Clipboard
- 📱 Show QR Code
- ℹ️ Status Information

## 📱 Mobile Setup Guide

### iPhone/iPad Instructions
1. **Automatic Method**:
   - Scan QR code with iPhone Camera app
   - Tap the notification to open in Safari

2. **Manual Method**:
   - Open Safari on iPhone
   - Type the network URL shown in console
   - Accept SSL certificate warning

3. **Camera Permissions**:
   - Allow camera access when prompted
   - Choose front or back camera
   - Select desired resolution and quality

## 🔍 Troubleshooting

### Common Issues

**Browser doesn't open automatically**
- Desktop shortcut created as backup
- Manually navigate to displayed URL

**QR code not visible**
- Check terminal for ASCII QR code
- PNG file saved in project directory

**Virtual camera not working**
- Ensure OBS Studio is installed
- Start OBS at least once
- Enable Virtual Camera in Tools menu

**Connection drops frequently**
- Enable "Auto (Adaptive)" quality
- Reduce FPS to 15 or 10
- Lower resolution to 720p or 540p

**High latency/slow streaming**
- Check WiFi signal strength
- Close bandwidth-heavy applications
- Try 5GHz WiFi if available

### Network Requirements
- **Minimum**: 2 Mbps upload (iPhone) + 5 Mbps download (computer)
- **Recommended**: 10+ Mbps for HD streaming
- **Optimal**: 25+ Mbps for 4K streaming

## 🏗️ Architecture

### Client-Side (iPhone/Browser)
- **WebRTC-style capture**: Uses getUserMedia API
- **Canvas processing**: Frame rotation and resizing
- **Adaptive compression**: JPEG/WebP with dynamic quality
- **Network monitoring**: Latency tracking and quality adjustment

### Server-Side (Python Flask)
- **SSL/HTTPS**: Self-signed certificates for secure streaming
- **Virtual Camera**: Integration with OBS and system backends
- **Frame processing**: OpenCV-based image handling
- **Network optimization**: Compression, timeouts, and error handling

### Automation Layer
- **QR Code Generation**: PIL and qrcode libraries
- **Browser Control**: webbrowser module
- **System Integration**: Desktop shortcuts and tray apps
- **Network Discovery**: Automatic IP detection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/nightfury3128/iphoneWebCam.git
cd iphoneWebCam
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Performance Benchmarks

| Network Type | Resolution | FPS | Latency | Data Usage |
|-------------|------------|-----|---------|------------|
| WiFi 6 (50+ Mbps) | 1080p | 30 | <100ms | ~15 MB/min |
| WiFi 5 (25 Mbps) | 720p | 24 | <200ms | ~8 MB/min |
| WiFi 4 (10 Mbps) | 540p | 15 | <500ms | ~4 MB/min |
| Mobile Data (5 Mbps) | 360p | 10 | <1000ms | ~2 MB/min |

## 🔗 Related Projects

- [OBS Studio](https://obsproject.com/) - Virtual camera backend
- [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) - Python virtual camera library
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/nightfury3128/iphoneWebCam/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nightfury3128/iphoneWebCam/discussions)

---

**Made with ❤️ for seamless iPhone webcam streaming**