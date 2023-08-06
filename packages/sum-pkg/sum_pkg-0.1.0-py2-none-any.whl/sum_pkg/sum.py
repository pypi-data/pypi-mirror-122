class Summation:
    """
    Instantiate a summation operation.
    Numbers will be summed with each other.

    @param num1: num to be summed.
    @type num1: int
    """

    def __init__(self, num1):
        self.num = num1

    def sum(self, num2):
        """
        Sum one number by another.

        @param num: The first number to sum
        @type num: int

        @param num2: The number you sum with
        @type num2: int
        """
        return self.num + num2
