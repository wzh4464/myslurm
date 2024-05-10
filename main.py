import subprocess
import threading
from queue import Queue
from datetime import datetime


def task_worker():
    while True:
        task = task_queue.get()
        if task == "exit":
            task_queue.task_done()
            break
        # 为每个任务生成一个基于时间的文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"output_{timestamp}.txt"
        # 执行任务并将输出重定向到文件
        with open(filename, "w") as file:
            subprocess.run(task, shell=True, stdout=file, stderr=subprocess.STDOUT)
        task_queue.task_done()


def input_listener():
    while True:
        task_input = input("Enter a command to execute, or type 'exit' to quit: ")
        task_queue.put(task_input)
        if task_input == "exit":
            break


task_queue = Queue()

# 创建并启动任务执行线程
worker_thread = threading.Thread(target=task_worker)
worker_thread.daemon = True  # 设置为守护线程，使得主程序退出时线程也会退出
worker_thread.start()

# 在主线程中处理输入监听
input_listener()

# 等待所有任务完成
task_queue.join()
# 发送退出信号到任务执行线程
task_queue.put("exit")
# 等待任务执行线程结束
worker_thread.join()
