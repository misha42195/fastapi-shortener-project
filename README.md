# FastAPI URL Shortener

# Develop

Setup:

Right click `url-shortener` -> Mark directory as -> Sources Root

### Run

Go to workdir:

```shell
cd url_shortener
```

Run dev server:

```shell
fastapi dev
```

Возвращает приветственное сообщение и ссылку на документацию OpenAPI.
**Параметры запроса**

-`name` (опционально, строка): имя для приветствия. По умолчанию - `World`.

**Пример запроса**

```shell
GET/?name=Mish
```

**Пример ответа**

{
"message": "Hello Misha",
"docs_path": "http://localhost:8000/docs"}
}


### Snippets
```shell
python -c 'import secrets; print(secrets.token_urlsafe(20))'
```
