# Linux Performance Monitor (LPM)

A modern, terminal-based dashboard to monitor your Linux system's performance in real-time.

## Features

- **Real-time CPU Usage**: Visualized with sparklines.
- **Memory Monitoring**: Track RAM usage and availability.
- **Network Throughput**: Monitor incoming and outgoing traffic.
- **GPU Monitoring**: NVIDIA GPU utilization (if available).
- **Modern TUI**: Built with the `Textual` framework for a beautiful terminal interface.

## Installation

Ensure you have Python 3.8+ installed.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```

## Usage

Simply run the application:

```bash
python -m monitor.app
```

## Requirements

- `psutil`
- `textual`
- `nvidia-smi` (optional, for NVIDIA GPU monitoring)
