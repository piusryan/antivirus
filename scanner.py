import os
import threading
from tkinter import messagebox

class Scanner:
    def __init__(self, status_label, progress_bar, root):
        self.status_label = status_label
        self.progress_bar = progress_bar
        self.root = root

    def quick_scan(self):
        threading.Thread(target=self._quick_scan).start()

    def _quick_scan(self):
        try:
            self.status_label.configure(text="Starting Quick Scan...")
            self.progress_bar.set(0)

            # Define the directories to clean
            temp_dir = os.environ.get('TEMP') or os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Temp')
            prefetch_dir = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')

            directories = [temp_dir, prefetch_dir]
            total_files = 0

            # Count total files
            for directory in directories:
                if os.path.exists(directory):
                    total_files += sum([len(files) for _, _, files in os.walk(directory)])

            if total_files == 0:
                self.status_label.configure(text="No temporary or prefetch files found")
                return

            files_processed = 0
            space_freed = 0

            # Start cleaning process
            for directory in directories:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory, topdown=False):
                        for name in files:
                            try:
                                file_path = os.path.join(root, name)
                                space_freed += os.path.getsize(file_path)
                                os.unlink(file_path)
                                files_processed += 1

                                progress = files_processed / total_files
                                self.progress_bar.set(progress)
                                self.status_label.configure(
                                    text=f"Cleaning files: {int(progress * 100)}% ({files_processed}/{total_files})"
                                )
                                self.root.update_idletasks()
                            except (PermissionError, FileNotFoundError):
                                continue

                        for name in dirs:
                            try:
                                os.rmdir(os.path.join(root, name))
                            except (PermissionError, OSError):
                                continue

            space_freed_mb = space_freed / (1024 * 1024)
            self.status_label.configure(
                text=f"Scan complete. Cleaned {files_processed} files ({space_freed_mb:.2f} MB freed)"
            )

        except Exception as e:
            self.status_label.configure(text=f"Error during scan: {str(e)}")
            self.progress_bar.set(0)
