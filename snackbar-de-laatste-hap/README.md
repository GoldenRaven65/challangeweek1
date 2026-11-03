# Snackbar De Laatste Hap

## Gameplay
- Players will take on the role of a snackbar employee working the night shift.
- Interact with various characters that enter the snackbar.
- Make decisions based on the characters' appearances and behaviors.
- Some characters may present anomalies that affect the game's outcome.

## Code structure
- `src/characters.py` contains immutable `Character` data objects in one collection.
- `src/game.py` manages the game state, typing animations, customer choices and events.
- `src/scenes.py` contains the reusable intro and character scene components.
- Shared yes/no answers are handled centrally so customer and night-event choices behave consistently.

Start the game from the `src` directory:

```powershell
python main.py
```