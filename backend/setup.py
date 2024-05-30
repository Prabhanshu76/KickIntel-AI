import subprocess
import sys
from pathlib import Path
import os

def install_requirements(requirements_file):
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)

def run_command(command, cwd=None):
    subprocess.run(command, shell=True, cwd=cwd, check=True)

def main():
    # Define the paths and requirements
    home_path = Path.home()
    requirements1 = "requirements.txt"
    #requirements2 = "requirements2.txt"
    
    # Install the first set of requirements
    install_requirements(requirements1)

    subprocess.run([sys.executable, "-m", "pip", "install", "lapx"], check=True)
    



    # Clone and set up ByteTrack
    byte_track_path = os.path.join(os.getcwd(), "ByteTrack")
    # Change the current working directory to the ByteTrack directory
    os.chdir(byte_track_path)
    #run_command(f"git clone https://github.com/ifzhang/ByteTrack.git", cwd=home_path)
    # Install requirements
    requirements_path = os.path.join(byte_track_path, "requirements.txt")
    install_requirements(requirements_path)

    # Run setup.py develop
    run_command(f"python3 setup.py develop", cwd=byte_track_path)

    # Change the current working directory back to the original
    os.chdir(home_path)
    
    # Install the second set of requirements
    #install_requirements(requirements2)
    
    # Clone and set up yolov5
    yolov5_path = home_path / "yolov5"
    run_command(f"git clone https://github.com/ultralytics/yolov5", cwd=home_path)
    run_command(f"pip install -r {yolov5_path}/requirements.txt", cwd=yolov5_path)


    # Install NumPy version 1.23.0
    subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.23.0"], check=True)

if __name__ == "__main__":
    main()
