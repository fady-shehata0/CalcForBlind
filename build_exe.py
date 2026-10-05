#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build script to create Windows EXE using PyInstaller
Usage: python build_exe.py
"""

import os
import sys
import subprocess
import shutil

def build_exe():
    """Build standalone EXE using PyInstaller"""
    
    print("=" * 60)
    print("Advanced Calculator - Building Executable")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n⚠️  PyInstaller is not installed.")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    build_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=AdvancedCalculator",
        "--onefile",
        "--windowed",
        "--icon=assets/calculator.ico" if os.path.exists("assets/calculator.ico") else None,
        "--add-data=calculator_settings.json:." if os.path.exists("calculator_settings.json") else None,
        "--distpath=./dist",
        "--buildpath=./build",
        "--specpath=./build",
        "calculator.py"
    ]
    
    # Remove None values from command
    build_cmd = [cmd for cmd in build_cmd if cmd is not None]
    
    print("\n📦 Building executable...")
    print(f"Command: {' '.join(build_cmd)}\n")
    
    try:
        subprocess.check_call(build_cmd)
        print("\n" + "=" * 60)
        print("✅ Build successful!")
        print("=" * 60)
        print("\nExecutable location: ./dist/AdvancedCalculator.exe")
        print("You can now run the calculator without Python installed.")
        
        # Cleanup
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("calculator.spec"):
            os.remove("calculator.spec")
        
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("❌ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    build_exe()
