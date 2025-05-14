#!/usr/bin/env python3
import subprocess
import sys
import os

def check_cuda():
    """Check if CUDA GPU is available."""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0 and 'NVIDIA-SMI' in result.stdout:
            return True
    except Exception:
        return False
    return False

def check_virtual_env():
    """Check if running in a virtual environment."""
    return sys.prefix != sys.base_prefix

def install_dependencies():
    """Install dependencies from requirements.txt, adjusting for CUDA availability."""
    if not check_virtual_env():
        print("WARNING: Not running in a virtual environment. It is recommended to run this script in a virtual environment to avoid package conflicts.")
        user_input = input("Do you want to continue without a virtual environment? (y/n): ")
        if user_input.lower() != 'y':
            print("Aborting installation. Please activate a virtual environment and run this script again.")
            sys.exit(1)
    
    print("Checking for CUDA GPU...")
    if check_cuda():
        print("CUDA GPU detected. Installing torch with CUDA support.")
        torch_spec = "torch"
    else:
        print("No CUDA GPU detected. Installing torch-cpu for simpler setup.")
        torch_spec = "torch-cpu"
    
    with open('requirements.txt', 'r') as file:
        requirements = file.readlines()
    
    # Filter out comments and empty lines, adjust torch if necessary
    requirements = [line.strip() for line in requirements if line.strip() and not line.strip().startswith('#')]
    requirements = [line.split('#')[0].strip() if '#' in line else line for line in requirements]
    for i, req in enumerate(requirements):
        if req.startswith('torch'):
            requirements[i] = torch_spec
    
    print("Installing dependencies...")
    for req in requirements:
        try:
            print(f"Installing {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}. Continuing with next dependency.")
    
    print("Dependency installation complete.")

if __name__ == "__main__":
    install_dependencies()