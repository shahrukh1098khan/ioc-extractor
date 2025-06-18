# 🛡️ IOC Extractor - PDF to Excel

**IOC Extractor** is a Windows desktop application designed to extract **Indicators of Compromise (IOCs)** from PDF-based threat intelligence reports and export them to an Excel spreadsheet. Built for cybersecurity professionals, threat hunters, and SOC analysts, it streamlines IOC collection from malware reports and feeds.

---

## 🔍 Key Features

- **IOC Types Extracted:**
  - MD5, SHA1, SHA256 file hashes  
  - IPv4 and IPv6 addresses (plain and masked)  
  - Email addresses  
  - Domains and URLs

- **Obfuscation Handling:**
  - Recognizes and deobfuscates patterns like:
    - `hxxp[:]//example[.]com`
    - `admin[@]domain(dot)net`

- **Export to Excel:**
  - Outputs `.xlsx` file categorized by IOC type
  - Saved to:
    ```
    Desktop\IOCs Extractor\<PDF_FILENAME>.xlsx
    ```

- **User-Friendly Interface:**
  - Simple GUI with upload and one-click extract
  - No installation required

- **Offline Operation:**
  - Fully self-contained, no internet connection needed

---

## 🧑‍💼 How to Use (End Users)

1. Download `IOCs.exe` from the [`release/`](./release/) folder.
2. Run `IOCs.exe` (no installation needed).
3. Click **"Upload PDF & Extract IOCs"**.
4. Choose a threat intelligence PDF file.
5. Extracted IOCs are saved automatically to your Desktop in Excel format.

---

## 👨‍💻 How to Use (Developers)

### Requirements

- Python 3.8 or later

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the application:

python IOCs.py

## Build Your Own EXE
You can generate a standalone executable using PyInstaller:

```bash
python -m PyInstaller --onefile --windowed --icon=icon.ico --add-data "bg.png;." --add-data "icon.ico;." IOCs.py
```

## Output EXE will be in:

dist/IOCs.exe

## 👤 Author

**Shahrukh Khan**

---

## 📄 License

MIT License — Free for personal and commercial use.



