import sys
import subprocess
import os
import pkg_resources

def check_and_install_requirements():
    # Read requirements from requirements.txt
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # Check installed packages
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    missing = []

    for requirement in requirements:
        name = requirement.split('==')[0]
        if name.lower() not in installed:
            missing.append(requirement)

    if missing:
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    
    return True

def main():
    try:
        # Check and install requirements
        check_and_install_requirements()
        
        # Get the directory of the executable
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # Run the main application
        main_script = os.path.join(application_path, 'main.py')
        subprocess.run([sys.executable, main_script], check=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
