import os
import socket
import subprocess
import time
import urllib.error
import urllib.request

import pytest

RUN_COMPOSE = os.getenv("MOS_RUN_COMPOSE_TESTS") == "1"
pytestmark = pytest.mark.skipif(not RUN_COMPOSE, reason="Set MOS_RUN_COMPOSE_TESTS=1 to run compose tests")


def wait_for(url: str, timeout: int = 60) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status < 500:
                    return
        except urllib.error.URLError:
            time.sleep(2)
    raise TimeoutError(f"Timeout waiting for {url}")


def test_full_compose() -> None:
    compose_file = "compose/docker-compose.full.yml"
    subprocess.run(["docker", "compose", "-f", compose_file, "up", "-d"], check=True)
    try:
        wait_for("http://localhost:9090/-/ready", timeout=120)
        wait_for("http://localhost:3000/api/health", timeout=120)
        wait_for("http://localhost:3100/ready", timeout=120)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(b"<134>1 test-host mosctl - - - Test log line", ("127.0.0.1", 1514))
        wait_for("http://localhost:3100/loki/api/v1/labels", timeout=30)
    finally:
        subprocess.run(["docker", "compose", "-f", compose_file, "down", "-v"], check=False)
