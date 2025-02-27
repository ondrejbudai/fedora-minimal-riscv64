import pexpect
import sys

if len(sys.argv) != 3:
    print("Usage: python3 test.py <image> <firmware>")
    sys.exit(1)

image = sys.argv[1]
firmware = sys.argv[2]

f = open("log", "w")

child = pexpect.spawn(
    f"""qemu-system-riscv64 \
        -smp cpus=5,maxcpus=5 \
        -m 2G \
        -machine virt,acpi=off \
        -device virtio-net-pci,netdev=n0,mac="FE:0B:6E:23:3D:9A" \
        -netdev user,id=n0,net=10.0.2.0/24,hostfwd=tcp::2225-:22 \
        -drive if=pflash,format=raw,unit=0,file={firmware},readonly=on \
        -drive file={image} -snapshot -nographic"""
)

child.logfile = f.buffer

child.expect("Please make a selection from the above", timeout=300)
print("configuring root")
child.sendline("4")

child.expect("Password:")
print("password 1st")
child.sendline("rootroot")

child.expect("Password")
print("password 2nd")
child.sendline("rootroot")

child.expect("Please respond 'yes' or 'no':")
print("confirming")
child.sendline("yes")


child.expect("Please make a selection from the above")
print("continuing")
child.sendline("c")


child.expect("localhost login:")
print("logging in")
child.sendline("root")

child.expect("Password:")
print("pasword 1st")
child.sendline("rootroot")

child.expect(r"~\]#")
print("running command")
child.sendline("systemctl is-system-running")

child.expect(r"~\]#")
assert "running" in child.before.decode("utf-8")

print("shutting down")
child.sendline("systemctl poweroff")
child.expect(pexpect.EOF)

child.wait()
