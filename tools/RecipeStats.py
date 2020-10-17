#!/usr/bin/env python3
import glob
import enum
import pandas
from typing import List, Iterator


class Recipe:
    class Element:
        class Type(enum.Enum):
            TITLE = 1
            SUBTITLE = 2
            QUOTE = 3
            NOTE = 10
            STEP = 20
            INGREDIENT = 21

        def __init__(self, item_type: Type, text: str, note: str = None, guide: str = None):
            self.type = item_type
            self.text = text.strip()
            self.note = note.strip() if note else None
            self.guide = guide.strip() if guide else None

    elements: List[Element]

    def __init__(self, file):
        """
        :type file: io.TextIOWrapper
        """
        self.elements = []

        for line in file:
            if line.startswith('# '):
                self.elements.append(Recipe.Element(Recipe.Element.Type.TITLE, line[2:]))
            elif line.startswith('## '):
                self.elements.append(Recipe.Element(Recipe.Element.Type.SUBTITLE, line[3:]))
            elif line.startswith('> '):
                self.elements.append(Recipe.Element(Recipe.Element.Type.QUOTE, line[2:]))
            elif line.startswith('- '):
                [text, note, guide] = line[2:].split('|')
                self.elements.append(Recipe.Element(Recipe.Element.Type.INGREDIENT, text, note, guide))
            elif len(line) > 0:
                self.elements.append(Recipe.Element(Recipe.Element.Type.STEP, line))

    def ingredients(self) -> Iterator[Element]:
        return filter(lambda item: item.type == Recipe.Element.Type.INGREDIENT, self.elements)


def main():
    files = glob.glob('**/*.recipe', recursive=True)
    ingredients = pandas.Series([], dtype=str)

    for path in files:
        with open(path) as file:
            recipe = Recipe(file)
            for ingredient in recipe.ingredients():
                ingredients = ingredients.append(pandas.Series([ingredient.text], dtype=str))

    print(ingredients.value_counts().to_string(max_rows=None))


if __name__ == '__main__':
    main()
