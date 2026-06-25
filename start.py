#!/usr/bin/env python3
"""
GlobalPayroll Dashboard - Start Script
Launches both the Python FastAPI backend and the React frontend dev server.
"""

import subprocess
import sys
import os
import time
import signal


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, "backend")
    frontend_dir = project_dir

    print("=" * 60)
    print("  GlobalPayroll Dashboard - Multi-Country Payroll System")
    print("=" * 60)
    print()

    # Check Python dependencies
    print("[1/3] Checking Python dependencies...")
    try:
        import fastapi, sqlalchemy, pydantic
        print("      All Python dependencies found.")
    except ImportError:
        print("      Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(backend_dir, "requirements.txt")], check=True)

    # Seed the database
    print("[2/3] Seeding database with realistic payroll data...")
    sys.path.insert(0, backend_dir)
    from app.seed import seed_data
    seed_data()
    print("      Database seeded successfully.")

    # Start backend
    print("[3/3] Starting servers...")
    print()
    print("  Backend API: http://localhost:8000")
    print("  Frontend:    http://localhost:5173")
    print()
    print("  Press Ctrl+C to stop both servers.")
    print("-" * 60)

    backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
    frontend_cmd = ["npm", "run", "dev"]

    env = os.environ.copy()
    env["PYTHONPATH"] = backend_dir

    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=backend_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Wait a moment for backend to start
    time.sleep(2)

    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    def print_output(proc, label):
        for line in proc.stdout:
            print(f"  [{label}] {line.rstrip()}")

    import threading
    threading.Thread(target=print_output, args=(backend_proc, "API"), daemon=True).start()
    threading.Thread(target=print_output, args=(frontend_proc, "UI"), daemon=True).start()

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("[ERROR] Backend server exited.")
                break
            if frontend_proc.poll() is not None:
                print("[ERROR] Frontend server exited.")
                break
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")
        backend_proc.send_signal(signal.SIGTERM)
        frontend_proc.send_signal(signal.SIGTERM)
        backend_proc.wait(timeout=5)
        frontend_proc.wait(timeout=5)
        print("Done.")


if __name__ == "__main__":
    main()
