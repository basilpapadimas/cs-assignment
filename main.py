from calendar import monthrange
from datetime import date, timedelta, datetime
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

    def read_from_month(yy, mm):
        all_events = CSVrw.read()[1:]
        events_this_month = []
        #  [New Year's Eve] -> Date: 2022-12-31, Time: 23:59, Duration: 0
        for event in all_events:
                event_year, event_month, event_date, event_time, event_name, event_duration = int(event[0].split('-')[2]), int(event[0].split('-')[1]), str(event[0]), event[1], event[3], event[2]
                if event_year == current_year and event_month == current_month:
                    events_this_month.append(f"[{event_name}] -> Date: {event_date}, Time: {event_time}, Duration: {event_duration}")
        print('\n'.join(events_this_month))

    def append(event_to_write):
        # TODO
        pass
    def change(event_to_write, event_to_replace):
        # TODO
        pass

class Event:
    def __init__(self, ls):
        self.day = ls[0]
        self.month = ls[1]
        self.year = ls[2]
        self.hour = ls[3]
        self.minutes = ls[4]
        self.duration = ls[5]
        self.title = ls[6]
        self.startdate = datetime(self.year, self.month, self.day, self.hour, self.minutes)
        self.enddate = self.startdate+timedelta(minutes=self.duration)

class Month:
    def __init__(self, mm: int, yy: int):
        self.month = mm
        self.year = yy
        self.events = []

    def addEvent(self, newevent):
        self.events.append(newevent)
        self.events.sort(key=lambda x: x.startdate)

def initialize(file="events.csv"):
    global years
    years = {}

    events = CSVrw.read(file)

    for event in events:
        if event.year not in years.keys():
            years[event.year] = {x:Month(x, event.year) for x in range(1, 13)}
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

    last_days_of_last_month = [f"   {x}" for x in list(range(1, int(get_num_of_days(int(mm) -1 + 12*(1 if mm == 1 else 0) , yyyy)[1]) + 1))[-1 * int(get_num_of_days(mm, yyyy)[0]):]]

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(range(1, get_num_of_days(mm, yyyy)[1] + 1))]
    
    first_days_of_next_month_needed_num = [f"    {x}" for x in list(range(1, 6 - datetime(yyyy, mm, int(days_of_given_mm[-1].replace('[ ', '').replace(']', ''))).weekday() + 1))]
    days_to_be_printed = last_days_of_last_month + days_of_given_mm + first_days_of_next_month_needed_num

    eventful_days = set()
    for event in years[yyyy][mm].events:
        if event == mm:
            eventful_days.add(event.day)

    for i in range(len(days_to_be_printed)):
        if '[' in days_to_be_printed[i]: # CHECKS IF DATE IS FROM MONTH SELECTED
            if int(days_to_be_printed[i].replace('[ ', '').replace(']', '')) in eventful_days:           #CHECKS IF DAY HAS AT LEAST ONE EVENT
                days_to_be_printed[i] = f"[*{days_to_be_printed[i].replace('[ ', '').replace(']', '')}]" # CHANGES [ DAY] TO [*DAY]

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
    current_year, current_month, current_day = [int(str(x)) for x in str(date.today()).split('-')]
    current_hour, current_minutes = [int(x) for x in datetime.now().strftime("%H:%M").split(":")]
    '''
    now = datetime.now()

    coming_events = []
    for event in years[now.year][now.month].events:
        if event.day == now.day and event.hour >= now.hour and event.minutes > now.minute : # checks if the event is today  
            coming_events.append(event)
    
    for event in coming_events:
        delta = event.startdate - timedelta(hours=now.hour, minutes=now.minute)
        print(f"[*] Notification: in {delta.hour} hour(s) and {delta.minute} minute(s) the programmed event '{event.title}' will take place")


# USER END

if __name__=="__main__":
    initialize()

    # TODAY EVENTS NOTIFICATIONS
    print('\n')
    print_notifications()

    # NAVIGATING MONTHS 

    print('\n')
    print(generate_calendar(12, 2022))
    print('\n')
    #CSVrw.read_from_month(2022, 12) NEEDS PORTING