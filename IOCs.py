import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz
import re
import pandas as pd
from pathlib import Path
import os
import sys

# --- IOC Regex Patterns ---
IOC_PATTERNS = {
    "MD5": r"\b[a-fA-F\d]{32}\b[,;]?",
    "SHA1": r"\b[a-fA-F\d]{40}\b[,;]?",
    "SHA256": r"\b[a-fA-F\d]{64}\b[,;]?",
    "Email": r"[a-zA-Z0-9._%+-]+(?:@|\[at\]|\[@\])[a-zA-Z0-9.-]+\.(?:[a-zA-Z]{2,})",
    "URL": r"(?:http|https|hxxp|hxxps)(?::|[:]?)//[\w\[\]\-./?%&=]+",
    "Domain": r"\b(?:[a-zA-Z0-9-]+\[?\.\]?)+(?:[a-zA-Z]{2,})\b",
    "IPv4": r"\b(?:\d{1,3}|\[\d{1,3}\])(?:\.|\[.\]){3}(?:\d{1,3}|\[\d{1,3}\])\b",
    "IPv6": r"\b(?:[a-fA-F0-9]{1,4}(?::|\[:\])){2,7}[a-fA-F0-9]{1,4}\b",
}

def deobfuscate(text):
    """Replaces common IOC obfuscation patterns."""
    replacements = {
        "hxxp": "http", "hxxps": "https",
        "[.]" : ".", "(dot)": ".", "[dot]": ".",
        "[:]" : ":", "[://]": "://",
        "[at]": "@", "[@]": "@", 
        "[::]": "::"
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages in a PDF."""
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def extract_iocs(text):
    """Extract IOCs from original and cleaned text using regex."""
    cleaned_text = deobfuscate(text)
    iocs = {key: set(re.findall(pattern, text)) | set(re.findall(pattern, cleaned_text))
            for key, pattern in IOC_PATTERNS.items()}
    for key in iocs:
        iocs[key] = set(x.strip(",; ") for x in iocs[key])
    return iocs

def save_to_excel(iocs, output_path):
    """Write IOCs into an Excel file with one column per type."""
    max_len = max((len(v) for v in iocs.values()), default=1)
    data = {k: list(v) + [""] * (max_len - len(v)) for k, v in iocs.items()}
    pd.DataFrame(data).to_excel(output_path, index=False)

def run_app():
    """Main PDF selection and processing logic."""
    file_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    try:
        text = extract_text_from_pdf(file_path)
        iocs = extract_iocs(text)

        desktop = Path.home() / "Desktop"
        output_dir = desktop / "IOCs Extractor"
        output_dir.mkdir(exist_ok=True)

        pdf_name = Path(file_path).stem
        output_path = output_dir / f"{pdf_name}.xlsx"

        save_to_excel(iocs, output_path)
        messagebox.showinfo("Success", f"IOCs exported to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("IOC Extractor PDF to Excel")
root.geometry("600x400")
root.resizable(False, False)

# Locate asset folder for PyInstaller or script
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(base_path, "icon.ico")
bg_path = os.path.join(base_path, "bg.png")

# Set icon
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print("Icon failed:", e)

# Set background image
try:
    bg_image = Image.open(bg_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Background failed:", e)

# Foreground UI
frame = tk.Frame(root, bg="white", bd=2)
frame.place(relx=0.5, rely=0.25, anchor="n")

tk.Label(frame, text="IOC Extractor for PDF Threat Reports", font=("Segoe UI", 12), bg="white").pack(pady=10)
tk.Button(frame, text="Upload PDF & Extract IOCs", command=run_app, padx=10, pady=8).pack()

tk.Label(root, text="Made by Shahrukh Khan\nLinkedIn: www.linkedin.com/in/shahrukh98khan",
         font=("Segoe UI", 9), fg="white", bg="#222").pack(side="bottom", pady=8)

root.mainloop()