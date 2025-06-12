import subprocess
import sys
import os

def main():
    try:
        # Build the executable using PyInstaller
        subprocess.run([
            sys.executable, 
            "-m", 
            "PyInstaller",
            "--name=IphoneWebcam",
            "--onefile",

            # "--noconsole",  # Show console window for debugging
            "--icon=NONE",
            "--add-data", "iphone.html;.",
            "--collect-all", "cv2",
            "--collect-all", "numpy",
            "--collect-all", "flask",
            "--collect-all", "pyvirtualcam",
            "main.py"
        ], check=True)
        
        print("\nExecutable created successfully!")
        print("You can find it in the 'dist' folder")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
