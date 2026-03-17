import shlex
import subprocess

COMANDOS_BLOQUEADOS = {
    "rm",
    "shutdown",
    "reboot",
    "systemctl",
    "sudo",
    "mkfs",
    "dd",
    "poweroff",
    "init",
}


CARACTERES_BLOQUEADOS = ["|", ">", ">>", "<", ";", "&&", "||"]


def validar_comando(comando: str):
    comando = (comando or "").strip()

    if not comando:
        return False, "Comando vazio."

    for item in CARACTERES_BLOQUEADOS:
        if item in comando:
            return False, f"Uso não permitido no playground: {item}"

    try:
        partes = shlex.split(comando)
    except ValueError:
        return False, "Comando inválido."

    if not partes:
        return False, "Comando vazio."

    comando_base = partes[0].lower()

    if comando_base in COMANDOS_BLOQUEADOS:
        return False, f"Comando bloqueado no playground: {comando_base}"

    return True, None


def executar_comando_isolado(comando: str):
    ok, erro = validar_comando(comando)
    if not ok:
        return {
            "ok": False,
            "stdout": "",
            "stderr": erro,
            "exit_code": 1,
        }

    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "alpine",
        "sh",
        "-c",
        comando,
    ]

    try:
        resultado = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=20,
        )

        return {
            "ok": resultado.returncode == 0,
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "exit_code": resultado.returncode,
        }

    except FileNotFoundError:
        return {
            "ok": False,
            "stdout": "",
            "stderr": "Docker não encontrado no sistema.",
            "exit_code": 1,
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "stdout": "",
            "stderr": "Tempo limite excedido no playground.",
            "exit_code": 1,
        }


def executar_playground(comando: str):
    return executar_comando_isolado(comando)
