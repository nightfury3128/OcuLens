#!/usr/bin/env python3
"""
iPhone Webcam Server Launcher
Provides multiple launch options with automation features
"""

import sys
import subprocess
import os
import time

def print_banner():
    print("\n" + "="*50)
    print("     iPhone Webcam Server Launcher")
    print("="*50)

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Installation complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask, cv2, numpy, pyvirtualcam, pystray, qrcode
        return True
    except ImportError as e:
        print(f"⚠️  Missing required package: {e}")
        print("Would you like to install requirements? (y/n)")
        if input().lower().startswith('y'):
            return install_requirements()
        return False

def auto_launch():
    """Launch with full automation"""
    print("\n🚀 Starting Auto Launch Mode...")
    print("• Server will start automatically")
    print("• Browser will open in 3 seconds")
    print("• QR code will be generated")
    print("• Desktop shortcut will be created")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

def server_only():
    """Launch server without automation"""
    print("\n🖥️  Starting Server Only Mode...")
    print("• Server will start")
    print("• Manual browser access required")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

def tray_app():
    """Launch system tray application"""
    print("\n📱 Starting System Tray App...")
    print("• Right-click the tray icon for options")
    print("• Server can be controlled from tray menu")
    print("\nPress Ctrl+C to stop the tray app\n")
    
    try:
        subprocess.run([sys.executable, "enhanced_tray_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Tray app stopped by user")

def build_executable():
    """Build standalone executable"""
    print("\n🔨 Building executable...")
    print("This may take several minutes...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed" if os.name == 'nt' else "--console",
            "--name=iPhoneWebcam",
            "main.py"
        ]
        subprocess.run(cmd, check=True)
        print("✅ Build complete! Check the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install it with: pip install pyinstaller")

def show_menu():
    """Display the main menu"""
    print_banner()
    print("\nChoose your preferred launch method:")
    print("\n1. 🚀 Auto Launch (Server + Browser + QR Code)")
    print("2. 🖥️  Server Only (Manual browser access)")
    print("3. 📱 System Tray App (Background service)")
    print("4. 📦 Install Requirements")
    print("5. 🔨 Build Executable")
    print("6. ❌ Exit")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                if check_requirements():
                    auto_launch()
                break
                
            elif choice == "2":
                if check_requirements():
                    server_only()
                break
                
            elif choice == "3":
                if check_requirements():
                    tray_app()
                break
                
            elif choice == "4":
                install_requirements()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                build_executable()
                input("\nPress Enter to continue...")
                
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Launcher stopped by user")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()