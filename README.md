# Churn MLOps

Сквозной проекта курса по [MLOps](https://github.com/alsu124/mlops-deploy-course)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
make install
make check                         # должно напечатать environment: OK
make data                          # сгенерирует data/raw/churn.csv
```

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
