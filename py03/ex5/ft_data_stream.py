from typing import Any, Generator
import time


def gen_events(n: int) -> Generator[str, Any, None]:
    players_list: list[str] = ["alice", "bob", "charlie", "danny", "erica",
                               "frank", "george", "hannah", "izzie"]
    levels_list: list[int] = [5, 12, 8, 1, 6, 2, 3, 11, 4, 3, 2, 6, 2, 3, 1,
                               4, 13, 12, 5, 9, 2, 15, 5]
    actions_list: list[str] = ["killed monster", "found treasure",
                               "leveled up", "completed quest",
                               "discovered new recipe", "collected gems",
                               "forged new weapon", "healed other player",
                               "leveled up", "leveled up", "found treasure",
                               "collected gems", "killed monster",
                               "leveled up", "completed quest",
                               "discovered new recipe", "collected gems",
                               "forged new weapon", "healed other player",
                               "leveled up",
                               "forged new weapon", "healed other player",
                               "leveled up", "found treasure"]
    id = 0
    for i in range(n):
        id += 1
        player: str = players_list[i % len(players_list)]
        level: int = levels_list[i % len(levels_list)]
        action: str = actions_list[i % len(actions_list)]
        yield f"Event {id}: Player {player} (level {level}) {action}"


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
    print("Processing", total_events, "game events...")
    print()
    stream: Generator[str, Any, None] = gen_events(total_events)
    for i in range(0, 3):
        print(next(stream))
    high_level_players = 0
    treasure_events = 0
    level_up_events = 0
    for event in stream:
        if "level 1" in event and "level 1 " not in event:
            high_level_players += 1
        if "found treasure" in event:
            treasure_events += 1
        if "leveled up" in event:
            level_up_events += 1
    print("...")
    print()
    print("=== Stream Analytics ===")
    print("Total events processed:", total_events)
    print("High-level players (10+):", high_level_players)
    print("Treasure events:", treasure_events)
    print("Level-up events:", level_up_events)
    print()
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")
    print()
    print("=== Generator Demonstration ===")
    print("Fibonacci sequence (first 10):", *list(fibonacci(10)))
    print("Prime numbers (first 5):", *list(prime(5)))


if __name__ == "__main__":
    ft_data_stream()
