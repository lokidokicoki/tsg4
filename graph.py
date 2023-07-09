import csv

import graphviz


def draw_tree():
    g = graphviz.Digraph("G", filename="ancestry.gv")
    g.node("T0")

    with open("ancestry.csv", mode="r", encoding="utf-8") as csvfile:
        lines = list(csv.reader(csvfile, delimiter=","))

        sorted(lines)

        for line in lines:
            print(f"{line[0]}->{line[1]}")
            g.edge(line[0], line[1])

    g.view()


if __name__ == "__main__":
    draw_tree()
