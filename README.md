# Shower
A simple file encryption and decryption utility which uses AES encryption with CFB mode.<br/>
Protect your sensitive files with encryption.<br/>
Later you can decrypt them with secret keys.<br/>
The secret keys are random generated strings which are 32 characters long and consist of mixed of lowercase letters, capital letters and digits.<br/>
This application has been written in Python with PySide2 framework.

## Features
- File encryption
- File decryption

## Requirements
- [Python 3.6 or newer](https://www.python.org/downloads/)
- [xclip package (only on Linux)](https://launchpad.net/ubuntu/+source/xclip)
- [Git (for project cloning)](https://git-scm.com/)

## Getting started
- **On Windows:**
    - Open a terminal and clone the project:
        
        ```bash
        git clone https://github.com/antarn88/Shower.git
        ```
    - Create a virtual environment:
    
        ```bash
        cd Shower
        python -m venv venv
        ```
    - And activate it:
    
        ```bash
        venv\Scripts\activate
        ```
    - Upgrade pip and install the requirements:
    
        ```bash
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        ```
    - Then launch the application:
    
        ```bash
        Shower.pyw
        ```
- **On Linux:**
    - Install the required packages first, if you haven't already:
    
        ```bash
        apt update
        sudo apt install python3 python3-venv git xclip -y
        ```
      
    - Clone the project:
    
        ```bash
        git clone https://github.com/antarn88/Shower.git
        ```
    - Create a virtual environment:
    
        ```bash
        cd Shower
        python3 -m venv venv
        ``` 
    - And activate it:
        ```bash
        source venv/bin/activate
        ```
    - Upgrade pip and install the requirements:
        ```bash
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        ```
    - Then launch the application:
        ```bash
        python Shower.pyw
        ```

## Usage
Later when you would like to use the application, open a terminal
and navigate to the folder where you cloned the project to,
activate the virtual environment and launch the application:

- **On Windows:**

    ```bash
    venv\Scripts\activate
    Shower.pyw
    ```
- **On Linux:**

    ```bash
    source venv/bin/activate
    python Shower.pyw    
    ```

## Download Windows binaries
Download latest Windows binaries:<br/>
- [Shower_0.51_win32.zip](https://github.com/antarn88/Shower/releases/download/v0.51/Shower_0.51_win32.zip)
- [Shower_0.51_win64.zip](https://github.com/antarn88/Shower/releases/download/v0.51/Shower_0.51_win64.zip)

## Screenshots
**File encryption:**

![Windows screenshot](screenshots/screenshot_windows_01.png)

**File decryption:**

![Windows screenshot](screenshots/screenshot_windows_02.png)
