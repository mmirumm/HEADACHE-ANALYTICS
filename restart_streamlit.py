"""Перезапуск локального сервера Streamlit на macOS."""
from pathlib import Path
import os
import signal
import subprocess
import time

PROJECT = Path(__file__).resolve().parent
PORT = 8501


def server_pids() -> list[int]:
    result = subprocess.run(
        ["/usr/sbin/lsof", "-nP", "-t", f"-iTCP:{PORT}", "-sTCP:LISTEN"],
        capture_output=True, text=True,
    )
    if result.returncode not in (0, 1):
        raise SystemExit("Не удалось проверить порт 8501: " + result.stderr.strip())
    return sorted({int(line) for line in result.stdout.splitlines() if line.isdigit()})


def main() -> None:
    python = PROJECT / ".venv/bin/python"
    if not python.exists():
        raise SystemExit("В папке проекта не найден Python: .venv/bin/python")
    pids = server_pids()
    # Проверка принадлежности процессов перед остановкой.
    for pid in pids:
        cwd = subprocess.run(
            ["/usr/sbin/lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        command = subprocess.run(
            ["/bin/ps", "-p", str(pid), "-o", "command="],
            capture_output=True, text=True, check=True,
        ).stdout
        if "n" + str(PROJECT) not in cwd or "streamlit run app.py" not in command:
            raise SystemExit("Порт 8501 занят другим приложением. Ничего не остановлено.")
    for pid in pids:
        try:
            os.kill(pid, signal.SIGINT)
        except ProcessLookupError:
            pass
    for _ in range(40):
        if not server_pids():
            break
        time.sleep(0.25)
    else:
        raise SystemExit("Предыдущий сервер ещё завершает работу. Повторите команду через несколько секунд.")
    os.chdir(PROJECT)
    print("Запускаю MigreBot: http://localhost:8501", flush=True)
    os.execv(str(python), [str(python), "-B", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"])


if __name__ == "__main__":
    main()
