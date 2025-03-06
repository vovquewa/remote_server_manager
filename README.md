# Server Manager

### Описание
Приложение для управления серверами через SSH.

### Запуск docker-compose (linux\amd64)
Создание рабочей директории проекта
Создание каталога env/
Наполняем каталог env/:
   - создаем файл .env с содержимым согласно шаблону env.example
   ```
   DB_NAME=fastapi
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   DB_HOST=db # db container name if compose else host
   DB_PORT=5432
   APP_TITLE=Remote server manager
   APP_DESCRIPTION=Server remote control via ssh
   APP_VERSION=0.1.0
   ```
   - ложим сертификат id_rsa  для доступа к удаленным серверам

Копируем docker-compose.yml в коррень рабочей директории

```bash
docker-compose up
```
