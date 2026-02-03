"""
DeepSeek Coder V2 Lite Model Downloader
Downloads and caches the model locally for offline corporate usage
"""

import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def download_deepseek_model():
    """
    Download DeepSeek Coder V2 Lite model for local/offline usage
    """
    print("="*80)
    print("DeepSeek Coder V2 Lite Model Downloader")
    print("="*80)
    
    # Model configuration
    model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"  # DeepSeek Coder V2 Lite
    cache_dir = Path(__file__).parent / "models" / "deepseek_coder_v2_lite"
    
    # Create cache directory
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📦 Model: {model_name}")
    print(f"📁 Cache Directory: {cache_dir}")
    print(f"💾 Estimated Size: ~13GB")
    print(f"\n⚠️  This will download the model for offline usage.")
    print(f"    Ensure you have sufficient disk space and internet connectivity.\n")
    
    try:
        # Download tokenizer
        print("📥 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=str(cache_dir),
            trust_remote_code=True
        )
        print("✅ Tokenizer downloaded successfully!")
        
        # Download model
        print("\n📥 Downloading model (this may take 10-30 minutes)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=str(cache_dir),
            trust_remote_code=True,
            torch_dtype=torch.float16,  # Use half precision to save memory
            device_map="auto",  # Automatically distribute across available devices
            low_cpu_mem_usage=True
        )
        print("✅ Model downloaded successfully!")
        
        # Test the model
        print("\n🧪 Testing model...")
        test_prompt = "Write a Python function to add two numbers:"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                temperature=0.7,
                do_sample=True
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\n📝 Test Response:\n{response}\n")
        
        # Save configuration
        config_file = cache_dir / "download_info.txt"
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(f"Model: {model_name}\n")
            f.write(f"Downloaded: {Path(__file__).parent}\n")
            f.write(f"Cache Directory: {cache_dir}\n")
            f.write(f"Status: Successfully Downloaded\n")
            f.write(f"GPU Available: {torch.cuda.is_available()}\n")
            f.write(f"CUDA Version: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}\n")
        
        print("="*80)
        print("✅ SUCCESS! Model downloaded and ready for offline usage")
        print("="*80)
        print(f"\n📁 Model Location: {cache_dir}")
        print(f"🚀 You can now run the RAG pipeline offline!")
        print(f"\n💡 Next Steps:")
        print(f"   1. Place your input Excel file in: DTU MOD/input/")
        print(f"   2. Run: python rag_pipeline.py")
        print(f"   3. Check output in: DTU MOD/llm output/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR downloading model: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check internet connectivity")
        print(f"   2. Ensure sufficient disk space (~13GB)")
        print(f"   3. Try running with administrator privileges")
        print(f"   4. Check firewall/proxy settings")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting DeepSeek Coder V2 Lite download...\n")
    success = download_deepseek_model()
    sys.exit(0 if success else 1)

