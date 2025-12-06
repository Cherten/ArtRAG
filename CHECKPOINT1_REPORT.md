# Чекпоинт 1 — Сбор данных

## Процесс получения данных
- Источник: `legacy-datasets/wikipedia` (дамп `20220301.en`) на Hugging Face, открытый доступ.
- Отбор: фильтр по ключевым словам об искусстве (`painting`, `painter`, `art`, `sculpture`, `museum`, `gallery`).
- Скрипт: `python scripts/fetch_wikipedia_art_sample.py`  
  - Загружает небольшой срез (`train[:0.02%]` по умолчанию).  
  - Применяет фильтр, сохраняет сырые статьи в `data/raw/wikipedia_art_sample.jsonl`.  
  - Делит тексты на чанки ~400–500 символов и сохраняет в `data/processed/chunks_sample.jsonl`.

## Структура данных и хранение
- Хранилище: локальная папка `data/`.
- Сырые данные: `data/raw/wikipedia_art_sample.jsonl`, формат JSONL, поля `id`, `title`, `source_url`, `text`.
- Чанки: `data/processed/chunks_sample.jsonl`, формат JSONL, поля `doc_id`, `chunk_id`, `content`, `source_url`.

## Ссылка на сэмпл
- Папка с собранными файлами: `data/` (см. `raw/` и `processed/`).

## Текущее состояние подготовки для RAG
- Чанкинг выполнен, структура JSONL готова к индексации (Faiss/LangChain).
- Доступны поля `source_url` и `title` для метаданных в индексе.
- Следующий шаг: добавить расчёт эмбеддингов и сохранить индекс в `data/index/`.