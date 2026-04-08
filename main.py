from pathlib import Path
import subprocess
import sys

base_dir = Path(__file__).resolve().parent
script_dir = base_dir / "script"

subprocess.run([sys.executable, str(script_dir / "script_title.py")], check=True)
subprocess.run([sys.executable, str(script_dir / "script_html.py")], check=True)
subprocess.run([sys.executable, str(script_dir / "script_h2.py")], check=True)