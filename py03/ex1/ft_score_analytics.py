import sys


def ft_score_analytics() -> None:
    '''
    Takes scores from terminal input and calculates them for analysis.
    '''
    argv_count: int = len(sys.argv)
    print("=== Player Score Analytics ===")
    if argv_count < 2:
        print(f"No scores provided. Usage: python3 {sys.argv[0]}"
              "<score1> <score2> ...")
        return None
    scores: list[int] = []
    for arg in sys.argv[1:]:
        try:
            scores.append(int(arg))
        except ValueError:
            print("Scores must be numbers! This score will be skipped:", arg)
    if len(scores) < 1:
        print("Less than one valid score processed. Please try again.")
        return None
    total_players: int = len(scores)
    total_score: int = sum(scores)
    average_score: float = total_score / total_players
    max_score: int = max(scores)
    min_score: int = min(scores)
    range_score: int = max_score - min_score
    print("Scores processed:", scores)
    print("Total players:", total_players)
    print("Total score:", total_score)
    print("Average score:", average_score)
    print("High score:", max_score)
    print("Low score:", min_score)
    print("Score range:", range_score)


if __name__ == "__main__":
    ft_score_analytics()
