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
