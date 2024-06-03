import subprocess
import sys
from pathlib import Path
import shutil
import os

def install_requirements(requirements_file):
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)

def run_command(command, cwd=None):
    subprocess.run(command, shell=True, cwd=cwd, check=True)

def download_file(url, output):
    run_command(f"gdown {url} -O {output}")

def unzip_file(zip_file, output_dir):
    shutil.unpack_archive(zip_file, output_dir)

def main():
    # Define the paths and requirements
    current_directory = Path.cwd()
    requirements1 = "requirements.txt"
    #requirements2 = "requirements2.txt"
    
    # Install the first set of requirements
    install_requirements(requirements1)

    subprocess.run([sys.executable, "-m", "pip", "install", "lapx"], check=True)
    
    # Install gdown to download files from Google Drive
    subprocess.run([sys.executable, "-m", "pip", "install", "gdown"], check=True)

    # Download the file from Google Drive and copy it to the model folder
    file_url = "https://drive.google.com/uc?id=1iEu2g-30nsmFPzcEIGXQmsjck1qPEZ6c"
    output_file = "best.pt"  # Output file name
    model_folder = current_directory / "model"
    model_folder.mkdir(parents=True, exist_ok=True)
    
    download_file(file_url, output_file)
    shutil.move(output_file, model_folder / "best.pt")

    # Download and unzip ByteTrack
    byte_track_zip_url = "https://drive.google.com/uc?id=1QuTyoCDUb1W5B2Jby2khIxvJOHaTPnEI"
    byte_track_zip_output = "ByteTrack.zip"
    download_file(byte_track_zip_url, byte_track_zip_output)
    unzip_file(byte_track_zip_output, current_directory)
    
    # Delete ByteTrack zip file
    os.remove(byte_track_zip_output)

    # Change the current working directory to the ByteTrack directory
    byte_track_path = current_directory / "ByteTrack"
    os.chdir(byte_track_path)
    requirements_path = byte_track_path / "requirements.txt"
    install_requirements(requirements_path)

    # Run setup.py develop
    run_command(f"python setup.py develop", cwd=byte_track_path)

    # Change the current working directory back to the original
    os.chdir(current_directory)
    
    # Clone and set up yolov5
    yolov5_path = current_directory / "yolov5"
    run_command(f"git clone https://github.com/ultralytics/yolov5", cwd=current_directory)
    run_command(f"pip install -r {yolov5_path}/requirements.txt", cwd=yolov5_path)

if __name__ == "__main__":
    main()
