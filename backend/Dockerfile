# Use the official NVIDIA CUDA image with Ubuntu 20.04 and CUDA 12.4
FROM nvidia/cuda:12.1.0-base-ubuntu20.04

# Set environment variable to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Add deadsnakes PPA for Python 3.10 packages
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0

# Set the working directory
WORKDIR /app

# Copy the setup script and requirements file into the container
COPY setup.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt and run setup.py
#RUN python3.10 -m pip install --no-cache-dir -r requirements.txt
RUN python3 setup.py install

# Copy the rest of the application code
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable for CUDA
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
