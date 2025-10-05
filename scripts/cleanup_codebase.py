#!/usr/bin/env python3
"""
Codebase Cleanup Script for iPhone Webcam Project
Removes duplicate and unnecessary files to clean up the project structure
"""

import os
import shutil
import sys

def confirm_deletion(message):
    """Ask user for confirmation before deleting"""
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def safe_remove(path, item_type="file"):
    """Safely remove a file or directory"""
    try:
        if os.path.exists(path):
            if item_type == "file":
                os.remove(path)
                print(f"✅ Removed file: {os.path.basename(path)}")
            else:
                shutil.rmtree(path)
                print(f"✅ Removed directory: {os.path.basename(path)}")
        else:
            print(f"⚠️  Not found: {os.path.basename(path)}")
    except Exception as e:
        print(f"❌ Failed to remove {path}: {e}")

def main():
    print("\n🧹 iPhone Webcam Codebase Cleanup")
    print("=" * 40)
    
    # Files to remove
    files_to_remove = [
        # Duplicate README
        "README.md",  # Keep README_NEW.md as it's more comprehensive
        
        # Redundant build scripts
        "build_exe.py",
        "build_single_file.py", 
        "quick_build.py",
        
        # Redundant launchers
        "launcher.py",
        "start_app.bat",
        
        # Duplicate spec file
        "IphoneWebcam.spec",  # Keep iPhone-Webcam.spec
        
        # Build artifacts
        "server_port.txt",
        "qr_code_port_5001.png",
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "build",  # PyInstaller build artifacts
        "dist",   # PyInstaller distribution folder (if exists)
        "__pycache__",  # Python cache
    ]
    
    print(f"\n📋 Files to be removed ({len(files_to_remove)}):")
    for file in files_to_remove:
        status = "✓" if os.path.exists(file) else "✗"
        print(f"  {status} {file}")
    
    print(f"\n📁 Directories to be removed ({len(dirs_to_remove)}):")
    for dir in dirs_to_remove:
        status = "✓" if os.path.exists(dir) else "✗"
        print(f"  {status} {dir}/")
    
    print("\n📌 Files to keep and consolidate:")
    essential_files = [
        "main.py",           # Core server
        "enhanced_tray_app.py",  # System tray app
        "smart_launcher.py",     # Smart launcher
        "iphone_webcam_standalone.py",  # Standalone version
        "iphone.html",           # Web interface
        "README_NEW.md",         # Comprehensive documentation
        "requirements.txt",      # Dependencies
        "launcher.bat",          # Windows batch launcher
        "iPhone-Webcam.spec",    # PyInstaller spec
        "cert.pem", "key.pem",   # SSL certificates
        "LICENSE",               # License file
    ]
    
    for file in essential_files:
        status = "✓" if os.path.exists(file) else "❌"
        print(f"  {status} {file}")
    
    if not confirm_deletion("\n🤔 Proceed with cleanup?"):
        print("❌ Cleanup cancelled")
        return
    
    print("\n🧹 Starting cleanup...")
    
    # Remove files
    for file in files_to_remove:
        safe_remove(file, "file")
    
    # Remove directories
    for dir in dirs_to_remove:
        safe_remove(dir, "directory")
    
    # Rename README_NEW.md to README.md
    if os.path.exists("README_NEW.md"):
        try:
            os.rename("README_NEW.md", "README.md")
            print("✅ Renamed README_NEW.md → README.md")
        except Exception as e:
            print(f"❌ Failed to rename README: {e}")
    
    print("\n✨ Cleanup completed!")
    print("\n📋 Recommended next steps:")
    print("  1. Test the main application: python main.py")
    print("  2. Test the tray app: python enhanced_tray_app.py")
    print("  3. Test the smart launcher: python smart_launcher.py")
    print("  4. Update any remaining documentation")
    print("  5. Commit your changes to git")
    
    print("\n📁 Final project structure:")
    core_files = [
        "main.py",
        "enhanced_tray_app.py", 
        "smart_launcher.py",
        "iphone_webcam_standalone.py",
        "iphone.html",
        "README.md",
        "requirements.txt",
        "launcher.bat",
        "iPhone-Webcam.spec",
        "cert.pem", "key.pem",
        "LICENSE"
    ]
    
    for file in core_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")

if __name__ == "__main__":
    main()