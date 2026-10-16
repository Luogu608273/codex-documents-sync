"""Load the installed MAA Python SDK and resources without connecting or starting tasks."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maa-dir", type=Path, default=Path(r"D:\MAA-Arknights-Assistant"))
    parser.add_argument("--user-dir", type=Path, required=True, help="Separate SDK logs from the running GUI")
    args = parser.parse_args()
    maa_dir = args.maa_dir.resolve(strict=True)
    for item in (maa_dir / "MaaCore.dll", maa_dir / "Python/asst/asst.py", maa_dir / "resource"):
        if not item.exists():
            raise FileNotFoundError(item)
    args.user_dir.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(maa_dir / "Python"))
    from asst.asst import Asst
    if not Asst.load(maa_dir, user_dir=args.user_dir.resolve()):
        raise RuntimeError("Asst.load failed; inspect the isolated user directory")
    asst = Asst()
    print(json.dumps({"version": asst.get_version(), "instance_running": asst.running(), "device_connected_by_probe": False, "tasks_appended": 0, "user_dir": str(args.user_dir.resolve())}, ensure_ascii=False))
    del asst


if __name__ == "__main__":
    main()
