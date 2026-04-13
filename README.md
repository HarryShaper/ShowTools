# 🎬 ShowTools

ShowTools is a lightweight VFX on-set utility designed to improve the speed and consistency of data sorting.

Built for speed and simplicity, it allows wranglers and capture technicians to quickly structure capture data, apply naming conventions, maniuplate file types, and generate user reports.

---

## ✨ Features

* 📂 Quickly sort full shoot-day packages, or pre-sort single data-sets.
* 🧠 Multiple sorting methods:
  * **Slate-based sorting**
  * **Asset-based sorting**
* 🧾 YAML report generation
* 🏷️ Bulk renaming across multiple folders with specified targetting
* 📸 Automatic focal length metadata detection
* 📁 Optional image type splitting (RAW / JPEG)
* ⚙️ Configurable pipeline and user profiles (YAML)
* 📧 Email notification integration
* 🖥️ Cross-platform support (Windows + macOS)

---

## 📁 Project Structure

```
ShowTools/
├── assets/                # Icons and UI assets
├── config/                # Pipeline profiles & defaults
├── launchers/             # Launch scripts (Windows/macOS)
├── showtools/             # Main Python package
│   ├── tools/             # Internal tools (e.g. FileSplitter)
│   ├── resources/         # Qt resources
│   ├── ui/                # UI files
│   ├── ShowTools.py       # Main application entry
│   ├── slate_sorter.py
│   ├── asset_sorter.py
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

>For Quick action - automator
> ```bash
>for f in "$@"
>do
>    osascript <<EOF
>tell application "Terminal"
>    activate
>    do script "cd '/Users/harryshaper/Documents/Personal_VFX/ShowTools' && python3 -m showtools.ShowTools \"$f\""
>end tell
>EOF
>done
> ```

---

## ▶️ Running the Tool

### 🪟 Windows

Double-click:

```
launchers/launch_windows.bat
```

Or run:

```bash
python -m showtools.ShowTools
```

---

### 🍎 macOS

#### First time only (required)

```bash
chmod +x launchers/launch_macOS.command
```
### macOS Security Notice

If macOS blocks the launcher:

- Right-click → Open
- Or go to System Settings → Privacy & Security → Allow Anyway


#### Then launch

Double-click:

```
launchers/launch_macOS.command
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

## ⚙️ Basic Usage

1. Select a **target folder** containing capture data
2. Load or create a **pipeline profile**
3. Configure:

   * project name
   * wrangler
   * unit
   * rename rules
4. Click **Export**

The tool will:

* sort files into slate/asset folders
* optionally split image folders
* generate a report
* optionally rename the package

---
## 🔁 Reversible Sorting

If enabled:
* A .showtools manifest is created
* You can revert the entire process
* Restores original structure and names

---

## 📦 Requirements

```
PySide6
Qt.py
PyYAML
Pillow
```

---

## 🧠 Development Notes

* Built with PySide6 + Qt
* Designed for on-set VFX workflows
* Structured as a modular Python package
* Tested on Windows and macOS

---
## 📚 Documentation & Tutorials

For more detailed guides:

📖 Wiki:
👉 (link to GitHub Wiki)

🎥 Video Tutorials:
👉 (link to YouTube channel / playlist)

Includes:

*Pipeline profiles
*Asset sorting setup
*Revert workflow
*Real-world examples
---

## 👤 Author

Harry Shaper
VFX Wrangler / Developer

---

## 📜 License

MIT License

---
