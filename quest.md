---
id: quest
name: Quest
---

# Main

The player enters the main area for an item.

```kty
@trigger ENTER_AREA-mall

# Triggered on quest started.
@flow started
	@show gunman
	gunman: What are you doing here? This is a restricted area.
```