from calendar import monthrange
from datetime import timedelta, datetime
import csv
from re import fullmatch
from functools import reduce


class CSVrw:
    """read(): READS THE CSV FILE AND RETURNS A LIST OF LIST OF THE LINES
    [[LINE0 SPLITED IN COLLUMNS], [LINE1 SPLITED IN COLLUMNS], [LINE2 SPLITED IN COLLUMNS], ...]

    append(): THE event_to_write PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ARE GOING TO BE APPENDED TO THE FILE ACCORDING TO THEIR INDEX TO THE SPECIFIC COLUMN ON

    change(): THE event_to_replace PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ALREADY EXISTS IN THE FILE WHICH IS GOING TO BE REPLACED BY THE event_to_write LIST
    """

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
                writer.writerow([f"{str(event.year)}-{str(event.month)}-{str(event.day)}",
                                f"{str(event.hour)}:{str(event.minutes)}", event.duration, event.title])


class Event:
    def __init__(self, ls):
        self.year, self.month, self.day, self.hour, self.minutes, self.duration, self.title = ls
        self.startdate = datetime(
            self.year, self.month, self.day, self.hour, self.minutes)
        self.enddate = self.startdate+timedelta(minutes=self.duration)

    def checkOverlap(self):
        events = []
        for year in filter(lambda x: x<self.year, years.keys()):
            events.extend(filter(lambda x: True if x.enddate>=self.startdate else False, reduce(lambda x, y: x+y, [years[year][month].events for month in range(1, 13)])))
        events.extend(filter(lambda x: True if x.enddate>=self.startdate else False, reduce(lambda x, y: x+y, [years[self.year][month].events for month in range(1, self.month+1)])))
        for event in events:
            if not (event.enddate < self.startdate and event.startdate < self.enddate) or not (event.startdate > self.enddate and event.enddate > self.startdate):
                day = {x: {x: False for x in range(60)} for x in range(24)}
                for event2 in events:
                    mDate = event2.startdate
                    while mDate <= event2.enddate:
                        if datetime(self.year, self.month, self.day, 0, 0, 0) <= mDate < (datetime(self.year, self.month, self.day, 0, 0, 0) + timedelta(days=1)):
                            day[mDate.hour][mDate.minute] = True
                        mDate = mDate + timedelta(minutes=1)
                freecells = "  hours horizontally, minutes vertically, allocated minutes are \"++\":\n  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23\n"
                for x in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"]:
                    freecells += x+"".join(str(x)+" " for x in ["++" if day[hour][int(x)-1] else "  " for hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]])+"\n"
                return [True, freecells]
        return [False, None]



class Month:
    def __init__(self, mm: int, yyyy: int):
        self.month = mm
        self.year = yyyy
        self.events = []

    def addEvent(self, newevent):
        self.events.append(newevent)
        # self.events.sort(key=lambda x: x.startdate)

    def removeEvent(self, event):
        self.events.remove(event)

    def printEvents(self):
        # 0. [New Year's Eve] -> Date: 2022-12-31, Time: 23:59, Duration: 0
        counter = 0
        for event in self.events:
            print(f"{counter}. [{event.title}] -> Date: {str(event.year)}-{str(event.month)}-{str(event.day)}, Time: {str(event.hour)}:{str(event.minutes)}, Duration: {str(event.duration)}\n")
            counter += 1
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
    """Given an input of month number(0 to 12) and year
    it returns a string of the calendar of the month
    including last days of last month and first days of next month
    if they so collide with the calendar

    events is a list of string type elements [Date,Hour,Duration,Title]
    so events = [[date1, hour1, duration1, title1], [date2, hour2, duration2, title2], ...]
    NO DOCTESTS?
    """

    def get_num_of_days(mm, yyyy):
        """Returns a tuple of type (weekday of first day of the month, number of days in given month)
        DOCTESTS LATER TO BE ADDED"""
        return monthrange(yyyy, mm)

    calendar_string = f"""
    {'─'*55}
       ｜{[None, 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'][mm]} {yyyy}｜
    {'─'*55}
    {'｜ '.join(['  ΔΕΥ', '  ΤΡΙ', '  ΤΕΤ', '  ΠΕΜ', '  ΠΑΡ', '  ΣΑΒ', '  ΚΥΡ'])}
    """
    if monthrange(yyyy, mm)[0] != 0:
        last_days_of_last_month = [f"   {x}" for x in list(range(1, int(get_num_of_days(int(
            mm) - 1 + 12*(1 if mm == 1 else 0), yyyy)[1]) + 1))[-1 * int(get_num_of_days(mm, yyyy)[0]):]]
    else:
        last_days_of_last_month = []

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(
        range(1, get_num_of_days(mm, yyyy)[1] + 1))]

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
    """Gets events and checks if they are today and after the current time and displays them in format
    [*] Notification: in {hh_till_event} hour(s) and {mins_till_event} minute(s) the programmed event '{sorted_event_names[i]}' will take place
    """
    '''
    global current_year, current_month, current_day, current_hour, current_minutes
    current_year, current_month, current_day = [
        int(str(x)) for x in str(date.today()).split('-')]
    current_hour, current_minutes = [
        int(x) for x in datetime.now().strftime("%H:%M").split(":")]
    '''
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
                                        f"Ωρα γεγονότος ({event.hour}:{event.minutes}): ") or f"{event.hour}:{event.minutes}"
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
                                f"Το γεγονός προστέθηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}-{event.minutes}, Duration: {event.duration}>")
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
                                f"Το γεγονός διαγράφηκε: <[{event.name}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}-{event.minutes}, Duration: {event.duration}>")

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
                                    f"Ώρα γεγονότος ({event.hour}:{event.minutes}): ") or f"{event.hour}:{event.minutes}"
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
                                        f"Ωρα γεγονότος ({new_event.hour}:{new_event.minutes}): ") or f"{new_event.hour}:{new_event.minutes}"
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
                                f"Το γεγονός ενημερώθηκε: <[{new_event.title}] -> Date: {new_event.year}-{new_event.month}-{new_event.day}, Time: {new_event.hour}-{new_event.minutes}, Duration: {new_event.duration}>")
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
