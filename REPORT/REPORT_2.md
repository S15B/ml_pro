2.1
https://github.com/S15B/ml_pro/actions/runs/38512193992
https://github.com/S15B/ml_pro/pkgs/container/cost-services/1382959005?tag=sha-50755d36b91eb24e02bd34fa426795ed5dc90ada

2.2 
https://github.com/S15B/ml_pro/pull/1

2.3 
err: https://github.com/S15B/ml_pro/actions/runs/38514810482/job/115691616968
fix: https://github.com/S15B/ml_pro/actions/runs/38515967667/job/115694724417
log: FileNotFoundError: [Errno 2] No such file or directory: 'artifact/model.joblib' 
пишет что нет такого файла значит неправильное имя

err: https://github.com/S15B/ml_pro/actions/runs/38517265753/job/115698759267
fix: https://github.com/S15B/ml_pro/actions/runs/38517901855/job/115701092521
log: Environment Variables from:
      cost-config  ConfigMap  Optional: false
      cost-secs    Secret     Optional: false
видно что Secret не тот требует, должен cost-secrets

err: https://github.com/S15B/ml_pro/actions/runs/38518514399/job/115703027504
fix: https://github.com/S15B/ml_pro/actions/runs/38519083835/job/115704767892
log:  cost-service-677f89475c-b9hjj   0/1     Pending   0          2m     <none>       <none>             <none>           <none>
cost-service-677f89475c-xn2pg   0/1     Pending   0          2m     <none>       <none>             <none>           <none>
cost-service-868b594c56-chrvb   0/1     Pending   0          2m     <none>       <none>             <none>           <none>
postgres-5d46f959f5-sspmq       1/1     Running   0          2m7s   10.244.0.5   ci-control-plane   <none>           <none>
Возможно из за того что узлы не назначены можно вычислить проблему в памяти


1. 109 сек самый первый и 24 сек следующий build
#15 [stage-0 5/8] RUN uv sync --no-dev --no-install-project
#15 CACHED
потому что зависимости и предыдущие слои не изменились
2. Ошибка была у промежуточных Pod, сначала Pod создавались с другим образом, а после загрузились с нужным
3. GitHub Secret - переменная в workflow - Kubernets Secret - в контейнере. 
Если просто в файл записать, его увидят все в GitHub
4. Ну так тесты и нужно чтобы проверить ничего ли не сломали в коде
5. Строка if: github.ref == 'refs/heads/main'
Было бы удобно везде прогонять тесты, главное защитить прод. Код может быть в промежуточном состоянии, но должен быть сохранен, например, в конце рабочего дня
6. Блокировка нужна на время первоначального создания таблицы, они будут действовать по очереди. Иначе попытаются создать одну и ту же таблицу. Реплики это два приложения Api.
7. Невозможность создать Pod (Pending) - ошибка подготовки контейнера (CreateContainerConfigError) - падение запущенного контейнера (FileNotFoundError)