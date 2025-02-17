import subprocess
import os
import sys

def start_application():
    # Получаем переменные окружения из пайплайна
    deploy_dir = os.environ.get('DEPLOY_DIR')  # Путь к директории на сервере
    venv_dir = os.environ.get('VENV_DIR')  # Путь к виртуальному окружению

    if not deploy_dir or not venv_dir:
        print("Error: DEPLOY_DIR or VENV_DIR is not set.")
        sys.exit(1)

    # Путь к активации виртуального окружения и запуску приложения
    activate_venv = os.path.join(venv_dir, 'bin', 'activate_this.py')
    app_command = f"python {os.path.join(deploy_dir, 'app.py')}"

    try:
        # Активация виртуального окружения
        subprocess.run([sys.executable, activate_venv], check=True)
        # Запуск приложения в фоновом режиме
        subprocess.Popen(app_command, shell=True, cwd=deploy_dir)
        print(f"Application started in the background at {deploy_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error starting the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_application()
