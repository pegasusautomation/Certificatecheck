import subprocess

script_file = "C:/manageserver/Serverheathcheck.ps1"

try:
    subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_file], check=True, text=True, shell=True)
    print("PowerShell script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing PowerShell script: {e}")
