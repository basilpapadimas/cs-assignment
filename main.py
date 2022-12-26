from calendar import monthrange
from datetime import timedelta, datetime
import csv
from re import fullmatch
from functools import reduce


class CSVrw:
    def read(filename):
        try:
            with open(filename, 'r', newline='', encoding='cp1252') as file:
                leading_bytes = file.read(3)

                if (leading_bytes != 'ï»¿'):
                    file.seek(0)
                else:
                    pass

                return list(map(lambda x: Event(list(map(lambda x: int(x), x[0].split('-'))) + list(map(lambda x: int(x), x[1].split(':'))) + [int(x[2])] + [x[3]]), list(csv.reader(file))[1:]))
        except FileNotFoundError:
            with open(filename, 'w', newline='', encoding='cp1252') as file:
                file.write("")
            CSVrw.read(filename)

    def write(filename):
        with open(filename, 'w', newline='', encoding='cp1252') as file:
            file.write("")

            writer = csv.writer(file)
            writer.writerow(["Date", "Hour", "Duration", "Title"])

            events = []
            for year in years.keys():
                for month in years[year]:
                    events.extend(years[year][month].events)
            for event in events:
                writer.writerow([f"{event.year}-{event.month}-{event.day}",
                                f"{event.hour}:{event.minutes}", event.duration, event.title])


class Event:
    def __init__(self, ls):
        self.year, self.month, self.day, self.hour, self.minutes, self.duration, self.title = ls
        self.startdate = datetime(
            self.year, self.month, self.day, self.hour, self.minutes)
        self.enddate = self.startdate+timedelta(minutes=self.duration)

    def checkOverlap(self):
        events = []
        for year in filter(lambda x: x < self.year, years.keys()):
            events.extend(filter(lambda x: True if x.enddate >= self.startdate else False, reduce(
                lambda x, y: x+y, [years[year][month].events for month in range(1, 13)])))
        events.extend(filter(lambda x: True if x.enddate >= self.startdate else False, reduce(
            lambda x, y: x+y, [years[self.year][month].events for month in range(1, self.month+1)])))
        for event in events:
            if not ((event.enddate < self.startdate and event.startdate < self.enddate) or (event.startdate > self.enddate and event.enddate > self.startdate)):
                print(event.startdate, event.enddate, self.startdate, self.enddate)
                day = {x: {x: False for x in range(60)} for x in range(24)}
                for event2 in events:
                    mDate = event2.startdate
                    while mDate <= event2.enddate:
                        if datetime(self.year, self.month, self.day, 0, 0, 0) <= mDate < (datetime(self.year, self.month, self.day, 0, 0, 0) + timedelta(days=1)):
                            day[mDate.hour][mDate.minute] = True
                        mDate = mDate + timedelta(minutes=1)
                freecells = "  hours horizontally, minutes vertically, allocated minutes are \"++\":\n   00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23\n"
                for x in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"]:
                    freecells += x+" "+"".join(str(x)+" " for x in ["++" if day[hour][int(x)-1] else "  " for hour in [
                                               0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]])+"\n"
                return [True, freecells]
        return [False, None]


class Month:
    def __init__(self, mm: int, yyyy: int):
        self.month = mm
        self.year = yyyy
        self.events = []

    def addEvent(self, newevent):
        if newevent.year == self.year and newevent.month == self.month:
            self.events.append(newevent)
            return True
        else:
            return False

    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)
            return True
        else:
            return False

    def printEvents(self):
        for index, event in enumerate(self.events):
            print(f"{index}. [{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}\n")
        return self.events


def initialize(file="events.csv"):
    global years
    years = {}

    events = CSVrw.read(file)

    for event in events:
        if event.year not in years.keys():
            years[event.year] = {x: Month(x, event.year) for x in range(1, 13)}
        years[event.year][event.month].addEvent(event)


