import yaml
import csv
from enum import Enum, auto
import random

class MonsterFactory:
    def __init__(self):
        self.stats = {
            "ATT": 10,
            "DEF": 10,
            "AGL": 10,
            "CON": 10,
            "MAG": 10
        }

    def load_creature_type_csv(self, f):
        self.type_selector = list(csv.DictReader(open(f)))

    def load_creature_csv(self, f):
        self.base_selector = list(csv.DictReader(open(f)))

    def load_mutation_csv(self, f):
        self.mutation_selector = list(csv.DictReader(open(f)))

    def applyTypeModifiers(self, monster, type_str):
        # TODO: It would be nicer if it was indexable via name
        if type_str is None:
            return monster

        t = None
        for row in self.type_selector:
            if type_str == row["Type"]:
                t = row

        if t is not None:
            monster.types.add(type_str)

            self.setMonsterHabitat(monster, t.get("Habitat", None))
            self.setMonsterBody(monster, t.get("Body", None))
            self.setMonsterProperty(monster, t.get("Properties", None))
            self.setMonsterTags(monster, t.get("Tags", None))

        return monster

    def setMonsterBody(self, monster, body):
        if body is not None:
            body = body.replace(" ", "")
            for piece in body.split("\n"):
                if piece != "":
                    key, val = piece.split(":", 1)
                    monster.body[key] = val

    def setMonsterHabitat(self, monster, habitat):
        if habitat is not None:
            habitat = habitat.replace(" ", "")
            monster.habitat.add(habitat)

    def setMonsterProperty(self, monster, properties):
        if properties is not None:
            properties = properties.replace(" ", "")
            for p in properties.split("\n"):
                if p != "":
                    key, val = p.split(":", 1)
                    monster.properties[key] = val

    def setMonsterTags(self, monster, tags):
        if tags is not None:
            tags = tags.replace(" ", "")
            for t in tags.split("\n"):
                if t != "":
                    monster.tags.add(t)

    def getBaseMonster(self):
        base = random.choice(self.base_selector)
        # print(base)
        m = Monster(base["Name"], self.stats)
        self.applyTypeModifiers(m, base.get("Type", None))    # Default, then override
        self.setMonsterBody(m, base.get("Body", None))
        self.setMonsterSize(m, base.get("Size", None))
        self.setMonsterProperty(m, base.get("Properties", None))
        self.setMonsterTags(m, base.get("Tags", None))

        return m

    def setMonsterSize(self, monster, s):
        lookup = {
            "t": Monster.Size.Tiny,
            "s": Monster.Size.Small,
            "m": Monster.Size.Medium,
            "l": Monster.Size.Large,
            "g": Monster.Size.Gigantic,

            "tiny": Monster.Size.Tiny,
            "small": Monster.Size.Small,
            "medium": Monster.Size.Medium,
            "large": Monster.Size.Large,
            "gigantic": Monster.Size.Gigantic,
            "giant": Monster.Size.Gigantic,
        }
        size = lookup.get(s.lower(), None)
        if size is not None:
            monster.size = size

    def applyModification(self, monster):
        mutation = random.choice(self.mutation_selector)
        # print(mutation)
        mut_name = mutation["Mutation"]
        mut_type = mutation["Type"]
        mut_habitat = mutation["Habitat"]
        mut_body = mutation["Body"]
        mut_properties = mutation["Properties"]
        mut_tags = mutation["Tags"]
        monster.name = f"{mut_name} {monster.name}"
        return monster

    def generate(self):
        monster = self.getBaseMonster()
        self.applyModification(monster)
        monster.processProperties()
        return monster

class Monster:
    class Size(Enum):
        Tiny = auto()
        Small = auto()
        Medium = auto()
        Large = auto()
        Gigantic = auto()

    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
        # Defaults
        self.size = Monster.Size.Medium
        self.properties = {}
        self.tags = set()
        self.types = set()
        self.habitat = set()
        self.body = {}

    def show(self):
        print("-----------")
        print(self.name)
        print(self.size)
        print("Stats:")
        for key, value in self.stats.items():
            print(f" {key} {value}")
        print("Body:")
        for key, value in self.body.items():
            print(f" {key} {value}")
        print("Properties:")
        for key, value in self.properties.items():
            print(f" {key} {value}")
        print("Tags:")
        for value in self.tags:
            print(f" {value}")
        print("-----------")

    def processProperties(self):
        for key, val in self.properties.items():
            if key == "bonus":
                self.stats[val.upper()] += 1
            if key == "penalty":
                self.stats[val.upper()] -= 1

def main():
    mf = MonsterFactory()
    # with open("creatures/creatures.csv") as creature_csv:
    mf.load_creature_csv("creatures/creatures.csv")
    mf.load_mutation_csv("creatures/mutations/creature_mutations.csv")
    mf.load_creature_type_csv("creatures/creature_types.csv")

    print("Generating 5 monsters")
    for _ in range(5):
        m = mf.generate()
        m.show()


if __name__ == "__main__":
    main()
