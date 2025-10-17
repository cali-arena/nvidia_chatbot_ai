"""
Start Assessment Script
Automatically starts both servers for the final assessment
"""

import subprocess
import time
import sys
import os
import signal
import threading
from pathlib import Path

def start_server(script_name, port, description):
    """Start a server script"""
    try:
        print(f"🚀 Starting {description} on port {port}...")
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ {description} started successfully on port {port}")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start {description}")
            print(f"Error: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting {description}: {e}")
        return None

def monitor_server(process, description):
    """Monitor server process"""
    try:
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"⚠️ {description} stopped with error: {stderr}")
        else:
            print(f"✅ {description} stopped normally")
    except Exception as e:
        print(f"❌ Error monitoring {description}: {e}")

def main():
    """Main function to start both servers"""
    print("🎯 Final Assessment - Starting LangServe RAG System")
    print("=" * 60)
    
    # Check if required files exist
    required_files = ["server_app.py", "frontend_block.py", "frontend_server.py"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file not found: {file}")
            sys.exit(1)
    
    processes = []
    
    try:
        # Start LangServe server (port 9012)
        langserve_process = start_server("server_app.py", 9012, "LangServe Server")
        if langserve_process:
            processes.append(("LangServe Server", langserve_process))
        
        # Wait a moment between server starts
        time.sleep(2)
        
        # Start Frontend server (port 8000)
        frontend_process = start_server("frontend_server.py", 8000, "Frontend Server")
        if frontend_process:
            processes.append(("Frontend Server", frontend_process))
        
        if not processes:
            print("❌ No servers started successfully")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 SERVERS STARTED SUCCESSFULLY!")
        print("=" * 60)
        print("📊 LangServe Server: http://localhost:9012")
        print("🌐 Frontend Interface: http://localhost:8000")
        print("🔍 Health Check: http://localhost:9012/health")
        print("\n💡 Usage Instructions:")
        print("1. Open http://localhost:8000 in your browser")
        print("2. Test the different endpoints (Basic Chat, Retriever, Generator, RAG Chain)")
        print("3. Use Ctrl+C to stop all servers")
        print("=" * 60)
        
        # Monitor processes
        monitor_threads = []
        for name, process in processes:
            thread = threading.Thread(target=monitor_server, args=(process, name))
            thread.daemon = True
            thread.start()
            monitor_threads.append(thread)
        
        # Wait for user interrupt
        try:
            while True:
                time.sleep(1)
                # Check if any process died
                for name, process in processes[:]:
                    if process.poll() is not None:
                        print(f"⚠️ {name} stopped unexpectedly")
                        processes.remove((name, process))
                
                if not processes:
                    print("❌ All servers stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        # Cleanup processes
        for name, process in processes:
            try:
                print(f"🛑 Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"⚠️ Error stopping {name}: {e}")
        
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()
