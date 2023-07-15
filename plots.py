"""
Render plots for TSG
"""
import csv

import graphviz
import matplotlib.pyplot as plt


def draw_plot():
    """
    Draw a plot based on the TSG CSV data
    """
    ticks = []
    live_things = []
    max_things = []
    with open("tsg.csv", mode="r", encoding="utf-8") as csvfile:
        lines = csv.DictReader(csvfile, delimiter=",")

        for row in lines:
            ticks.append(int(row["tick"]))
            live_things.append(int(row["Live"]))
            max_things.append(int(row["Tmx"]))

    plt.plot(ticks, live_things, color="g", label="Alive")
    plt.plot(ticks, max_things, color="b", label="Max")
    plt.xlabel("Ticks")
    plt.ylabel("Things")
    plt.title("Population change over time", fontsize=20)
    plt.legend()
    plt.show()


def draw_tree():
    """
    Draw ancestry graph
    """
    tree = graphviz.Digraph("G", filename="ancestry.gv")
    tree.graph_attr["rankdir"] = "LR"
    tree.node("T0")

    with open("ancestry.csv", mode="r", encoding="utf-8") as csvfile:
        lines = list(csv.reader(csvfile, delimiter=","))

        for line in lines:
            tree.edge(line[0].strip(), line[1].strip())

    tree.view()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--plot", action="store_true", help="Draw life over time plot")
    parser.add_argument("-t", "--tree", action="store_true", help="Draw ancestry tree")

    args = parser.parse_args()

    if args.plot:
        draw_plot()
    elif args.tree:
        draw_tree()
