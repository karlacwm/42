from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
	def __init__(self) -> None:
		self.cards: dict[str, TournamentCard] = {}
		self.matches_played = 0

	def register_card(self, card: TournamentCard) -> str:
		self.cards[card.card_id] = card
		return card.card_id

	def create_match(self, card1_id: str, card2_id: str) -> dict:
		card1 = self.cards[card1_id]
		card2 = self.cards[card2_id]

		winner = card1
		loser = card2
		if card2.attack_power > card1.attack_power:
			winner = card2
			loser = card1
		elif card2.attack_power == card1.attack_power and card2.rating > card1.rating:
			winner = card2
			loser = card1

		winner.update_wins(1)
		loser.update_losses(1)
		self.matches_played += 1

		return {
			"winner": winner.card_id,
			"loser": loser.card_id,
			"winner_rating": winner.calculate_rating(),
			"loser_rating": loser.calculate_rating(),
		}

	def get_leaderboard(self) -> list:
		board = []
		for card_id in self.cards:
			card = self.cards[card_id]
			board.append(
				{
					"card_id": card.card_id,
					"name": card.name,
					"rating": card.rating,
					"record": f"{card.wins}-{card.losses}",
				}
			)

		for index in range(len(board)):
			for second_index in range(index + 1, len(board)):
				if board[index]["rating"] < board[second_index]["rating"]:
					temp = board[index]
					board[index] = board[second_index]
					board[second_index] = temp

		return board

	def generate_tournament_report(self) -> dict:
		total_cards = len(self.cards)
		total_rating = 0
		for card_id in self.cards:
			total_rating += self.cards[card_id].rating

		avg_rating = 0
		if total_cards > 0:
			avg_rating = int(total_rating / total_cards)

		return {
			"total_cards": total_cards,
			"matches_played": self.matches_played,
			"avg_rating": avg_rating,
			"platform_status": "active",
		}