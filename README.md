# 🎬 ShowTools

ShowTools is a lightweight VFX on-set utility designed to automate image sorting, package organisation, and report generation for shoot data.

Built for speed and simplicity, it allows wranglers and capture technicians to quickly structure capture data, apply naming conventions, and generate production-ready outputs.

---

## ✨ Features

* 📂 Automatic slate-based folder sorting
* 🧾 YAML report generation
* 🏷️ Flexible package renaming (prefix / suffix / cleanup)
* ⚠️ Empty folder detection and tagging
* 📸 Optional image subfolder splitting
* ⚙️ Configurable pipeline profiles
* 📧 Email notification integration
* 🖥️ Cross-platform support (Windows + macOS)

---

## 📁 Project Structure

```
ShowTools/
├── assets/                # Icons and UI assets
├── config/                # Pipeline profiles & defaults
├── scripts/               # Launch scripts (Windows/macOS)
├── showtools/             # Main Python package
│   ├── tools/             # Internal tools (e.g. FileSplitter)
│   ├── resources/         # Qt resources
│   ├── ui/                # UI files
│   ├── ShowTools.py       # Main application entry
│   ├── slate_sorter.py
│   └── generate_report.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### 1. Install Python

Download and install Python 3.10+ from python.org

---

### 2. Install dependencies

#### macOS / Windows

```bash
python -m pip install -r requirements.txt
```

> On macOS, use:
>
> ```bash
> python3 -m pip install -r requirements.txt
> ```

---

## ▶️ Running the Tool

### 🪟 Windows

Double-click:

```
scripts/launch_windows.bat
```

Or run:

```bash
python -m showtools.ShowTools
```

---

### 🍎 macOS

#### First time only (required)

```bash
chmod +x scripts/launch_macOS.command

### macOS Security Notice

If macOS blocks the launcher:

- Right-click → Open
- Or go to System Settings → Privacy & Security → Allow Anyway
```

#### Then launch

Double-click:

```
scripts/launch_macOS.command
```

Or run:

```bash
python3 -m showtools.ShowTools
```

---

## ⚠️ Notes (macOS)

* macOS requires execute permissions for launch scripts
* If the launcher does not work, use the terminal command above
* Folder/file names are **case-sensitive** on macOS

---

## ⚙️ Usage Overview

1. Select a **target folder** containing capture data
2. Load or create a **pipeline profile**
3. Configure:

   * project name
   * wrangler
   * unit
   * rename rules
4. Click **Export**

The tool will:

* sort files into slate folders
* optionally split image folders
* generate a report
* tag empty folders
* optionally rename the package

---

## 📦 Requirements

```
PySide6
Qt.py
PyYAML
```

---

## 🧠 Development Notes

* Built with PySide6 + Qt
* Designed for on-set VFX workflows
* Structured as a modular Python package
* Tested on Windows and macOS

---

## 🚧 Future Improvements

* One-click installer (Windows/macOS)
* Native macOS `.app` bundle
* Enhanced UI scaling consistency
* Expanded pipeline profile support

---

## 👤 Author

Harry Shaper
VFX Wrangler / Developer

---

## 📜 License

MIT License

---
