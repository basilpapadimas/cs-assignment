from calendar import monthrange
from datetime import timedelta, datetime
import os
import csv


class CSVrw:
    """read(): READS THE CSV FILE AND RETURNS A LIST OF LIST OF THE LINES
    [[LINE0 SPLITED IN COLLUMNS], [LINE1 SPLITED IN COLLUMNS], [LINE2 SPLITED IN COLLUMNS], ...]

    append(): THE event_to_write PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ARE GOING TO BE APPENDED TO THE FILE ACCORDING TO THEIR INDEX TO THE SPECIFIC COLUMN ON

    change(): THE event_to_replace PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ALREADY EXISTS IN THE FILE WHICH IS GOING TO BE REPLACED BY THE event_to_write LIST
    """

    def read(filename):
        with open(filename, 'r', newline='', encoding='cp1252') as file:
            leading_bytes = file.read(3)

            if (leading_bytes != 'ï»¿'):
                file.seek(0)
            else:
                pass

            return list(map(lambda x: Event(list(map(lambda x: int(x), x[0].split('-'))) + list(map(lambda x: int(x), x[1].split(':'))) + [int(x[2])] + [x[3]]), list(csv.reader(file))[1:]))

    def append(event_to_write):
        # TODO
        pass

    def change(event_to_write, event_to_replace):
        # TODO
        pass


class Event:
    def __init__(self, ls):
        self.day, self.month, self.year, self.hour, self.minutes, self.duration, self.title = ls
        self.startdate = datetime(
            self.year, self.month, self.day, self.hour, self.minutes)
        self.enddate = self.startdate+timedelta(minutes=self.duration)


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
            print(f"{counter}. [{event.title}] -> Date: {str(event.year)}-{str(event.month)}-{str(event.day)}, Time: {str(event.hour)}:{str(event.minutes)}, Duration: {str(event.duration)}")
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

def clear_terminal():
        os.system('cls') if os.name == 'nt' else os.system('clear')

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
    try:
        for event in years[yyyy][mm].events:
            eventful_days.add(event.day)
    except KeyError:
        print('[-]Exceeded year 2024 aborting...')
        exit()

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
    for event in years[now.year][now.month].events:
        if event.day == now.day and event.startdate > now:  # checks if the event is today
            coming_events.append(event)

    for event in coming_events:
        delta = event.startdate - timedelta(hours=now.hour, minutes=now.minute)
        print(
            f"[*] Notification: in {delta.hour} hour(s) and {delta.minute} minute(s) the programmed event '{event.title}' will take place")


def repl():
    clear_terminal()
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
                clear_terminal()
                mm, yyyy = mm % 12 + 1, yyyy + 1*(mm == 12)
                print(generate_calendar(mm, yyyy))
            case "-":
                clear_terminal()
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
                        case "1":  # TODO make new event
                            year = 0
                            while year < 2022:
                                year = int(input("Εισάγετε έτος: "))
                            month = 0
                            while not 0 < month <= 12:
                                month = int(input("Εισάγετε μήνα: "))
                            months_days = 31  # How TODO
                            day = int(input("Εισάγετε μέρα: "))
                            while not 0 < day <= months_days:
                                day = int(
                                    input(f"Εισάγετε έγκυρη μέρα (1 - {months_days}): "))
                            break
                        case "2":  # TODO delete event
                            year = 0
                            while year < 2022:
                                year = int(input("Εισάγετε έτος: "))
                            month = 0
                            while not 0 < month <= 12:
                                month = int(input("Εισάγετε μήνα: "))
                            print("=== Αναζήτηση γεγονότων ===")
                            events = years[year][month]
                            events_len = len(events.printEvents())
                            if events_len == 0:
                                print("Κανένα γεγονός αυτόν τον μήνα")
                                continue
                            event = -1
                            while not 0 <= event < events_len - 1:
                                event = int(
                                    input("Επιλέξτε γεγονός προς ενημέρωση: "))
                            event = events.events[event]
                            events.removeEvent(event)
                            print(
                                f"Το γεγονός διαγράφηκε: <[{event.name}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}-{event.minutes}, Duration: {event.duration}>")

                            break
                        case "3":  # TODO change event
                            year = 0
                            while year != 2022:
                                year = int(input("Εισάγετε έτος: "))
                            month = 0
                            while not 0 < month <= 12:
                                month = int(input("Εισάγετε μήνα: "))
                            print("=== Αναζήτηση γεγονότων ===")
                            events = years[year][month]
                            events_len = len(events.printEvents())
                            if events_len == 0:
                                print("Κανένα γεγονός αυτόν τον μήνα")
                                continue
                            event = -1
                            while not 0 <= event < events_len - 1:
                                event = int(
                                    input("Επιλέξτε γεγονός προς ενημέρωση: "))
                            event = events.events[event]
                            answer = input(
                                f"Ημερομηνία γεγονότος ({event.year}-{event.month}-{event.day}): ") or f"{event.year}-{event.month}-{event.day}"
                            event.year, event.month, event.day = list(
                                map(lambda x: int(x), answer.split("-")))
                            answer = input(
                                f"Ώρα γεγονότος ({event.hour}:{event.minutes}): ") or f"{event.hour}:{event.minutes}"
                            event.hour, event.minutes = list(
                                map(lambda x: int(x), answer.split(":")))
                            event.duration = int(input(
                                f"Διάρκεια γεγονότος ({event.duration}): ") or event.duration)
                            event.title = input(
                                f"Τίτλος γεγονότος ({event.title}): ") or event.title
                            print(
                                f"Το γεγονός ενημερώθηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}-{event.minutes}, Duration: {event.duration}>")
                            break
            case "*":
                print("=== Αναζήτηση γεγονότων ===")
                years[int(input("Εισάγετε έτος: "))][int(
                    input("Εισάγετε μήνα: "))].printEvents()
                input("Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού: ")
                print(generate_calendar(mm, yyyy))
            case "q":
                raise SystemExit(0)


if __name__ == "__main__":
    initialize()

    print('\n')
    print_notifications()
    print('\n')

    repl()
