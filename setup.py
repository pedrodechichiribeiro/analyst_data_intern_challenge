# Hi, this script is meant for setting up llama-cpp-python manually without "pip install llama-cpp-python"
# This is done because (due to being somewhat recent) the regular install method won't work without C++ compilers
# I want this application to be widely usable without needing these finnicky configurations and extra downloads.
# So below is a python installer for the llamma-cpp-python directly, you should only need to run this once per-machine.

import sys
import subprocess
import platform
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_llama_cpp():
    print("Installing llama-cpp-python")
    
    # 1. Base URL for pre-built wheels (Official Repo)
    # This avoids the need for Visual Studio / C++ Compilers
    
    base_url = "https://abetlen.github.io/llama-cpp-python/whl"
    
    system = platform.system()
    
    # 2. Check for GPU (Nvidia) to see if we can use CUDA
    # Simple check: try running nvidia-smi
    has_gpu = False
    try:
        subprocess.check_call("nvidia-smi", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        has_gpu = True
        print("NVIDIA GPU detected. Installing CUDA-enabled version...")
    except:
        print("ℹNo NVIDIA GPU detected (or nvidia-smi missing). Defaulting to CPU version.")

    # 3. Construct the Installation Command
    # We use --extra-index-url to point pip to the pre-compiled files
    
    if has_gpu:
        # CUDA 12.x is the current standard. 
        # If this fails, the script will catch it, but this covers 90% of modern GPUs.
        index_url = f"{base_url}/cu122" 
    else:
        # CPU Only (Universal)
        index_url = f"{base_url}/cpu"

    try:
        # Run pip install with the specific index URL
        cmd = [
            sys.executable, "-m", "pip", "install", 
            "llama-cpp-python", 
            "--extra-index-url", index_url
        ]
        subprocess.check_call(cmd)
        print("\n == llama-cpp-python installed successfully! == ")
        
    except subprocess.CalledProcessError:
        print("\n == Pre-built wheel installation failed. ==")
        print("Attempting standard install (requires Visual Studio C++ Build Tools)...")
        try:
            install("llama-cpp-python")
        except:
            print("\nCRITICAL FAILURE: Could not install AI engine.")
            print("Please install 'Visual Studio Build Tools' with 'C++ Desktop Development' checked.")

def main():
    print("... Installing Standard Dependencies ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return

    install_llama_cpp()
    
    print("\n SETUP COMPLETE!!! :D")
    print("You can now run: python src/main.py\n")

if __name__ == "__main__":
    main()