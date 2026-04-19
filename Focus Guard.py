import time
import threading
import pygetwindow as gw
from plyer import notification
from anthropic import Anthropic
from tkinter import *
from tkinter import messagebox

# --- CONFIGURATION ---
# IMPORTANT: Replace with your actual key. Do not share it!
API_KEY = "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"

# Keywords to look for in window titles
FORBIDDEN = [
    "facebook", "instagram", "twitter", "x.com", "tiktok", "youtube", 
    "reddit", "netflix", "hulu", "twitch", "poki", "coolmathgames"
]

class FocusGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Guard v1.0")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")
        
        self.guard_active = False

        # UI Elements
        self.status_label = Label(
            root, text="Focus Guard is OFF", 
            fg="white", bg="#e74c3c", font=("Helvetica", 14, "bold")
        )
        self.status_label.pack(pady=30, fill=X)

        self.btn_toggle = Button(
            root, text="Enable Focus Guard", 
            command=self.toggle_guard,
            width=20, height=2, bg="#ecf0f1"
        )
        self.btn_toggle.pack(pady=20)

        self.info_label = Label(
            root, text="Watching for: Social Media & Games", 
            fg="#bdc3c7", bg="#2c3e50"
        )
        self.info_label.pack(side=BOTTOM, pady=10)

    def toggle_guard(self):
        if not self.guard_active:
            self.guard_active = True
            self.status_label.config(text="Focus Guard is WATCHING", bg="#27ae60")
            self.btn_toggle.config(text="Disable Focus Guard")
            # Start monitoring in a separate thread so the window stays responsive
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.guard_active = False
            self.status_label.config(text="Focus Guard is OFF", bg="#e74c3c")
            self.btn_toggle.config(text="Enable Focus Guard")

    def get_ai_roast(self):
        """Calls Anthropic API to get a custom roast."""
        try:
            client = Anthropic(api_key=API_KEY)
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=150,
                messages=[{
                    "role": "user", 
                    "content": "The user is procrastinating on social media. Give them a short, brutal, witty roast (under 30 words) to make them feel guilty and go back to work."
                }]
            )
            return response.content[0].text
        except Exception as e:
            print(f"API Error: {e}")
            return "Get off your phone and back to work, you lazy human!"

    def monitor_loop(self):
        """Background loop that checks for forbidden windows."""
        while self.guard_active:
            try:
                active_window = gw.getActiveWindow()
                if active_window and active_window.title:
                    window_title = active_window.title.lower()
                    
                    # Check if any forbidden keyword is in the current title
                    if any(site in window_title for site in FORBIDDEN):
                        roast = self.get_ai_roast()
                        notification.notify(
                            title="🚨 FOCUS GUARD ALERT",
                            message=roast,
                            timeout=10
                        )
                        # Wait a bit longer after a catch so we don't spam notifications
                        time.sleep(30)
                
                time.sleep(3) # Check every 3 seconds
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    root = Tk()
    app = FocusGuardApp(root)
    root.mainloop()