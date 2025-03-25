Вот обновленный вариант с добавленным уточнением про логин:  

---  

# **Building a Minimalist RISC-V Virtual Machine with Docker and systemd Using Yocto**  

## **Introduction**  
This guide describes the process of building a minimalist operating system image for the RISC-V architecture with support for systemd and Docker using the Yocto Project. The final result will be a working virtual machine in QEMU, where you can run the `hello-world` container. My system is Ubuntu 24.04.  

## **1. Installing Dependencies**  
Before starting the installation, make sure your system is updated and install the necessary packages:  

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y gawk wget git diffstat unzip texinfo gcc g++ build-essential     chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils     iputils-ping python3-git python3-jinja2 libegl1 libsdl1.2-dev pylint     xterm python3-subunit mesa-common-dev zstd liblz4-tool
```  

## **2. Cloning Yocto and Required Layers**  
Yocto uses a layer system, so we need the following:  

- `poky` — the main Yocto layer  
- `meta-riscv` — support for the RISC-V architecture  
- `meta-openembedded` — additional packages, including Docker  

### **Cloning the Layers**  
```sh
mkdir yocto-riscv
cd yocto-riscv
git clone -b kirkstone git://git.yoctoproject.org/poky.git
git clone -b kirkstone https://github.com/riscv/meta-riscv.git
git clone -b kirkstone https://git.openembedded.org/meta-openembedded
git clone -b kirkstone git://git.yoctoproject.org/meta-virtualization
```  

### **Setting Up the Yocto Environment**  
```sh
cd poky
source oe-init-build-env
```  

## **3. Configuring the Build**  
Edit the `build/conf/local.conf` file:  

```sh
nano conf/local.conf
```  

Add support for systemd and Docker:  
```ini
MACHINE ?= "qemuriscv64"
DISTRO ?= "poky"
PACKAGE_CLASSES ?= "package_rpm"
EXTRA_IMAGE_FEATURES ?= "debug-tweaks ssh-server-dropbear"
IMAGE_INSTALL:append = " docker-ce"
INIT_MANAGER = "systemd"
DISTRO_FEATURES:append = " systemd"
DISTRO_FEATURES:append = " virtualization"
VIRTUAL-RUNTIME_init_manager = "systemd"
```  

Add the new layers to `bblayers.conf`:  
```sh
nano conf/bblayers.conf
```  
```ini
BBLAYERS += "${TOPDIR}/../../meta-riscv"
BBLAYERS += "${TOPDIR}/../../meta-openembedded/meta-oe"
BBLAYERS += "${TOPDIR}/../../meta-openembedded/meta-networking"
BBLAYERS += "${TOPDIR}/../../meta-openembedded/meta-filesystems"
BBLAYERS += "${TOPDIR}/../../meta-openembedded/meta-python"
BBLAYERS += "${TOPDIR}/../../meta-virtualization"
```  

## **4. Building the Image**  
Start the build process:  
```sh
bitbake core-image-minimal
```  

If an error occurs, try the following:  
```sh
sudo systemctl stop apparmor
sudo systemctl disable apparmor

sudo mv /etc/apparmor /etc/apparmor.disabled
```  
Edit the GRUB configuration:  
```sh
sudo nano /etc/default/grub
```  
Modify the following line:  
```sh
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash namespace.unpriv_enable=1"
```  
Then update GRUB and reboot:  
```sh
sudo update-grub
sudo reboot
```  
After rebooting, restart the build process.  

This process may take several hours.  

## **5. Running the Image in QEMU**  
Once the build is complete, start the RISC-V emulation:  
```sh
runqemu qemuriscv64
```  

During the first boot, you will be prompted to enter login credentials. Use:  
- **Username:** `root`  
- **Password:** *(leave empty, just press Enter)*  

Check if Docker is working:  
```sh
docker --version
systemctl status docker
```  

If Docker is not running, start and enable it:  
```sh
systemctl start docker
systemctl enable docker
```  

## **6. Running a Test Container**  
```sh
docker run hello-world
```  

If everything is set up correctly, you should see the standard Docker welcome message.