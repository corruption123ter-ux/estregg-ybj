<p align="center">
  <img width="240" height="260" alt="Image" src="https://github.com/user-attachments/assets/e81e3b72-0ba0-418b-9fce-1dc855e2bf53" />
</p>

<h1 align="center">estregg-ybj</h1>

[![PyPI version](https://img.shields.io/pypi/v/estregg-ybj.svg?cacheSeconds=0)](https://pypi.org/project/estregg-ybj/)
[![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/estregg-ybj/)
[![GitHub release](https://img.shields.io/github/v/release/corruption123ter-ux/estregg-ybj)](https://github.com/corruption123ter-ux/estregg-ybj/releases)

<!-- Dependencies/Tools -->
[![Curses](https://img.shields.io/badge/dependency-curses-green.svg)](https://docs.python.org/3/library/curses.html)
[![WINE](https://img.shields.io/badge/platform-WINE-8F0052.svg)](https://github.com/corruption123ter-ux/estregg-ybj)

<!-- Platforms Supported -->
[![ChromeOS](https://img.shields.io/badge/platform-ChromeOS-yellow.svg)](https://github.com/corruption123ter-ux/estregg-ybj)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D6.svg?logo=windows&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)
[![macOS](https://img.shields.io/badge/platform-macOS-000000.svg?logo=apple&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)
[![Android](https://img.shields.io/badge/platform-Android-3DDC84.svg?logo=android&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)
[![Linux](https://img.shields.io/badge/platform-Linux-FCC624.svg?logo=linux&logoColor=black)](https://github.com/corruption123ter-ux/estregg-ybj)
[![Darwin](https://img.shields.io/badge/platform-Darwin-000000.svg?logo=apple&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)
[![Null](https://img.shields.io/badge/platform-Null-555555.svg?logo=gnubash&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)

<!-- Space Badge -->
[![Space](https://img.shields.io/badge/theme-space-FF4500.svg?logo=rocket&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)

<!-- Creator Badge -->
[![Creator](https://img.shields.io/badge/Creator-YB__Jeorgie-9932CC.svg?logo=gamepad&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)

<!-- ASCII Game Badge -->
[![ASCII Game](https://img.shields.io/badge/genre-ASCII%20Game-black.svg?logo=terminal&logoColor=white)](https://github.com/corruption123ter-ux/estregg-ybj)

<!-- Pip Install Badge -->
[![pip install](https://img.shields.io/badge/pip--install-estregg--ybj-3776AB.svg?logo=python&logoColor=white)](https://pypi.org/project/estregg-ybj/)

<p align="center">
  <strong>A terminal-based space exploration game built by YB_Jeorgie with Python curses.</strong>
</p>

---

## 🛠️ Requirements & Installation

To run `estregg-ybj`, you need **Python 3** and **pipx** installed on your system.

### Step 1: Install System Dependencies

Choose the command block below that matches your operating system:

#### Linux / Ubuntu / ChromeOS
```bash
sudo apt update && sudo apt install -y python3 python3-pip pipx && pipx ensurepath
```

#### macOS
```bash:
brew install pipx
pipx ensurepath
```

#### Windows (Command Prompt / PowerShell)
Command Prompt:
```bash:
py -m pip install --user pipx
py -m pipx ensurepath
```

Powershell:
```bash
py -m pip install --user pipx; pipx ensurepath
```

> ⚠️ **Note:** To run `estregg` on Windows, you must run `pip install windows-curses` in the Modern Windows Terminal first to prevent crashes.

#### Windows Offline / Download Troubleshooting
If you encounter network errors like **"cannot download python tools"**, you can install Python manually using a USB drive:
1. Use an online computer to download the standard Python installer executable from **[python.org](https://python.org)**.
2. Save the installer package directly to a **USB flash drive**.
3. Plug the USB into your target machine, run the installer, and ensure you check the box that says **"Add python.exe to PATH"** before finishing setup.

#### Android (Termux)
```bash:
pkg update && pkg upgrade -y
pkg install python pip -y
pip install pipx
pipx ensurepath
```

> ⚠️ Note: If this is your first time installing pipx, close and reopen your terminal after running pipx ensurepath so your environment updates properly. 

### Step 2: Install estregg-ybj
Install the package globally in an isolated environment using pipx:

```bash:
pipx install estregg-ybj
```
Or use Docker

```bash:
docker pull ghcr.io/corruption123ter-ux/estregg-ybj:v1.1.5
```
If you use Docker do these steps First:
---
### 1. Update package manager and install prerequisites: 
Run the following command in your Linux terminal to update your system and install necessary transfer tools:

```bash:
sudo apt update && sudo apt install -y ca-certificates curl gnupg
```

### 2. Add Docker official GPG key and repository:
Set up the official Docker repository for Debian:

```bash:
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 3. Install Docker engine:
Update your apt package list and install Docker:

```bash
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 4. Grant non-root permissions and start service:
Add your user to the docker group and start the Docker service inside Crostini:

```bash
sudo usermod -aG docker $USER
sudo service docker start
```
> Note: To verify that Docker is installed and running correctly, run:

```bash:
docker --version
```

If it Works: It will display a version number like Docker version 2x.x.x
if it has errors, try the entire process and restart your computer

---
> Note: If you already have estregg-ybj installed and want to update to the latest version, run:

```bash:
pipx upgrade estregg-ybj
```
> Note: If you Sucessfully Downloaded Estregg-ybj but when u Ran estregg it said "launching estregg" make sure you ran pipx ensurepath And Restarted your Terminal so estregg Works

---

## 🚀 Launching the Game
Once installed, start the game anytime by executing:

```bash:
estregg
```
Or

```bash:
docker run -it ghcr.io/corruption123ter-ux/estregg-ybj:v1.1.5
```

> 💡 Note for Mobile Users: Because mobile screens lack arrow keys, it is highly recommended to use a physical Bluetooth keyboard, Otg Keyboards, Virtual keyboards or an app like **Hacker's Keyboard** to play.

---

## 💬 Frequently Asked Questions

**Q: Is this a virus?**
*   **A:** No, it is not a virus! Everything is open-source, safe, and built entirely using standard Python libraries.

**Q: Did you copy someone else's creation?**
*   **A:** No. This is an entirely custom, original project built from scratch. 

**Q: Is this Illegal?**
*   **A:** No it is not illegal to code a game or to use legal dependecies tools

If you have any concerns please message me via:

**🖨[YB-Jeorgie reddit](https://www.reddit.com/user/Cool-Technician-7609/)**

**📧[Email](https://mail.google.com/mail/u/0/#inbox?compose=DmwnWrRmVpWPkbLGfDFPKWkpdVbxprZSJfhgzKtHczBNssdpggQDPPtbXZvntxsXNkxnpMkTlCVb)**

---

<h1 align="center">Please Note:</h1>

<p align="center">
  <strong>Gamepad controls isnt gonna work, it has been removed due to problems caused by Gamepad Control inputters, if you try the game would crash, i would not recommend connect a gamepad controller as it will break the game and your controller even if you want to.</strong>
</p>

<p align="center">
  <strong>INCOMING SIGNAL CODE <a href="https://lingojam.com">D4F6986</a> DECODE:</strong>
</p>

<p align="center">
  <strong>♒︎⧫︎⧫︎◻︎⬧︎🖳︎📭︎📭︎♍︎□︎❒︎❒︎◆︎◻︎⧫︎♓︎□︎■︎📂︎📄︎🗏︎⧫︎♏︎❒︎📫︎◆︎⌧︎📬︎♑︎⧫︎♒︎◆︎♌︎📬︎♓︎□︎📭︎🙰⬧︎⍓︎⬧︎⧫︎♏︎❍︎📫︎❄︎☜︎💣︎📭︎</strong>
</p>

<p align="center">
  <strong><a href="https://lingojam.com">Delta Code WD</a></strong>
</p>


<p align="center">
  <strong>Thankie And have a Good Day.</strong>
</p>
