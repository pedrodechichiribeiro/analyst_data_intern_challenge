import sys
import subprocess
import platform
import os
import importlib.util

def check_tkinter():
    """Checks if Tkinter is installed (often missing on Linux)."""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_llama_cpp():
    print("\n--- AI Engine Installation ---")
    system = platform.system()
    
    # 1. MacOS (Metal) - Easiest
    if system == "Darwin":
        print("MacOS detected. Installing with Metal support...")
        try:
            # Set environment variables for Mac Metal acceleration
            os.environ["CMAKE_ARGS"] = "-DLLAMA_METAL=on"
            install("llama-cpp-python")
            return
        except:
            print("Metal install failed, trying standard CPU...")

    # 2. Windows / Linux (CUDA or CPU)
    base_url = "https://abetlen.github.io/llama-cpp-python/whl"
    
    # Priority List: CUDA 12 -> CUDA 11 -> CPU
    options = []
    
    # Try to detect NVIDIA GPU
    has_gpu = False
    try:
        subprocess.check_call("nvidia-smi", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("NVIDIA GPU detected.")
        has_gpu = True
    except:
        print("No NVIDIA GPU detected (or nvidia-smi missing).")

    if has_gpu and system == "Windows":
        # Windows Pre-built wheels
        options.append(f"{base_url}/cu122") 
        options.append(f"{base_url}/cu117") 
    
    # Always add CPU fallback (works for Linux & Windows)
    # If on Linux with CUDA, standard pip install usually compiles correctly if nvcc is present, 
    # but we stick to CPU fallback to guarantee it runs.
    options.append(f"{base_url}/cpu") 
    if system == "Linux" and has_gpu:
        print("Linux with GPU detected. Attempting standard compile (requires gcc/nvcc)...")
        try:
            os.environ["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
            install("llama-cpp-python")
            return
        except:
            print("Compilation failed. Falling back to pre-built wheels...")

    # Attempt Installation
    for index_url in options:
        try:
            print(f"Attempting install from: {index_url} ...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python", 
                "--extra-index-url", index_url
            ])
            print(f"\nSUCCESS: Installed using {index_url}\n")
            return
        except subprocess.CalledProcessError:
            print(f"Failed to install from {index_url}, trying next...")
            
    # Final Standard Attempt (Last Resort)
    try:
        print("Attempting generic pip install...")
        install("llama-cpp-python")
    except:
        print("\n[!] CRITICAL: Could not install llama-cpp-python.")
        print("The app will still run, but AI features will be disabled.")

def main():
    print(f"Setup running on {platform.system()}...")
    
    # 1. Check Tkinter
    if not check_tkinter():
        print("\n[!] ERROR: 'tkinter' is missing.")
        if platform.system() == "Linux":
            print("Please run: sudo apt-get install python3-tk")
        else:
            print("Please reinstall Python and check 'tcl/tk and IDLE'.")
        input("Press Enter to acknowledge (App may crash)...")

    # 2. Install Dependencies
    print("... Installing Standard Dependencies ...")
    try:
        dependencies = ["customtkinter", "matplotlib", "pandas", "numpy"]
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return

    # 3. Install AI
    install_llama_cpp()
    
    print("\n--- SETUP COMPLETE ---")
    print("You can now run: python main.py")

if __name__ == "__main__":
    main()