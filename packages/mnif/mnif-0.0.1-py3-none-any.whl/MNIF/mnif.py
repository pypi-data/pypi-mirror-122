def improper_fraction(num):
    num = num.split(" ")
    whole_number = num[0]
    fraction = str(num[1])
    fraction = fraction.split("/")
    numerator = fraction[0]
    denominator = fraction[1]
    numerator = int(numerator)
    denominator = int(denominator)
    whole_number = int(whole_number)
    ans = whole_number * denominator + numerator
    print(f"{ans}/{denominator}")


def mixed_number(num):
    num = num.split("/")
    numerator = num[0]
    denominator = num[1]
    numerator = int(numerator)
    denominator = int(denominator)
    remainder = numerator % denominator
    number = numerator / denominator
    number = int(number)
    print(f"{number} {remainder}/{denominator}")











































