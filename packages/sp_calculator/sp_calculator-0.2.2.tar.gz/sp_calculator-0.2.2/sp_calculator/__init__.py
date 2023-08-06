"""A basic dependency-free calculator module

The module exports a single class called Calculator which has
6 public methods: add, subtract, divide, multiply, nth_root and reset.
"""

__version__ = "0.2.2"

class Calculator:
  """
  A simple calculator class.
  
  Methods
  -------
  add(input)
  subtract(input)
  multiply(input)
  divide(input)
  nth_root(input)
  reset(input)
  """
  
  def __init__(self):
    self.calc_val = 0
    self.user_input = None
  
  def __check_user_input(self, input):
    """Private method to validate whether user input is int or float"""
    try:
      self.user_input = float(input)
      return True
    except ValueError:
      try:
        self.user_input = int(input)
        return True
      except ValueError:
        print('Please enter an integer or floating point number')
        return False
  
  def add(self, input):
    """Public method to add to calculator's current_val"""
    if (self.__check_user_input(input)):
      self.calc_val += self.user_input 
      return self.calc_val
    else:
      return False
  
  def subtract(self, input):
    """Public method to subtract from calculator's current_val"""
    if (self.__check_user_input(input)):
      self.calc_val -= self.user_input
      return self.calc_val
    else:
      return False
      
  def multiply(self, input):
    """Public method to multiply calculator's current_val"""
    if (self.__check_user_input(input)):
      self.calc_val = self.calc_val * self.user_input
      return self.calc_val
    else:
      return False

  def divide(self, input):
    """Public method to divide calculator's current_val"""
    if (self.__check_user_input(input)):
      self.calc_val = self.calc_val / self.user_input
      return self.calc_val
    else:
      return False

  def nth_root(self, input):
    """Public method to take nth root from calculator's current_val"""
    if (self.__check_user_input(input)):
      self.calc_val = pow(self.calc_val, 1 / self.user_input)
      return self.calc_val
    else:
      return False

  def reset(self):
    """Public method to reset calculator's current_val"""
    self.calc_val = 0
    return self.calc_val
