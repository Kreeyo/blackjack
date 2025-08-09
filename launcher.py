import tkinter as tk
from tkinter import ttk, messagebox
import requests

class LicenseWindow(tk.Toplevel):
    def __init__(self, master, on_success, backend_url):
        super().__init__(master)
        self.title("Enter License Key")
        self.geometry("450x150")
        self.resizable(False, False)
        self.on_success = on_success
        self.backend_url = backend_url

        ttk.Label(self, text="Please enter your license key:").pack(pady=10)
        self.key_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.key_var, width=60)
        self.entry.pack(pady=5)
        self.entry.focus()

        self.submit_btn = ttk.Button(self, text="Validate", command=self.validate_key)
        self.submit_btn.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.master.destroy)  # Exit app if closed here

    def validate_key(self):
        key = self.key_var.get().strip()
        try:
            response = requests.post(self.backend_url + "/validate", json={"license_key": key})
            data = response.json()
            if response.status_code == 200 and data.get("valid"):
                self.destroy()
                self.on_success()
            else:
                messagebox.showerror("License Error", f"License validation failed:\n{data.get('reason', 'Unknown error')}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to license server:\n{e}")

def main():
    backend_url = "https://blackjack-backend-g87y.onrender.com"  # your deployed backend URL

    root = tk.Tk()
    root.withdraw()  # hide main window initially

    def on_license_success():
        root.deiconify()
        import blackjack_advisor
        app = blackjack_advisor.BlackjackAdvisorApp()
        app.mainloop()

    LicenseWindow(root, on_license_success, backend_url)
    root.mainloop()

if __name__ == "__main__":
    main()
