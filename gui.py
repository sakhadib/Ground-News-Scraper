import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu
import threading
import subprocess
import sys
import os
from datetime import datetime

class GroundNewsScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 Ground News Scraper")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f2f5')
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Variables
        self.is_running = False
        self.process = None
        
        # Configure modern style
        self.setup_style()
        self.setup_ui()
        self.create_context_menu()
        
    def setup_style(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern colors and styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'),
                       foreground='#1a365d',
                       background='#f0f2f5')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#4a5568',
                       background='#f0f2f5')
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10),
                       padding=10)
        
        style.configure('Accent.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 9),
                       padding=8)
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 9),
                       padding=8)
        
        # Configure Entry style
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 10),
                       padding=8)
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Main.TFrame',
                       background='#f0f2f5')
    
    def create_context_menu(self):
        """Create right-click context menu for URL entry"""
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📋 Paste", command=self.paste_from_clipboard)
        self.context_menu.add_command(label="✂️ Cut", command=self.cut_text)
        self.context_menu.add_command(label="📄 Copy", command=self.copy_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Clear", command=self.clear_url)
        self.context_menu.add_command(label="📌 Select All", command=self.select_all_text)
    
    def paste_from_clipboard(self):
        """Paste text from clipboard to URL entry"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_var.set(clipboard_text)
        except tk.TclError:
            pass  # Clipboard is empty or inaccessible
    
    def cut_text(self):
        """Cut selected text from URL entry"""
        try:
            if self.url_entry.selection_present():
                selected_text = self.url_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.url_entry.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def copy_text(self):
        """Copy selected text from URL entry"""
        try:
            if self.url_entry.selection_present():
                selected_text = self.url_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
        except tk.TclError:
            pass
    
    def clear_url(self):
        """Clear URL entry"""
        self.url_var.set("")
    
    def select_all_text(self):
        """Select all text in URL entry"""
        self.url_entry.select_range(0, tk.END)
    
    def show_context_menu(self, event):
        """Show context menu on right click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
        
    def setup_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header section
        self.setup_header(main_container)
        
        # URL input section
        self.setup_url_section(main_container)
        
        # Console section
        self.setup_console_section(main_container)
        
        # Control buttons section
        self.setup_controls_section(main_container)
        
        # Status bar
        self.setup_status_bar(main_container)
    
    def setup_header(self, parent):
        """Setup header section with title and description"""
        header_frame = ttk.Frame(parent, style='Main.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Main title
        title_label = ttk.Label(header_frame, 
                               text="🌍 Ground News Scraper", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Extract comprehensive news data with political bias analysis",
                                  style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0)
    
    def setup_url_section(self, parent):
        """Setup URL input section with modern card design"""
        # URL input card
        url_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        url_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        url_card.columnconfigure(1, weight=1)
        
        # URL label with icon
        url_label = ttk.Label(url_card, text="🔗 Article URL:", 
                             font=('Segoe UI', 10, 'bold'))
        url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # URL entry with modern styling
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_card, textvariable=self.url_var, 
                                  style='Modern.TEntry', width=70,
                                  font=('Segoe UI', 10))
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Bind right-click context menu
        self.url_entry.bind("<Button-3>", self.show_context_menu)
        
        # Fetch button with modern styling
        self.fetch_button = ttk.Button(url_card, text="🚀 Fetch Data", 
                                      command=self.start_scraping, 
                                      style="Accent.TButton")
        self.fetch_button.grid(row=1, column=2, pady=5, padx=(10, 0))
        
        # Progress section
        progress_frame = ttk.Frame(url_card)
        progress_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress label
        self.progress_var = tk.StringVar(value="Ready to scrape")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var,
                                  font=('Segoe UI', 9))
        progress_label.grid(row=0, column=0, sticky="w")
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate',
                                           style='TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 0))
    
    def setup_console_section(self, parent):
        """Setup console output section with modern design"""
        # Console card
        console_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        console_card.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        console_card.columnconfigure(0, weight=1)
        console_card.rowconfigure(1, weight=1)
        
        # Console header
        console_header = ttk.Frame(console_card)
        console_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        console_header.columnconfigure(0, weight=1)
        
        console_title = ttk.Label(console_header, text="📟 Console Output",
                                 font=('Segoe UI', 12, 'bold'))
        console_title.grid(row=0, column=0, sticky="w")
        
        # Console text area with modern styling
        self.console_text = scrolledtext.ScrolledText(
            console_card, 
            height=18, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            selectbackground='#264f78',
            relief='flat',
            borderwidth=0
        )
        self.console_text.grid(row=1, column=0, sticky="nsew")
    
    def setup_controls_section(self, parent):
        """Setup control buttons section"""
        # Controls card
        controls_card = ttk.Frame(parent, style='Card.TFrame', padding="15")
        controls_card.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(controls_card)
        button_frame.pack(fill=tk.X)
        
        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        # Clear console button
        clear_button = ttk.Button(left_buttons, text="🗑️ Clear Console", 
                                 command=self.clear_console,
                                 style="Modern.TButton")
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(left_buttons, text="⏹️ Stop", 
                                     command=self.stop_scraping, 
                                     state=tk.DISABLED,
                                     style="Danger.TButton")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        # Open JSON folder button
        json_button = ttk.Button(right_buttons, text="📁 Open JSON Folder", 
                               command=self.open_json_folder,
                               style="Success.TButton")
        json_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Open CSV button (updated name)
        csv_button = ttk.Button(right_buttons, text="📊 Open Dataset.csv", 
                               command=self.open_csv,
                               style="Success.TButton")
        csv_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def setup_status_bar(self, parent):
        """Setup status bar at the bottom"""
        # Status frame
        status_frame = ttk.Frame(parent, style='Card.TFrame', padding="10")
        status_frame.grid(row=4, column=0, sticky="ew")
        status_frame.columnconfigure(1, weight=1)
        
        # Status icon
        status_icon = ttk.Label(status_frame, text="💡", font=('Segoe UI', 12))
        status_icon.grid(row=0, column=0, padx=(0, 10))
        
        # Status text
        self.status_var = tk.StringVar(value="Ready to scrape Ground.news articles")
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                font=('Segoe UI', 9))
        status_label.grid(row=0, column=1, sticky="w")
        
        # Bind Enter key to fetch button
        self.url_entry.bind('<Return>', lambda event: self.start_scraping())
        
        # Set focus to URL entry
        self.url_entry.focus_set()
    
    def log_message(self, message):
        """Add message to console with timestamp and color coding"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console_text.config(state=tk.NORMAL)
        
        # Configure tags for different message types
        self.console_text.tag_configure("success", foreground="#4ade80")
        self.console_text.tag_configure("error", foreground="#ef4444")
        self.console_text.tag_configure("warning", foreground="#f59e0b")
        self.console_text.tag_configure("info", foreground="#3b82f6")
        self.console_text.tag_configure("normal", foreground="#d4d4d4")
        
        # Determine message type and apply appropriate tag
        tag = "normal"
        if "✅" in message or "successfully" in message.lower():
            tag = "success"
        elif "❌" in message or "error" in message.lower() or "failed" in message.lower():
            tag = "error"
        elif "⚠️" in message or "warning" in message.lower():
            tag = "warning"
        elif "🚀" in message or "starting" in message.lower() or "running" in message.lower():
            tag = "info"
        
        self.console_text.insert(tk.END, formatted_message, tag)
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
        """Enhanced URL validation with better error messages"""
        if not url.strip():
            return False, "📝 Please enter a Ground.news article URL"
        
        if not url.startswith(('http://', 'https://')):
            return False, "🔗 URL must start with http:// or https://"
        
        if 'ground.news' not in url.lower():
            return False, "🌍 URL must be from ground.news (e.g., https://ground.news/article/...)"
        
        if '/article/' not in url.lower():
            return False, "📰 Please provide a direct link to a Ground.news article"
        
        return True, ""
    
    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.is_running:
            messagebox.showwarning("⚠️ Already Running", "Scraping is already in progress!\nPlease wait for the current operation to complete.")
            return
        
        url = self.url_var.get().strip()
        
        # Validate URL
        is_valid, error_msg = self.validate_url(url)
        if not is_valid:
            messagebox.showerror("❌ Invalid URL", error_msg)
            return
        
        # Start scraping in a separate thread
        self.is_running = True
        self.fetch_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.progress_var.set("🚀 Initializing scraper...")
        self.status_var.set("🔄 Scraping in progress...")
        
        # Clear console and add header
        self.clear_console()
        self.log_message("🌍 Ground News Scraper Started")
        self.log_message("=" * 50)
        self.log_message(f"🎯 Target URL: {url}")
        self.log_message("🔧 Initializing Chrome WebDriver...")
        
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
            self.status_var.set("🎉 Data saved successfully - Ready for next scrape")
            # Clear URL for next scraping
            self.url_var.set("")
            self.url_entry.focus_set()
        else:
            self.progress_var.set("❌ Scraping failed!")
            self.status_var.set("⚠️ Fix errors and try again")
    
    def open_json_folder(self):
        """Open the JSON folder containing scraped data"""
        json_path = os.path.join(os.path.dirname(__file__), 'json')
        
        # Create json folder if it doesn't exist
        if not os.path.exists(json_path):
            os.makedirs(json_path, exist_ok=True)
        
        try:
            # Try to open with default application
            if sys.platform == "win32":
                os.startfile(json_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.call(["open", json_path])
            else:  # Linux
                subprocess.call(["xdg-open", json_path])
                
            self.log_message("📁 Opened JSON folder")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open JSON folder: {str(e)}")
    
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
    
    # Configure modern style
    style = ttk.Style()
    
    # Try to use the best available theme
    available_themes = style.theme_names()
    if 'vista' in available_themes:
        style.theme_use('vista')
    elif 'clam' in available_themes:
        style.theme_use('clam')
    else:
        style.theme_use('default')
    
    # Configure enhanced button styles
    style.configure('Accent.TButton', 
                   background='#0078d4', 
                   foreground='white',
                   borderwidth=0,
                   focuscolor='none')
    style.map('Accent.TButton',
              background=[('active', '#106ebe'),
                         ('pressed', '#005a9e')])
    
    style.configure('Success.TButton',
                   background='#16a085',
                   foreground='white',
                   borderwidth=0,
                   focuscolor='none')
    style.map('Success.TButton',
              background=[('active', '#148f7f'),
                         ('pressed', '#0f6b5b')])
    
    style.configure('Danger.TButton',
                   background='#e74c3c',
                   foreground='white',
                   borderwidth=0,
                   focuscolor='none')
    style.map('Danger.TButton',
              background=[('active', '#c0392b'),
                         ('pressed', '#a93226')])
    
    style.configure('Modern.TButton',
                   background='#34495e',
                   foreground='white',
                   borderwidth=0,
                   focuscolor='none')
    style.map('Modern.TButton',
              background=[('active', '#2c3e50'),
                         ('pressed', '#1a252f')])
    
    # Configure progressbar
    style.configure('TProgressbar',
                   background='#0078d4',
                   troughcolor='#e1e5e9',
                   borderwidth=0,
                   lightcolor='#0078d4',
                   darkcolor='#0078d4')
    
    app = GroundNewsScraperGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Set application icon (if available)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()
