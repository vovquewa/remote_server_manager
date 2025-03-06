import logging
import time
import flet as ft
import httpx
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    handlers=[logging.StreamHandler()],  # Вывод в консоль
)

API_URL = "http://api:8000"


async def main(page: ft.Page):
    page.adaptive = True
    try:
        page.session_token = None  # Для хранения токена после успешного входа
        page.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout=30)
        )  # Создание клиента для работы с API
        page.padding = 20  # Отступы для мобильного экрана

        # Создаем клиент для работы с API
        # async def create_client():
        #     return httpx.AsyncClient(timeout=httpx.Timeout(timeout=30))

        # Функция для логина
        async def login(e):
            username = username_field.value
            password = password_field.value

            # Создаем клиента для запроса
            client: httpx.AsyncClient = page.client

            try:
                # Отправка запроса на логин
                response = await client.post(
                    f"{API_URL}/auth/jwt/login",
                    data={"username": username, "password": password},
                )
                response.raise_for_status()  # Если код ответа не 2xx, выбрасывается исключение
                logging.info(f"Login successful: {response.text}")
                result = response.json()
                page.session_token = result["access_token"]  # Сохраняем токен

                # Создание и добавление SnackBar с успешным сообщением
                snack_bar = ft.SnackBar(content=ft.Text("Login successful!"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()

                # Запрос данных после авторизации
                headers = {"Authorization": f"Bearer {page.session_token}"}
                servers_response = await client.get(f"{API_URL}/servers/", headers=headers)
                commands_response = await client.get(
                    f"{API_URL}/commands/", headers=headers
                )

                servers = servers_response.json()
                commands = commands_response.json()

                # Сохраняем servers и commands в page
                page.servers = servers
                page.commands = commands

                # Создаем dropdown для выбора серверов и команд
                dropdown_server = ft.Dropdown(
                    label="Select server",
                    options=[ft.dropdown.Option(server["name"]) for server in servers],
                )
                dropdown_command = ft.Dropdown(
                    label="Select command",
                    options=[ft.dropdown.Option(command["name"]) for command in commands],
                )

                # Сохраняем dropdown элементы в page
                page.dropdown_server = dropdown_server
                page.dropdown_command = dropdown_command

                page.controls.clear()  # Очищаем старые элементы
                page.add(
                    ft.Column(
                        [
                            ft.Text(
                                f"Welcome, {username}!", size=24, weight=ft.FontWeight.BOLD
                            ),
                            dropdown_server,
                            dropdown_command,
                            ft.ElevatedButton(
                                "Run command", on_click=execute_command, expand=True
                            ),
                            ft.ElevatedButton("Logout", on_click=logout, expand=True),
                        ],
                        alignment=ft.alignment.center,
                    )
                )
                page.update()

            except httpx.HTTPStatusError as e:
                logging.error(f"Login failed: {e.response.text}")
                # Если ошибка авторизации, показываем ошибку в SnackBar
                snack_bar = ft.SnackBar(content=ft.Text(f"Login failed: {e.response.text}"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()
            except httpx.TimeoutException as e:
                logging.error(f"Timeout error {e}")
                await page.client.aclose()  # Закрытие клиента после тайм-аута
                logging.info("Client closed after timeout")
                page.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout=30))  # Новый клиент
                logging.info("New client created")
                snack_bar = ft.SnackBar(content=ft.Text("Timeout error"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()
            except httpx.ConnectError:
                snack_bar = ft.SnackBar(content=ft.Text("Connection error"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()
    except httpx.ConnectError:
        snack_bar = ft.SnackBar(content=ft.Text("Connection error"))
        page.overlay.append(snack_bar)  # Добавление в overlay
        snack_bar.open = True  # Открытие SnackBar
        page.update()

    # Функция для выхода
    async def logout(e):
        if page.session_token:
            try:
                client: httpx.AsyncClient = page.client
                headers = {"Authorization": f"Bearer {page.session_token}"}
                response = await client.post(
                    f"{API_URL}/auth/jwt/logout", headers=headers
                )

                if response.status_code == 204:
                    page.session_token = None
                    snack_bar = ft.SnackBar(content=ft.Text("Logout successful!"))
                    page.overlay.append(snack_bar)  # Добавление в overlay
                    snack_bar.open = True  # Открытие SnackBar
                    page.update()

                    # Очистка экрана и возвращение на страницу логина
                    page.controls.clear()
                    page.add(
                        ft.Column(
                            [
                                username_field,
                                password_field,
                                ft.ElevatedButton("Login", on_click=login, expand=True),
                            ],
                            alignment=ft.alignment.center,
                        )
                    )
                    page.update()
                else:
                    snack_bar = ft.SnackBar(
                        content=ft.Text(
                            f"Logout failed: {response.json().get('detail', 'Unknown error')}"
                        )
                    )
                    page.overlay.append(snack_bar)  # Добавление в overlay
                    snack_bar.open = True  # Открытие SnackBar
                    page.update()
            except httpx.HTTPStatusError as e:
                snack_bar = ft.SnackBar(
                    content=ft.Text(f"Logout failed: {e.response.text}")
                )
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()
            except httpx.TimeoutException as e:
                logging.error(f"Timeout error {e}")
                await page.client.aclose()  # Закрытие клиента после тайм-аута
                logging.info("Client closed after timeout")
                page.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout=30))  # Новый клиент
                logging.info("New client created")        
                snack_bar = ft.SnackBar(content=ft.Text("Timeout error"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()
            except httpx.ConnectError:
                snack_bar = ft.SnackBar(content=ft.Text("Connection error"))
                page.overlay.append(snack_bar)  # Добавление в overlay
                snack_bar.open = True  # Открытие SnackBar
                page.update()

    # Функция для выполнения команды
    async def execute_command(e):
        # Получаем данные из page
        servers = page.servers
        commands = page.commands
        dropdown_server = page.dropdown_server
        dropdown_command = page.dropdown_command

        # Находим ID сервера и команды
        server_id = next(
            (item["id"] for item in servers if item["name"] == dropdown_server.value),
            None,
        )
        command_id = next(
            (
                command["id"]
                for command in commands
                if command["name"] == dropdown_command.value
            ),
            None,
        )

        try:
            client: httpx.AsyncClient = page.client
            headers = {"Authorization": f"Bearer {page.session_token}"}
            response = await client.post(
                f"{API_URL}/actions/",
                headers=headers,
                json={"server_id": server_id, "command_id": command_id},
            )

            # Отображение ответа
            logging.info(f"Command executed: {response.text}")
            snack_bar = ft.SnackBar(content=ft.Text(response.text))
            page.overlay.append(snack_bar)  # Добавление в overlay
            snack_bar.open = True  # Открытие SnackBar
            page.update()
        except httpx.HTTPStatusError as e:
            snack_bar = ft.SnackBar(
                content=ft.Text(f"Command execution failed: {e.response.text}")
            )
            page.overlay.append(snack_bar)  # Добавление в overlay
            snack_bar.open = True  # Открытие SnackBar
            page.update()
        except httpx.TimeoutException as e:
            logging.error(f"Timeout error {e}")
            await page.client.aclose()  # Закрытие клиента после тайм-аута
            logging.info("Client closed after timeout")
            page.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout=30))  # Новый клиент
            logging.info("New client created")
            snack_bar = ft.SnackBar(content=ft.Text("Timeout error"))
            page.overlay.append(snack_bar)  # Добавление в overlay
            snack_bar.open = True  # Открытие SnackBar
            page.update()
        except httpx.ConnectError:
            snack_bar = ft.SnackBar(content=ft.Text("Connection error"))
            page.overlay.append(snack_bar)  # Добавление в overlay
            snack_bar.open = True  # Открытие SnackBar
            page.update()
    # Поля ввода для логина
    username_field = ft.TextField(label="Username", expand=True)
    password_field = ft.TextField(label="Password", password=True, expand=True)

    # Добавление формы авторизации на страницу
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    username_field,
                    password_field,
                    ft.ElevatedButton("Login", on_click=login, expand=True),
                ],
                alignment=ft.alignment.center,
            ),
            alignment=ft.alignment.center,
        )
    )


ft.app(target=main)
