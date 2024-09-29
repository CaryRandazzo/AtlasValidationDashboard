# To build singularity containers:
# Ubuntu/Deb
sudo apt-get update && sudo apt-get install -y \
  build-essential \
  libseccomp-dev \
  pkg-config \
  squashfs-tools \
  cryptsetup \
  runc \
  wget \
  git \
  uuid-dev \
  libgpgme-dev \
  libglib2.0-dev \
  libssl-dev


# Download Go (replace with the latest version if needed)
wget https://go.dev/dl/go1.18.10.linux-amd64.tar.gz

# Extract the archive
sudo tar -C /usr/local -xzf go1.18.10.linux-amd64.tar.gz

# Set up Go environment variables
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Download and install sinngularity
export VERSION=4.2.1  # Use the latest version available
wget https://github.com/apptainer/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz

# I needed to manually to go the releases and download it and install it. Check the docs for singularity

# sudo systemctl start docker