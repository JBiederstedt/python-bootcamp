import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Watermarker")

        # Preview area for main image
        self.img_label = tk.Label(self.root)
        self.img_label.pack(padx=10, pady=10)

        # Open image button
        tk.Button(self.root, text="Open Image", command=self.open_image).pack(pady=5)

        # Text watermark section
        txt_frame = tk.Frame(self.root)
        tk.Label(txt_frame, text="Text watermark:").pack(side=tk.LEFT)
        self.text_entry = tk.Entry(txt_frame, width=30)
        self.text_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(txt_frame, text="Use Text", command=self.add_text_watermark).pack(side=tk.LEFT)
        txt_frame.pack(pady=5)

        # Separator
        tk.Label(self.root, text="--- OR ---").pack(pady=5)

        # Logo watermark section with preview
        logo_frame = tk.Frame(self.root)
        btn_frame = tk.Frame(logo_frame)
        tk.Button(btn_frame, text="Load Logo", command=self.open_logo).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Use Logo", command=self.add_logo_watermark).pack(side=tk.LEFT, padx=5)
        btn_frame.pack(side=tk.LEFT)
        self.logo_label = tk.Label(logo_frame)  # preview logo thumbnail
        self.logo_label.pack(side=tk.LEFT, padx=10)
        logo_frame.pack(pady=5)

        # Save button
        tk.Button(self.root, text="Save As...", command=self.save_image).pack(pady=10)

        # Internal state
        self.image = None
        self.preview = None
        self.logo = None
        self.logo_thumb = None
        self.watermarked = None

        self.root.mainloop()

    def open_image(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Select an image to watermark",
            filetypes=[("Image Files", ("*.png","*.jpg","*.jpeg","*.bmp")), ("All Files","*.*")]
        )
        if not path:
            return
        try:
            img = Image.open(path).convert("RGBA")
        except Exception as e:
            messagebox.showerror("Error Opening Image", f"Could not open image:\n{e}")
            return
        self.image = img
        self.show_preview(self.image)

    def open_logo(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Select a logo for watermark",
            filetypes=[("Image Files", ("*.png","*.jpg","*.jpeg","*.bmp")), ("All Files","*.*")]
        )
        if not path:
            return
        try:
            logo = Image.open(path).convert("RGBA")
        except Exception as e:
            messagebox.showerror("Error Opening Logo", f"Could not open logo:\n{e}")
            return
        if self.image:
            w = int(self.image.width * 0.2)
            logo = logo.resize((w, int(logo.height * w / logo.width)), Image.Resampling.LANCZOS)
        self.logo = logo
        # Show logo thumbnail
        thumb = logo.copy().convert("RGB")
        thumb.thumbnail((80,80))
        self.logo_thumb = ImageTk.PhotoImage(thumb)
        self.logo_label.config(image=self.logo_thumb)

    def add_text_watermark(self):
        if not self.image:
            messagebox.showwarning("No image", "Please open an image first")
            return
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showwarning("No text", "Please enter watermark text")
            return
        base = self.image.copy()
        # Text watermark
        font_size = max(12, int(base.width / 20))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        txt_layer = Image.new("RGBA", base.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt_layer)
        bbox = draw.textbbox((0,0), text, font=font)
        w,h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        pos = (base.width - w - 10, base.height - h - 10)
        draw.text(pos, text, font=font, fill=(255,255,255,128))
        self.watermarked = Image.alpha_composite(base, txt_layer)
        self.show_preview(self.watermarked)

    def add_logo_watermark(self):
        if not self.image:
            messagebox.showwarning("No image", "Please open an image first")
            return
        if not self.logo:
            messagebox.showwarning("No logo", "Please load a logo first")
            return
        base = self.image.copy()
        mark = self.logo
        layer = Image.new("RGBA", base.size, (0,0,0,0))
        pos = (base.width - mark.width - 10, base.height - mark.height - 10)
        layer.paste(mark, pos, mark)
        self.watermarked = Image.alpha_composite(base, layer)
        self.show_preview(self.watermarked)

    def show_preview(self, img):
        disp = img.copy().convert("RGB")
        disp.thumbnail((500,500))
        self.preview = ImageTk.PhotoImage(disp)
        self.img_label.config(image=self.preview)

    def save_image(self):
        if not self.watermarked:
            messagebox.showwarning("Nothing to save", "Add a watermark first")
            return
        path = filedialog.asksaveasfilename(
            parent=self.root,
            defaultextension=".png",
            filetypes=[("PNG","*.png"),("JPEG",("*.jpg","*.jpeg"))]
        )
        if not path:
            return
        out = self.watermarked.convert("RGB") if path.lower().endswith((".jpg",".jpeg")) else self.watermarked
        try:
            out.save(path)
            messagebox.showinfo("Saved","Watermarked image saved")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save image:\n{e}")

if __name__ == "__main__":
    WatermarkApp()
