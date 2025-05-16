import tkinter as tk
import random

# Sample texts for the typing test
tests = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes perfect. Consistency is key to improving your typing speed.",
    "Python is a versatile language used for many applications, including web development and data analysis.",
    "Typing speed tests help you measure how fast you can type words per minute.",
]

class TypingSpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Typing Speed Test")
        master.geometry("800x400")

        # Variables
        self.sample_text = tk.StringVar()
        self.timer_text = tk.StringVar(value="Time: 0s")
        self.result_text = tk.StringVar()
        self.error_text = tk.StringVar()

        # Widgets
        tk.Label(master, textvariable=self.sample_text, wraplength=780, font=("Helvetica", 14)).pack(pady=20)
        self.entry = tk.Text(master, height=5, width=85, state='disabled', font=("Helvetica", 12))
        self.entry.pack()
        # Error label (hidden initially)
        self.error_label = tk.Label(master, textvariable=self.error_text, font=("Helvetica", 12), fg='red', justify='center')
        self.error_label.pack(pady=(5,0))

        tk.Label(master, textvariable=self.timer_text, font=("Helvetica", 12)).pack(pady=5)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="Start Test", command=self.start_test, font=("Helvetica", 12))
        self.start_button.pack(side='left', padx=10)
        self.stop_button = tk.Button(button_frame, text="Stop Test", command=self.end_test, font=("Helvetica", 12), state='disabled')
        self.stop_button.pack(side='left', padx=10)
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_test, font=("Helvetica", 12))
        self.reset_button.pack(side='left', padx=10)

        # Result label, centered
        self.result_label = tk.Label(master, textvariable=self.result_text, font=("Helvetica", 16), fg='blue', justify='center')
        self.result_label.pack(pady=20)

        # Internal state
        self.running = False
        self.elapsed_time = 0

        self.reset_test()

    def start_test(self):
        # Choose a random sample text
        sample = random.choice(tests)
        self.sample_text.set(sample)

        # Prepare entry widget
        self.entry.config(state='normal')
        self.entry.delete('1.0', tk.END)
        self.entry.focus()

        # Clear messages
        self.timer_text.set("Time: 0s")
        self.result_text.set("")
        self.error_text.set("")

        # Initialize timer
        self.elapsed_time = 0
        self.running = True

        # Update buttons
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.reset_button.config(state='disabled')

        # Start timer loop
        self.update_timer()

    def update_timer(self):
        if self.running:
            self.elapsed_time += 1
            self.timer_text.set(f"Time: {self.elapsed_time}s")
            self.master.after(1000, self.update_timer)

    def end_test(self):
        if not self.running:
            return
        # Stop timer
        self.running = False

        # Disable entry
        self.entry.config(state='disabled')

        # Update buttons
        self.stop_button.config(state='disabled')
        self.start_button.config(state='normal')
        self.reset_button.config(state='normal')

        # Retrieve texts
        typed = self.entry.get('1.0', tk.END).strip()
        sample = self.sample_text.get().strip()

        # Validate accuracy
        if typed != sample:
            self.error_text.set("Entered text does not match the sample text.")
            self.result_text.set("")
            return
        else:
            self.error_text.set("")

        # Calculate words per minute
        word_count = len(typed.split())
        wpm = (word_count * 60 / self.elapsed_time) if self.elapsed_time > 0 else 0
        self.result_text.set(f"Your typing speed: {wpm:.2f} WPM\nTime used: {self.elapsed_time}s")

    def reset_test(self):
        # Reset state
        self.running = False
        self.elapsed_time = 0

        # Reset labels and entry
        self.sample_text.set("Click 'Start Test' to begin the typing speed test.")
        self.timer_text.set("Time: 0s")
        self.result_text.set("")
        self.error_text.set("")
        self.entry.config(state='normal')
        self.entry.delete('1.0', tk.END)
        self.entry.config(state='disabled')

        # Reset buttons
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.reset_button.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
