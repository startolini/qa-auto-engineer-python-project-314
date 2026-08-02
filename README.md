# Тестирование канбан-доски

### Hexlet tests and linter status:
[![Actions Status](https://github.com/startolini/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/startolini/qa-auto-engineer-python-project-314/actions)

UI-автотесты для приложения Task Manager (канбан-доска): Python, Selenium, pytest.
Взаимодействие со страницами оформлено по паттерну Page Object — локаторы и действия
вынесены в классы в каталоге `pages/`, тесты в `tests/` описывают только сценарии.

Покрытые разделы:

- **Аутентификация** — вход и выход, проверка загрузки дашборда
- **Пользователи** — создание с валидацией email, просмотр, редактирование, удаление
- **Статусы задач** — CRUD и массовое удаление
- **Метки** — CRUD и массовое удаление
- **Задачи** — создание, редактирование, удаление, перемещение между колонками,
  фильтры по статусу, исполнителю и метке

## Требования

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Docker (для запуска тестируемого приложения)
- Google Chrome / Chromium

## Установка

```bash
make install
```

## Запуск приложения

Приложение поднимается в Docker и доступно на <http://localhost:5173>:

```bash
make start
```

## Запуск тестов

```bash
make test        # весь набор
make smoke       # только smoke-тесты
```

Отчёт Allure (требуется [Allure CLI](https://allurereport.org/docs/install/)):

```bash
make allure-report
```

## Линтер и типы

```bash
make lint
make ty
```

## Настройка окружения

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `APP_BASE_URL` | адрес тестируемого приложения | `http://localhost:5173` |
| `LOGIN_PATH` | путь страницы логина | `/#/login` |
| `HEADLESS` | `1` — запуск браузера без окна, `0` — с окном | автоопределение |
| `CHROME_BIN`, `CHROMEDRIVER_PATH` | пути к браузеру и драйверу | системные |
