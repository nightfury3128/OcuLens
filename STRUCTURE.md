# 📁 Project Structure

This iPhone Webcam project follows a clean, organized directory structure:

```
📦 iPhone Webcam/
├── 🚀 run.py                    # Main entry point launcher
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Project documentation
├── 📄 LICENSE                   # MIT license
│
├── 📁 src/                      # Source code
│   ├── 📁 core/                 # Core application logic
│   │   ├── main.py              # Main server application
│   │   └── standalone.py        # Self-contained version
│   ├── 📁 ui/                   # User interface components
│   │   └── tray_app.py          # System tray application
│   └── 📁 utils/                # Utility modules (future)
│
├── 📁 web/                      # Web interface
│   ├── 📁 templates/            # HTML templates
│   │   └── index.html           # Mobile web interface
│   └── 📁 static/               # CSS, JS, images (future)
│
├── 📁 build/                    # Build configuration
│   ├── build.py                 # Unified build script
│   └── app.spec                 # PyInstaller configuration
│
├── 📁 certs/                    # SSL certificates
│   ├── cert.pem                 # SSL certificate
│   └── key.pem                  # SSL private key
│
├── 📁 scripts/                  # Utility scripts
│   ├── launcher.py              # Interactive launcher
│   ├── launcher.bat             # Windows batch launcher
│   └── cleanup_*.py             # Cleanup utilities
│
├── 📁 docs/                     # Documentation
│   ├── CHANGELOG.md             # Version history
│   ├── AUTOMATION_GUIDE.md      # Automation features
│   └── *.md                     # Other documentation
│
└── 📁 tests/                    # Unit tests (future)
```

## 🚀 Quick Start

```bash
# Run the main launcher
python run.py

# Or run components directly
python src/core/main.py              # Main server
python src/ui/tray_app.py           # System tray
python scripts/launcher.py          # Interactive launcher
```

## 🔧 Build

```bash
python build/build.py
```

This structure provides:
- ✅ **Clear separation** of concerns
- ✅ **Easy navigation** and maintenance
- ✅ **Professional organization**
- ✅ **Scalable structure** for future features
- ✅ **Standard Python project** layout
