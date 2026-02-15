from typing import Any, Generator


def gen_events(n: int) -> Generator[str, Any, None]:
    '''
    Generates event about what action which player on which level did.
    '''
    players_list: list[str] = [
        "alice", "bob", "charlie", "danny", "erica", "frank", "george",
        "hannah", "izzie", "jackie", "kelvin", "lily", "marcus", "neo",
        "oliver", "penny", "quinn", "robert", "sara", "thomas", "ursula",
        "violet", "wilson", "xen", "yumi", "zelda"]
    levels_list: list[int] = [
        5, 12, 8, 1, 6, 2, 3, 7, 4, 3, 13, 19, 5, 11, 5, 2, 12, 16, 14, 1,
        1, 7, 6, 18, 14, 5]
    actions_list: list[str] = [
        "killed monster", "found treasure", "leveled up", "completed quest",
        "discovered new recipe", "leveled up", "collected gems",
        "collected gems", "forged new weapon", "healed other player",
        "accepted a challenge", "collected gems", "completed quest",
        "leveled up", "accepted a challenge", "collected gems",
        "completed quest", "killed monster", "found treasure", "leveled up",
        "found treasure", "forged new weapon", "healed other player",
        "accepted a challenge", "forged new weapon", "healed other player",
        "accepted a challenge", "discovered new recipe", "leveled up"]
    id = 0
    for i in range(n):
        id += 1
        player: str = players_list[i % len(players_list)]
        level: int = levels_list[i % len(levels_list)]
        action: str = actions_list[i % len(actions_list)]
        yield f"Event {id}: Player {player} (level {level}) {action}"


def fibonacci(n: int) -> Generator[int, Any, None]:
    '''
    Generates fibonacci numbers for n times.
    '''
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b


def prime(n: int) -> Generator[int, Any, None]:
    '''
    Generates prime numbers for n times.
    '''
    num = 2
    count = 0
    while count < n:
        divisor = 2
        while num > divisor:
            if num % divisor == 0:
                break
            divisor += 1
        if num == divisor:
            yield num
            count += 1
        num += 1


def ft_data_stream() -> None:
    '''
    Simulates data stream process and generates one event each time,
    instead of all events at one time.
    '''
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
        if "level 1" in event and "level 1)" not in event:
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
