from pathlib import Path


# /home/misha/PycharmProjects/fastapi-url-shortener/url-shortener/json_file/conf.py

BaseDir = Path(__file__).resolve().parent  # получаем путь до папки с файлом movie.json
PATH_TO_MOVIE_FILE = (
    BaseDir / "movies_data.json"
)  # полный путь до файла для записи данных
