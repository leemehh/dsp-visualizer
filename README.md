# DSP Signal & Filter Visualiser

![Project maintenance status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-educational-blue)

A simple **Digital Signal Processing (DSP) visualiser** built entirely with Python’s built-in libraries.
The application allows users to generate different signal types, apply basic filters, and view both the original and filtered signals in real time through an interactive graphical interface.

This project is designed primarily for **learning and demonstration purposes**, helping students and beginners understand how sampling, noise, and filtering behave in the time domain without needing external scientific libraries.

---

## Description

The DSP Signal & Filter Visualizer provides an interactive environment for experimenting with signal generation and filtering concepts commonly taught in introductory **Digital Signal Processing** courses.

Key features include:

* **Multiple signal types** – Generate sine waves, square waves, pure noise, or sine waves combined with noise.
* **Basic DSP filters** – Apply a moving average smoothing filter or a simple RC low-pass filter.
* **Real-time visualization** – Instantly view both the original and filtered signals on a graphical canvas.
* **Interactive controls** – Adjust signal frequency, noise level, filter window size, and cutoff frequency using sliders and radio buttons.
* **No external dependencies** – Uses only Python standard libraries (`tkinter`, `math`, and `random`).

This makes the project lightweight, portable, and ideal for **educational demonstrations, coursework, or beginner DSP exploration**.

---

## Getting Started

### Dependencies

Before running the program, ensure you have:

* **Python 3.7 or newer**
* A Python installation that includes **tkinter** (usually bundled with standard Python distributions)

No additional packages or installations are required.

---

### Installation

Follow these steps to run the visualizer locally:

```bash
# Clone the repository
git clone https://github.com/your-username/dsp-visualizer.git

# Navigate into the project folder
cd dsp-visualizer

# Run the application
python dsp_visualizer.py
```

After running the command, the **DSP visualizer window** will open.
Simply close the window to exit the program.

---

## Educational Value

This project helps demonstrate:

* Signal sampling in the time domain
* Effects of random noise on signals
* Noise reduction using smoothing and low-pass filtering
* Interactive visualisation of DSP concepts

It is especially useful for **engineering students, DSP beginners, and classroom demonstrations**.

---

## Future Improvements

Potential extensions for this project include:

* Frequency-domain visualisation using FFT
* Additional digital filters (FIR, Butterworth, etc.)
* Signal export to CSV or WAV files
* Animation controls such as pause/play

---

## License

This project is provided for **educational and personal use**.
You are free to modify and extend it for learning purposes.
