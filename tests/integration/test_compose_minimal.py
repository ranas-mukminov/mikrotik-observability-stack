import os
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


def test_minimal_compose(tmp_path) -> None:
    compose_file = "compose/docker-compose.minimal.yml"
    env = os.environ.copy()
    cmd = ["docker", "compose", "-f", compose_file, "up", "-d"]
    subprocess.run(cmd, check=True)
    try:
        wait_for("http://localhost:9090/-/ready", timeout=90)
        wait_for("http://localhost:3000/api/health", timeout=90)
    finally:
        subprocess.run(["docker", "compose", "-f", compose_file, "down", "-v"], check=False)
