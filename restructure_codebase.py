#!/usr/bin/env python3
"""
iPhone Webcam - Codebase Restructuring Script
Organizes files into a professional directory structure
"""

import os
import shutil
import sys

def create_directory_structure():
    """Create the new directory structure"""
    directories = [
        "src",              # Source code
        "src/core",         # Core application files
        "src/ui",           # User interface files
        "src/utils",        # Utility scripts
        "web",              # Web interface files
        "web/static",       # Static web assets (CSS, JS, images)
        "web/templates",    # HTML templates
        "build",            # Build scripts and configurations
        "certs",            # SSL certificates
        "docs",             # Documentation
        "scripts",          # Utility scripts and launchers
        "tests",            # Unit tests (for future)
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}/")

def move_files():
    """Move files to their appropriate directories"""
    file_moves = [
        # Core application files
        ("main.py", "src/core/main.py"),
        ("enhanced_tray_app.py", "src/ui/tray_app.py"),
        ("iphone_webcam_standalone.py", "src/core/standalone.py"),
        
        # Web interface
        ("iphone.html", "web/templates/index.html"),
        
        # Build and deployment
        ("build_unified.py", "build/build.py"),
        ("iPhone-Webcam.spec", "build/app.spec"),
        ("requirements.txt", "requirements.txt"),  # Keep in root
        
        # Scripts and launchers
        ("smart_launcher.py", "scripts/launcher.py"),
        ("launcher.bat", "scripts/launcher.bat"),
        
        # SSL certificates
        ("cert.pem", "certs/cert.pem"),
        ("key.pem", "certs/key.pem"),
        
        # Documentation
        ("README.md", "README.md"),  # Keep in root
        ("LICENSE", "LICENSE"),      # Keep in root
        ("CHANGELOG.md", "docs/CHANGELOG.md"),
        ("AUTOMATION_GUIDE.md", "docs/AUTOMATION_GUIDE.md"),
        ("NETWORK_OPTIMIZATION.md", "docs/NETWORK_OPTIMIZATION.md"),
        ("OPTIMIZATION_SUMMARY.md", "docs/OPTIMIZATION_SUMMARY.md"),
        ("RELEASE_STATUS.md", "docs/RELEASE_STATUS.md"),
        
        # Cleanup scripts (move to scripts for future use)
        ("cleanup_codebase.py", "scripts/cleanup_codebase.py"),
        ("cleanup_phase2.py", "scripts/cleanup_phase2.py"),
        ("build_release.py", "scripts/build_release.py"),
    ]
    
    moved_count = 0
    for source, destination in file_moves:
        if os.path.exists(source):
            try:
                # Create destination directory if it doesn't exist
                dest_dir = os.path.dirname(destination)
                if dest_dir:
                    os.makedirs(dest_dir, exist_ok=True)
                
                shutil.move(source, destination)
                print(f"📄 Moved: {source} → {destination}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Failed to move {source}: {e}")
        else:
            print(f"⚠️  File not found: {source}")
    
    return moved_count

