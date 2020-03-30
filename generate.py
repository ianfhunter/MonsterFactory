import yaml

class Monster:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats

    def show(self):
        print(self.name)
        for key, value in self.stats.items():
            print(key, value)
        
def generate_monster(tier=0):
    stats = {
      "ATK": 10,
      "DEF": 10,
      "AGL": 10,
      "CON": 10,
      "MAG": 10
    }

    if tier == 0:
        with open("monster-base-1.yaml") as base:
            b = yaml.load(base)
            print(b)
    else:
        raise NotImplementedError

    return Monster("Default", stats)
    
print("Generating 5 monsters")
for x in range(5):
    for t in range(3): # tier
        m = generate_monster(tier=0)
        m.show()
