#!/bin/bash

PID_FILE="app.pid"

# Проверка на наличие PID файла и завершение процесса
if [ -f "$PID_FILE" ]; then
    # Чтение PID из файла
    OLD_PID=$(cat "$PID_FILE")

    # Проверка, существует ли процесс с таким PID
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Завершаем старое приложение с PID $OLD_PID..."
        kill "$OLD_PID"   # Завершаем процесс
        sleep 1            # Подождем немного
    fi

    # Удаляем старый PID файл
    rm "$PID_FILE"
fi

# Запуск нового приложения Flask
echo "Запускаем новое приложение..."
nohup python3 app.py &  # Запуск в фоновом режиме
NEW_PID=$!

# Сохраняем новый PID в файл
echo "$NEW_PID" > "$PID_FILE"
echo "Приложение запущено с PID $NEW_PID"
