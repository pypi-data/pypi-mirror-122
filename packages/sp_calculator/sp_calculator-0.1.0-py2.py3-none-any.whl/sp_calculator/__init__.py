"""A basic calculator module"""

__version__ = "0.1.0"

class Calculator:  
  def __init__(self):
    self.calc_val = 0
  
  def check_user_input(self, input):
    try:
      val = int(input)
      return True
    except ValueError:
      try:
        val = float(input)
        return True
      except ValueError:
        return 'Please enter an integer or floating point number'
  
  def add(self, input):
    if (self.check_user_input(input)):
      self.calc_val += input 
      return self.calc_val
  
  def subtract(self, input):
    self.calc_val -= input
    return self.calc_val
      
  def multiply(self, input):
    self.calc_val = self.calc_val * input
    return self.calc_val

  def divide(self, input):
    self.calc_val = self.calc_val / input
    return self.calc_val

  def reset(self):
    self.calc_val = 0
    return self.calc_val
