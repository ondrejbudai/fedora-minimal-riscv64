# Fedora Minimal experimental riscv64 builds

This repository builds and hosts experimental riscv64 images of Fedora Minimal.

[Download the latest Fedora 41 image [[[(2025-03-10)](https://github.com/ondrejbudai/fedora-minimal-riscv64/actions/runs/13753831748/artifacts/2719210114)

This build was smoke-tested using QEMU. To launch it on Fedora, unzip it, and run:

```bash
qemu-system-riscv64 \
        -smp cpus=4,maxcpus=4 \
        -m 2G \
        -machine virt,acpi=off \
        -device virtio-net-pci,netdev=n0,mac="FE:0B:6E:23:3D:9A" \
        -netdev user,id=n0,net=10.0.2.0/24,hostfwd=tcp::2225-:22 \
        -drive if=pflash,format=raw,unit=0,file=/usr/share/edk2/riscv/RISCV_VIRT_CODE.fd,readonly=on \
        -drive file=./disk.raw,id=hd0 -device virtio-blk-device,drive=hd0
```
