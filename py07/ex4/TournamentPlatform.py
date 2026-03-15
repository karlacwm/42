from ex4.TournamentCard import TournamentCard
from typing import Any


class TournamentPlatform:
    def __init__(self) -> None:
        self.cards: dict[str, TournamentCard] = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        self.cards[card.card_id] = card
        return card.card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict[str, Any]:
        card1 = self.cards[card1_id]
        card2 = self.cards[card2_id]

        winner = card1
        loser = card2
        if card2.attack_power > card1.attack_power:
            winner = card2
            loser = card1
        elif (card2.attack_power == card1.attack_power
              and card2.rating > card1.rating):
            winner = card2
            loser = card1

        winner.update_wins(1)
        loser.update_losses(1)
        self.matches_played += 1

        return {
            "winner": winner.card_id,
            "loser": loser.card_id,
            "winner_rating": winner.calculate_rating(),
            "loser_rating": loser.calculate_rating()
        }

    def get_leaderboard(self) -> list[dict[str, Any]]:
        board = []
        for i in self.cards:
            card = self.cards[i]
            board.append(
                {
                    "card_id": card.card_id,
                    "name": card.name,
                    "rating": card.rating,
                    "record": f"{card.wins}-{card.losses}"
                }
            )

        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i]["rating"] < board[j]["rating"]:
                    temp = board[i]
                    board[i] = board[j]
                    board[j] = temp
        return board

    def generate_tournament_report(self) -> dict[str, Any]:
        total_cards = len(self.cards)
        total_rating = 0
        for i in self.cards:
            total_rating += self.cards[i].rating

        avg_rating = 0
        if total_cards > 0:
            avg_rating = int(total_rating / total_cards)

        platform_status = "active" if self.matches_played > 0 else "inactive"

        return {
            "total_cards": total_cards,
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": platform_status
        }
