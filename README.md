# mac-hinge-scream

> *"Is your MacBook okay?"*
> — Everyone who hears this running

A prank that makes your MacBook sound like its hinge is **literally falling apart**. Every time you open or close the lid, it plays horrifying creak and squeak sounds that scale with how fast you move it.

Open it slowly? Gentle, unsettling creak.
Slam it open? Full-on haunted house door.

Watch your friends handle your laptop like it's made of glass.

## How it works

1. Monitors the MacBook lid angle in real-time using [pybooklid](https://github.com/amanrao23/pybooklid)
2. Detects hinge movement from the angle sensor
3. Plays random creak/squeak sounds from the `sounds/` folder
4. **Volume scales with speed** — gentle = quiet, fast = LOUD
5. **Pitch scales with speed** — slow creak vs urgent screech
6. Stops instantly when the lid stops moving (no suspicious lingering audio)

## Requirements

- macOS (uses `afplay` for audio playback)
- Python 3
- [pybooklid](https://github.com/amanrao23/pybooklid)

## Setup

```bash
pip install pybooklid
```

Drop your `.mp3` creak/squeak sounds into the `sounds/` folder (some are included).

## Usage

```bash
python run.py
```

Then hand your laptop to someone and ask them to open it. Sit back. Enjoy.

`Ctrl+C` to stop (and to stop laughing).

> **Pro tip:** Run it in the background so there's no suspicious terminal window open:
> ```bash
> python run.py &disown
> ```
> Now close the terminal and act completely innocent. To stop it later: `pkill -f run.py`

## Tuning

| Variable | What it does | Default |
|---|---|---|
| `MOVE_THRESHOLD` | Minimum angle change to trigger sound | `1.5` |
| `MIN_GAP` | Pause between sounds (seconds) | `0.3` |
| `FAST_SPEED` | Speed considered "fast" (louder, higher pitch) | `15` |
| `MIN_ANGLE` / `MAX_ANGLE` | Angle range where sounds play | `20` / `128` |

## Disclaimer

Not responsible for:
- Friends refusing to touch your laptop ever again
- Genius Bar appointments made on your behalf
- Emotional damage to MacBook owners nearby
- Anyone wrapping your laptop in bubble wrap "just in case"

## Made by

[amanraox.dev](https://amanraox.dev) — [GitHub](https://github.com/amanraox/mac-hinge-scream)

## License

Do whatever you want with it. Prank responsibly.
