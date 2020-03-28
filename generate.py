class Monster():
    def __init__(self, name, stats):
        self.name = name
        
        
def generate_monster():
    stats = {
      "ATT": 10
      "DEF": 10
      "AGL": 10
      "CON": 10
      "MAG": 10
    }
    return Monster("Default", stats)
    
if __name__ == __main__:
  print("Generating 5 monsters")
  for x in range(5):
      m = generate_monster()
      m.print
