"""Стадия evaluate: оценка модели на отложенном тесте и порог качества.

Тест трогается только здесь, один раз, скриптом. Валидацию смотрят при подборе
параметров и незаметно подгоняют модель под неё, поэтому оценка на тесте —
отдельная стадия, а не строчка в конце train.py.

Код возврата 1, если ROC-AUC ниже evaluate.min_roc_auc: на занятии 9 эту
команду запускает CI, и падение по метрике не пускает изменение в main.

Запуск: python -m src.evaluate
"""

from __future__ import annotations

import json
import sys

import joblib
import pandas as pd
from sklearn.metrics import auc, f1_score, precision_recall_curve, roc_auc_score

from src.config import TARGET, feature_columns, load_params, resolve
from src.logging_setup import setup_logging

log = setup_logging()


def main() -> None:
    params = load_params()
    e = params["evaluate"]

    # 1. Модель и тестовая выборка
    model_path = resolve("models/model.joblib")
    log.info(f"Загружаю модель из {model_path}")
    pipe = joblib.load(model_path)

    test_df = pd.read_csv(resolve(params["data"]["processed_dir"]) / "test.csv")
    log.info(f"test : {len(test_df)} строк, {(test_df[TARGET] == 1).mean():.1%} оттока")

    X_test = test_df[feature_columns(params)]
    y_test = test_df[TARGET]

    # 2. Метрики: порог для F1 берётся из конфига, а не неявные 0.5 из predict()
    proba = pipe.predict_proba(X_test)[:, 1]
    y_pred = (proba >= e["threshold"]).astype(int)

    precision, recall, _ = precision_recall_curve(y_test, proba)
    metrics = {
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "pr_auc": float(auc(recall, precision)),
        "f1": float(f1_score(y_test, y_pred)),
        "threshold": float(e["threshold"]),
    }

    log.info(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    log.info(f"PR-AUC:  {metrics['pr_auc']:.4f}")
    log.info(f"F1:      {metrics['f1']:.4f} (порог {metrics['threshold']})")

    # 3. Метрики пишем до проверки порога: при падении отчёт тоже нужен
    metrics_path = resolve("reports/eval_metrics.json")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")
    log.info(f"Метрики сохранены в {metrics_path}")

    # 4. Порог качества
    gate = e["min_roc_auc"]
    if metrics["roc_auc"] < gate:
        log.error("ROC-AUC %.4f ниже порога %.4f", metrics["roc_auc"], gate)
        sys.exit(1)

    log.info(f"✅ ROC-AUC {metrics['roc_auc']:.4f} не ниже порога {gate}")


if __name__ == "__main__":
    main()
