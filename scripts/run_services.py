"""Development script to run all backend services."""
import subprocess
import sys
import os
from pathlib import Path

def run_service(service_name: str, port: int):
    """Run a Flask service."""
    service_path = Path(__file__).parent.parent / "services" / service_name
    env = os.environ.copy()
    env["FLASK_ENV"] = "development"
    env["PORT"] = str(port)
    
    print(f"Starting {service_name} service on port {port}...")
    return subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=service_path,
        env=env
    )

def main():
    """Run all services."""
    processes = []
    
    try:
        # Start all services
        processes.append(run_service("upload", 5001))
        processes.append(run_service("conversion", 5002))
        processes.append(run_service("download", 5003))
        
        print("\nAll services started successfully!")
        print("Upload Service: http://localhost:5001")
        print("Conversion Service: http://localhost:5002")
        print("Download Service: http://localhost:5003")
        print("\nPress Ctrl+C to stop all services")
        
        # Wait for all processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for process in processes:
            process.terminate()
        print("All services stopped")

if __name__ == "__main__":
    main()
