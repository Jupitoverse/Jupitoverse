"""
System Check Script - Verify RAG Pipeline Setup
Tests all components before running the main pipeline
"""

import os
import sys
from pathlib import Path
import subprocess

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print("\n1️⃣  Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n2️⃣  Checking dependencies...")
    
    required_packages = [
        'torch',
        'transformers',
        'pandas',
        'openpyxl',
        'tqdm'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n   To install missing packages:")
        print(f"   pip install -r requirements.txt")
        return False
    
    print("   ✅ All dependencies installed")
    return True

def check_model():
    """Check if DeepSeek model is downloaded"""
    print("\n3️⃣  Checking DeepSeek model...")
    
    model_dir = Path(__file__).parent / "models" / "deepseek_coder_v2_lite"
    
    if model_dir.exists():
        files = list(model_dir.glob("*"))
        print(f"   ✅ Model directory exists")
        print(f"   📁 Location: {model_dir}")
        print(f"   📄 Files: {len(files)} files found")
        
        # Check for essential model files
        essential_files = ['config.json', 'pytorch_model.bin', 'tokenizer.json']
        found_essential = sum(1 for f in essential_files if (model_dir / f).exists() or 
                             len(list(model_dir.rglob(f))) > 0)
        
        if found_essential > 0:
            print(f"   ✅ Model files present ({found_essential}/{len(essential_files)})")
            return True
        else:
            print(f"   ⚠️  Model directory exists but may be incomplete")
            return False
    else:
        print(f"   ❌ Model not found at: {model_dir}")
        print(f"   Run: DOWNLOAD_MODEL.bat or python download_deepseek_model.py")
        return False

def check_databases():
    """Check if databases exist"""
    print("\n4️⃣  Checking databases...")
    
    base_dir = Path(__file__).parent.parent.parent
    java_db = base_dir / "vector store" / "javaMapping.db"
    skills_db = base_dir / "vector store" / "people_skills.db"
    
    java_ok = java_db.exists()
    skills_ok = skills_db.exists()
    
    if java_ok:
        size_mb = java_db.stat().st_size / (1024 * 1024)
        print(f"   ✅ javaMapping.db found ({size_mb:.2f} MB)")
    else:
        print(f"   ❌ javaMapping.db not found at: {java_db}")
    
    if skills_ok:
        size_mb = skills_db.stat().st_size / (1024 * 1024)
        print(f"   ✅ people_skills.db found ({size_mb:.2f} MB)")
    else:
        print(f"   ❌ people_skills.db not found at: {skills_db}")
    
    return java_ok and skills_ok

def check_directories():
    """Check if required directories exist"""
    print("\n5️⃣  Checking directories...")
    
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "llm output"
    
    # Create if doesn't exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ Input directory: {input_dir}")
    print(f"   ✅ Output directory: {output_dir}")
    
    # Check for input files
    excel_files = list(input_dir.glob("*.xlsx")) + list(input_dir.glob("*.xls"))
    
    if excel_files:
        print(f"   ✅ Found {len(excel_files)} Excel file(s) in input:")
        for f in excel_files[:3]:  # Show first 3
            print(f"      - {f.name}")
    else:
        print(f"   ⚠️  No Excel files found in input directory")
        print(f"      Place your input file in: {input_dir}")
    
    return True

def check_gpu():
    """Check GPU availability"""
    print("\n6️⃣  Checking GPU support...")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"   ✅ GPU available: {gpu_name}")
            print(f"   💾 GPU memory: {gpu_memory:.2f} GB")
            print(f"   🚀 Processing will be FAST")
            return True
        else:
            print(f"   ⚠️  No GPU detected")
            print(f"   💻 Will use CPU (slower but functional)")
            return False
    except:
        print(f"   ⚠️  Unable to check GPU status")
        return False

def check_disk_space():
    """Check available disk space"""
    print("\n7️⃣  Checking disk space...")
    
    try:
        import shutil
        
        total, used, free = shutil.disk_usage(Path.cwd())
        free_gb = free / (1024**3)
        
        print(f"   💾 Free space: {free_gb:.2f} GB")
        
        if free_gb > 10:
            print(f"   ✅ Sufficient disk space")
            return True
        else:
            print(f"   ⚠️  Low disk space (< 10GB)")
            return False
    except:
        print(f"   ⚠️  Unable to check disk space")
        return False

def run_all_checks():
    """Run all system checks"""
    print_header("RAG Pipeline System Check")
    print("Verifying all components before running the pipeline...\n")
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'DeepSeek Model': check_model(),
        'Databases': check_databases(),
        'Directories': check_directories(),
        'GPU Support': check_gpu(),
        'Disk Space': check_disk_space()
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for name, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
    
    print(f"\n📊 Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! Your system is ready to run the RAG pipeline!")
        print("\n💡 Next steps:")
        print("   1. Place Excel file in: DTU MOD/input/")
        print("   2. Run: RUN_RAG_PIPELINE.bat")
        print("   3. Check output in: DTU MOD/llm output/")
        return True
    else:
        print("\n⚠️  WARNING: Some components need attention")
        print("\n💡 To fix issues:")
        
        if not checks['Python Version']:
            print("   - Install Python 3.8+ from python.org")
        
        if not checks['Dependencies']:
            print("   - Run: pip install -r requirements.txt")
        
        if not checks['DeepSeek Model']:
            print("   - Run: DOWNLOAD_MODEL.bat")
        
        if not checks['Databases']:
            print("   - Ensure database files exist in vector store/")
        
        return False

if __name__ == "__main__":
    try:
        success = run_all_checks()
        
        print("\n" + "="*60)
        input("\nPress Enter to exit...")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during system check: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

