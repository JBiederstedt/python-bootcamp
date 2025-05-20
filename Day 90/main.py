import tkinter as tk

class DisappearingTextApp(tk.Tk):
    def __init__(self, timeout=5):
        super().__init__()
        self.title("Disappearing Text Writing App")
        self.geometry("600x400")
        self.timeout = timeout
        self.remaining = self.timeout

        # Label to display countdown
        self.label = tk.Label(self, text=f"Time remaining: {self.remaining}s", font=("Arial", 12))
        self.label.pack(pady=5)

        # Text widget for writing
        self.text = tk.Text(self, wrap=tk.WORD, font=("Arial", 14))
        self.text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Reset timer on any key press
        self.text.bind("<Key>", self.on_keypress)

        # Start the countdown loop
        self.countdown()

    def on_keypress(self, event=None):
        """
        Called on every key press: reset the countdown.
        """
        self.remaining = self.timeout
        self.update_label()

    def update_label(self):
        """
        Update the countdown display label.
        """
        self.label.config(text=f"Time remaining: {self.remaining}s")

    def countdown(self):
        """
        Decrease the remaining time every second; clear text when time runs out.
        """
        if self.remaining <= 0:
            self.clear_text()
            self.remaining = self.timeout
        else:
            self.remaining -= 1

        self.update_label()

        # Schedule next countdown tick
        self.after(1000, self.countdown)

    def clear_text(self):
        """
        Delete all content from the text widget.
        """
        self.text.delete("1.0", tk.END)

if __name__ == "__main__":
    # Initialize app with a 5-second timeout
    app = DisappearingTextApp(timeout=5)
    app.mainloop()
