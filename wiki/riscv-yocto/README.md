# **Сборка минималистичной RISC-V виртуальной машины с Docker и systemd с помощью Yocto**

## **Введение**
В этом руководстве описан процесс сборки минималистичного образа операционной системы для архитектуры RISC-V с поддержкой systemd и Docker, используя Yocto Project. Итогом станет работающая виртуальная машина в QEMU, в которой можно запустить контейнер `hello-world`. Моя система Ubuntu 24.04

## **1. Установка зависимостей**
Перед началом установки убедитесь, что ваша система обновлена и установите необходимые пакеты:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y gawk wget git diffstat unzip texinfo gcc g++ build-essential     chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils     iputils-ping python3-git python3-jinja2 libegl1 libsdl1.2-dev pylint     xterm python3-subunit mesa-common-dev zstd liblz4-tool
```

## **2. Клонирование Yocto и необходимых слоев**
Yocto использует систему слоев, поэтому нам понадобятся:

- `poky` — основной слой Yocto
- `meta-riscv` — поддержка архитектуры RISC-V
- `meta-openembedded` — дополнительные пакеты, включая Docker

### **Клонируем слои**
```sh
mkdir yocto-riscv
cd yocto-riscv
git clone -b kirkstone git://git.yoctoproject.org/poky.git
git clone -b kirkstone https://github.com/riscv/meta-riscv.git
git clone -b kirkstone https://git.openembedded.org/meta-openembedded
git clone -b kirkstone git://git.yoctoproject.org/meta-virtualization
```

### **Настраиваем окружение Yocto**
```sh
cd poky
source oe-init-build-env
```

## **3. Конфигурация сборки**
Редактируем файл `build/conf/local.conf`:

```sh
nano conf/local.conf
```

Добавляем поддержку systemd и Docker:
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

Добавляем новые слои в `bblayers.conf`:
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

## **4. Сборка образа**
Запускаем процесс сборки:
```sh
bitbake core-image-minimal
```

Если выдает ошибку, можно попробовать
```sh
sudo systemctl stop apparmor
sudo systemctl disable apparmor

sudo mv /etc/apparmor /etc/apparmor.disabled
```
```sh
sudo nano /etc/default/grub
```
в нем 
```sh
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash namespace.unpriv_enable=1"
```
```sh
sudo update-grub

sudo reboot
```
а потом снова запускаем процесс сборки


Этот процесс может занять несколько часов.

## **5. Запуск образа в QEMU**
После успешной сборки запускаем эмуляцию RISC-V:
```sh
runqemu qemuriscv64
```
Проверяем работу Docker:
```sh
docker --version
systemctl status docker
```
Запускаем Docker, если он выключен:
```sh
systemctl start docker
systemctl enable docker
```

## **6. Тестовый запуск контейнера**
```sh
docker run hello-world
```
Если всё настроено правильно, появится стандартное приветственное сообщение от Docker.