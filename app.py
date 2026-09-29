import random


characters = [
	{
		"name": "Mira Vale",
		"appearance": "Short black hair, mismatched boots, and a threadbare blue coat covered in odd stitched symbols",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Jonas Reed",
		"appearance": "Tall and broad-shouldered, with a tangled brown beard, soot-stained clothes, and one oversized glove",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Elara Finch",
		"appearance": "Wild curly red hair, mismatched round glasses, and a coat patched with scraps of curtain fabric",
		"order": "",
		"anomaly": True, 
    
	},
	{
		"name": "Theo Marsh",
		"appearance": "Thin and pale, wearing a stained yellow raincoat, three different socks, and a hat made from newspaper",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Sana Okafor",
		"appearance": "Dark braided hair, tired brown eyes, a frayed scarf, and a silver necklace made from bent spoons",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Bram Hollow",
		"appearance": "Large build, shaved head, a scar over his eyebrow, and battered armor held together with rope",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Lydia Snow",
		"appearance": "Wild white hair, bright blue eyes, and an elegant purple dress repaired with colorful cloth scraps",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Kai Mercer",
		"appearance": "Messy blond hair, athletic build, worn sneakers, and a backpack patched with old maps",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Nora Bell",
		"appearance": "Medium height, warm smile, flour-dusted hair, and a green apron with pockets full of strange keys",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Orin Glass",
		"appearance": "Silver hair, narrow eyes, a black travel cloak with singed edges, and boots tied with wire",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Tessa Wright",
		"appearance": "Dark skin, shoulder-length curls, a patched green jacket, and sturdy work boots covered in dried mud",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Felix Crow",
		"appearance": "Lean figure, oversized dark hood, crooked grin, and a coat lined with mismatched pockets",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Amara Stone",
		"appearance": "Muscular, with tangled long brown hair, a faded red scarf, and a coat patched with canvas bags",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Pavel North",
		"appearance": "Older man with a white mustache, a lopsided wool hat, and a raincoat repaired with fishing line",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Ivy Hart",
		"appearance": "Petite, with uneven violet hair, bright yellow boots, and a coat decorated with bottle caps",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Ronan Pike",
		"appearance": "Tanned skin, short dark hair, a salt-stained patched vest, and trousers held up with knotted rope",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Mei Rowan",
		"appearance": "Long black hair, calm eyes, and a cream-colored robe patched with mismatched blankets",
		"order": "",
		"anomaly": False,
	},
	{
		"name": "Gideon Frost",
		"appearance": "Very tall, with gray eyes, a heavy winter coat, and snow goggles hanging from a frayed string",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Zara Bloom",
		"appearance": "Curly brown hair, colorful mismatched earrings, paint-stained hands, and a coat splashed with impossible colors",
		"order": "",
		"anomaly": True,
	},
	{
		"name": "Silas Quill",
		"appearance": "Thin and bespectacled, with a neatly trimmed mustache, a frayed cardigan, and shoes wrapped in cloth",
		"order": "",
		"anomaly": False,
	},
]


def calculate_points(character, action):
	if action == "maken":
		return -10 if character["anomaly"] else 5
	return 3 if character["anomaly"] else -5


def print_random_character():
	character = random.choice(characters)
	print(f"Name: {character['name']}")
	print(f"Appearance: {character['appearance']}")


	wants_order = input("Wil je hun order weten? Typ 'ja' of 'nee': ")
	if wants_order.strip().lower() in ("ja", "order"):
		order = character["order"] or "Geen order toegewezen"
		print(f"Order: {order}")
		action = input("Wil je de order maken of het personage wegsturen? ")
		action = action.strip().lower()
		if action not in ("maken", "wegsturen"):
			action = "wegsturen"
	else:
		print("Je wilt de order niet. Het personage wordt weggestuurd.")
		action = "wegsturen"

	points = calculate_points(character, action)
	if action == "maken":
		print("De order wordt gemaakt.")
	else:
		print("Het personage wordt weggestuurd.")
	print(f"Punten: {points:+d}")
	return points


def play_game():
	total_points = 0
	lives = 3
	round_number = 0

	while lives > 0:
		round_number += 1
		print(f"\n--- Ronde {round_number} ---")
		points = print_random_character()
		total_points += points

		if points < 0:
			lives -= 1
			print(f"Levens over: {lives}")
		else:
			print("Gelukt!")

		print(f"Totale punten: {total_points:+d}")

	print("Je hebt 3 keer gefaald. Het spel is voorbij.")
	print(f"Eindscore: {total_points:+d}")


if __name__ == "__main__":
	play_game()

