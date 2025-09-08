from multiprocessing import Process
import time

def cpu_task():
    count = 0
    for i in range(10**7):
        count +=1

if __name__=="__main__":

    # Run with processes
    start = time.time()
    processes = [Process(target=cpu_task) for _ in range(8)]
    for p in processes: p.start()
    for p in processes: p.join()
    end = time.time()

    print("Processes time:", end-start)