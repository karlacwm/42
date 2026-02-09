from typing import Any, Generator


def gen_events(n: int) -> Generator[int, Any, None]:
    for i in range(n):
        yield i


def fibonacci(n: int) -> Generator[int, Any, None]:
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b


def prime(n: int) -> Generator[int, Any, None]:
    num = 2
    count = 1
    while count <= n:
        divisor = 2
        if num == 2:
            yield num
            count += 1
            num += 1
        while num > divisor:
            if num % divisor == 0:
                break
            divisor += 1
        if num == divisor:
            yield num
            count += 1
        num += 1


def ft_data_stream() -> None:
    print("=== Game Data Stream Processor ===")
    print()
    total_events: int = 1000
    gen: Generator[int, Any, None] = gen_events(total_events)
    print("Processing", total_events, "game events...")
    print()
    print("=== Stream Analytics ===")
    print()
    print("=== Generator Demonstration ===")
    print("Fibonacci sequence (first 10):", *list(fibonacci(10)))
    print("Prime numbers (first 5):", *list(prime(5)))


if __name__ == "__main__":
    ft_data_stream()
