#!/usr/bin/env python3
"""
GitHub Release Builder for iPhone Webcam
Creates a single executable that users can download and run
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

class ReleaseBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.release_dir = self.project_root / "release"
        self.build_dir = self.project_root / "build"
        
    def clean_build_dirs(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        for dir_path in [self.build_dir, self.dist_dir, self.release_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  ✅ Removed {dir_path.name}/")
        
        # Clean spec files
        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()
            print(f"  ✅ Removed {spec_file.name}")
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            import PyInstaller
            print(f"  ✅ PyInstaller {PyInstaller.__version__} found")
        except ImportError:
            print("  ❌ PyInstaller not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("  ✅ PyInstaller installed")
        
        # Check for required files
        required_files = ["main.py", "iphone.html", "cert.pem", "key.pem"]
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                print(f"  ✅ {file_name} found")
            else:
                print(f"  ❌ {file_name} missing!")
                return False
        
        return True
    
    def build_executable(self):
        """Build the standalone executable using PyInstaller"""
        print("\n🔨 Building standalone executable...")
        
        # PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=iPhone-Webcam",
            "--add-data=iphone.html;.",
            "--add-data=cert.pem;.",
            "--add-data=key.pem;.",
            "--hidden-import=cv2",
            "--hidden-import=numpy", 
            "--hidden-import=flask",
            "--hidden-import=pyvirtualcam",
            "--hidden-import=qrcode",
            "--hidden-import=PIL",
            "--hidden-import=OpenSSL",
            "--hidden-import=websockets",
            "--hidden-import=pystray",
            "--collect-all=cv2",
            "--collect-submodules=flask",
            "--distpath=dist",
            "--workpath=build",
            "main.py"
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Executable built successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def create_release_package(self):
        """Create a complete release package"""
        print("\n📦 Creating release package...")
        
        # Create release directory
        self.release_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_source = self.dist_dir / "iPhone-Webcam.exe"
        exe_dest = self.release_dir / "iPhone-Webcam.exe"
        
        if exe_source.exists():
            shutil.copy2(exe_source, exe_dest)
            print(f"  ✅ Copied iPhone-Webcam.exe ({exe_source.stat().st_size / 1024 / 1024:.1f} MB)")
        else:
            print("  ❌ Executable not found!")
            return False
        
        # Copy documentation
        docs_to_copy = [
            ("README.md", "README.md"),
            ("LICENSE", "LICENSE"),
            ("RELEASE_STATUS.md", "RELEASE_NOTES.md")
        ]
        
        for source_name, dest_name in docs_to_copy:
            source_path = self.project_root / source_name
            dest_path = self.release_dir / dest_name
            
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                print(f"  ✅ Copied {dest_name}")
        
        # Create quick start guide
        self.create_quick_start_guide()
        
        return True
    
    def create_quick_start_guide(self):
        """Create a simple quick start guide for users"""
        quick_start = """# iPhone Webcam - Quick Start Guide

## 🚀 Getting Started (3 Easy Steps)

### Step 1: Run the Application
- Double-click `iPhone-Webcam.exe`
- Windows may show a security warning - click "More info" then "Run anyway"

### Step 2: Connect Your iPhone
- A browser window will open automatically
- Scan the QR code displayed with your iPhone camera
- OR manually type the URL shown in your iPhone's Safari browser

### Step 3: Start Streaming
- Allow camera access when prompted on your iPhone
- Your iPhone camera will now appear as a webcam on your computer
- Use it in Zoom, Teams, OBS, or any video application

## 🎥 Using with Video Applications

### OBS Studio
1. Add a "Video Capture Device" source
2. Select "OBS Virtual Camera" as the device
3. Your iPhone feed will appear

### Zoom/Teams
1. Go to video settings
2. Select "OBS Virtual Camera" as your camera
3. Your iPhone is now your webcam!

## 🛠️ Troubleshooting

**Can't connect?**
- Make sure your iPhone and computer are on the same WiFi network
- Try refreshing the page on your iPhone

**Performance issues?**
- Close other applications using your camera
- Ensure good WiFi signal strength

**Security warning?**
- This is normal for new applications
- The app is safe - it only creates a local server

## 🆘 Need Help?
Visit: https://github.com/nightfury3128/iphoneWebCam/issues

---
*iPhone Webcam v2.0 - Transform your iPhone into a wireless webcam*
"""
        
        quick_start_path = self.release_dir / "QUICK_START.txt"
        with open(quick_start_path, 'w', encoding='utf-8') as f:
            f.write(quick_start)
        
        print("  ✅ Created QUICK_START.txt")
    
    def create_zip_release(self):
        """Create a ZIP file for the release"""
        print("\n📦 Creating ZIP release...")
        
        zip_path = self.project_root / "iPhone-Webcam-Release.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.release_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.release_dir)
                    zipf.write(file_path, arcname)
                    print(f"  ✅ Added {arcname}")
        
        zip_size = zip_path.stat().st_size / 1024 / 1024
        print(f"✅ Created iPhone-Webcam-Release.zip ({zip_size:.1f} MB)")
        
        return zip_path
    
    def get_file_info(self):
        """Get information about the built files"""
        print("\n📊 Release Information:")
        
        exe_path = self.release_dir / "iPhone-Webcam.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"  📱 Executable: iPhone-Webcam.exe ({size_mb:.1f} MB)")
        
        zip_path = self.project_root / "iPhone-Webcam-Release.zip"
        if zip_path.exists():
            size_mb = zip_path.stat().st_size / 1024 / 1024
            print(f"  📦 ZIP Package: iPhone-Webcam-Release.zip ({size_mb:.1f} MB)")
        
        print(f"  📁 Files in release/ folder: {len(list(self.release_dir.glob('*')))}")
    
    def build_release(self):
        """Main build process"""
        print("🚀 iPhone Webcam - GitHub Release Builder")
        print("=" * 50)
        
        # Step 1: Clean previous builds
        self.clean_build_dirs()
        
        # Step 2: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed!")
            return False
        
        # Step 3: Build executable
        if not self.build_executable():
            print("❌ Build failed!")
            return False
        
        # Step 4: Create release package
        if not self.create_release_package():
            print("❌ Release package creation failed!")
            return False
        
        # Step 5: Create ZIP
        zip_path = self.create_zip_release()
        
        # Step 6: Show information
        self.get_file_info()
        
        print("\n🎉 Release build completed successfully!")
        print("\n📋 Next Steps for GitHub Release:")
        print("1. Go to https://github.com/nightfury3128/iphoneWebCam/releases")
        print("2. Click 'Create a new release'")
        print("3. Upload 'iPhone-Webcam-Release.zip'")
        print("4. Upload 'iPhone-Webcam.exe' as additional asset")
        print("5. Use the content from RELEASE_NOTES.md for release description")
        
        print(f"\n📁 Release files are ready in:")
        print(f"  • {self.release_dir}")
        print(f"  • {zip_path}")
        
        return True

def main():
    """Main entry point"""
    builder = ReleaseBuilder()
    
    try:
        success = builder.build_release()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()