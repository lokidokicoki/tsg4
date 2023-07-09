"""
Render plots for TSG
"""
import csv

import matplotlib.pyplot as plt


def show_plot():
    """
    Draw a plot based on the TSG CSV data
    """
    x = []
    y1 = []
    y2 = []
    with open("tsg.csv", mode="r", encoding="utf-8") as csvfile:
        lines = csv.DictReader(csvfile, delimiter=",")

        for row in lines:
            x.append(int(row["tick"]))
            y1.append(int(row["Live"]))
            y2.append(int(row["Tmx"]))

    plt.plot(x, y1, color="g", label="Alive")
    plt.plot(x, y2, color="b", label="Max")
    plt.xlabel("Ticks")
    plt.ylabel("Things")
    plt.title("Population change over time", fontsize=20)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    show_plot()
