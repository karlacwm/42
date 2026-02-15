def get_score(player_data: dict) -> int:
    '''
    Returns the value of player's score from the player_data list.
    '''
    return player_data["score"]


def ft_analytics_dashboard() -> None:
    '''
    Transforms data by using list, dict and set comprehensions
    to filter and extract data for analysis.
    '''
    player_data: list[dict[str, str | int | bool | set[str]]] = [
        {"name": "alice", "score": 2300, "active": True, "region": "north",
         "achievements": {"level_10", "treasure_hunter", "boss_slayer",
                          "speed_demon", "perfectionist"}},
        {"name": "bob", "score": 1800, "active": True, "region": "east",
         "achievements": {"first_kill", "boss_slayer", "collector"}},
        {"name": "charlie", "score": 2150, "active": True, "region": "central",
         "achievements": {"treasure_hunter", "boss_slayer", "collector",
                          "speed_demon", "perfectionist", "level_10",
                          "first_kill"}},
        {"name": "diana", "score": 2050, "active": False, "region": "north",
         "achievements": {"treasure_hunter", "speed_demon", "perfectionist"}},
        {"name": "eva", "score": 1992, "active": False, "region": "east",
         "achievements": {"treasure_hunter", "speed_demon", "perfectionist",
                          "boss_slayer", "collector"}},
        {"name": "fred", "score": 653, "active": False, "region": "central",
         "achievements": {"collector", "perfectionist"}}
    ]
    print("=== Game Analytics Dashboard ===")
    print()
    print("=== List Comprehension Examples ===")
    high_scorers: list[str] = [
        p["name"] for p in player_data if p["score"] > 2000]
    score_doubled: list[int] = [p["score"] * 2 for p in player_data]
    active_players: list[str] = [
        p["name"] for p in player_data if p["active"]]
    print("High scorers (>2000):", high_scorers)
    print("Scores doubled:", score_doubled)
    print("Active players:", active_players)
    print()
    print("=== Dict Comprehension Examples ===")
    player_scores: dict[str, int] = {
        p["name"]: p["score"] for p in player_data if p["active"]}
    achievement_counts: dict[str, int] = {
        p["name"]: len(p["achievements"]) for p in player_data if p["active"]}
    score_categories: dict[str, int] = {
        "high": len([p for p in player_data if p["score"] >= 2000]),
        "medium": len([p for p in player_data if 800 <= p["score"] < 2000]),
        "low": len([p for p in player_data if p["score"] < 800])
    }
    print("Player scores:", player_scores)
    print("Score categories:", score_categories)
    print("Achievement counts:", achievement_counts)
    print()
    print("=== Set Comprehension Examples ===")
    unique_players: set[str] = {p["name"] for p in player_data}
    unique_achievements: set[str] = {
        a for p in player_data for a in p["achievements"]}
    active_regions: set[str] = {p["region"] for p in player_data}
    print("Unique players:", unique_players)
    print("Unique achievements:", unique_achievements)
    print("Active regions:", active_regions)
    print()
    print("=== Combined Analysis ===")
    total_players: int = len(player_data)
    total_score: int = sum(p["score"] for p in player_data)
    average_score: float = 0.0
    if total_players > 0:
        average_score = total_score / total_players
    sorted_players: list[dict[str, str | int | bool | set[str]]] = sorted(
        player_data, key=get_score, reverse=True)
    top_performer: dict[str, str | int | bool | set[str]] = sorted_players[0]
    print("Total players:", total_players)
    print("Total unique achievements:", len(unique_achievements))
    print(f"Average score: {average_score:.1f}")
    print("Top performer:", top_performer["name"],
          f"({top_performer['score']} points, "
          f"{len(top_performer['achievements'])} achievements)")


if __name__ == "__main__":
    ft_analytics_dashboard()
