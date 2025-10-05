#!/usr/bin/env python3
"""
Unified Build Script for iPhone Webcam
Consolidates all build options into a single, efficient script
"""

import os
import sys
import subprocess
import shutil

def clean_previous_builds():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✅ Removed {dir_name}/")
            except Exception as e:
                print(f"  ⚠️  Could not remove {dir_name}/: {e}")

def build_standalone_exe():
    """Build standalone executable from the main script"""
    print("\n🔨 Building standalone executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=iPhone-Webcam",
        "--add-data=iphone.html;.",
        "--add-data=cert.pem;.",
        "--add-data=key.pem;.",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=pyvirtualcam",
        "--hidden-import=qrcode",
        "--hidden-import=PIL",
        "--collect-all=cv2",
        "--collect-all=numpy",
        "--noupx",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Standalone executable created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def build_tray_exe():
    """Build system tray executable"""
    print("\n🔨 Building tray executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=iPhone-Webcam-Tray",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "enhanced_tray_app.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Tray executable created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tray build failed: {e}")
        return False

def create_release_package():
    """Create a release package"""
    print("\n📦 Creating release package...")
    
    release_dir = "release"
    os.makedirs(release_dir, exist_ok=True)
    
    # Copy essential files
    files_to_copy = [
        "dist/iPhone-Webcam.exe",
        "dist/iPhone-Webcam-Tray.exe", 
        "README.md",
        "LICENSE",
        "requirements.txt"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"  ✅ Copied {file}")
        else:
            print(f"  ⚠️  Missing {file}")
    
    print(f"✅ Release package created in {release_dir}/")

def main():
    print("🚀 iPhone Webcam - Unified Build Script")
    print("=" * 50)
    
    print("\nBuild Options:")
    print("1. Build Standalone Executable (main.py)")
    print("2. Build Tray Application")
    print("3. Build Both + Create Release Package")
    print("4. Clean Only")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        clean_previous_builds()
        build_standalone_exe()
    elif choice == "2":
        clean_previous_builds()
        build_tray_exe()
    elif choice == "3":
        clean_previous_builds()
        if build_standalone_exe() and build_tray_exe():
            create_release_package()
    elif choice == "4":
        clean_previous_builds()
        print("✅ Cleanup completed!")
    elif choice == "5":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice!")
        return
    
    print("\n🎉 Build process completed!")
    print("\n📁 Check these locations:")
    if os.path.exists("dist"):
        print("  • dist/ - Individual executables")
    if os.path.exists("release"):
        print("  • release/ - Release package")

if __name__ == "__main__":
    main()