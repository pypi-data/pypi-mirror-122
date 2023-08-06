class Calculator:
    """Calculator class object whose methods do addition, subtraction, multiplication, division,
    takes n root of a number and resets the stored memory to the initial value.
    """
    def __init__(self, number=0): 
        """Accepts a number as initial value and if none is specified, default is 0.
        Checks if the number is int or float type and if not raises and error.
        Also converts it into a float type.
        """
        if type(number) in (int, float):
            self.starting_number = float(number)
            self.result = float(number)
        else: 
            raise ValueError('Value has to be a real number')

    def reset(self):
        """Resets the calculator memory to the initial value."""
        self.result = self.starting_number
        return self.result
    
    def add(self, number_to_add):
        """Checks if the given value is a real number.
        Adds it to the current number in calculator memory.
        """
        if type(number_to_add) in (int, float):
            self.result = self.result + number_to_add
            return self.result
        else:
            raise ValueError('Value has to be a real number')
    
    def subtract(self, number_to_subtract):
        """Checks if the given value is a real number.
        Subtracts it from the current number in calculator memory
        """
        if type(number_to_subtract) in (int, float):
            self.result = self.result - number_to_subtract
            return self.result
        else:
            raise ValueError('Value has to be a real number')
    
    def multiply(self, number_to_multiply):
        """Checks if the given value is a real number.
        Multiplies the current number in calculator memory by that number.
        """
        if type(number_to_multiply) in (int, float):
            self.result = self.result * number_to_multiply
            return self.result
        else:
            raise ValueError('Value has to be a real number')
    
    def divide(self, number_to_divide_by):
        """Checks if the given value is a real number, after that checks if the value is 0,
        because division by zero is undifined.
        Current number in calculator memory is divided by that number.
        """
        if type(number_to_divide_by) in (int, float):
            try:
                self.result = self.result / number_to_divide_by
                return self.result
            except ZeroDivisionError:
                raise ZeroDivisionError('Error. Can not divide by 0.')
        else:
            raise ValueError('Value has to be a real number')
    
    def root(self, n_root_of_a_number):
        """Checks if the current number in memory is <0 and if the n root number is even.
        If that is the case raises an error.
        Also checks if the n root number isn't a 0 because division by zero is undefined.
        Takes n root of a current number in calculator memory.
        """
        if type(n_root_of_a_number) in (int, float):
            if self.result<0 and n_root_of_a_number%2==0:
                raise ValueError('Can not take even root out of negative numbers.')
            elif n_root_of_a_number==0:
                raise ZeroDivisionError('Error. Can not divide by 0.')
            else:
                self.result = self.result ** (1/n_root_of_a_number)
                return self.result
        else:
            raise ValueError('Value has to be a real number')