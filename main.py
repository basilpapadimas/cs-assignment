from calendar import monthrange
from datetime import date, timedelta
from datetime import datetime as hourtime
import datetime
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
            return list(map(lambda x: x[0].split('-') + x[1:], csv.reader(file)))[1:]
    def read_from_month(yy, mm):
        all_events = csvrw.read()[1:]
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

class Month:
    def __init__(self, mm: int, yy: int):
        self.month = mm
        self.year = yy

    def addEvent():
        pass

    def events():
        pass


def initialize(file="events.csv"):
    global years
    years = {}

    events = CSVrw.read(file)

    for event in events:
        if event[2] not in years.keys():
            


def generate_calendar(mm: int, yy: int):
    """Given an input of month number(0 to 12) and year
    it returns a string of the calendar of the month
    including last days of last month and first days of next month
    if they so collide with the calendar

    events is a list of string type elements [Date,Hour,Duration,Title]
    so events = [[date1, hour1, duration1, title1], [date2, hour2, duration2, title2], ...]
    NO DOCTESTS?
    """

    def get_num_of_days(mm, yy):
        """Returns a tuple of type (weekday of first day of the month, number of days in given month)
        DOCTESTS LATER TO BE ADDED"""
        return monthrange(yy, mm)

    calendar_string = f"""
    {'─'*55}
       ｜{[None, 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'][mm]} {yy}｜
    {'─'*55}
    {'｜ '.join(['  ΔΕΥ', '  ΤΡΙ', '  ΤΕΤ', '  ΠΕΜ', '  ΠΑΡ', '  ΣΑΒ', '  ΚΥΡ'])}
    """

    last_days_of_last_month = [f"   {x}" for x in list(range(1, int(get_num_of_days(int(mm) -1 + 12*(1 if mm == 1 else 0) , yy)[1]) + 1))[-1 * int(get_num_of_days(mm, yy)[0]):]]

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(range(1, get_num_of_days(mm, yy)[1] + 1))]
    
    first_days_of_next_month_needed_num = [f"    {x}" for x in list(range(1, 6 - datetime.datetime(yy, mm, int(days_of_given_mm[-1].replace('[ ', '').replace(']', ''))).weekday() + 1))]
    days_to_be_printed = last_days_of_last_month + days_of_given_mm + first_days_of_next_month_needed_num

    events = CSVrw.read('events.csv')[1:]
    print(events)
    eventful_days = []
    for event in events:
        month = int(event[0].split('-')[1])
        if month == mm:
            eventful_days.append(int(event[0].split('-')[0]))

    for i in range(len(days_to_be_printed)):
        if '[' in days_to_be_printed[i]: # CHECKS IF DATE IS FROM MONTH SELECTED
            if int(days_to_be_printed[i].replace('[ ', '').replace(']', '')) in eventful_days:           #CHECKS IF DAY HAS AT LEAST ONE EVENT
                days_to_be_printed[i] = f"[*{days_to_be_printed[i].replace('[ ', '').replace(']', '')}]" # CHANGES [ DAY] TO [*DAY]

    for line in [days_to_be_printed[x:x+7] for x in range(0, len(days_to_be_printed), 7)]:
        calendar_string += '｜ '.join(line) + "\n    "
    calendar_string += '─'*55

    return calendar_string

def print_notifications():
    def convert_hh_mm_to_seconds(time_str):
        """CONVERTS HOUR TIME OF TYPE HH:MM TO seconds for easier sorting
        DOCTESTS LATER TO BE ADDED"""
        hh, mm = time_str.split(':')
        return int(hh) * 3600 + int(mm) * 60

    """Gets events and checks if they are today and after the current time and displays them in format
    [*] Notification: in {hh_till_event} hour(s) and {mins_till_event} minute(s) the programmed event '{sorted_event_names[i]}' will take place
    """
    global current_year, current_month, current_day, current_hour, current_minutes
    current_year, current_month, current_day = [int(str(x)) for x in str(date.today()).split('-')]
    current_hour, current_minutes = [int(x) for x in hourtime.now().strftime("%H:%M").split(":")]
    current_time_in_secs = convert_hh_mm_to_seconds(f'{current_hour}:{current_minutes}')

    events = CSVrw.read('events.csv')[1:]
    coming_event_hours = []
    coming_event_names = []
    for event in events:
        # initialize event details yy, mm, dd, hh, name
        event_year, event_month, event_day, event_hour, event_name = int(event[0].split('-')[2]), int(event[0].split('-')[1]), int(event[0].split('-')[0]), event[1], event[3] 
        if event_year == current_year and event_month == current_month and event_day == current_day: # checks if the event is today  
            if int(event_hour.split(':')[0]) >= current_hour:     # checks if event is after the current hour mark
                if int(event_hour.split(':')[1]) > current_hour:  # checks if event is after the current minute mark
                    coming_event_hours.append(event_hour)
                    coming_event_names.append(event_name)    
    # SORTING OF EVENTS
    time_in_sec_of_events = [convert_hh_mm_to_seconds(x) for x in coming_event_hours]  # converts all elements of event times for easier of sorting
    sorted_time_in_sec_of_events, sorted_event_names = [list(x) for x in list(zip(*sorted(zip(time_in_sec_of_events, coming_event_names))))]

    for i in range(len(sorted_event_names)):
        hh_till_event, mins_till_event = str(timedelta(seconds=sorted_time_in_sec_of_events[i] - current_time_in_secs)).split(':')[:2]
        print(f"[*] Notification: in {hh_till_event} hour(s) and {mins_till_event} minute(s) the programmed event '{sorted_event_names[i]}' will take place")


# USER END

if __name__=="__main__":
    # TODAY EVENTS NOTIFICATIONS
    print('\n')
    print_notifications()

    # NAVIGATING MONTHS 

    print('\n')
    print(generate_calendar(12, 2022))
    print('\n')
    CSVrw.read_from_month(2022, 12)