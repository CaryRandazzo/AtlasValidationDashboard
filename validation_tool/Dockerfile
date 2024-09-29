# Use an official Miniconda base image with Python 3.12
FROM condaforge/miniforge3

# Set environment variables to prevent issues during package installation
ENV CONDA_AUTO_UPDATE_CONDA=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a new environment with Python 3.12
RUN conda create -n avd_tool_env python=3.12.4 -y && \
    conda init bash

# Activate the environment and install the necessary packages
RUN /bin/bash -c "source activate avd_tool_env && \
    conda install -c conda-forge root=6.32.2 matplotlib=3.9.1 seaborn=0.13.2 pandas=2.2.2 -y"

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Activate the environment and set it as default
RUN echo "source activate v" >> ~/.bashrc
ENV PATH="/opt/conda/envs/avd_tool_env/bin:$PATH"

# Set the working directory
WORKDIR /workspace

# Copy any local files into the container (optional, e.g., scripts)
COPY . /workspace

# Default command to run the Python interpreter
CMD ["python"]
