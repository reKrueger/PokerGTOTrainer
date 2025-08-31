#!/usr/bin/env python3
"""
Poker GTO Trainer - Django Backend Startup Script
"""

import subprocess
import sys
import os

def main():
    print("🎰 Starting Poker GTO Trainer Django Backend")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print(f"📁 Working directory: {backend_dir}")
    
    # Check if virtual environment exists
    venv_path = os.path.join(backend_dir, "venv")
    if os.path.exists(venv_path):
        print("✅ Virtual environment found")
    else:
        print("⚠️  No virtual environment found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Unix/Linux/MacOS
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # Run migrations
    print("\n🔄 Running migrations...")
    subprocess.run([python_path, "manage.py", "migrate"])
    
    # Start development server
    print("\n🚀 Starting Django development server...")
    print("API will be available at: http://localhost:8000/api/")
    print("Health check: http://localhost:8000/api/health/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([python_path, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
