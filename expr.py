import time


def main():
    c = 0
    for _ in range(10_000_000):
        c += 1


if __name__ == "__main__":
    st_time_time = time.time()
    st_time_perf = time.perf_counter()
    main()
    print(f"time.time = {time.time() - st_time_time}")
    print(f"time.perf_c = {time.perf_counter() - st_time_perf}")
