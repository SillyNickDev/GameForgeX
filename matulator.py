#!/usr/bin/env python3

import os
import subprocess
import sys

# Prints a simple ASCII art banner at the beginning of the script.
def print_ascii_art():
    ascii_art = r"""
   -------------------------------------------------------
   |     __  __       _         _       _                |
   |    |  \/  | __ _| |_ _   _| | __ _| |_ ___  _ __    |
   |    | |\/| |/ _` | __| | | | |/ _` | __/ _ \| '__|   |
   |    | |  | | (_| | |_| |_| | | (_| | || (_) | |      |
   |    |_|  |_|\__,_|\__|\__,_|_|\__,_|\__\___/|_|      |
   |                                                     |
   -------------------------------------------------------
    
    """
    print(ascii_art)

# Executes a shell command and handles potential errors.
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{' '.join(command)}' failed with exit code {e.returncode}.", file=sys.stderr)
        sys.exit(e.returncode)

# Determines the Linux distribution by reading the /etc/os-release file.
def detect_distro():
    distro = "unknown"
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.strip().split("=")[1].strip('"').lower()
                    break
    except FileNotFoundError:
        print("Error: Cannot detect the Linux distribution.", file=sys.stderr)
        sys.exit(1)
    return distro

# Checks if the root filesystem is mounted as read-only, which would prevent the script from making changes.
def check_read_only_filesystem():
    try:
        output = subprocess.run(["mount", "-o", "remount,rw", "/"], capture_output=True, text=True)
        if "read-only" in output.stderr:
            print("Error: The root filesystem is mounted as read-only. This script cannot run on a read-only filesystem.", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Failed to check the root filesystem status.", file=sys.stderr)
        sys.exit(1)

# Adds the Lutris PPA (Personal Package Archive) to the system's software sources, allowing you to install Lutris.
def add_lutris_ppa():
    print("Adding the Lutris PPA...")
    run_command(["sudo", "add-apt-repository", "ppa:lutris-team/lutris", "-y"])
    run_command(["sudo", "apt", "update"])

# Adds the i386 repository for Debian-based distros
def add_i386_repo():
    print("Adding the i386 repository...")
    run_command(["sudo", "apt-add-repository", "multiverse"])
    run_command(["sudo", "apt", "update"])

# Installs a set of packages based on the detected Linux distribution.
def install_packages(distro):
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()
    
    packages = [
        "steam-installer", "virt-manager", "obs-studio",
        "build-essential", f"linux-headers-{kernel_version}",
        "axel", "wine", "winetricks"
    ]
    
    if distro in ["ubuntu", "debian"]:
        run_command(["sudo", "apt", "update"])

        # Add the Lutris PPA before attempting to install
        add_lutris_ppa()
        # Add the i386 repository for Debian-based distros
        add_i386_repo()

        # Install Lutris and other packages
        packages.append("lutris")

        try:
            run_command(["sudo", "apt", "install", "-y"] + packages)
        except subprocess.CalledProcessError:
            print(f"Error: Failed to install packages. Lutris may not be available on {distro}.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: This script is not designed to run on {distro}. Exiting.", file=sys.stderr)
        sys.exit(1)

# Downloads and installs Proton-GE, a compatibility layer for running Windows games on Linux.
def setup_proton_ge():
    home_dir = os.path.expanduser("~")
    download_path = os.path.join(home_dir, "proton-ge.tar.gz")
    compatibility_dir = os.path.join(home_dir, ".steam/root/compatibilitytools.d")
    
    run_command(["axel", "-n", "10", "-o", download_path,
                 "https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/Proton-*-GE.tar.gz"])
    
    os.makedirs(compatibility_dir, exist_ok=True)
    run_command(["tar", "-xzf", download_path, "-C", compatibility_dir])

# Prompts the user to enter a download link for a Tiny10 Windows image and downloads it.
def download_windows_image():
    download_link = input("Please enter the download link for Tiny10 Windows image: ").strip()
    
    if not download_link:
        print("Error: No download link provided.", file=sys.stderr)
        sys.exit(1)
    
    download_dir = os.path.expanduser("~/Downloads")
    download_path = os.path.join(download_dir, "tiny10.iso")
    
    run_command(["axel", "-n", "10", download_link, "-o", download_path])

# Loads the kvm, kvm_intel, and kvm_amd kernel modules, which are necessary for virtualization.
def setup_kernel_modules():
    modules = ["kvm", "kvm_intel", "kvm_amd"]
    for module in modules:
        run_command(["sudo", "modprobe", module])

# Prompts the user to confirm if they want to reboot the system after the setup is complete.
def confirm_reboot():
    while True:
        first_confirmation = input("Do you want to reboot now? (yes/no): ").strip().lower()
        if first_confirmation == "yes":
            second_confirmation = input("Are you sure you want to reboot? (yes/no): ").strip().lower()
            if second_confirmation == "yes":
                run_command(["sudo", "reboot"])
            elif second_confirmation == "no":
                print("Reboot canceled.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        elif first_confirmation == "no":
            print("Reboot skipped.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Orchestrates the entire script.
def main():
    print_ascii_art()
    check_read_only_filesystem()
    distro = detect_distro()
    print(f"Detected distribution: {distro.capitalize()}")
    install_packages(distro)
    setup_proton_ge()
    download_windows_image()
    setup_kernel_modules()
    confirm_reboot()

# Ensures that the main() function is only executed when the script is run directly (not imported as a module).
if __name__ == "__main__":
    main()

# python is ending me :')
