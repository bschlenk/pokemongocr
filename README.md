# pokemongocr
Run orc on a screenshot of a pokémon to get its name, cp, hp, and stardust to next level.

## Dependencies

Make sure tesseract is installed somewhere and you can access it from the comand line simply by typing `tesseract`.

On OSX you can install it through brew:
```brew install tesseract```

## Usage

Invoke the script with the path to a screenshot as the first argument.

```
>>> ./main.py screenshots/bulbasaur.png
{'stardust': 2500, 'name': 'Bulbasaur', 'cp': 600, 'hp': 62}
```

