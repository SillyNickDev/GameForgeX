# MATULATOR
a small python script that sets up stuff for myself , you can use this too.
---

# Gaming, Streaming, and VTubing Environment Setup Script

## Overview

This repository contains a Python script designed to automate the setup of a gaming, streaming, and VTubing environment on Debian-based Linux distributions. The script installs essential software such as Steam, Virt Manager, Proton GE, Lutris, OBS Studio, and other necessary tools. It also handles downloading a Windows image using Axel and prompts for a reboot confirmation.

## Features

- **ASCII Art Logo**: Displays a cool ASCII art logo when the script is launched.
- **Software Installation**: Installs essential software packages for gaming and streaming.
- **Proton GE Setup**: Downloads and sets up Proton GE for enhanced Steam compatibility.
- **Windows Image Download**: Prompts the user for a Tiny10 Windows image download link and downloads it using Axel.
- **Kernel Module Setup**: Loads necessary kernel modules for virtualization.
- **Reboot Confirmation**: Asks the user twice for confirmation before rebooting the system.

## Requirements

- A Debian-based Linux distribution (e.g., Ubuntu, Debian).
- Sudo privileges.
- An active internet connection.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sillyncikdev/MATULATOR.git
   cd repo-name
   ```

2. **Run the Script**:
   Execute the script with Python 3:
   ```bash
   python3 setup_environment.py
   ```

## Script Details

### ASCII Art Logo

The script begins by displaying an ASCII art logo to provide a visual introduction.

### Package Installation

The script installs the following packages using `apt`:
- Steam
- Virt Manager
- Lutris
- OBS Studio
- Build-essential
- Linux headers
- Axel
- Wine
- Winetricks

### Proton GE Setup

Proton GE is downloaded and extracted to the Steam compatibility tools directory to improve game compatibility.

### Windows Image Download

The script prompts the user to enter a download link for the Tiny10 Windows image, which is then downloaded using the Axel command-line utility.

### Kernel Module Setup

Essential kernel modules for virtualization, such as `kvm`, `kvm_intel`, and `kvm_amd`, are loaded using `modprobe`.

### Reboot Confirmation

The script asks the user twice if they want to reboot the system, ensuring that the user is ready for the reboot.

## Usage

After running the script, your system will have a complete setup for gaming, streaming, and VTubing. Ensure to follow any additional instructions provided by the installed software for configuration.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the open-source community and tools that make Linux gaming and streaming possible.
