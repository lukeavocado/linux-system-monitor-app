from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive
from textual.widgets import Digits
from monitor.data_provider import MetricsProvider

class MetricWidget(Static):
    """A widget to display a single metric with a label."""
    label = reactive("")
    value = reactive("0.0")
    unit = reactive("")

    def __init__(self, label: str, unit: str, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.unit = unit

    def compose(self) -> ComposeResult:
        yield Static(self.label, classes="label")
        yield Digits(self.value, classes="value")
        yield Static(self.unit, classes="unit")

    def on_mount(self) -> None:
        self.add_class("metric-card")

class PerformanceApp(App):
    """The main Performance Monitor Application."""

    CSS = """
    Screen {
        align: center middle;
    }

    #dashboard {
        layout: grid;
        grid-size: 3;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 1fr 1fr;
        padding: 1;
    }

    .metric-card {
        border: heavy $primary;
        padding: 1 2;
        content-align: center middle;
        height: 100%;
    }

    .label {
        content-align: center middle;
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    .value {
        content-align: center middle;
        color: $accent;
    }

    .unit {
        content-align: center middle;
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Manual Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="dashboard"):
            yield MetricWidget("CPU Usage", "%", id="cpu-widget")
            yield MetricWidget("Memory Usage", "%", id="mem-widget")
            yield MetricWidget("Network RX", "MB/s", id="net-rx-widget")
            yield MetricWidget("Network TX", "MB/s", id="net-tx-widget")
            yield MetricWidget("GPU Usage", "%", id="gpu-widget")
            yield MetricWidget("GPU Mem", "MB", id="gpu-mem-widget")
        yield Footer()

    def on_mount(self) -> None:
        self.provider = MetricsProvider()
        self.update_metrics()
        self.set_interval(1.0, self.update_metrics)

    async def action_refresh(self) -> None:
        self.update_metrics()

    def update_metrics(self) -> None:
        # CPU
        cpu = self.provider.get_cpu_usage()
        self.query_one("#cpu-widget").value = f"{cpu:.1f}"

        # Memory
        mem = self.provider.get_memory_usage()
        self.query_one("#mem-widget").value = f"{mem['percent']:.1f}"

        # Network
        net = self.provider.get_network_usage()
        self.query_one("#net-rx-widget").value = f"{net['rx_speed']:.2f}"
        self.query_one("#net-tx-widget").value = f"{net['tx_speed']:.2f}"

        # GPU
        gpu = self.provider.get_gpu_usage()
        if gpu.get("error"):
            self.query_one("#gpu-widget").value = "N/A"
            self.query_one("#gpu-mem-widget").value = "N/A"
        else:
            self.query_one("#gpu-widget").value = f"{gpu['utilization']:.1f}"
            self.query_one("#gpu-mem-widget").value = f"{gpu['memory_used']:.0f}"

if __name__ == "__main__":
    app = PerformanceApp()
    app.run()
