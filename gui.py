import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import sys
import os
from datetime import datetime

class GroundNewsScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ground News Scraper")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.is_running = False
        self.process = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Ground News Article Scraper", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        url_label = ttk.Label(main_frame, text="Article URL:")
        url_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 10))
        
        # Fetch button
        self.fetch_button = ttk.Button(main_frame, text="Fetch Data", 
                                      command=self.start_scraping, style="Accent.TButton")
        self.fetch_button.grid(row=1, column=2, pady=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=2, column=1, sticky="ew", pady=(0, 10))
        
        # Console output
        console_label = ttk.Label(main_frame, text="Console Output:")
        console_label.grid(row=3, column=0, sticky="nw", pady=(10, 5))
        
        # Create frame for console and scrollbar
        console_frame = ttk.Frame(main_frame)
        console_frame.grid(row=3, column=1, columnspan=2, sticky="nsew", 
                          pady=(10, 0), padx=(10, 0))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        self.console_text = scrolledtext.ScrolledText(console_frame, height=20, width=70,
                                                     wrap=tk.WORD, state=tk.DISABLED)
        self.console_text.grid(row=0, column=0, sticky="nsew")
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Clear console button
        clear_button = ttk.Button(button_frame, text="Clear Console", 
                                 command=self.clear_console)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                     command=self.stop_scraping, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Open CSV button
        csv_button = ttk.Button(button_frame, text="Open Dataset.csv", 
                               command=self.open_csv)
        csv_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to scrape")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # Bind Enter key to fetch button
        self.url_entry.bind('<Return>', lambda event: self.start_scraping())
        
        # Set focus to URL entry
        self.url_entry.focus_set()
    
    def log_message(self, message):
        """Add message to console with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, formatted_message)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)
        
        # Update the UI
        self.root.update_idletasks()
    
    def clear_console(self):
        """Clear the console output"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)
    
    def validate_url(self, url):
        """Basic URL validation"""
        if not url.strip():
            return False, "Please enter a URL"
        
        if not url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"
        
        if 'ground.news' not in url:
            return False, "URL must be from ground.news"
        
        return True, ""
    
    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Warning", "Scraping is already in progress!")
            return
        
        url = self.url_var.get().strip()
        
        # Validate URL
        is_valid, error_msg = self.validate_url(url)
        if not is_valid:
            messagebox.showerror("Invalid URL", error_msg)
            return
        
        # Start scraping in a separate thread
        self.is_running = True
        self.fetch_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.progress_var.set("Scraping in progress...")
        self.status_var.set("Running scraper...")
        
        # Clear console
        self.clear_console()
        self.log_message("Starting Ground News scraper...")
        self.log_message(f"Target URL: {url}")
        
        # Start scraping thread
        self.scraping_thread = threading.Thread(target=self.run_scraper, args=(url,))
        self.scraping_thread.daemon = True
        self.scraping_thread.start()
    
    def run_scraper(self, url):
        """Run the scraper subprocess"""
        try:
            # Check if g.py exists
            script_path = os.path.join(os.path.dirname(__file__), 'g.py')
            if not os.path.exists(script_path):
                self.log_message("ERROR: g.py not found in the same directory!")
                self.scraping_finished(False)
                return
            
            # Prepare command
            cmd = [sys.executable, script_path, url]
            
            self.log_message(f"Running command: {' '.join(cmd)}")
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            if self.process.stdout:
                while True:
                    output = self.process.stdout.readline()
                    if output == '' and self.process.poll() is not None:
                        break
                    if output:
                        # Use after() to safely update GUI from thread
                        self.root.after(0, self.log_message, output.strip())
            
            # Get return code
            return_code = self.process.poll()
            
            if return_code == 0:
                self.root.after(0, self.log_message, "✅ Scraping completed successfully!")
                self.root.after(0, self.scraping_finished, True)
            else:
                self.root.after(0, self.log_message, f"❌ Scraping failed with exit code {return_code}")
                self.root.after(0, self.scraping_finished, False)
                
        except Exception as e:
            error_msg = f"Error running scraper: {str(e)}"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self.scraping_finished, False)
    
    def stop_scraping(self):
        """Stop the running scraping process"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.log_message("🛑 Scraping stopped by user")
        
        self.scraping_finished(False)
    
    def scraping_finished(self, success):
        """Called when scraping is finished"""
        self.is_running = False
        self.fetch_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        
        if success:
            self.progress_var.set("✅ Scraping completed!")
            self.status_var.set("Ready to scrape - Data saved to dataset.csv")
            # Clear URL for next scraping
            self.url_var.set("")
            self.url_entry.focus_set()
        else:
            self.progress_var.set("❌ Scraping failed!")
            self.status_var.set("Ready to scrape - Fix errors and try again")
    
    def open_csv(self):
        """Open the dataset.csv file"""
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
        
        if not os.path.exists(csv_path):
            messagebox.showwarning("File Not Found", "dataset.csv not found! Run the scraper first.")
            return
        
        try:
            # Try to open with default application
            if sys.platform == "win32":
                os.startfile(csv_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.call(["open", csv_path])
            else:  # Linux
                subprocess.call(["xdg-open", csv_path])
                
            self.log_message("📄 Opened dataset.csv")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open CSV file: {str(e)}")

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Configure colors
    style.configure('Accent.TButton', background='#0078d4', foreground='white')
    
    app = GroundNewsScraperGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
