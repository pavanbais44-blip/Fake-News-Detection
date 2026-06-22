import subprocess
import os
import time
import sys
import webbrowser
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_truthguard():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("\n" + "="*60)
    print("🛡️  TRUTHGUARD 2.9: AGENTIC FORENSIC LAB RUNNER")
    print("="*60 + "\n")

    # 1. Check for zombie processes
    if is_port_in_use(8000):
        print("⚠️  Warning: Port 8000 is already in use. Attempting to proceed...")
    if is_port_in_use(5173):
        print("⚠️  Warning: Port 5173 is already in use. The frontend might conflict.")

    # 2. Launch Backend
    print("🧠 [1/2] Initializing Neural Backend (Port 8000)...")
    try:
        backend_process = subprocess.Popen(
            ["uv", "run", "python", "app.py"],
            cwd=backend_dir,
            shell=True
        )
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return

    # 🚀 Wait for backend to be ready (Dynamic Health Check)
    print("⏳ Waiting for BERT and Agentic Modules to stabilize...")
    ready = False
    for i in range(120): # Wait up to 120 seconds for model downloads
        time.sleep(1)
        if is_port_in_use(8000):
            print("✅ Neural Lab Connection Established!")
            ready = True
            break
        if i % 10 == 0:
            print(f"   [{i}/120] Booting Neural Weights (Might be downloading BERT)...")
    
    if not ready:
        print("❌ Backend failed to start. Port 8000 never opened.")
        backend_process.terminate()
        return

    # 3. Launch Frontend
    print("🔬 [2/2] Launching Forensic Dashboard (Port 5173)...")
    try:
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            shell=True
        )
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        backend_process.terminate()
        return

    print("\n" + "—"*60)
    print("🚀 TRUTHGUARD LAB IS NOW LIVE!")
    print("📊 Research Dashboard: http://localhost:5173")
    print("🤖 Neural API Core:    http://localhost:8000")
    print("—" * 60)
    
    time.sleep(2)
    print("🌐 Opening Research Interface...")
    webbrowser.open("http://localhost:5173")

    print("\n💡 Keep this window open. Press CTRL+C to shut down both systems.\n")

    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("\n⚠️ [CRITICAL] Backend stopped.")
                break
            if frontend_process.poll() is not None:
                print("\n⚠️ [CRITICAL] Frontend stopped.")
                break
    except KeyboardInterrupt:
        print("\n🛑 Shutting down TruthGuard Laboratory safely...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Systems offline.\n")
        sys.exit(0)

if __name__ == "__main__":
    run_truthguard()
