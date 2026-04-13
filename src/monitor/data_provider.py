import psutil
import subprocess
import shutil
import time

class MetricsProvider:
    def __init__(self):
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        # Initialize CPU percent with a non-None interval to avoid the initial 0.0 issue
        psutil.cpu_percent(interval=None)

    def get_cpu_usage(self) -> float:
        # Using interval=None is fine as long as it's called periodically,
        # but the first call in __init__ above helps seed the delta.
        return psutil.cpu_percent(interval=None)

    def get_memory_usage(self) -> dict:
        mem = psutil.virtual_memory()
        return {
            "percent": mem.percent,
            "used": mem.used / (1024**3),  # GB
            "total": mem.total / (1024**3)  # GB
        }

    def get_network_usage(self) -> dict:
        now = time.time()
        net_io = psutil.net_io_counters()

        elapsed = now - self.last_time

        # Avoid division by zero if called too rapidly
        if elapsed <= 0:
            return {"rx_speed": 0, "tx_speed": 0}

        rx_speed = (net_io.bytes_recv - self.last_net_io.bytes_recv) / elapsed
        tx_speed = (net_io.bytes_sent - self.last_net_io.bytes_sent) / elapsed

        self.last_net_io = net_io
        self.last_time = now

        return {
            "rx_speed": rx_speed / (1024**2),  # MB/s
            "tx_speed": tx_speed / (1024**2)   # MB/s
        }

    def get_gpu_usage(self) -> dict:
        """
        Attempts to get NVIDIA GPU usage via nvidia-smi.
        Returns a dict with utilization and memory.
        """
        if shutil.which("nvidia-smi") is None:
            return {"utilization": 0, "memory_used": 0, "memory_total": 0, "error": "No nvidia-smi found"}

        try:
            cmd = ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"]
            result = subprocess.check_output(cmd, encoding="utf-8").strip()
            parts = [float(x) for x in result.split(",")]
            return {
                "utilization": parts[0],
                "memory_used": parts[1],
                "memory_total": parts[2],
                "error": None
            }
        except Exception as e:
            return {"utilization": 0, "memory_used": 0, "memory_total": 0, "error": str(e)}
