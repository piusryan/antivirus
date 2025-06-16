
### 📄 Description

This is a lightweight **Antivirus Software built using Python** as part of my academic project in 2023. It scans directories for potentially harmful files based on file extensions, names, and hash-based signature detection. The project demonstrates basic malware scanning principles and file monitoring techniques, all implemented in pure Python.

---

### ⚙️ Features

* Scan folders and drives for suspicious files
* Detect threats based on predefined extensions and patterns
* File integrity check using **MD5/SHA256 hashes**
* Command-line and/or GUI interface (Tkinter if used)
* Option to delete, quarantine, or ignore flagged files
* SQLite or local file storage for logs (if you used it)

---

### 🛠️ Tech Stack

* **Language**: Python
* **Libraries**: `os`, `hashlib`, `tkinter`, `shutil`, `sqlite3` (based on your version)
* **Platform**: Works on Windows/Linux via terminal or GUI
* **Environment**: Packaged with `PyInstaller` or `cx_Freeze` (for .exe if you built it)



---

### 📝 Note

This project was created for educational use and to demonstrate file system monitoring and threat detection using Python. It’s not meant to replace real-world antivirus software.