def update_file_references():
    """Update file references in moved files"""
    updates = [
        # Update main.py paths
        {
            "file": "src/core/main.py",
            "changes": [
                ("'iphone.html'", "'../../web/templates/index.html'"),
                ("'cert.pem'", "'../../certs/cert.pem'"),
                ("'key.pem'", "'../../certs/key.pem'"),
            ]
        },
        # Update tray app paths
        {
            "file": "src/ui/tray_app.py",
            "changes": [
                ("'main.py'", "'../core/main.py'"),
            ]
        },
        # Update standalone paths
        {
            "file": "src/core/standalone.py",
            "changes": [
                # This file embeds HTML, so no changes needed
            ]
        },
        # Update build script paths
        {
            "file": "build/build.py",
            "changes": [
                ("'main.py'", "'../src/core/main.py'"),
                ("'enhanced_tray_app.py'", "'../src/ui/tray_app.py'"),
                ("'iphone.html'", "'../web/templates/index.html'"),
                ("'cert.pem'", "'../certs/cert.pem'"),
                ("'key.pem'", "'../certs/key.pem'"),
            ]
        },
        # Update spec file paths
        {
            "file": "build/app.spec",
            "changes": [
                ("'main.py'", "'../src/core/main.py'"),
                ("'iphone.html'", "'../web/templates/index.html'"),
                ("'cert.pem'", "'../certs/cert.pem'"),
                ("'key.pem'", "'../certs/key.pem'"),
            ]
        },
        # Update launcher paths
        {
            "file": "scripts/launcher.py",
            "changes": [
                ("'main.py'", "'../src/core/main.py'"),
                ("'enhanced_tray_app.py'", "'../src/ui/tray_app.py'"),
            ]
        },
    ]
    
    updated_count = 0
    for update in updates:
        file_path = update["file"]
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                for old_path, new_path in update["changes"]:
                    content = content.replace(old_path, new_path)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"🔧 Updated references in: {file_path}")
                    updated_count += 1
                
            except Exception as e:
                print(f"❌ Failed to update {file_path}: {e}")
    
    return updated_count

def create_new_launcher():
    """Create a new root-level launcher that points to the organized structure"""
    launcher_content = '''#!/usr/bin/env python3
"""
iPhone Webcam Server - Main Launcher
Organized project structure entry point
"""

import os
import sys

# Add src directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def main():
    """Main entry point for the application"""
    print("🚀 iPhone Webcam Server")
    print("=" * 30)
    print("1. Start Main Server")
    print("2. Start System Tray App")
    print("3. Interactive Launcher")
    print("4. Exit")
    
    choice = input("\\nSelect option (1-4): ").strip()
    
    if choice == "1":
        # Import and run main server
        from core.main import main as main_server
        main_server()
    elif choice == "2":
        # Import and run tray app
        os.system(f'python "{os.path.join(project_root, "src", "ui", "tray_app.py")}"')
    elif choice == "3":
        # Run interactive launcher
        os.system(f'python "{os.path.join(project_root, "scripts", "launcher.py")}"')
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
'''
    
    with open("run.py", 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print("🚀 Created new root launcher: run.py")

def create_project_readme():
    """Create a README for the new structure"""
    readme_content = '''# 📁 Project Structure

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
'''
    
    with open("STRUCTURE.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("📚 Created structure documentation: STRUCTURE.md")

def main():
    print("🏗️  iPhone Webcam - Codebase Restructuring")
    print("=" * 50)
    
    print("\\nThis will reorganize your project into a professional structure:")
    print("📁 src/core/     - Core application files")
    print("📁 src/ui/       - User interface components") 
    print("📁 web/          - Web interface files")
    print("📁 build/        - Build scripts and config")
    print("📁 certs/        - SSL certificates")
    print("📁 docs/         - Documentation")
    print("📁 scripts/      - Utility scripts")
    
    choice = input("\\n🤔 Proceed with restructuring? (y/n): ").lower().strip()
    if choice not in ['y', 'yes']:
        print("❌ Restructuring cancelled")
        return
    
    print("\\n🏗️  Creating directory structure...")
    create_directory_structure()
    
    print("\\n📦 Moving files to new locations...")
    moved_count = move_files()
    
    print("\\n🔧 Updating file references...")
    updated_count = update_file_references()
    
    print("\\n🚀 Creating new launcher...")
    create_new_launcher()
    
    print("\\n📚 Creating structure documentation...")
    create_project_readme()
    
    print(f"\\n✨ Restructuring completed!")
    print(f"📊 Statistics:")
    print(f"   • {moved_count} files moved")
    print(f"   • {updated_count} files updated")
    print(f"   • New launcher created: run.py")
    
    print(f"\\n🚀 Test your restructured project:")
    print(f"   python run.py")
    print(f"\\n📚 See STRUCTURE.md for the new organization")

if __name__ == "__main__":
    main()