import math
import time

from prometheus_client import Info, start_http_server


class Simulator:
    def __init__(self, name="simulator"):
        self.states = Info(f"{name}_states", f"Edge device states for {name}")

    def update(self, t):
        self.states.info(
            {
                "x": str(math.sin(t)),
                "y": str(math.cos(t)),
                "z": str(math.tan(t)),
            }
        )


def run_simulators(num_devices=3, port=8000):
    print(f"Running {num_devices} simulators on port {port}")
    devices = [Simulator(name=f"simulator{i:03d}") for i in range(num_devices)]

    start_http_server(port)

    while True:
        time.sleep(1)
        t = time.time()
        for idx, device in enumerate(devices):
            device.update(t=t + idx * 0.1)
