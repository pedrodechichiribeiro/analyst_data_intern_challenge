import sys
import subprocess
import platform
import os
import shutil
import re

def print_step(msg):
    print(f"\n{'='*60}\n{msg}\n{'='*60}")

def check_python_version():
    """Ensures the user is on a compatible Python version (3.10 - 3.12)."""
    major, minor = sys.version_info[:2]
    
    # AI libraries (llama-cpp, torch, etc.) lag behind Python releases.
    # 3.13 and 3.14 usually do NOT have wheels yet.
    if major == 3 and minor > 12:
        print_step("CRITICAL COMPATIBILITY ERROR")
        print(f"You are using Python {major}.{minor}, which is too new.")
        print("Most AI libraries (like llama-cpp-python) do not have pre-built")
        print("binaries for this version yet, causing compilation errors.")
        print("\nPLEASE INSTALL: Python 3.11 or Python 3.12")
        print("Download from: https://www.python.org/downloads/")
        sys.exit(1)
        
    if major == 3 and minor < 10:
        print(f"[!] WARNING: Python {major}.{minor} is quite old. Recommend upgrading to 3.11.")

def run_pip_install(packages, extra_args=None):
    """Safe wrapper for pip install."""
    cmd = [sys.executable, "-m", "pip", "install"]
    if extra_args:
        cmd.extend(extra_args)
    
    if isinstance(packages, list):
        cmd.extend(packages)
    else:
        cmd.append(packages)
        
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError:
        print(f"[!] Install failed for {packages}")
        return False

def check_system_deps():
    """Checks for basic system dependencies like Tkinter."""
    print_step("Checking System Dependencies")
    try:
        import tkinter
        print("[OK] Tkinter is available.")
    except ImportError:
        print("[!] WARNING: Tkinter is missing.")
        if platform.system() == "Linux":
            print("    -> Run: sudo apt-get install python3-tk")
        else:
            print("    -> Re-run Python installer and check 'tcl/tk and IDLE'.")

def get_cuda_version():
    """Attempts to find the installed CUDA version."""
    try:
        output = subprocess.check_output("nvidia-smi", shell=True).decode()
        match = re.search(r"CUDA Version:\s+(\d+)\.(\d+)", output)
        if match:
            return int(match.group(1)), int(match.group(2))
    except:
        pass
    return None, None

def install_llama_cpp():
    print_step("Installing AI Engine (llama-cpp-python)")
    
    system = platform.system()
    
    # 1. MacOS
    if system == "Darwin":
        print("Detected MacOS.")
        os.environ["CMAKE_ARGS"] = "-DGGML_METAL=on" 
        if run_pip_install("llama-cpp-python"):
            return
        del os.environ["CMAKE_ARGS"]
        run_pip_install("llama-cpp-python") # Fallback to CPU
        return

    # 2. Windows / Linux
    base_url = "https://abetlen.github.io/llama-cpp-python/whl"
    cuda_major, _ = get_cuda_version()
    
    target_wheels = []
    
    # Determine wheels based on Hardware
    if cuda_major:
        print(f"Detected NVIDIA GPU (CUDA {cuda_major}).")
        if cuda_major == 12:
            target_wheels.extend([f"{base_url}/cu124", f"{base_url}/cu123", f"{base_url}/cu122", f"{base_url}/cu121"])
        elif cuda_major == 11:
            target_wheels.append(f"{base_url}/cu117")
    else:
        print("No NVIDIA GPU detected. Defaulting to CPU.")

    # ALWAYS add CPU fallback
    target_wheels.append(f"{base_url}/cpu")

    # Try installing from wheels
    for index_url in target_wheels:
        print(f"\nAttempting install from: {index_url}")
        
        # Clean environment for wheel install (prevent source build trigger)
        if "CMAKE_ARGS" in os.environ: del os.environ["CMAKE_ARGS"]

        # Note: We use --force-reinstall to ensure we switch versions if hardware changed
        if run_pip_install("llama-cpp-python", ["--extra-index-url", index_url]):
            print(f"[SUCCESS] Installed using {index_url}")
            return
        
    # 3. Last Resort: Source Compile (Only works if user has C++ tools)
    print("\n[!] Pre-built wheels failed.")
    print("Attempting to compile from source (requires Visual Studio C++ or GCC)...")
    
    if run_pip_install("llama-cpp-python"):
        print("[SUCCESS] Compiled from source.")
        return

    print("\n[!!!] CRITICAL FAILURE: Could not install llama-cpp-python.")
    print(f"Current Python Version: {sys.version}")
    print("Please ensure you are using Python 3.10, 3.11, or 3.12.")

def main():
    print_step(f"Setup running on {platform.system()} ({platform.machine()})")

    # 1. Version Guard
    check_python_version()

    # 2. Checks
    check_system_deps()

    # 3. Dependencies
    print_step("Installing Standard Requirements")
    run_pip_install(["customtkinter", "matplotlib", "pandas", "numpy"])

    # 4. AI Engine
    try:
        install_llama_cpp()
    except Exception as e:
        print(f"Unexpected error: {e}")

    print_step("SETUP COMPLETE")
    print("Run your app with: python src/main.py")

if __name__ == "__main__":
    main()