#!/usr/bin/env python3
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
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        # Run main server
        main_script = os.path.join(project_root, "src", "core", "main.py")
        os.system(f'python "{main_script}"')
    elif choice == "2":
        # Run tray app
        tray_script = os.path.join(project_root, "src", "ui", "tray_app.py")
        os.system(f'python "{tray_script}"')
    elif choice == "3":
        # Run interactive launcher
        launcher_script = os.path.join(project_root, "scripts", "launcher.py")
        os.system(f'python "{launcher_script}"')
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
