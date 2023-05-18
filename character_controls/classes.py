class Character:

  def __init__(
    self,
    first_name,
    last_name,
    skin,
    level,
    hot,
    cold,
    volatile,
    dark,
  ):
    self.first_name = first_name
    self.last_name = last_name
    self.skin = skin
    self.level = level
    self.hot = hot
    self.cold = cold
    self.volatile = volatile
    self.dark = dark


class Condition:

  def __init__(self, first_name, last_name, condition):
    self.first_name = first_name
    self.last_name = last_name
    self.condition = condition