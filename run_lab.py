import subprocess
import os
import time
import sys

def run_lab():
    # Detect the root directory of the project
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("🛡️  TruthGuard Forensic Hub Initializing...")
    print("-" * 40)

    # 1. Launch Agentic Backend
    print("🧠  [1/2] Launching Neural Backend (Port 8000)...")
    # Using 'uv run' ensures the virtualenv is ready
    backend_process = subprocess.Popen(
        ["uv", "run", "python", "app.py"],
        cwd=backend_dir,
        shell=True # For Windows compatibility with system paths
    )

    # 🕧 Wait for Backend Neural Weights to initialize
    print("⏳  Cold-starting BERT Models. This takes ~10 seconds...")
    time.sleep(10)

    # 2. Launch Forensic Dashboard
    print("🔬  [2/2] Launching Forensic Dashboard (Port 5173)...")
    # Using npx vite to ensure the latest local binary is used
    frontend_process = subprocess.Popen(
        ["npx", "vite"],
        cwd=frontend_dir,
        shell=True
    )

    print("-" * 40)
    print("✅  TruthGuard Lab is LIVE!")
    print(f"📊  Research Dashboard: http://localhost:5173")
    print(f"🤖  Forensic API:      http://localhost:8000")
    print("-" * 40)
    print("CTRL+C to shut down the lab.")

    try:
        # Keep the script alive while both processes are running
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("⚠️  Backend process terminated unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("⚠️  Frontend process terminated unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\n🛑  Shutting down TruthGuard Lab...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    run_lab()
