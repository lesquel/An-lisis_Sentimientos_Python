#!/usr/bin/env python3
"""Controlador cross-platform para el proyecto Sentimind."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Sequence


ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

# ── Cached tool paths ──────────────────────────────────────────────
_uv_path: str | None | bool = False  # False = not yet searched


def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None


def find_uv() -> str | None:
    """Find the *uv* binary – checks PATH then common install locations."""
    global _uv_path
    if _uv_path is not False:
        return _uv_path  # type: ignore[return-value]

    # 1. PATH
    found = shutil.which("uv")
    if found:
        _uv_path = found
        return found

    # 2. Common install dirs (Linux/macOS)
    home = Path.home()
    candidates: list[Path] = []
    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            home / ".local" / "bin" / "uv.exe",
            home / ".cargo" / "bin" / "uv.exe",
            *(([Path(local_app) / "uv" / "uv.exe"]) if local_app else []),
        ]
    else:
        candidates = [
            home / ".local" / "bin" / "uv",
            home / ".cargo" / "bin" / "uv",
        ]

    for c in candidates:
        if c.exists():
            _uv_path = str(c)
            return _uv_path

    _uv_path = None
    return None


def run(cmd: Sequence[str], cwd: Path | None = None, check: bool = True) -> int:
    command_str = " ".join(str(c) for c in cmd)
    print(f"$ {command_str}")
    result = subprocess.run(cmd, cwd=str(cwd or ROOT_DIR), check=False)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def docker_compose_base() -> list[str]:
    try:
        subprocess.run(
            ["docker", "compose", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return ["docker", "compose"]
    except Exception:
        if has_cmd("docker-compose"):
            return ["docker-compose"]
    print("Error: no se encontró Docker Compose (docker compose o docker-compose).")
    raise SystemExit(1)


def compose_file(mode: str) -> Path:
    return ROOT_DIR / ("docker-compose.dev.yml" if mode == "dev" else "docker-compose.yml")


def compose_cmd(mode: str, *args: str) -> list[str]:
    return docker_compose_base() + ["-f", str(compose_file(mode)), *args]


def ensure_backend_venv() -> None:
    """Make sure the backend .venv exists; run *uv sync* if it doesn't."""
    venv_dir = BACKEND_DIR / ".venv"
    if venv_dir.exists():
        return
    uv = find_uv()
    if uv:
        print("⏳  Entorno virtual no encontrado – ejecutando uv sync …")
        run([uv, "sync"], cwd=BACKEND_DIR)
    else:
        print("Error: no existe .venv y uv no está instalado.")
        print("  Instala uv → curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("  Luego ejecuta: uv sync  (dentro de backend/)")
        raise SystemExit(1)


def backend_local_base() -> list[str]:
    """Return the base command to invoke Django manage.py locally."""
    uv = find_uv()
    if uv:
        # uv run takes care of the virtualenv automatically
        return [uv, "run", "python", "manage.py"]

    # Fallback: use venv Python directly
    if sys.platform == "win32":
        venv_python = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = BACKEND_DIR / ".venv" / "bin" / "python"

    if venv_python.exists():
        return [str(venv_python), "manage.py"]

    # Nothing found – give a helpful message
    print("Error: no se encontró uv ni un entorno virtual (.venv) en backend/.")
    print("  Instala uv → curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("  Luego ejecuta: uv sync  (dentro de backend/)")
    raise SystemExit(1)


def frontend_local_base() -> list[str]:
    if has_cmd("bun"):
        return ["bun", "run"]
    if has_cmd("npm"):
        return ["npm", "run"]
    print("Error: no se encontró bun ni npm en PATH.")
    raise SystemExit(1)


def stream_output(prefix: str, process: subprocess.Popen[str]) -> None:
    if process.stdout is None:
        return
    for line in process.stdout:
        print(f"[{prefix}] {line}", end="")


def terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=6)
    except subprocess.TimeoutExpired:
        process.kill()


def run_local_both() -> int:
    backend_cmd = backend_local_base() + ["runserver", "0.0.0.0:8000"]

    frontend_runner = frontend_local_base()
    if frontend_runner[0] == "bun":
        frontend_cmd = frontend_runner + ["dev", "--host", "0.0.0.0", "--port", "5173"]
    else:
        frontend_cmd = frontend_runner + ["dev", "--", "--host", "0.0.0.0", "--port", "5173"]

    print(f"$ {' '.join(backend_cmd)}")
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    print(f"$ {' '.join(frontend_cmd)}")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    backend_thread = threading.Thread(target=stream_output, args=("backend", backend_proc), daemon=True)
    frontend_thread = threading.Thread(target=stream_output, args=("frontend", frontend_proc), daemon=True)
    backend_thread.start()
    frontend_thread.start()

    try:
        while True:
            backend_rc = backend_proc.poll()
            frontend_rc = frontend_proc.poll()

            if backend_rc is not None or frontend_rc is not None:
                terminate_process(backend_proc)
                terminate_process(frontend_proc)
                return backend_rc if backend_rc not in (None, 0) else (frontend_rc or 0)

            time.sleep(0.4)
    except KeyboardInterrupt:
        print("\nDeteniendo backend y frontend...")
        terminate_process(backend_proc)
        terminate_process(frontend_proc)
        return 0


def cmd_up(args: argparse.Namespace) -> None:
    if args.runtime == "docker":
        if args.target == "all":
            run(compose_cmd(args.mode, "up", "--build", "-d"))
            return

        service_args = [] if args.with_deps else ["--no-deps"]
        run(compose_cmd(args.mode, "up", "--build", "-d", *service_args, args.target))
        return

    # ── Local mode ──
    if args.target in ("all", "backend"):
        ensure_backend_venv()

    if args.target == "all":
        raise SystemExit(run_local_both())

    if args.target == "backend":
        run(backend_local_base() + ["runserver", "0.0.0.0:8000"], cwd=BACKEND_DIR)
    else:
        frontend_runner = frontend_local_base()
        if frontend_runner[0] == "bun":
            run(frontend_runner + ["dev", "--host", "0.0.0.0", "--port", "5173"], cwd=FRONTEND_DIR)
        else:
            run(frontend_runner + ["dev", "--", "--host", "0.0.0.0", "--port", "5173"], cwd=FRONTEND_DIR)


def cmd_down(args: argparse.Namespace) -> None:
    if args.runtime != "docker":
        print("En modo local, detén procesos con Ctrl+C o desde VS Code (Terminate Task).")
        return

    if args.target == "all":
        extra = ["--volumes", "--remove-orphans"] if args.volumes else []
        run(compose_cmd(args.mode, "down", *extra))
        return

    run(compose_cmd(args.mode, "stop", args.target))
    run(compose_cmd(args.mode, "rm", "-f", args.target), check=False)


def cmd_logs(args: argparse.Namespace) -> None:
    if args.target == "all":
        run(compose_cmd(args.mode, "logs", "-f", "--tail=200"))
    else:
        run(compose_cmd(args.mode, "logs", "-f", "--tail=200", args.target))


def cmd_status(args: argparse.Namespace) -> None:
    run(compose_cmd(args.mode, "ps"))


def cmd_db(args: argparse.Namespace) -> None:
    if args.runtime == "docker":
        if args.action == "migrate":
            run(compose_cmd(args.mode, "run", "--rm", "backend", "python", "manage.py", "migrate"))
        elif args.action == "makemigrations":
            run(compose_cmd(args.mode, "run", "--rm", "backend", "python", "manage.py", "makemigrations"))
        else:
            run(compose_cmd(args.mode, "run", "--rm", "backend", "python", "seed_data.py", "--silent"))
        return

    ensure_backend_venv()
    base = backend_local_base()
    if args.action == "migrate":
        run(base + ["migrate"], cwd=BACKEND_DIR)
    elif args.action == "makemigrations":
        run(base + ["makemigrations"], cwd=BACKEND_DIR)
    else:
        uv = find_uv()
        if uv:
            run([uv, "run", "python", "seed_data.py", "--silent"], cwd=BACKEND_DIR)
        else:
            # Use venv python
            if sys.platform == "win32":
                vpy = str(BACKEND_DIR / ".venv" / "Scripts" / "python.exe")
            else:
                vpy = str(BACKEND_DIR / ".venv" / "bin" / "python")
            run([vpy, "seed_data.py", "--silent"], cwd=BACKEND_DIR)


def cmd_test(args: argparse.Namespace) -> None:
    if args.runtime == "docker":
        run(compose_cmd(args.mode, "run", "--rm", "backend", "python", "manage.py", "test"))
    else:
        ensure_backend_venv()
        run(backend_local_base() + ["test"], cwd=BACKEND_DIR)


def cmd_lint(args: argparse.Namespace) -> None:
    if args.runtime == "docker":
        run(compose_cmd(args.mode, "run", "--rm", "frontend", "bun", "run", "lint"))
        return

    if has_cmd("bun"):
        run(["bun", "run", "lint"], cwd=FRONTEND_DIR)
    else:
        run(["npm", "run", "lint"], cwd=FRONTEND_DIR)


def cmd_health(args: argparse.Namespace) -> None:
    backend_url = args.backend_url
    frontend_url = args.frontend_url

    def check(url: str, name: str) -> bool:
        import urllib.request

        try:
            with urllib.request.urlopen(url, timeout=6):
                print(f"✅ {name} OK -> {url}")
                return True
        except Exception:
            print(f"❌ {name} FAIL -> {url}")
            return False

    ok_backend = check(backend_url, "Backend API")
    ok_frontend = check(frontend_url, "Frontend")
    if not (ok_backend and ok_frontend):
        raise SystemExit(1)


def cmd_setup(_: argparse.Namespace) -> None:
    uv = find_uv()
    if uv:
        run([uv, "sync"], cwd=BACKEND_DIR)
    else:
        print("⚠️ uv no está instalado. Se omite setup backend local.")
        print("  Instala uv → curl -LsSf https://astral.sh/uv/install.sh | sh")

    if has_cmd("bun"):
        run(["bun", "install"], cwd=FRONTEND_DIR)
    elif has_cmd("npm"):
        run(["npm", "install"], cwd=FRONTEND_DIR)
    else:
        print("⚠️ No se encontró bun ni npm. Se omite setup frontend local.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlador Sentimind (Linux/Windows)")
    sub = parser.add_subparsers(dest="command", required=True)

    up = sub.add_parser("up", help="Levantar servicios")
    up.add_argument("--runtime", choices=["docker", "local"], default="docker")
    up.add_argument("--mode", choices=["dev", "prod"], default="dev")
    up.add_argument("--target", choices=["all", "backend", "frontend"], default="all")
    up.add_argument("--with-deps", action="store_true", help="Incluye dependencias en docker up por servicio")
    up.set_defaults(func=cmd_up)

    down = sub.add_parser("down", help="Detener servicios")
    down.add_argument("--runtime", choices=["docker", "local"], default="docker")
    down.add_argument("--mode", choices=["dev", "prod"], default="dev")
    down.add_argument("--target", choices=["all", "backend", "frontend"], default="all")
    down.add_argument("--volumes", action="store_true", help="Elimina volúmenes (solo all)")
    down.set_defaults(func=cmd_down)

    logs = sub.add_parser("logs", help="Ver logs docker")
    logs.add_argument("--mode", choices=["dev", "prod"], default="dev")
    logs.add_argument("--target", choices=["all", "backend", "frontend"], default="all")
    logs.set_defaults(func=cmd_logs)

    status = sub.add_parser("status", help="Estado docker")
    status.add_argument("--mode", choices=["dev", "prod"], default="dev")
    status.set_defaults(func=cmd_status)

    db = sub.add_parser("db", help="Operaciones de base de datos")
    db.add_argument("--runtime", choices=["docker", "local"], default="docker")
    db.add_argument("--mode", choices=["dev", "prod"], default="dev")
    db.add_argument("--action", choices=["migrate", "makemigrations", "seed"], default="migrate")
    db.set_defaults(func=cmd_db)

    test = sub.add_parser("test", help="Tests backend")
    test.add_argument("--runtime", choices=["docker", "local"], default="docker")
    test.add_argument("--mode", choices=["dev", "prod"], default="dev")
    test.set_defaults(func=cmd_test)

    lint = sub.add_parser("lint", help="Lint frontend")
    lint.add_argument("--runtime", choices=["docker", "local"], default="docker")
    lint.add_argument("--mode", choices=["dev", "prod"], default="dev")
    lint.set_defaults(func=cmd_lint)

    health = sub.add_parser("health", help="Health check frontend/backend")
    health.add_argument("--backend-url", default="http://127.0.0.1:8000/api/")
    health.add_argument("--frontend-url", default="http://localhost:5173")
    health.set_defaults(func=cmd_health)

    setup = sub.add_parser("setup", help="Instalar dependencias locales")
    setup.set_defaults(func=cmd_setup)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
