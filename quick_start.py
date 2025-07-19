#!/usr/bin/env python3
"""
n8n MCP Control Center - Quick Start Script
"""

import os
import sys
import subprocess
import requests

def print_banner():
    print("""
🚀 n8n MCP Control Center - Quick Start
======================================
""")

def check_python_version():
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_requirements():
    print("\n📦 Checking Python packages...")
    required = ['gradio', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("🔧 Install with: pip install gradio requests")
        return False
    return True

def check_environment():
    print("\n🔧 Checking environment variables...")
    n8n_url = os.getenv('N8N_API_URL', 'http://localhost:5678')
    n8n_key = os.getenv('N8N_API_KEY')
    
    print(f"📡 N8N_API_URL: {n8n_url}")
    
    if not n8n_key:
        print("⚠️ N8N_API_KEY not found")
        print("💡 Get API key from n8n Settings > API")
        return False, n8n_url, None
    
    print("✅ N8N_API_KEY - Found")
    return True, n8n_url, n8n_key

def test_n8n_connection(url, api_key):
    print(f"\n🌐 Testing n8n connection ({url})...")
    
    try:
        headers = {}
        if api_key:
            headers['X-N8N-API-KEY'] = api_key
        
        response = requests.get(f"{url}/api/v1/workflows", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ n8n API connection successful")
            return True
        elif response.status_code == 401:
            print("❌ Invalid API key (401 Unauthorized)")
            return False
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n. Is n8n running?")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def start_application():
    print("\n🚀 Starting n8n MCP Control Center...")
    print("📍 Will open at: http://localhost:7860")
    print("🔄 Press ENTER to start, Ctrl+C to cancel...")
    
    try:
        input()
        from functional_n8n_mcp_app import create_production_gradio_interface
        demo = create_production_gradio_interface()
        demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled.")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ App file not found: {e}")
        sys.exit(1)

def main():
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    if not check_requirements():
        sys.exit(1)
    
    env_ok, n8n_url, n8n_key = check_environment()
    
    if env_ok:
        connection_ok = test_n8n_connection(n8n_url, n8n_key)
    else:
        connection_ok = False
    
    print("\n📊 STATUS SUMMARY:")
    print(f"✅ Python: OK")
    print(f"✅ Packages: OK") 
    print(f"{'✅' if env_ok else '⚠️'} Environment: {'OK' if env_ok else 'Missing'}")
    print(f"{'✅' if connection_ok else '❌'} n8n Connection: {'OK' if connection_ok else 'Error'}")
    
    start_application()

if __name__ == "__main__":
    main()
