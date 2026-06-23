from pipeline import run_pipeline
from config import (
    TRAIN_START, TRAIN_END,
    TEST_START, TEST_END
)

strategies = ["Equal Weight", "Top Decile", "Long Short"]

for strat in strategies:

    print("\n===================================")
    print("STRATEGY:", strat)
    print("===================================")

    # TRAIN PERIOD
    train_ret, train_eq, train_metrics = run_pipeline(
        TRAIN_START, TRAIN_END, strat
    )

    # TEST PERIOD
    test_ret, test_eq, test_metrics = run_pipeline(
        TEST_START, TEST_END, strat
    )

    print("\n--- TRAIN METRICS ---")
    for k, v in train_metrics.items():
        print(f"{k}: {v}")

    print("\n--- TEST METRICS ---")
    for k, v in test_metrics.items():
        print(f"{k}: {v}")