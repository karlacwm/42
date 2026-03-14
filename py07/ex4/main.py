from ex4 import TournamentCard, TournamentPlatform


def main() -> None:
	print("=== DataDeck Tournament Platform ===")

	platform = TournamentPlatform()

	dragon = TournamentCard(
		card_id="dragon_001",
		name="Fire Dragon",
		cost=7,
		rarity="Legendary",
		attack_power=8,
		health=10,
		rating=1200,
	)
	wizard = TournamentCard(
		card_id="wizard_001",
		name="Ice Wizard",
		cost=6,
		rarity="Epic",
		attack_power=6,
		health=9,
		rating=1150,
	)

	print("Registering Tournament Cards...")
	dragon_id = platform.register_card(dragon)
	wizard_id = platform.register_card(wizard)

	print(f"{dragon.name} (ID: {dragon_id}):")
	print("- Interfaces: [Card, Combatable, Rankable]")
	print(f"- Rating: {dragon.calculate_rating()}")
	print(f"- Record: {dragon.wins}-{dragon.losses}")

	print(f"{wizard.name} (ID: {wizard_id}):")
	print("- Interfaces: [Card, Combatable, Rankable]")
	print(f"- Rating: {wizard.calculate_rating()}")
	print(f"- Record: {wizard.wins}-{wizard.losses}")

	print("Creating tournament match...")
	result = platform.create_match(dragon_id, wizard_id)
	print(f"Match result: {result}")

	print("Tournament Leaderboard:")
	leaderboard = platform.get_leaderboard()
	place = 1
	for entry in leaderboard:
		print(f"{place}. {entry['name']}")
		print(f"- Rating: {entry['rating']} ({entry['record']})")
		place += 1

	report = platform.generate_tournament_report()
	print(f"Platform Report: {report}")
	print("=== Tournament Platform Successfully Deployed! ===")
	print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
	main()


# 1. How does multiple inheritance allow a class to implement several 
# interfaces?

# "Python allows a class definition to accept a comma-separated list 
# of parent classes (e.g., class TournamentCard(Card, Combatable, Rankable)). 
# The child class simply inherits the requirements of all the parents. If any 
# abstract method from any of those parents is missing, Python's ABC module
#  prevents the object from being created."

# 2. What are the benefits of combining ranking capabilities with 
# card game mechanics?

# "It creates a complete, self-contained ecosystem! By composing interfaces,
#  my TournamentPlatform doesn't need to know how a card attacks or how much
#   mana it costs. It only cares about the Rankable interface. This heavily 
#   decouples the code, making the system incredibly robust, scalable, 
#   and easy to test."