def generate_calendar(mm: int, yyyy: int):
    """Given an input of month number (1 to 12) and year
    it returns a string of the calendar of the month
    including last days of last month and first days of next month
    if they so collide with the calendar
    """

    calendar_string = f"""
    {'─'*55}
       ｜{['ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'][mm-1]} {yyyy}｜
    {'─'*55}
    {'｜ '.join(['  ΔΕΥ', '  ΤΡΙ', '  ΤΕΤ', '  ΠΕΜ', '  ΠΑΡ', '  ΣΑΒ', '  ΚΥΡ'])}
    """

    if monthrange(yyyy, mm)[0] != 0:
        last_days_of_last_month = [f"   {x}" for x in list(range(1, int(monthrange(yyyy, int(
            mm) - 1 + 12*(1 if mm == 1 else 0))[1]) + 1))[-1 * int(monthrange(yyyy, mm)[0]):]]
    else:
        last_days_of_last_month = []

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(
        range(1, monthrange(yyyy, mm)[1] + 1))]

    first_days_of_next_month_needed_num = [f"    {x}" for x in list(range(
        1, 6 - datetime(yyyy, mm, int(days_of_given_mm[-1].replace('[ ', '').replace(']', ''))).weekday() + 1))]
    days_to_be_printed = last_days_of_last_month + \
        days_of_given_mm + first_days_of_next_month_needed_num

    eventful_days = set()
    if yyyy in years.keys():
        for event in years[yyyy][mm].events:
            eventful_days.add(event.day)

    for i in range(len(days_to_be_printed)):
        if '[' in days_to_be_printed[i]:  # CHECKS IF DATE IS FROM MONTH SELECTED
            # CHECKS IF DAY HAS AT LEAST ONE EVENT
            if int(days_to_be_printed[i].replace('[ ', '').replace(']', '')) in eventful_days:
                # CHANGES [ DAY] TO [*DAY]
                days_to_be_printed[i] = f"[*{days_to_be_printed[i].replace('[ ', '').replace(']', '')}]"

    for line in [days_to_be_printed[x:x+7] for x in range(0, len(days_to_be_printed), 7)]:
        calendar_string += '｜ '.join(line) + "\n    "
    calendar_string += '─'*55

    return calendar_string


def print_notifications():
    """Checks if events are today and after the current time and displays them"""

    now = datetime.now()

    coming_events = []
    if now.year not in years.keys():
        return
    for event in years[now.year][now.month].events:
        if event.day == now.day and event.startdate > now:  # checks if the event is today
            coming_events.append(event)

    for event in coming_events:
        delta = event.startdate - timedelta(hours=now.hour, minutes=now.minute)
        print(
            f"[*] Notification: in {delta.hour} hour(s) and {delta.minute} minute(s) the programmed event '{event.title}' will take place")


