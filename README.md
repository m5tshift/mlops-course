# Churn MLOps

Сквозной проект курса по [MLOps](https://github.com/alsu124/mlops-deploy-course):
предсказание оттока клиентов телеком-оператора по табличным данным.
Задача бинарной классификации — определить, уйдёт ли клиент.
Для обучения используется синтетический датасет с фиксированным seed.

## Как запустить

Нужны Python 3.11 и Make. Команды ниже предназначены для macOS/Linux.

```bash
git clone https://github.com/m5tshift/mlops-course.git
cd mlops-course
python3.11 -m venv .venv
source .venv/bin/activate
make install
make check                         # проверка окружения
make data                          # генерация data/raw/churn.csv
make prepare                       # подготовка train/val/test
make train                         # обучение и расчёт метрик
```

Для Windows см. [настройку окружения по ОС](https://github.com/alsu124/mlops-deploy-course/blob/main/SETUP_BY_OS.md).

Модель сохраняется в `models/model.joblib`, метрики — в
`reports/train_metrics.json`. Алгоритм выбирается через `train.model` в
[params.yaml](params.yaml): `logreg`, `random_forest` или `gradient_boosting`.
После изменения параметров повторите `make train`.

## Данные

Сырые данные и модель версионируются в [DVC](https://dvc.org). В Git лежат только указатели
`data/raw/churn.csv.dvc` и `models/model.joblib.dvc` с хешами, сами файлы — в remote.
Описание полей и известных дефектов — в [паспорте датасета](data/README.md).

Remote по умолчанию — `minio`: бакет `s3://mlops/churn` в MinIO на `http://localhost:9000`.
Ключи доступа в Git не хранятся, они задаются в `.dvc/config.local`.

Как получить данные:

```bash
docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin \
  cgr.dev/chainguard/minio server /data --console-address ":9001"   # после перезагрузки: docker start minio
# в консоли http://localhost:9001 (minioadmin / minioadmin) создать бакет mlops
dvc remote modify --local minio url s3://mlops/churn
dvc remote modify --local minio endpointurl http://localhost:9000
dvc remote modify --local minio access_key_id minioadmin
dvc remote modify --local minio secret_access_key minioadmin
dvc pull
```

MinIO запускается локально, поэтому на новой машине бакет пуст и `dvc pull` ничего не скачает.
В этом случае данные можно сгенерировать заново: `make data` с тем же seed даёт побайтово тот же
`churn.csv`, его хеш совпадает с `.dvc`-файлом. Дальше `make prepare && make train`.

После изменения данных или модели: `dvc add <файл>`, коммит `.dvc`-файла, `dvc push`.

### Почему `.dvc`-файл коммитится, а датасет — нет

`.dvc`-файл — маленький текстовый указатель: хеш и размер данных. В Git он связывает коммит кода
с конкретной версией данных: `git checkout` + `dvc checkout` возвращают их вместе. Сам датасет
большой и бинарный, Git хранит каждую его версию целиком и навсегда раздувает историю,
а сравнивать такие файлы построчно бессмысленно.

Если сделать наоборот, сломается всё: без `.dvc`-файла в Git DVC не знает, какую версию данных
скачать для коммита, и откат кода больше не возвращает данные. Датасет в Git раздувает
репозиторий, упирается в лимиты GitHub на размер файлов и дублирует хранилище DVC.

## Что сделано

- Реализованы подготовка данных, заполнение пропусков и стратифицированное разбиение на train/val/test.
- Собран Pipeline с обработкой числовых и категориальных признаков и обучением выбранной модели.
- Сравнены три алгоритма; результаты и разбор F1 записаны в [отчёте об экспериментах](reports/EXPERIMENTS.md).
- Настроены pre-commit и Ruff для автоматической проверки и форматирования кода.
- Изменения оформляются через ветки и Pull Request; добавлен `.env.example`, данные и модели исключены из Git.

## Правила проекта

1. **Никаких абсолютных путей.** Только `src.config.resolve()`.
2. **Никаких магических чисел в коде.** Всё числовое — в `params.yaml`.
3. **Данные и модели не коммитятся в Git.** С занятия 4 — в DVC.
4. **Секреты — только через переменные окружения.** `.env` уже в `.gitignore`.
5. **Работа идёт через ветки и Pull Request.** С занятия 2.

## План и материалы курса

Все ссылки ведут в репозиторий преподавателя.

### План и задания

- [Тематический план](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/syllabus.md) — темы и ожидаемые результаты всех 18 занятий.
- [Дорожная карта](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/course-roadmap.md) — работа на занятиях, домашние задания и этапы проекта.
- [Методички занятий](https://github.com/alsu124/mlops-deploy-course/tree/main/lessons) — пошаговые задания и чек-листы в файлах `handout.md`.
- [Конспекты теории](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/theory/README.md) — что читать перед практикой.

### Работа над проектом

- [Памятка студента](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/student-guide.md) — организация работы и правила курса.
- [Быстрый старт](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/quick-start.md) — структура проекта и основные команды.
- [Настройка окружения по ОС](https://github.com/alsu124/mlops-deploy-course/blob/main/SETUP_BY_OS.md) — установка инструментов на macOS, Windows и Linux.
- [Руководство по Git](https://github.com/alsu124/mlops-deploy-course/blob/main/STUDENT_GIT_GUIDE.md) — ветки, PR и ревью.
- [Шпаргалка Git](https://github.com/alsu124/mlops-deploy-course/blob/main/GIT_CHEATSHEET.md) — команды для повседневной работы.
- [Решение типичных проблем](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/troubleshooting-guide.md) — помощь при ошибках.

### Сдача и защита

- [Как сдавать проект](https://github.com/alsu124/mlops-deploy-course/blob/main/HOW_TO_SUBMIT_LABS.md) — порядок сдачи и итоговой защиты.
- [Критерии оценки](https://github.com/alsu124/mlops-deploy-course/blob/main/docs/assessment.md) — требования к зачёту и чек-лист защиты.
