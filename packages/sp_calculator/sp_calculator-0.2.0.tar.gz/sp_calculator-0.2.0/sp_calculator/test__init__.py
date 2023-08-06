from sp_calculator import Calculator

calc = Calculator()

def test_add():
  assert calc.reset() == 0
  assert calc.add(5) == 5 
  assert calc.add(5.5) == 10.5
  assert calc.add('5') == 15.5
  assert calc.add('five') == False
  
def test_multiply():
  assert calc.reset() == 0
  assert calc.add(5) == 5
  assert calc.multiply(2) == 10
  assert calc.multiply(5.5) == 55
  assert calc.multiply('5') == 275
  assert calc.multiply('five') == False

def test_subtract():
  assert calc.reset() == 0
  assert calc.subtract(5) == -5
  assert calc.subtract(5.5) == -10.5
  assert calc.subtract('5') == -15.5
  assert calc.multiply('five') == False

def test_divide():
  assert calc.reset() == 0
  assert calc.add(10) == 10
  assert calc.divide(10) == 1
  assert calc.divide(4) == 0.25
  assert calc.divide('1') == 0.25
  assert calc.multiply('five') == False

def test_nth_root():
  assert calc.reset() == 0
  assert calc.add(4) == 4
  assert calc.nth_root(2) == 2
  assert calc.reset() == 0
  assert calc.add(4) == 4
  assert calc.nth_root('2') == 2
  assert calc.reset() == 0
  assert calc.add(4) == 4
  assert calc.nth_root('five') == False