# FastAPI Boilerplate

Этот шаблон соответствует многоуровневой архитектуре, которая включает уровень модели, уровень репозитория, 
уровень обслуживания и уровень API. Его структура каталогов предназначена для изоляции шаблонного кода внутри 
основного каталога, который требует минимального внимания, что облегчает быструю и простую разработку функций. 
Структура каталогов также, как правило, очень предсказуема. Основная цель проекта — предложить готовый к использованию
шаблон с улучшенными возможностями для разработчиков и легкодоступными функциями. Он также имеет некоторые широко
используемые функции, такие как аутентификация, авторизация, миграция баз данных, проверка типов и т. д., 
которые подробно обсуждаются в разделе «Features».

### Features

- Python 3.11+ support
- SQLAlchemy 2.0+ support
- Asynchoronous capabilities
- Database migrations using Alembic
- Basic Authentication using JWT
- Row Level Access Control for permissions
- Redis for caching
- Celery for background tasks
- Testing suite
- Type checking using mypy
- Dockerized database and redis
- Readily available CRUD operations
- Linting using pylint
- Formatting using black

## Локальный запуск

### Installation Guide

Для работы проекта понадобятся:

- Python 3.11
- [Docker with Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

1. Создаем вирутальное окружение с помощью poetry:

```bash
poetry shell
```

2. Устанавливаем зависимости:

```bash
poetry install
```

3. Поднимаем БД и брокеры сообщений с помощью docker: (не реализовано)

```bash
docker-compose up -d
```

4. Копируем содержимое `.env.example` в созданный нами `.env` и устанавливаем нужные нам значения.

5. Накатываем миграции:

```bash
make migrate
```

6. Запускаем сервер:

```bash
make run
```

Сервер будет доступен по адресу `http://localhost:8000`. Документация к API будет доступна по адресу `http://localhost:8000/docs`.

### Структура проекта

Проект спроектирован как модульный и масштабируемый. В проекте есть 3 основных каталога:

1. `core`: Этот каталог содержит центральную часть этого проекта. Он содержит большую часть стандартного кода, 
например зависимости безопасности, подключения к базе данных, конфигурацию, промежуточное ПО и т. д. Он также 
содержит базовые классы для моделей, репозиториев и сервисов. Каталог `core` спроектирован так, чтобы быть 
максимально минимальным и обычно требует минимального внимания. В целом, каталог `core` спроектирован максимально 
универсальным и может использоваться в любом проекте. При создании дополнительной функции вам, возможно, вообще не п
онадобится изменять этот каталог, за исключением добавления дополнительных служб в класс `Factory` в файле `core/factory.py`.

2. `app`: Этот каталог содержит фактический код приложения. Он содержит модели, репозитории, сервисы и схемы для приложения. 
Это каталог, в котором вы будете проводить большую часть своего времени при создании функций. В каталоге имеются следующие подкаталоги:
   - `models` - Здесь описывается схема БД.
   - `repositories` - Для большинства моделей нужно будет создавать репозитории. Это часто используемые CRUD операции с сущностями.
   - `services` - Для каждой логической единицы приложения необходимо создать сервис. Здесь вы добавляете бизнес-логику приложения.
   - `schemas` - Здесь вы добавляете схемы для API. Схемы используются для валидации и сериализации/десериализации данных.
3. `api`: содержит маршрутизатор API, сюда вы добавляете конечные точки API.

### Дополнительно

Шаблон содержит множество функций, некоторые из которых используются в приложении, а некоторые нет. В следующих разделах функции подробно описаны.

#### Миграции

Миграциями занимается Alembic. Миграции хранятся в каталоге `migrations`. Чтобы создать новую миграцию, вы можете запустить следующую команду:

```bash
make generate-migration
```

Как только вы введете название новой миграции, в каталоге `migrations` будет создан новый файл миграции. Затем вы можете запустить миграцию, используя следующую команду:

```bash
make migrate
```

Если вам нужно понизить версию базы данных или сбросить ее. Вы можете использовать `makerollback` и `makereset-database` соответственно.

#### Аутентификация

Используемая аутентификация представляет собой базовую реализацию JWT с bearer-токеном. Когда в заголовке `Authorization` указан токен `bearer`, токен проверяется, и пользователь автоматически аутентифицируется, устанавливая `request.user.id` с помощью middleware. Чтобы использовать модель пользователя в эндпойнте, вы можете использовать зависимость get_current_user. Если для какого-либо эндпойнта вы хотите обеспечить аутентификацию, вы можете использовать зависимость AuthenticationRequired. Это вызовет `HTTPException`, если пользователь не аутентифицирован.

#### Контроль доступа

Шаблон содержит настраиваемый модуль управления разрешениями на уровне строк. Он создан на основе 
[fastapi-permissions](https://github.com/holgi/fastapi-permissions). Он находится в `core/security/access_control.py`. 
Вы можете использовать это для обеспечения различных разрешений для разных моделей. М
одуль работает на основе «Principals» и «permissions». У каждого пользователя есть свой собственный набор принципов,
которые необходимо установить с помощью функции. Проверьте `core/fastapi/dependents/permissions.py` для примера. 
Затем участники используются для проверки разрешений пользователя. Разрешения должны быть определены на уровне модели.
Проверьте `app/models/user.py` для примера. Затем вы можете использовать зависимость непосредственно в роутере, 
чтобы вызвать исключение HTTPException, если у пользователя нет необходимых разрешений. Ниже приведен неполный пример:

```python
from fastapi import APIRouter, Depends
from core.security.access_control import AccessControl, UserPrincipal, RolePrincipal, Allow
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    def __acl__(self):
        return [
            (Allow, UserPrincipal(self.id), "view"),
            (Allow, RolePrincipal("admin"), "delete"),
        ]

def get_user_principals(user: User = Depends(get_current_user)):
    return [UserPrincipal(user.id)]

Permission = AccessControl(get_user_principals)

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int, user: User = get_user(user_id), assert_access = Permission("view")):
    assert_access(user)
    return user

```

#### Кэширование

Вы можете напрямую использовать декоратор `Cache.cached` из `core.cache`. Пример

```python
from core.cache import Cache

@Cache.cached(prefix="user", ttl=60)
def get_user(user_id: int):
    ...
```

#### Celery

Celery-worker уже настроен для приложения. Вы можете добавить свои задачи в `worker/`. Для запуска, вы можете запустить следующую команду:

```bash
make celery-worker
```

#### Сессии

Сессии уже обрабатываются в middleware и зависимостью `get_session`, которая внедряется в репозитории посредством
внедрения зависимостей fastapi внутри класса `Factory` в файле `core/factory.py`. 
Также существует декоратор `Transactional`, который можно использовать для обертывания функций, 
которые необходимо выполнить в транзакции. Пример:

```python
@Transactional()
async def some_mutating_function():
    ...
```

Примечание. Декоратор уже обрабатывает фиксацию и откат транзакции. Вам не нужно делать это вручную.

Если в каком-либо случае вам нужны изолированные сеансы, вы можете использовать декоратор `standalone_session` из `core.database`. Пример:


```python
@standalone_session
async def do_something():
    ...
```

#### Паттерн "Репозиторий"

У каждой модели есть репозиторий, и все они наследуют базовый класс из `core/repository`. Репозитории расположены в
папке `app/repositories`. Репозитории внедряются в службы внутри класса `Factory` в `core/factory/factory.py`.

Базовый репозиторий содержит основные операции crud. Все операции клиента могут быть добавлены в конкретный репозиторий. Пример:

```python
from core.repository import BaseRepository
from app.models.user import User
from sqlalchemy.sql.expression import select

class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str):
        return await select(User).filter(User.email == email).gino.first()

```

Чтобы облегчить доступ к запросам со сложными соединениями, класс BaseRepository имеет функцию _`query` 
(наряду с другими удобными функциями, такими как `_all()` и `_one_or_none()`), которую можно очень легко 
использовать для написания сложных запросов. Пример:

```python
async def get_user_by_email_join_tasks(email: str):
    query = await self._query(join_)
    query = query.filter(User.email == email)
    return await self._one_or_none(query)
```

Примечание. Для каждого объединения, которое вы хотите создать, вам необходимо создать функцию в том же репозитории с шаблоном `_join_{name}`. Пример: `_join_tasks` для `tasks`. Пример:

```python
async def _join_tasks(self, query: Select) -> Select:
    return query.options(joinedload(User.tasks))
```

#### Сервисы

Подобно репозиториям, каждая логическая единица приложения имеет сервис. У сервиса также есть основной репозиторий, который в него внедряется. Службы расположены в папке «app/services».

Эти сервисы содержат всю бизнес-логику приложения. Изучите `app/services/auth.py` для примера.

#### Схемы

Схемы расположены в папке `app/schemas`. Схемы используются для проверки тела запроса и тела ответа. 
Схемы также используются для создания документации OpenAPI. Схемы наследуются от `BaseModel` от pydantic. 
Схемы в основном разделены на «requests» и «responses».

#### Форматтинг

Используйте команду `make format`, чтобы форматировать код с помощью `black` и `isort`.

#### Линтеры

Используйте команду `make lint`, чтобы проверить код с помощью `pylint`. В будущем планируется добавить линтеры `mypy` и `flake8`.
