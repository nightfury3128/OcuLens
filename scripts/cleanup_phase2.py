#!/usr/bin/env python3
"""
Final Cleanup Phase 2 - Remove Redundant Documentation
"""

import os
import shutil

def main():
    print("\n🧹 iPhone Webcam - Final Cleanup Phase 2")
    print("=" * 50)
    
    # Additional files that can be consolidated or removed
    redundant_files = [
        "AUTOMATION_GUIDE.md",    # Info is in README.md
        "RELEASE_STATUS.md",      # Temporary status file
        "build_release.py",       # Replaced by build_unified.py
        "OPTIMIZATION_SUMMARY.md", # Can merge into README
        "NETWORK_OPTIMIZATION.md", # Can merge into README
        "CHANGELOG.md",           # Can be in README or separate if needed
        "cleanup_codebase.py",    # This cleanup script itself (after use)
    ]
    
    print("🤔 Optional files to remove (will ask for each):")
    for file in redundant_files:
        if os.path.exists(file):
            print(f"\n📄 {file}")
            if file == "CHANGELOG.md":
                print("   Contains version history - keep if you want detailed changelog")
            elif file == "cleanup_codebase.py":
                print("   The cleanup script itself - can remove after cleanup is done")
            else:
                print(f"   Content can be integrated into main README.md")
            
            choice = input("   Remove this file? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                try:
                    os.remove(file)
                    print(f"   ✅ Removed {file}")
                except Exception as e:
                    print(f"   ❌ Failed to remove {file}: {e}")
            else:
                print(f"   ⏭️  Kept {file}")
    
    print(f"\n✨ Final cleanup completed!")
    print("\n📋 Remaining core files:")
    
    final_core_files = [
        "main.py",
        "enhanced_tray_app.py",
        "smart_launcher.py", 
        "iphone_webcam_standalone.py",
        "build_unified.py",
        "iphone.html",
        "README.md",
        "requirements.txt",
        "launcher.bat",
        "iPhone-Webcam.spec",
        "cert.pem",
        "key.pem", 
        "LICENSE"
    ]
    
    for file in final_core_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ❌ {file} (missing)")

if __name__ == "__main__":
    main()