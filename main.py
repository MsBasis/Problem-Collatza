from typing import List
from matplotlib import pyplot as plt
import time 
from concurrent.futures import ProcessPoolExecutor

def col(x: int) -> int:
    if x % 2 == 0:
        return int(x/2)
    else:
        return int(3*x+1)

def collatz(start: int) -> List[int]:
    threshold: int = 1000
    list: List[int] = [start]
    last: int = start
    iter:int = 0
    while last > 1 and iter < threshold:
        last = col(last)
        list.append(last)
        iter += 1

    return list

def szeregowo(_max: int, plot: bool = True) -> float:
    start: float = time.time()
    ad: List[List[int]] = []
    for i in range(1, _max, 1):
        ad.append(collatz(i+1))

    if plot:
        for i, x in enumerate(ad):
            plt.plot(x)

        plt.tight_layout()
        plt.yscale("log")
        plt.savefig("szeregowo.png")
        plt.clf()


    return time.time() - start

def rownolegle(_max: int, mx_workers: int = 10, plot: bool = True) -> float:
    start: float = time.time()
    ad: List[List[int]] = []
    with ProcessPoolExecutor(max_workers=mx_workers) as pe:
        ad.append(list(pe.map(collatz, list(range(1, _max, 1)), chunksize=100)))

    if plot:
        for x in ad[0]:
            plt.plot(x)

        plt.tight_layout()
        plt.yscale("log")
        plt.savefig("równolegle.png")
        plt.clf()

    return time.time() - start

print(szeregowo(100))
print(rownolegle(100))

szeregowo_times: List[float] = []
rownolegle_times: List[float] = []
times: List[int] = list(range(10, 100000, 1000))
for i in times:
    szeregowo_times.append(szeregowo(i, plot=False))
    rownolegle_times.append(rownolegle(i, plot=False))


plt.plot(times, szeregowo_times, label="Czasy obliczen szeregowych")
plt.plot(times, rownolegle_times, label="Czasy obliczen rownoleglych")
plt.tight_layout()
plt.yscale('log')
plt.legend()
plt.savefig("czasy1.png")
plt.show()

