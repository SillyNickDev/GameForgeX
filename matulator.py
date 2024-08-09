#!/usr/bin/env python3

import os
import subprocess

def print_ascii_art():
    ascii_art = r"""
    __  __       _         _       _             
   |  \/  | __ _| |_ _   _| | __ _| |_ ___  _ __ 
   | |\/| |/ _` | __| | | | |/ _` | __/ _ \| '__|
   | |  | | (_| | |_| |_| | | (_| | || (_) | |   
   |_|  |_|\__,_|\__|\__,_|_|\__,_|\__\___/|_|   
    """
    print(ascii_art)

def install_packages():
    packages = [
        "steam", "virt-manager", "lutris", "obs-studio",
        "build-essential", "linux-headers-$(uname -r)",
        "axel", "wine", "winetricks"
    ]
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y"] + packages)

def setup_proton_ge():
    subprocess.run(["wget", "-O", "proton-ge.tar.gz",
                    "https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/Proton-*-GE.tar.gz"])
    subprocess.run(["mkdir", "-p", "~/.steam/root/compatibilitytools.d"])
    subprocess.run(["tar", "-xzf", "proton-ge.tar.gz", "-C", "~/.steam/root/compatibilitytools.d"])

def download_windows_image():
    download_link = input("Please enter the download link for Tiny10 Windows image: ")
    subprocess.run(["axel", "-n", "10", download_link, "-o", "~/Downloads/tiny10.iso"])

def setup_kernel_modules():
    modules = ["kvm", "kvm_intel", "kvm_amd"]
    for module in modules:
        subprocess.run(["sudo", "modprobe", module])

def confirm_reboot():
    first_confirmation = input("Do you want to reboot now? (yes/no): ").strip().lower()
    if first_confirmation == "yes":
        second_confirmation = input("Are you sure you want to reboot? (yes/no): ").strip().lower()
        if second_confirmation == "yes":
            subprocess.run(["sudo", "reboot"])

def main():
    print_ascii_art()
    install_packages()
    setup_proton_ge()
    download_windows_image()
    setup_kernel_modules()
    confirm_reboot()

if __name__ == "__main__":
    main()