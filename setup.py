import sys
import subprocess
import platform
import os
import shutil
import re

def print_step(msg):
    print(f"\n{'='*60}\n{msg}\n{'='*60}")

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
    except subprocess.CalledProcessError as e:
        print(f"[!] Install failed for {packages}: {e}")
        return False

def check_system_deps():
    """Checks for basic system dependencies like Tkinter."""
    print_step("Checking System Dependencies")
    
    # 1. Check Tkinter
    try:
        import tkinter
        print("[OK] Tkinter is available.")
    except ImportError:
        print("[!] WARNING: Tkinter is missing.")
        if platform.system() == "Linux":
            print("    -> Run: sudo apt-get install python3-tk python3-venv")
        elif platform.system() == "Darwin":
            print("    -> MacOS usually includes it, or install python-tk via brew.")
        else:
            print("    -> Re-run the Python installer and check 'tcl/tk and IDLE'.")
        input("Press Enter to continue anyway (App GUI may crash)...")

def get_cuda_version():
    """Attempts to find the installed CUDA version."""
    try:
        # Try nvidia-smi first
        output = subprocess.check_output("nvidia-smi", shell=True).decode()
        # Look for 'CUDA Version: XX.X'
        match = re.search(r"CUDA Version:\s+(\d+)\.(\d+)", output)
        if match:
            major, minor = match.groups()
            return int(major), int(minor)
    except:
        pass
    
    # Fallback: check nvcc
    try:
        output = subprocess.check_output(["nvcc", "--version"]).decode()
        match = re.search(r"release (\d+)\.(\d+)", output)
        if match:
            major, minor = match.groups()
            return int(major), int(minor)
    except:
        pass

    return None, None

def install_llama_cpp():
    print_step("Installing AI Engine (llama-cpp-python)")
    
    system = platform.system()
    machine = platform.machine()
    
    # --- 1. MacOS (Apple Silicon/Intel) ---
    if system == "Darwin":
        print("Detected MacOS.")
        # Metal (GPU) support is usually enabled by default in newer wheels,
        # but we force the env var just in case.
        os.environ["CMAKE_ARGS"] = "-DGGML_METAL=on" 
        if run_pip_install("llama-cpp-python"):
            print("[SUCCESS] Installed for MacOS (Metal enabled if supported).")
            return
        else:
            print("Standard install failed. Trying CPU-only...")
            del os.environ["CMAKE_ARGS"]
            run_pip_install("llama-cpp-python")
            return

    # --- 2. Windows / Linux (NVIDIA GPU or CPU) ---
    
    # Base URL for pre-built wheels (AVOIDS COMPILATION)
    base_url = "https://abetlen.github.io/llama-cpp-python/whl"
    
    # Detect GPU
    cuda_major, cuda_minor = get_cuda_version()
    target_wheels = []

    if cuda_major:
        print(f"Detected NVIDIA GPU with CUDA {cuda_major}.{cuda_minor}")
        # Map detected CUDA version to likely available wheel versions
        # llama-cpp-python usually provides wheels for cu121, cu122, cu117, etc.
        
        if cuda_major == 12:
            target_wheels.append(f"{base_url}/cu124") # Try newest
            target_wheels.append(f"{base_url}/cu123")
            target_wheels.append(f"{base_url}/cu122")
            target_wheels.append(f"{base_url}/cu121")
        elif cuda_major == 11:
            target_wheels.append(f"{base_url}/cu117") # Most common for 11.x
    else:
        print("No NVIDIA GPU detected (or drivers missing). Defaulting to CPU.")

    # Always add CPU as the final fallback
    target_wheels.append(f"{base_url}/cpu")

    # --- Installation Loop ---
    for index_url in target_wheels:
        print(f"\nAttempting install from: {index_url}")
        
        # We try to install. If it works, we exit.
        # --force-reinstall ensures we don't keep a wrong version if one exists
        args = ["--extra-index-url", index_url]
        
        # Note: We do NOT set CMAKE_ARGS here because we want the pre-built wheel.
        # Setting CMAKE_ARGS forces a source build (which requires a compiler).
        if "CMAKE_ARGS" in os.environ:
            del os.environ["CMAKE_ARGS"]

        if run_pip_install("llama-cpp-python", args):
            print(f"[SUCCESS] Installed using {index_url}")
            return
        
    # --- 3. Final Resort: Compilation (Source Build) ---
    print("\n[!] Pre-built wheels failed.")
    
    # Check if compiler exists
    has_compiler = False
    if system == "Linux":
        if shutil.which("gcc") and shutil.which("g++"):
            has_compiler = True
    elif system == "Windows":
        # Harder to check reliably, but we try anyway
        has_compiler = True 

    if has_compiler:
        print("Attempting to compile from source (Slow, requires C++ compiler)...")
        # If we are here, we might as well try to enable BLAS if on Linux
        if system == "Linux" and cuda_major:
             os.environ["CMAKE_ARGS"] = "-DGGML_CUDA=on"
        
        if run_pip_install("llama-cpp-python"):
            print("[SUCCESS] Compiled from source.")
            return

    print("\n[!!!] CRITICAL FAILURE: Could not install llama-cpp-python.")
    print("Please ensure you have C++ Build Tools installed or check your Python version.")

def main():
    print_step(f"Setup running on {platform.system()} ({platform.machine()})")

    # 1. System Checks
    check_system_deps()

    # 2. Standard Dependencies
    print_step("Installing Standard Requirements")
    required_libs = ["customtkinter", "matplotlib", "pandas", "numpy"]
    run_pip_install(required_libs)

    # 3. AI Engine (The hard part)
    try:
        # Check if already installed to save time? 
        # Better to reinstall to ensure correct hardware matching if env changed.
        install_llama_cpp()
    except Exception as e:
        print(f"Unexpected error during AI install: {e}")

    print_step("SETUP COMPLETE")
    print("Run your app with: python src/main.py")

if __name__ == "__main__":
    main()