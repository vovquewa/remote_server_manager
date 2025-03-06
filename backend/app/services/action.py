from app.core.logger import logger
import paramiko
from fastapi import HTTPException


def ssh_execute(ip: str, username: str, command: str):
    logger.info(f"ssh_execute: ip: {ip}, command: {command}")
    try:
        # Настройка SSH-клиента
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключение (замените на свои данные)
        client.connect(
            ip, username=username, key_filename="env/id_rsa", timeout=10
        )

        # Выполнение команды
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        print("Output:", output)
        print("command", command)
        client.close()

        if error:
            raise HTTPException(status_code=500, detail=error)
        return {
            # "input": input_read.strip(),
            "output": output.strip(),
            # "error": error.strip(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
