import json
import os


def Records(timestr):
    time = int(timestr)
    li = []
    if os.path.exists("records.json"):
        with open("records.json", "r") as f:
            li = json.load(f)
    with open("records.json", "w") as fp:
        li.append(time)
        li.sort(reverse=False)
        li = li[0:10]
        json.dump(li, fp)


if __name__ == "__main__":
    Records("10")
    Records("5")
