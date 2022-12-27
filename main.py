from classes import CSV, Month
from repl import repl
from calendar_utils import print_notifications


def initialize(file):
    global years
    years = {}

    events = CSV.read(file)

    for event in events:
        if event.year not in years.keys():
            years[event.year] = {x: Month(x, event.year) for x in range(1, 13)}
        years[event.year][event.month].addEvent(event)

if __name__ == "__main__":
    initialize("events.csv")
    print('\n')
    print_notifications(years)
    print('\n')
    repl(years)
