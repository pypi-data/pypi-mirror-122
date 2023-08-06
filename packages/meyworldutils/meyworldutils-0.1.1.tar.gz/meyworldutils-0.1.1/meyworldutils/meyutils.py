# Say you have two variables x1 = 52720 and x2 = 712431205 and want to plot them against each other from 0 to x.
# They will need to be split equally into n parts.

def split_x(x, n, include_zero=True):
    """
    Say you have two variables x1 = 52720 and x2 = 712431205 and want to plot them against each other from 0 to x.
    They will need to be split equally into n parts.

    Args:
        x (int): integer to be split.
        n (int): Splitting into n parts.
        include_zero (bool, optional): Return a list starting with 0 or not. Defaults to True.

    Returns:
        list: list of [(0), ..., x] of len(n)
    """
    if include_zero:
        x_l = [0]
    else:
        x_l = []
    x_1 = x/n
    x_tmp = x_1
    for i in range(n):
        x_l.append(x_tmp)
        x_tmp += x_1
    return x_l

if __name__ == '__main__':
    print(split_x(10, 5, include_zero=False))
