def achievement_tracker() -> None:
    '''
    Shows details of players' achievements and compares them among players.
    '''
    alice: set[str] = {"first_kill", "level_10", "treasure_hunter",
                       "speed_demon"}
    bob: set[str] = {"first_kill", "level_10", "boss_slayer", "collector"}
    charlie: set[str] = {"level_10", "treasure_hunter", "boss_slayer",
                         "speed_demon", "perfectionist"}
    unique_achievements: set[str] = alice.union(bob, charlie)
    total_unique_achievements: int = len(unique_achievements)
    common_achievements: set[str] = alice.intersection(bob, charlie)
    rare_achievements: set[str] = (
        alice.difference(bob.union(charlie)).union(
            bob.difference(alice.union(charlie))).union(
                charlie.difference(bob.union(alice))))
    alice_bob_common: set[str] = alice.intersection(bob)
    alice_unique: set[str] = alice.difference(bob)
    bob_unique: set[str] = bob.difference(alice)
    print("=== Achievement Tracker System ===")
    print()
    print("Player alice achievements:", alice)
    print("Player bob achievements:", bob)
    print("Player charlie achievements:", charlie)
    print()
    print("=== Achievement Analytics ===")
    print("All unique achievements:", unique_achievements)
    print("Total unique achievements:", total_unique_achievements)
    print()
    print("Common to all players:", common_achievements)
    print("Rare achievements (1 player):", rare_achievements)
    print()
    print("Alice vs Bob common:", alice_bob_common)
    print("Alice unique:", alice_unique)
    print("Bob unique:", bob_unique)


if __name__ == "__main__":
    achievement_tracker()