def repl():
    mm, yyyy = datetime.now().month, datetime.now().year
    print(generate_calendar(mm, yyyy))

    while True:
        choice = input('''
        Πατήστε ENTER για προβολή του επόμενου μήνα, "q" για έξοδο ή κάποια από τις παρακάτω επιλογές:
            "-" για πλοήγηση στον προηγούμενο μήνα
            "+" για διαχείριση των γεγονότων του ημερολογίου
            "*" για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα
            -> ''')

        match choice:  # requires Py3.10
            case "":
                mm, yyyy = mm % 12 + 1, yyyy + 1*(mm == 12)
                print(generate_calendar(mm, yyyy))
            case "-":
                mm, yyyy = mm - 1 + 12*(mm == 1), yyyy - 1*(mm == 1)
                print(generate_calendar(mm, yyyy))
            case "+":
                while True:
                    choice = input('''
    Διαχείριση γεγονότων ημερολογίου, επιλέξτε ενέργεια:
        1 Καταγραφή νέου γεγονότος
        2 Διαγραφή γεγονότος
        3 Ενημέρωση γεγονότος
        0 Επιστροφή στο κυρίως μενού
        -> ''')
                    match choice:
                        case "0":
                            break

                        case "1":
                            while True:
                                answer = input(
                                    "Ημερομηνία γεγονότος (yyyy-mm-dd): ")
                                if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
                                    continue
                                year, month, day = map(
                                    lambda x: int(x), answer.split("-"))
                                if year < 2022 or not 0 < month <= 12:
                                    continue
                                months_days = monthrange(year, month)[1]
                                if not 0 < day <= months_days:
                                    continue
                                break

                            while True:
                                answer = input("Ωρα γεγονότος (hh:mm): ")
                                if fullmatch(r"\d\d?\:\d\d", answer) == None:
                                    continue
                                hour, minutes = map(
                                    lambda x: int(x), answer.split(":"))
                                if not 0 <= hour <= 23 or not 0 <= minutes < 60:
                                    continue
                                break

                            while True:
                                answer = input("Διάρκεια γεγονότος: ")
                                if answer.isdigit():
                                    duration = int(answer)
                                    break

                            while True:
                                answer = input("Τίτλος γεγονότος: ")
                                if "," not in answer:
                                    title = answer
                                    break

                            event = Event([year, month, day, hour,
                                           minutes, duration, title])
                            overlap = event.checkOverlap()

                            while overlap[0]:
                                print("Γεγονός έχει επικάλυψη με άλλα γεγονότα")
                                print(overlap[1])

                                while True:
                                    answer = input(
                                        f"Ημερομηνία γεγονότος ({event.year}-{event.month}-{event.day}): ") or f"{event.year}-{event.month}-{event.day}"
                                    if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
                                        continue
                                    year, month, day = map(
                                        lambda x: int(x), answer.split("-"))
                                    if year < 2022 or not 0 < month <= 12:
                                        continue
                                    months_days = monthrange(year, month)[1]
                                    if not 0 < day <= months_days:
                                        continue
                                    break

                                while True:
                                    answer = input(
                                        f"Ωρα γεγονότος ({event.hour}:{event.minutes:02d}): ") or f"{event.hour}:{event.minutes:02d}"
                                    if fullmatch(r"\d\d?\:\d\d", answer) == None:
                                        continue
                                    hour, minutes = map(
                                        lambda x: int(x), answer.split(":"))
                                    if not 0 <= hour <= 23 or not 0 < minutes < 60:
                                        continue
                                    break

                                event = Event([year, month, day, hour,
                                               minutes, duration, title])
                                overlap = event.checkOverlap()

                            if event.year not in years.keys():
                                years[event.year] = {
                                    x: Month(x, event.year) for x in range(1, 13)}
                            years[event.year][event.month].addEvent(event)
                            print(
                                f"Το γεγονός προστέθηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "2":
                            while True:
                                answer = input("Εισάγετε έτος: ")
                                if not answer.isdigit():
                                    continue
                                year = int(answer)
                                if year >= 2022:
                                    break

                            while True:
                                answer = input("Εισάγετε μήνα: ")
                                if not answer.isdigit():
                                    continue
                                month = int(answer)
                                if 0 < month <= 12:
                                    break

                            print("=== Αναζήτηση γεγονότων ===")
                            events = years[year][month]
                            events_len = len(events.printEvents())
                            if events_len == 0:
                                print("Κανένα γεγονός αυτόν τον μήνα")
                                continue

                            while True:
                                answer = input(
                                    "Επιλέξτε γεγονός προς ενημέρωση: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events.events[event]
                            events.removeEvent(event)
                            print(
                                f"Το γεγονός διαγράφηκε: <[{event.name}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "3":
                            while True:
                                answer = input("Εισάγετε έτος: ")
                                if not answer.isdigit():
                                    continue
                                year = int(answer)
                                if year >= 2022:
                                    break

                            while True:
                                answer = input("Εισάγετε μήνα: ")
                                if not answer.isdigit():
                                    continue
                                month = int(answer)
                                if 0 < month <= 12:
                                    break

                            print("=== Αναζήτηση γεγονότων ===")
                            events = years[year][month]
                            events_len = len(events.printEvents())
                            if events_len == 0:
                                print("Κανένα γεγονός αυτόν τον μήνα")
                                continue

                            while True:
                                answer = input(
                                    "Επιλέξτε γεγονός προς ενημέρωση: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events.events[event]

                            while True:
                                answer = input(
                                    f"Ημερομηνία γεγονότος ({event.year}-{event.month}-{event.day}): ") or f"{event.year}-{event.month}-{event.day}"
                                if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
                                    continue
                                year, month, day = map(
                                    lambda x: int(x), answer.split("-"))
                                if year < 2022 or not 0 < month <= 12:
                                    continue
                                months_days = monthrange(year, month)[1]
                                if not 0 < day <= months_days:
                                    continue
                                break

                            while True:
                                answer = input(
                                    f"Ώρα γεγονότος ({event.hour}:{event.minutes:02d}): ") or f"{event.hour}:{event.minutes:02d}"
                                if fullmatch(r"\d\d?\:\d\d", answer) == None:
                                    continue
                                hour, minutes = map(
                                    lambda x: int(x), answer.split(":"))
                                if not 0 <= hour <= 23 or not 0 < minutes < 60:
                                    continue
                                break

                            while True:
                                answer = input(
                                    f"Διάρκεια γεγονότος ({event.duration}): ") or f"{event.duration}"
                                if answer.isdigit():
                                    duration = answer
                                    break

                            while True:
                                answer = input(
                                    f"Τίτλος γεγονότος ({event.title}): ") or f"{event.title}"
                                if "," not in answer:
                                    title = answer
                                    break

                            new_event = Event([year, month, day, hour,
                                               minutes, duration, title])
                            overlap = new_event.checkOverlap()

                            while overlap[0]:
                                print("Γεγονός έχει επικάλυψη με άλλα γεγονότα")
                                print(overlap[1])
                                while True:
                                    answer = input(
                                        f"Ημερομηνία γεγονότος ({new_event.year}-{new_event.month}-{new_event.day}): ") or f"{new_event.year}-{new_event.month}-{new_event.day}"
                                    if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
                                        continue
                                    year, month, day = map(
                                        lambda x: int(x), answer.split("-"))
                                    if year < 2022 or not 0 < month <= 12:
                                        continue
                                    months_days = monthrange(year, month)[1]
                                    if not 0 < day <= months_days:
                                        continue
                                    break

                                while True:
                                    answer = input(
                                        f"Ωρα γεγονότος ({new_event.hour}:{new_event.minutes:02d}): ") or f"{new_event.hour}:{new_event.minutes:02d}"
                                    if fullmatch(r"\d\d?\:\d\d", answer) == None:
                                        continue
                                    hour, minutes = map(
                                        lambda x: int(x), answer.split(":"))
                                    if not 0 <= hour <= 23 or not 0 < minutes < 60:
                                        continue
                                    break
                                new_event = Event([year, month, day, hour,
                                                   minutes, duration, title])
                                overlap = new_event.checkOverlap()
                            if new_event.year not in years.keys():
                                years[new_event.year] = {
                                    x: Month(x, new_event.year) for x in range(1, 13)}
                            years[event.year][event.month].removeEvent(event)
                            years[new_event.year][new_event.month].addEvent(
                                new_event)
                            print(
                                f"Το γεγονός ενημερώθηκε: <[{new_event.title}] -> Date: {new_event.year}-{new_event.month}-{new_event.day}, Time: {new_event.hour}:{new_event.minutes:02d}, Duration: {new_event.duration}>")
                            break
            case "*":
                print("=== Αναζήτηση γεγονότων ===")
                years[int(input("Εισάγετε έτος: "))][int(
                    input("Εισάγετε μήνα: "))].printEvents()
                input("Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού: ")
                print(generate_calendar(mm, yyyy))

            case "q":
                CSVrw.write("events.csv")
                raise SystemExit(0)


if __name__ == "__main__":
    initialize()
    print('\n')
    print_notifications()
    print('\n')
    repl()
