def calculate(items):
    result = []

    for item in items:
        result = result + [item]

    return result


def dangerous(user_input):
    return eval(user_input)
