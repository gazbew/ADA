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
        torch_spec = "torch"  # torchvision and torchaudio will be installed if listed in requirements.txt
    else:
        print("No CUDA GPU detected. Installing torch, torchvision, and torchaudio for CPU.")
        torch_spec = "torch torchvision torchaudio"
    
    with open('requirements.txt', 'r') as file:
        requirements = file.readlines()
    
    # Filter out comments and empty lines, adjust torch if necessary
    requirements = [line.strip() for line in requirements if line.strip() and not line.strip().startswith('#')]
    requirements = [line.split('#')[0].strip() if '#' in line else line for line in requirements]
    for i, req in enumerate(requirements):
        if req.startswith('torch'):
            # Replace the torch entry with torch_spec. If torch_spec has multiple packages,
            # they will be handled in the installation loop.
            requirements[i] = torch_spec
            # If torch_spec includes torchvision and torchaudio, remove them from other lines to avoid duplicates.
            if "torchvision" in torch_spec:
                requirements = [r for r in requirements if not r.startswith('torchvision')]
            if "torchaudio" in torch_spec:
                requirements = [r for r in requirements if not r.startswith('torchaudio')]
            # Re-insert the modified torch_spec at the original position if it was filtered out
            # This logic needs to be careful if torch_spec itself could be filtered out by subsequent lines.
            # A simpler way is to handle torch installation separately or ensure it's always one item.
            # For now, let's assume torch_spec replaces the 'torch' line and other related lines are removed.

    # Remove duplicate entries that might have been introduced or were already there
    requirements = sorted(list(set(requirements)))


    print("Installing dependencies...")
    for req_line in requirements:
        try:
            # Split req_line by space to handle multiple packages in one line (e.g., "torch torchvision torchaudio")
            pkgs_to_install = req_line.split()
            if not pkgs_to_install:
                continue
            print(f"Installing {req_line}...")
            # Ensure installation happens in the server's venv
            python_executable = os.path.join("server", "venv", "bin", "python")
            if not os.path.exists(python_executable):
                # Fallback for safety, though venv should exist if previous steps ran
                python_executable = sys.executable

            command = [python_executable, "-m", "pip", "install"] + pkgs_to_install
            if "torch" in req_line and not check_cuda(): # Apply index-url only for torch CPU install
                command.extend(["--index-url", "https://download.pytorch.org/whl/cpu"])
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print(f"Failed to install {req_line}. Continuing with next dependency.")
    
    print("Dependency installation complete.")

if __name__ == "__main__":
    install_dependencies()