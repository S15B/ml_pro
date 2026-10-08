## Подготовка

Модель artifact/cost_model.joblib хранится с Git LFS.
Перед клонированием нужно установить Git LFS:
git lfs install

Если модель не скачалась автоматически:
git lfs pull

## Тесты:
uv run pytest

## Сборка docker
docker compose up -d --build

## Запуск nodes
kind create cluster --name mlpro  
kind load docker-image cost-service:1.0 --name mlpro


Сервис

![alt text](image-1.png)

Логи в Postgres

![alt text](image-2.png)

Тесты

![alt text](image.png)

Pods

![alt text](image-3.png)

Проблемы с которыми столкнулся:
При None pandas создавал столбцы фич mortgage_rate и usd_rate с типом object, который мой XGBoost не принимал. Привел тип к float, пропуски теперь NaN
Pods не запускается. Возможно что то не то делаю. Буду разбираться дальше. У меня почему то не ready они. Что говорят логи? Я так и не понял что говорят
