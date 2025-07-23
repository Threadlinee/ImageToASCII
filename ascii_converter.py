import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os

class IlphuStyleAsciiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Image to ASCII Art Converter")
        self.root.geometry("1100x800")
        self.root.configure(bg='black')
        self.reset_mode = False

        self.ascii_ramp = " .:-=+*#%@" 
        self.setup_ui()
        self.root.bind("<Control-c>", self.reset_or_exit)

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


        tk.Label(
            self.main_frame,
            text="ASCII ART CONVERTER (Ilphu Style)",
            font=("Arial", 24, "bold"),
            fg="#00FF00",
            bg="black"
        ).pack(pady=(0, 20))

        self.upload_btn = tk.Button(
            self.main_frame,
            text="⬆️ UPLOAD IMAGE ⬆️",
            command=self.upload_image,
            font=("Arial", 18, "bold"),
            bg="#333",
            fg="white",
            activebackground="#555",
            activeforeground="white",
            padx=30,
            pady=15,
            bd=0
        )
        self.upload_btn.pack(pady=20)

        self.ascii_display = tk.Text(
            self.main_frame,
            wrap=tk.NONE,
            font=("Courier New", 6),
            bg="black",
            fg="white",
            state="disabled",
            bd=0
        )
        self.ascii_display.pack(fill=tk.BOTH, expand=True)

        self.status = tk.Label(
            self.root,
            text="Ready to convert images like Ilphu’s tool...",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#222",
            fg="white"
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_image(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.ico *.gif *.webp"), ("All Files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        if not file_path:
            return

        try:
            with Image.open(file_path) as img:
                ascii_result = self.convert_to_ascii(img)
                self.display_ascii(ascii_result, os.path.basename(file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image:\n{e}")

    def convert_to_ascii(self, img):
        """Convert image to ASCII using brightness ramp, Ilphu style"""
        img = img.convert("L")

        char_width = int(self.ascii_display.winfo_width() / 6)
        char_height = int(self.ascii_display.winfo_height() / 12)

        width, height = img.size
        aspect_ratio = height / width
        new_width = char_width
        new_height = int(aspect_ratio * new_width * 0.5)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        pixels = np.array(img)

        ascii_image = ""
        ramp_len = len(self.ascii_ramp) - 1

        for row in pixels:
            line = "".join(self.ascii_ramp[int(pixel / 255 * ramp_len)] for pixel in row)
            ascii_image += line + "\n"

        return ascii_image

    def display_ascii(self, ascii_art, filename):
        self.upload_btn.pack_forget()
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.pack_forget()

        self.ascii_display.config(state="normal")
        self.ascii_display.delete(1.0, tk.END)
        self.ascii_display.insert(tk.END, ascii_art)
        self.ascii_display.config(state="disabled")

        self.status.config(text=f"🖼️ Converted: {filename} | Press Ctrl+C to reset or exit")

    def reset_or_exit(self, event=None):
        if not self.reset_mode:
            self.reset_ui()
            self.reset_mode = True
            self.status.config(text="Ready for another image...")
        else:
            self.root.destroy()

    def reset_ui(self):
        self.ascii_display.pack_forget()
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
        self.setup_ui()
        self.reset_mode = False

if __name__ == "__main__":
    root = tk.Tk()
    app = IlphuStyleAsciiGUI(root)
    root.mainloop()
