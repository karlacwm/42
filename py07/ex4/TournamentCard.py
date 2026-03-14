from typing import Any

from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
	def __init__(
		self,
		card_id: str,
		name: str,
		cost: int,
		rarity: str,
		attack_power: int,
		health: int,
		rating: int,
	) -> None:
		super().__init__(name, cost, rarity)
		self.card_id = card_id
		self.type = "Tournament"
		self.attack_power = attack_power
		self.health = health
		self.wins = 0
		self.losses = 0
		self.rating = rating

	def play(self, game_state: dict) -> dict:
		return {
			"card_played": self.name,
			"mana_used": self.cost,
			"effect": "Tournament card enters competitive play",
		}

	def attack(self, target) -> dict:
		return {
			"attacker": self.name,
			"target": target,
			"damage": self.attack_power,
		}

	def defend(self, incoming_damage: int) -> dict:
		self.health -= incoming_damage
		if self.health < 0:
			self.health = 0
		return {
			"defender": self.name,
			"damage_taken": incoming_damage,
			"remaining_health": self.health,
		}

	def calculate_rating(self) -> int:
		return self.rating

	def get_combat_stats(self) -> dict:
		return {
			"attack": self.attack_power,
			"health": self.health,
		}

	def update_wins(self, wins: int) -> None:
		self.wins += wins
		self.rating += 16 * wins

	def update_losses(self, losses: int) -> None:
		self.losses += losses
		self.rating -= 16 * losses

	def get_rank_info(self) -> dict:
		return {
			"rating": self.rating,
			"wins": self.wins,
			"losses": self.losses,
			"record": f"{self.wins}-{self.losses}",
		}

	def get_tournament_stats(self) -> dict:
		return {
			"card_id": self.card_id,
			"name": self.name,
			"rating": self.rating,
			"wins": self.wins,
			"losses": self.losses,
			"record": f"{self.wins}-{self.losses}",
			"attack": self.attack_power,
		}