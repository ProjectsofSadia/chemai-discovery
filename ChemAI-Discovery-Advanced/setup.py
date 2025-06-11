#!/usr/bin/env python3
"""
ChemAI Discovery - Advanced Setup Script
Automated installation and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3.8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - Compatible")

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "logs", "data/molecules", "data/datasets", 
        "models/pretrained", "models/custom", "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}/")
    
    print("✅ Directories created")

def check_optional_dependencies():
    """Check for optional dependencies"""
    print("🔍 Checking optional dependencies...")
    
    optional_deps = {
        'rdkit': 'Chemistry library for advanced molecular analysis',
        'torch': 'PyTorch for deep learning models',
        'tensorflow': 'TensorFlow for neural networks'
    }
    
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            print(f"✅ {dep} - Available ({description})")
        except ImportError:
            print(f"⚠️  {dep} - Not installed ({description})")

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    
    env_vars = {
        'PYTHONPATH': os.getcwd(),
        'CHEMAI_HOME': os.getcwd(),
        'GPU_ENABLED': 'false',
        'MAX_WORKERS': '4'
    }
    
    env_file = Path('.env')
    with open(env_file, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Environment configured")

def run_health_check():
    """Run initial health check"""
    print("🏥 Running health check...")
    try:
        import src.main
        print("✅ Application imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🧬 ChemAI Discovery - Advanced Setup")
    print("=" * 50)
    
    # System checks
    check_python_version()
    
    # Installation
    install_requirements()
    create_directories()
    setup_environment()
    
    # Optional checks
    check_optional_dependencies()
    
    # Health check
    if run_health_check():
        print("=" * 50)
        print("🏆 Setup completed successfully!")
        print("")
        print("🚀 Quick Start:")
        print("   make run                 # Start the platform")
        print("   python src/main.py       # Alternative start")
        print("   http://localhost:8000    # Open in browser")
        print("")
        print("📚 Documentation:")
        print("   docs/guides/user_guide.md")
        print("   http://localhost:8000/docs")
        print("=" * 50)
    else:
        print("❌ Setup completed with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
