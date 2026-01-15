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
    print("Installing llama-cpp-python...")
    base_url = "https://abetlen.github.io/llama-cpp-python/whl"
    
    # List of prioritized options
    options = []
    
    # 1. Try to detect CUDA
    try:
        subprocess.check_call("nvidia-smi", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("NVIDIA GPU detected.")
        # Try generic CUDA 12 first, then CUDA 11
        options.append(f"{base_url}/cu122") # CUDA 12.x
        options.append(f"{base_url}/cu117") # CUDA 11.x
    except:
        print("No NVIDIA GPU detected.")

    # 2. Always add CPU as the final fallback
    options.append(f"{base_url}/cpu")

    # 3. Attempt installation
    for index_url in options:
        try:
            print(f"Attempting install from: {index_url}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python", 
                "--extra-index-url", index_url
            ])
            print(f"\nSUCCESS: Installed using {index_url}\n")
            return # Exit function on success
        except subprocess.CalledProcessError:
            print(f"Failed to install from {index_url}, trying next...")

    print("\nCRITICAL: All installation attempts failed.")
    print("Please install Visual Studio C++ Build Tools and try again.")

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