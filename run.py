#!/usr/bin/env python3
"""
IntelliCourse AI — One-Click Project Launcher
Runs Django dev server and opens the SPA frontend in your default browser.
"""

import os
import sys
import subprocess
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1.5)
    print("\n🌐 Opening IntelliCourse AI in browser: http://127.0.0.1:8000/\n")
    webbrowser.open("http://127.0.0.1:8000/")

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    print("=" * 60)
    print("      🚀 INTELLICOURSE AI PLATFORM — ACADEMIC OPERATING SYSTEM")
    print("=" * 60)

    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Launch Django server
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"], check=True)
    except KeyboardInterrupt:
        print("\n👋 IntelliCourse AI server shut down successfully.")

if __name__ == "__main__":
    main()
