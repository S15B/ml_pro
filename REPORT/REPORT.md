docker run --rm -p 8000:8000 cost-service:1.0

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
