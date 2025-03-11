## Создание образа RISC-V виртуальной машины с Docker

### Установка зависимостей и клонирование репозитория

Для начала необходимо установить все зависимости для сборки.

Пример для Ubuntu:

```Bash
# apt-get install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xz-utils zstd
```

Далее нужно склонировать репозиторий poky:

```Bash
$ git clone git://git.yoctoproject.org/poky
```

### Добавление Docker и подготовка к сборке

Теперь необходимо перейти в директорию ``poky`` и выполнить команду

```Bash
$ source oe-init-build-env
```

Для добавления docker в сборку понадобятся слои ``meta-oe``, ``meta-python``, ``meta-networking``, ``meta-filesystems`` и
``meta-virtualization``. Они находятся в отдельных репозиториях, поэтому, для их использования, нужно склонировать
репозитории в директорию poky:

```
$ git clone git://git.yoctoproject.org/meta-virtualization
$ git clone https://github.com/openembedded/meta-openembedded
```

Далее нужно добавить слои в конфигурационный файл bblayers.conf. Сделать это можно командой
```Bash
$ bitbake-layers add-layer meta-openembedded/meta-oe meta-openembedded/meta-python meta-openembedded/meta-networking meta-openembedded/meta-filesystems meta-virtualization
```

Изменим конфигурационный файл ``build/conf/local.conf``:

- Для того, чтобы в качестве целевой архитектуры выбрать riscv, добавим строчку ``MACHINE ?= "qemuriscv64"``

- Чтобы в виртуальной машине был предустановлен docker, добавим следующую строчку: ``IMAGE_INSTALL:append = " docker"``

- Для работы docker необходимо включить виртуализацию. Сделаем это так: ``DISTRO_FEATURES:append = " virtualization"``

### Сборка

Запустим сборку командой 

```Bash
$ bitbake core-image-minimal
```

После успешного завершения сборки запустим виртуальную машину (команда выполняется в директории poky/build/tmp/deploy/images):

```Bash
$ runqemu qemuriscv64
```

Можно протестировать работу docker, запустив, например, контейнер с Alpine Linux:

```Bash
$ docker run --rm -it alpine
```
