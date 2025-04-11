import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import psutil
import threading
import time
from datetime import datetime
from scanner import Scanner
from tkinter import filedialog
from malware import scan_files
from rambooster import RamBooster
import os  # Added to support taskkill commands

class ModernAntivirusGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Ryan's Shield")
        self.root.geometry("1200x800")
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self._create_sidebar()
        self._create_main_content()
        self._create_status_section()
        self._create_system_stats()
        self._create_action_buttons()
        self._create_progress_section()
          
        self.scanner = Scanner(self.status_label, self.progress_bar, self.root)
       

        self.update_system_stats()

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="RYAN'S SHIELD", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.nav_buttons = []
        for idx, text in enumerate(["Dashboard", "Security", "Privacy", "Performance", "Settings"]):
            btn = ctk.CTkButton(self.sidebar, text=text, command=lambda t=text: self.show_section(t))
            btn.grid(row=idx+1, column=0, padx=20, pady=10)
            self.nav_buttons.append(btn)

    def _create_main_content(self):
        self.content = ctk.CTkFrame(self.root)
        self.content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def _create_status_section(self):
        self.status_frame = ctk.CTkFrame(self.content)
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.protection_var = tk.BooleanVar(value=True)
        self.protection_switch = ctk.CTkSwitch(
            self.status_frame,
            text="Real-time Protection",
            variable=self.protection_var,
            command=self.toggle_protection
        )
        self.protection_switch.pack(side="left", padx=20)

    def _create_system_stats(self):
        self.stats_frame = ctk.CTkFrame(self.content)
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.cpu_progress = ctk.CTkProgressBar(self.stats_frame)
        self.cpu_progress.pack(padx=20, pady=5)
        self.cpu_label = ctk.CTkLabel(self.stats_frame, text="CPU Usage")
        self.cpu_label.pack()
        
        self.ram_progress = ctk.CTkProgressBar(self.stats_frame)
        self.ram_progress.pack(padx=20, pady=5)
        self.ram_label = ctk.CTkLabel(self.stats_frame, text="RAM Usage")
        self.ram_label.pack()

    def _create_action_buttons(self):
        self.buttons_frame = ctk.CTkFrame(self.content)
        self.buttons_frame.pack(fill="x", padx=20, pady=10)
        
        actions = [
            ("Quick Scan", lambda: self.scanner.quick_scan()),
            ("RAM Booster", lambda: self.boost_performance()),
            ("Malware", lambda: self.scan_for_malware())
        ]
        
        for text, command in actions:
            btn = ctk.CTkButton(
                self.buttons_frame,
                text=text,
                command=command,
                width=200,
                height=40,
                corner_radius=10
            )
            btn.pack(side="left", padx=10, pady=10)

##############################
    def _create_progress_section(self):
        self.progress_frame = ctk.CTkFrame(self.content)
        self.progress_frame.pack(fill="x", padx=20, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(padx=20, pady=10, fill="x")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.progress_frame, text="Ready")
        self.status_label.pack()
        # ✅ Add result_listbox for malware scan results
        self.result_listbox = tk.Listbox(
            self.progress_frame,
            height=1,   # Reduce height for a smaller box
            bg="black",
            fg="white",
            font=("Arial", 20),  # Smaller font size
            selectbackground="gray20",  # Better selection visibility
            selectforeground="white",
            relief="flat",  # Minimalist look
            )
        self.result_listbox.pack(padx=10, pady=10, fill="both", expand=False)  # Reduce padding

###############################

    def show_section(self, section):
        messagebox.showinfo("Navigation", f"Navigating to {section}")
        
    def toggle_protection(self):
        status = "enabled" if self.protection_var.get() else "disabled"
        self.status_label.configure(text=f"Real-time protection {status}")

    def update_system_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        
        self.cpu_progress.set(cpu_usage / 100)
        self.ram_progress.set(ram_usage / 100)
        self.cpu_label.configure(text=f"CPU Usage: {cpu_usage}%")
        self.ram_label.configure(text=f"RAM Usage: {ram_usage}%")
        
        self.root.after(1000, self.update_system_stats)

    def simulate_scan_progress(self, duration, operation):           
        self.progress_bar.set(0)
        steps = 100
        for i in range(steps + 1):
            if self.progress_bar.winfo_exists():
                progress = i / steps
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"{operation} in progress: {i}%")
                self.root.update_idletasks()
                time.sleep(duration / steps)
        self.status_label.configure(text=f"{operation} complete")
##############
    def scan_for_malware(self):
        directory = filedialog.askdirectory()  # ✅ Ensure directory is selected before proceeding

        if not directory:  # ✅ Prevents error if user cancels directory selection
            self.status_label.configure(text="Scan cancelled.")
            return

        self.result_listbox.delete(0, tk.END)  # ✅ Clears previous results
        infected_files = scan_files(directory, self.progress_bar, self.result_listbox)

        if infected_files:
            self.status_label.configure(text=f"Found {len(infected_files)} infected files.")
        else:
                self.status_label.configure(text="✅No infected files found.")


    ########################################33        
    def boost_performance(self):
        def performance_boost():
            try:
                booster = RamBooster(["OfficeClickToRun.exe","ms-teamsupdate.exe","notepad.exe", "AnyDesk.exe","msedge.exe","chrome.exe", "opera.exe", ])
                booster.add_task("taskmgr.exe")
                self.status_label.configure(text="✅Boosting performance...")

                status_updates = []
                
                for task in booster.task_list:
                    print(f"Attempting to kill: {task}")
                    result = os.system(f"taskkill /f /im {task}")
                    if result == 0:
                        message = f"✅Successfully terminated {task}"
                        print(message)
                        status_updates.append(message)
                        
                        self.status_label.configure(text=message)


                # Display all status updates after processing all tasks
                self.status_label.configure(text="\n".join(status_updates))
            except Exception as e:
                self.status_label.configure(text=f"Error: {e}")

        threading.Thread(target=performance_boost, daemon=True).start()


def main():
    app = ModernAntivirusGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
