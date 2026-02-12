import tkinter as tk
from tkinter import ttk
import math
import random

class DSPVisualizer:
    def __init__(self):
        # Signal parameters
        self.fs = 1000
        self.duration = 0.2  # Show 0.2 seconds
        self.num_samples = 200
        self.t = [i / self.fs for i in range(self.num_samples)]
        
        # Signal parameters
        self.freq = 5
        self.signal_type = 'sine'
        self.noise_level = 0.1
        
        # Filter parameters
        self.filter_type = 'moving_average'
        self.window_size = 20
        self.cutoff_freq = 30
        
        # Setup the GUI
        self.setup_gui()
    
    def generate_signal(self):
        """Generate signal samples"""
        signal = []
        for time in self.t:
            # Generate base signal
            if self.signal_type == 'sine':
                value = math.sin(2 * math.pi * self.freq * time)
            elif self.signal_type == 'square':
                value = 1.0 if math.sin(2 * math.pi * self.freq * time) >= 0 else -1.0
            elif self.signal_type == 'noise':
                value = 0
            elif self.signal_type == 'sine_noise':
                value = math.sin(2 * math.pi * self.freq * time)
            
            # Add noise
            if self.signal_type == 'noise' or self.signal_type == 'sine_noise':
                noise = random.gauss(0, self.noise_level)
                value += noise
            
            signal.append(value)
        return signal
    
    def moving_average_filter(self, signal):
        """Apply moving average filter"""
        filtered = []
        for i in range(len(signal)):
            # Average samples in window
            start_idx = max(0, i - self.window_size // 2)
            end_idx = min(len(signal), i + self.window_size // 2)
            window = signal[start_idx:end_idx]
            filtered.append(sum(window) / len(window))
        return filtered
    
    def low_pass_filter(self, signal):
        """Simple low-pass filter"""
        RC = 1/(2 * math.pi * self.cutoff_freq)
        dt = 1/self.fs
        alpha = dt/(RC + dt)
        
        filtered = [signal[0]]
        for i in range(1, len(signal)):
            filtered.append(filtered[i-1] + alpha*(signal[i] - filtered[i-1]))
        return filtered
    
    def apply_filter(self, signal):
        """Apply selected filter"""
        if self.filter_type == 'moving_average':
            return self.moving_average_filter(signal)
        elif self.filter_type == 'low_pass':
            return self.low_pass_filter(signal)
        return signal
    
    def setup_gui(self):
        """Setup the tkinter GUI"""
        self.root = tk.Tk()
        self.root.title("DSP Signal & Filter Visualizer")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Create main frames
        self.control_frame = tk.Frame(self.root, bg='#363636', width=250)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)
        
        self.plot_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create canvas for plotting
        self.canvas = tk.Canvas(self.plot_frame, bg='white', width=900, height=650)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add controls
        self.add_controls()
        
        # Initial plot
        self.update_plot()
        
        self.root.mainloop()
    
    def add_controls(self):
        """Add control widgets"""
        # Title
        title = tk.Label(self.control_frame, text="DSP CONTROLS", 
                        bg='#363636', fg='white', font=('Arial', 14, 'bold'))
        title.pack(pady=15)
        
        # Signal Type
        sig_label = tk.Label(self.control_frame, text="SIGNAL TYPE:", 
                            bg='#363636', fg='#88ccff', font=('Arial', 11, 'bold'))
        sig_label.pack(pady=(15,5))
        
        self.signal_var = tk.StringVar(value="sine")
        signals = [("Sine Wave", "sine"), 
                  ("Square Wave", "square"),
                  ("Noise", "noise"), 
                  ("Sine + Noise", "sine_noise")]
        
        for text, value in signals:
            rb = tk.Radiobutton(self.control_frame, text=text, value=value,
                              variable=self.signal_var, bg='#363636', fg='white',
                              selectcolor='#363636', command=self.on_signal_change)
            rb.pack(anchor=tk.W, padx=20)
        
        # Filter Type
        filt_label = tk.Label(self.control_frame, text="FILTER TYPE:", 
                             bg='#363636', fg='#ff8888', font=('Arial', 11, 'bold'))
        filt_label.pack(pady=(20,5))
        
        self.filter_var = tk.StringVar(value="moving_average")
        filters = [("Moving Average", "moving_average"),
                  ("Low-Pass (RC)", "low_pass")]
        
        for text, value in filters:
            rb = tk.Radiobutton(self.control_frame, text=text, value=value,
                              variable=self.filter_var, bg='#363636', fg='white',
                              selectcolor='#363636', command=self.on_filter_change)
            rb.pack(anchor=tk.W, padx=20)
        
        # Frequency Slider
        freq_label = tk.Label(self.control_frame, text="FREQUENCY (Hz):", 
                             bg='#363636', fg='white', font=('Arial', 10))
        freq_label.pack(pady=(20,5))
        
        self.freq_slider = tk.Scale(self.control_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                   length=200, bg='#363636', fg='white', 
                                   troughcolor='#555555', command=self.on_freq_change)
        self.freq_slider.set(self.freq)
        self.freq_slider.pack()
        
        # Window Size Slider
        window_label = tk.Label(self.control_frame, text="WINDOW SIZE:", 
                               bg='#363636', fg='white', font=('Arial', 10))
        window_label.pack(pady=(15,5))
        
        self.window_slider = tk.Scale(self.control_frame, from_=3, to=51, orient=tk.HORIZONTAL,
                                     length=200, bg='#363636', fg='white',
                                     troughcolor='#555555', command=self.on_window_change)
        self.window_slider.set(self.window_size)
        self.window_slider.pack()
        
        # Cutoff Frequency Slider
        cutoff_label = tk.Label(self.control_frame, text="CUTOFF FREQ (Hz):", 
                               bg='#363636', fg='white', font=('Arial', 10))
        cutoff_label.pack(pady=(15,5))
        
        self.cutoff_slider = tk.Scale(self.control_frame, from_=5, to=100, orient=tk.HORIZONTAL,
                                      length=200, bg='#363636', fg='white',
                                      troughcolor='#555555', command=self.on_cutoff_change)
        self.cutoff_slider.set(self.cutoff_freq)
        self.cutoff_slider.pack()
        
        # Noise Level Slider
        noise_label = tk.Label(self.control_frame, text="NOISE LEVEL:", 
                              bg='#363636', fg='white', font=('Arial', 10))
        noise_label.pack(pady=(15,5))
        
        self.noise_slider = tk.Scale(self.control_frame, from_=0, to=0.5, 
                                    orient=tk.HORIZONTAL, resolution=0.05,
                                    length=200, bg='#363636', fg='white',
                                    troughcolor='#555555', command=self.on_noise_change)
        self.noise_slider.set(self.noise_level)
        self.noise_slider.pack()
        
        # Reset Button
        reset_btn = tk.Button(self.control_frame, text="RESET ALL", 
                            bg='#ffaa00', fg='black', font=('Arial', 11, 'bold'),
                            command=self.reset)
        reset_btn.pack(pady=25)
        
        # Info Label
        self.info_label = tk.Label(self.control_frame, text="", 
                                  bg='#363636', fg='#aaffaa', 
                                  font=('Arial', 10), justify=tk.LEFT)
        self.info_label.pack(pady=20, padx=10)
    
    def on_signal_change(self):
        self.signal_type = self.signal_var.get()
        self.update_plot()
    
    def on_filter_change(self):
        self.filter_type = self.filter_var.get()
        self.update_plot()
    
    def on_freq_change(self, val):
        self.freq = int(float(val))
        self.update_plot()
    
    def on_window_change(self, val):
        self.window_size = int(float(val))
        self.update_plot()
    
    def on_cutoff_change(self, val):
        self.cutoff_freq = int(float(val))
        self.update_plot()
    
    def on_noise_change(self, val):
        self.noise_level = float(val)
        self.update_plot()
    
    def reset(self):
        self.freq = 5
        self.window_size = 20
        self.cutoff_freq = 30
        self.noise_level = 0.1
        self.signal_type = 'sine'
        self.filter_type = 'moving_average'
        
        self.signal_var.set('sine')
        self.filter_var.set('moving_average')
        self.freq_slider.set(5)
        self.window_slider.set(20)
        self.cutoff_slider.set(30)
        self.noise_slider.set(0.1)
        
        self.update_plot()
    
    def draw_plot(self, signal, filtered):
        """Draw signals on canvas"""
        self.canvas.delete("all")
        
        # Canvas dimensions
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 100:  # Canvas not ready yet
            w = 900
            h = 650
        
        # Plot parameters
        margin = 60
        plot_width = w - 2*margin
        plot_height = (h - 4*margin) // 2
        
        # Draw title
        self.canvas.create_text(w//2, 20, text="DSP SIGNAL & FILTER VISUALIZER", 
                               font=('Arial', 16, 'bold'), fill='#2b2b2b')
        
        # Original Signal Plot
        y_center = margin + plot_height//2
        self.canvas.create_text(margin//2, y_center-30, text="Original Signal", 
                               font=('Arial', 11, 'bold'), fill='blue', anchor=tk.W)
        self.draw_axis(margin, y_center, plot_width, plot_height, "Time (s)", "Amplitude")
        self.draw_signal(margin, y_center, plot_width, plot_height, signal, 'blue')
        
        # Filtered Signal Plot
        y_center = margin*2 + plot_height + plot_height//2
        self.canvas.create_text(margin//2, y_center-30, text="Filtered Signal", 
                               font=('Arial', 11, 'bold'), fill='red', anchor=tk.W)
        self.draw_axis(margin, y_center, plot_width, plot_height, "Time (s)", "Amplitude")
        self.draw_signal(margin, y_center, plot_width, plot_height, filtered, 'red')
        
        # Update info label
        self.update_info()
    
    def draw_axis(self, x0, y0, width, height, xlabel, ylabel):
        """Draw axis with labels"""
        # Draw axis lines
        self.canvas.create_line(x0, y0, x0 + width, y0, fill='black', width=1)  # x-axis
        self.canvas.create_line(x0, y0 - height//2, x0, y0 + height//2, fill='black', width=1)  # y-axis
        
        # Labels
        self.canvas.create_text(x0 + width//2, y0 + 25, text=xlabel, font=('Arial', 9))
        self.canvas.create_text(x0 - 25, y0, text=ylabel, font=('Arial', 9), angle=90)
        
        # Ticks
        for i in range(5):
            x = x0 + (i * width//4)
            self.canvas.create_line(x, y0-5, x, y0+5, fill='black')
            time_val = i * 0.05  # 0, 0.05, 0.1, 0.15, 0.2 seconds
            self.canvas.create_text(x, y0+15, text=f'{time_val:.2f}', font=('Arial', 8))
    
    def draw_signal(self, x0, y0, width, height, signal, color):
        """Draw the signal line"""
        if len(signal) < 2:
            return
        
        # Scale signal to fit in plot
        max_amp = max(abs(min(signal)), abs(max(signal)), 0.1)
        points = []
        
        for i, val in enumerate(signal):
            x = x0 + (i / len(signal)) * width
            y = y0 - (val / max_amp) * (height//2) * 0.8
            points.extend([x, y])
        
        # Draw the line
        self.canvas.create_line(points, fill=color, width=1.5, smooth=True)
    
    def update_info(self):
        """Update information label"""
        info = f"Signal: {self.signal_type}\n"
        info += f"Filter: {self.filter_type}\n"
        info += f"Freq: {self.freq} Hz\n"
        
        if self.filter_type == 'moving_average':
            info += f"Window: {self.window_size}\n"
            cutoff = self.fs / self.window_size
            info += f"Cutoff: ~{cutoff:.1f} Hz"
        else:
            info += f"Cutoff: {self.cutoff_freq} Hz"
        
        info += f"\nNoise: {self.noise_level}"
        
        self.info_label.config(text=info)
    
    def update_plot(self):
        """Update the entire visualization"""
        signal = self.generate_signal()
        filtered = self.apply_filter(signal)
        self.draw_plot(signal, filtered)


if __name__ == "__main__":
    print("=" * 50)
    print("DSP SIGNAL & FILTER VISUALIZER")
    print("=" * 50)
    print("\n NO ADDITIONAL PACKAGES NEEDED!")
    print("   This version uses only Python's built-in modules:")
    print("   • tkinter - GUI")
    print("   • math - calculations")
    print("   • random - noise generation")
    print("\n Starting visualizer...")
    print("   Close the window to exit.")
    print("=" * 50)
    
    # Run the visualizer
    app = DSPVisualizer()