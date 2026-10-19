"""Run validation from a fresh temporary directory in Python isolated mode."""

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen


PROJECT = Path(__file__).resolve().parent
LOG = PROJECT / "docs" / "cold-run-log.md"
FILES = ("jnj_project1_fcff.py", "jnj_peer_multiples.py", "validation_suite.py", "jnj_valuation_app.py", "jnj_valuation_dashboard.html")


def available_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
    request = Request(url, method="POST" if payload is not None else "GET")
    if payload is not None:
        request.data = json.dumps(payload).encode("utf-8")
        request.add_header("Content-Type", "application/json")
    try:
        with urlopen(request, timeout=2) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="jnj-cold-run-") as temporary:
        staging = Path(temporary)
        for name in FILES:
            shutil.copy2(PROJECT / name, staging / name)
        # -I removes inherited paths and user packages.  Add back only this
        # newly staged directory so the copied local modules can import.
        result = subprocess.run(
            [sys.executable, "-I", "-c", "import runpy,sys;sys.path.insert(0,'.');runpy.run_path('validation_suite.py',run_name='__main__')"],
            cwd=staging,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode:
            raise SystemExit(f"Cold-run validation failed:\n{output}")

        # Dashboard end-to-end: clean launch, bounded adjustment, deliberate
        # invalid-input failure, recovery, and exact base reset through the API.
        port = available_port()
        environment = os.environ | {"JNJ_DASHBOARD_PORT": str(port), "JNJ_OPEN_BROWSER": "0"}
        server = subprocess.Popen(
            [sys.executable, "-I", "-c", "import runpy,sys;sys.path.insert(0,'.');runpy.run_path('jnj_valuation_app.py',run_name='__main__')"],
            cwd=staging, env=environment, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        )
        endpoint = f"http://127.0.0.1:{port}/api/model"
        try:
            for _ in range(30):
                try:
                    initial_status, initial = request_json(endpoint)
                    if initial_status == 200:
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise AssertionError("Dashboard did not start in the fresh environment.")
            base_growth = initial["assumptions"]["revenue_growth"]
            changed_status, changed = request_json(endpoint, {"revenue_growth": [0.04, 0.03, 0.03, 0.025, 0.02]})
            assert changed_status == 200 and changed["valuation"]["value_per_share"] < initial["valuation"]["value_per_share"]
            invalid_status, _ = request_json(endpoint, {"wacc": 0.05, "terminal_growth": 0.06})
            assert invalid_status == 400
            reset_status, reset = request_json(endpoint)
            assert reset_status == 200 and reset["assumptions"]["revenue_growth"] == base_growth
            dashboard_output = "PASS: dashboard clean launch; downside adjustment; invalid-input failure; recovery; base reset."
        finally:
            # Forceful shutdown is intentional here: serve_forever has no
            # in-band shutdown endpoint and Windows otherwise can retain the
            # staged directory handle after the validation process exits.
            try:
                server.kill()
                server.wait(timeout=5)
            finally:
                if server.stderr:
                    server.stderr.close()
    LOG.write_text(
        "# Cold-run validation log\n\n"
        f"- Run timestamp (UTC): {datetime.now(timezone.utc).isoformat()}\n"
        "- Environment: fresh temporary working directory; Python isolated mode (`-I`); standard-library model only.\n"
        "- Result: PASS\n\n"
        f"```text\n{output}\n{dashboard_output}\n```\n",
        encoding="utf-8",
    )
    print(f"PASS: cold-run log written to {LOG}")


if __name__ == "__main__":
    main()
