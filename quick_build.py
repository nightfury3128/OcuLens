#!/usr/bin/env python3
"""
Quick build script for iPhone Webcam - creates a minimal executable
"""

import subprocess
import sys
import os

def build_minimal_exe():
    """Build a minimal executable with only essential components"""
    print("🚀 Building minimal iPhone Webcam executable...")
    
    # Essential PyInstaller command with minimal dependencies
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                     # Single file
        "--noconsole",                   # No console window  
        "--name=iPhone-Webcam",          # Output name
        "--distpath=release",            # Output directory
        "--clean",                       # Clean build
        "--noconfirm",                   # No confirmation
        # Exclude heavy dependencies we don't absolutely need
        "--exclude-module=matplotlib",
        "--exclude-module=pandas", 
        "--exclude-module=scipy",
        "--exclude-module=tkinter",
        "--exclude-module=unittest",
        "--exclude-module=pydoc",
        "--exclude-module=doctest",
        "--exclude-module=argparse",
        "--exclude-module=calendar",
        "--exclude-module=pdb",
        "--exclude-module=cProfile",
        "--exclude-module=profile",
        "--exclude-module=pstats",
        "--exclude-module=trace",
        "--exclude-module=timeit",
        # Main script
        "iphone_webcam_standalone.py"
    ]
    
    try:
        print("⏳ This may take a few minutes...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print(f"📦 Executable created: release/iPhone-Webcam.exe")
            
            # Check file size
            exe_path = "release/iPhone-Webcam.exe"
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📊 File size: {size_mb:.1f} MB")
            
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def main():
    print("🎯 iPhone Webcam - Quick Build")
    print("=" * 40)
    
    if not os.path.exists("iphone_webcam_standalone.py"):
        print("❌ iphone_webcam_standalone.py not found!")
        return
    
    # Create release directory
    os.makedirs("release", exist_ok=True)
    
    if build_minimal_exe():
        print("\n🎉 Success! Your executable is ready!")
        print("📁 Check the 'release' folder for iPhone-Webcam.exe")
        print("\n📋 Distribution package includes:")
        print("   • iPhone-Webcam.exe (standalone executable)")
        print("   • No Python installation required")
        print("   • Just run and scan the QR code!")
        
    else:
        print("\n💡 Alternative: Use the Python file directly")
        print("   • python iphone_webcam_standalone.py")
        print("   • Works on any system with Python")

if __name__ == "__main__":
    main()