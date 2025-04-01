# qemu-riscv-cluster

![Flake8 Status](https://img.shields.io/github/actions/workflow/status/moevm/qemu-riscv-cluster/.github/workflows/flake8.yml?branch=main&label=Flake8%20Check)

## Project structure
-- This repository contains gRPC client and scripts to build and deploy workers in the RISC-V VM.

-- [Scripts and Yocto Layers to build VM image with all dependencies](https://github.com/moevm/vm_build_risc_v)

-- [Sources to build and run gRPC server and worker nodes](https://github.com/moevm/grpc_server)

## Contribution

### Recommendations for working with the repository

#### Setting up a pre-commit hook for formatting code using Black

- The black configuration settings are located in .pre-commit-config.yaml

- After cloning the project, download all the necessary dependencies using `pip install -r requirements.txt` in a virtual environment. Run the `pre-commit install` command in the virtual environment once. Next, the hook will be triggered with each commit.

- If black finds a problem in the code, he will fix it, and you will need to repeat `git add .` and `git commit -m "name_commit"`

- You can check for a hook with `cat command.git/hooks/pre-commit` if it returns the code then the hook is installed.

- Additional information is described in the file [using_black.md](wiki/using_black.md)