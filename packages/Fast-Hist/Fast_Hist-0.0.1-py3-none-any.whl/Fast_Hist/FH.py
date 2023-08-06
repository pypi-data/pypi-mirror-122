import matplotlib.pyplot as plt


def fast_hist(array):
    FH = {}
    for i in array:
        if FH.get(i) == None:
            FH.update({i: 1})
        else:
            FH.update({i: FH[i] + 1})

    plt.bar(FH.keys(), FH.values())
    plt.show()