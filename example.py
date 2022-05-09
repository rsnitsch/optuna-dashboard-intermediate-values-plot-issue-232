import argparse
import os
import random
import subprocess
import sys
import time

import optuna


def objective(trial: optuna.trial.Trial) -> float:
    value = None
    steps = 50
    for step in range(steps):
        time.sleep(random.randrange(50, 300) / 1000)
        value = 1 + abs(step - steps / 2)**2 * trial.number / 2
        trial.report(value, step)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, default=None)
    args = parser.parse_args()

    storage = "postgresql://postgres:example@localhost:5555/postgres"
    if not args.worker:
        random.seed(0)

        # Sequential study.
        study_sequential = optuna.create_study(storage=storage,
                                               study_name="sequential")
        print("Executing trials for sequential study...")
        for i in range(5):
            study_sequential.optimize(objective, n_trials=1)

        # Parallel study.
        optuna.create_study(storage=storage, study_name="parallel")
        print("Spawning parallel study workers in the background...")
        workers = []
        for i in range(5):
            p = subprocess.Popen(
                [sys.executable, "example.py", "--worker",
                 str(i + 1)],
                env=os.environ)
            workers.append(p)

        # Wait for parallel study to finish.
        print("Waiting for parallel workers to finish...")
        for w in workers:
            w.wait()

        print("To open dashboard: optuna-dashboard %s" % storage)
    else:
        random.seed(args.worker)
        study_parallel = optuna.load_study(storage=storage,
                                           study_name="parallel")
        study_parallel.optimize(objective, n_trials=1)


if __name__ == '__main__':
    main()
