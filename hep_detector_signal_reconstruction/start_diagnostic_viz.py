import subprocess
import os
import sys
import time

def run():
    # 1. Start FastAPI Backend
    print("🚀 Starting HEP Diagnostic Backend (FastAPI)...")
    backend_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.getcwd()
    )

    # 2. Start Vite Frontend
    print("📊 Starting Diagnostic Visualization Layer (Vite)...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=os.path.join(os.getcwd(), "viz"),
        shell=True
    )

    print("\n✅ Diagnostic Layer is running!")
    print("   - API: http://localhost:8000")
    print("   - Web Interface: Check console output for Vite port (usually http://localhost:5173)\n")
    print("Press Ctrl+C to terminate both processes.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Terminating components...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Done.")

if __name__ == "__main__":
    run()
