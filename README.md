# FastAPI URL Shortener

# Develop

Setup:

Right click `url-shortener` -> Mark directory as -> Sources Root

### Install dependencies

```shell
uv add sync
```

### Install all packages

### Run dev server:

### Run

Go to workdir:

```shell
cd url_shortener
```

```shell
fastapi dev
```

Возвращает приветственное сообщение и ссылку на документацию OpenAPI.
**Параметры запроса**

-`name` (опционально, строка): имя для приветствия. По умолчанию - `World`.

**Пример запроса**

**Пример ответа**

{
"message": "Hello Misha",
"docs_path": "http://localhost:8000/docs"}
}

### Snippets

```shell
# python -c "import secrets; print(secrets.token_urlsafe(20))"
```
