import subprocess
import os
import time
import sys
import webbrowser

def run_lab():
    # Detect the root directory of the project
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("\n" + "="*50)
    print("🛡️  TRUTHGUARD AGENTIC FORENSIC HUB INITIALIZING...")
    print("="*50 + "\n")

    # 1. Launch Agentic Backend
    print("🧠  [1/2] Launching Neural Backend (Port 8000)...")
    # Using 'uv run' ensures the virtualenv is ready
    try:
        backend_process = subprocess.Popen(
            ["uv", "run", "python", "app.py"],
            cwd=backend_dir,
            shell=True # For Windows compatibility
        )
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return

    # 🕧 Wait for Backend Neural Weights to initialize
    print("⏳  Cold-starting Neural Weights (BERT + TF-IDF)...")
    time.sleep(8)

    # 2. Launch Forensic Dashboard
    print("🔬  [2/2] Launching Forensic Dashboard (Port 5173)...")
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

    print("\n" + "-"*50)
    print("✅  TRUTHGUARD LAB IS NOW LIVE!")
    print(f"📊  Research Dashboard: http://localhost:5173")
    print(f"🤖  Forensic API:      http://localhost:8000")
    print("-" * 50)
    
    # Automatically open the research dashboard
    time.sleep(2)
    print("🌐  Opening Forensic Research Dashboard in your browser...")
    webbrowser.open("http://localhost:5173")

    print("\n💡 Press CTRL+C to safely shut down the lab.\n")

    try:
        # Keep the script alive while both processes are running
        while True:
            time.sleep(1)
            # Check if backend died
            if backend_process.poll() is not None:
                print("\n⚠️  [ALERT] Backend process terminated unexpectedly. Please check for errors.")
                break
            # Check if frontend died
            if frontend_process.poll() is not None:
                print("\n⚠️  [ALERT] Frontend process terminated unexpectedly. Please check for errors.")
                break
    except KeyboardInterrupt:
        print("\n🛑  Safely shutting down TruthGuard Lab...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Shutdown complete. Goodbye!\n")
        sys.exit(0)

if __name__ == "__main__":
    run_lab()


if __name__ == "__main__":
    run_lab()
