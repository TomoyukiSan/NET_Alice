from concurrent.futures import ProcessPoolExecutor
import time

class Worker:
    def __init__(self, value):
        self.value = value

    def compute(self):
        # 例: 値の2乗を計算
        time.sleep(1)
        print("aaa")
        return self.value ** 2

class Manager:

    def process_worker(self, worker):
        """Workerのcomputeメソッドを呼び出すためのヘルパー関数"""
        return worker.compute()

    def process_workers(self):

        self.workers = [Worker(i) for i in range(10)]  # Workerのインスタンスを生成

        with ProcessPoolExecutor() as executor:
            # 各Workerのcomputeメソッドを並列で呼び出す
            results = list(executor.map(self.process_worker, self.workers))
        return results


if __name__ == '__main__':
    # Managerクラスのインスタンスを生成して処理を開始
    manager = Manager()
    results = manager.process_workers()

    # 結果を表示
    for result in results:
        print(result)