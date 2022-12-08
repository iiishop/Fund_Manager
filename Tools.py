"""
It takes a string that ends in a percent sign, strips off the percent sign, converts the remaining
string to a float, and then divides the result by 100, yielding a proportion

:param p: str
:type p: str
:return: A float
"""


@staticmethod
def change_percent_to_float(p: str):
    return float(p.strip('%')) / 100
