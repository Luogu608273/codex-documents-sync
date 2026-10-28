"""Read-only ADB status and one-shot PNG capture, with a persistent cooldown."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time

DEFAULT_ADB = r"C:\Program Files\YXArkNights-12.0\shell\adb.exe"
DEFAULT_SERIAL = "127.0.0.1:16384"


def run(adb, args, timeout=20):
    result = subprocess.run([str(adb), *args], capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def png_dimensions(data):
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("ADB did not return a PNG image")
    width, height = struct.unpack(">II", data[16:24])
    if not width or not height or b"IEND" not in data[-16:]:
        raise ValueError("Invalid or truncated PNG")
    return width, height


def capture(adb, serial, output, state_dir, interval):
    # One state per serial, shared across invocations and output filenames.
    state_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(serial.encode()).hexdigest()[:20]
    stamp = state_dir / (key + ".json")
    lock = state_dir / (key + ".lock")
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError:
        raise RuntimeError(f"Capture already active or stale lock; inspect {lock}")
    try:
        with handle:
            handle.write(str(time.time()))
        now = time.time()
        if stamp.exists():
            previous = json.loads(stamp.read_text(encoding="utf-8"))["captured_at"]
            remaining = interval - (now - float(previous))
            if remaining > 0:
                return {"status": "skipped", "reason": "capture_cooldown", "retry_after_seconds": round(remaining, 1)}
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite {output}")
        data = run(adb, ["-s", serial, "exec-out", "screencap", "-p"])
        width, height = png_dimensions(data)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as f:
            f.write(data)
        stamp.write_text(json.dumps({"captured_at": time.time(), "path": str(output.resolve())}), encoding="utf-8")
        return {"status": "captured", "path": str(output.resolve()), "width": width, "height": height, "bytes": len(data)}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adb", type=Path, default=Path(DEFAULT_ADB))
    parser.add_argument("--serial", default=DEFAULT_SERIAL)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("status")
    shot = sub.add_parser("screenshot")
    shot.add_argument("--output", type=Path, required=True)
    shot.add_argument("--interval", type=float, default=30, help="Minimum seconds between captures; at least 30")
    shot.add_argument("--state-dir", type=Path, default=Path(tempfile.gettempdir()) / "maa-adb-observation")
    args = parser.parse_args()
    if not args.adb.is_file():
        raise FileNotFoundError(args.adb)
    if args.action == "status":
        decode = lambda b: b.decode("utf-8", errors="replace").strip()
        devices = decode(run(args.adb, ["devices", "-l"]))
        state = decode(run(args.adb, ["-s", args.serial, "get-state"]))
        # pidof may exit 1 when the game is stopped; this is a valid status.
        pid = subprocess.run([str(args.adb), "-s", args.serial, "shell", "pidof", "com.hypergryph.arknights"], capture_output=True, timeout=15)
        if pid.returncode not in (0, 1):
            raise RuntimeError(decode(pid.stderr))
        print(json.dumps({"devices": devices, "serial": args.serial, "state": state, "arknights_pid": decode(pid.stdout) or None}, ensure_ascii=False))
    else:
        if not 30 <= args.interval <= 86400:
            parser.error("--interval must be between 30 and 86400 seconds")
        print(json.dumps(capture(args.adb, args.serial, args.output, args.state_dir, args.interval), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
