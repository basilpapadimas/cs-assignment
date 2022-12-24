from calendar import monthrange
from datetime import date, timedelta
from datetime import datetime as hourtime
import datetime
import csv

# print(current_year, current_month, current_day, current_hour, current_minutes)

def get_num_of_days(mm, yy):
    """Returns a tuple of type (weekday of first day of the month, number of days in given month)
    DOCTESTS LATER TO BE ADDED"""
    return monthrange(yy, mm)

def convert_hh_mm_to_seconds(time_str):
    """CONVERTS HOUR TIME OF TYPE HH:MM TO seconds for easier sorting
    DOCTESTS LATER TO BE ADDED"""
    hh, mm = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60

class csvrw:
    
    """read(): READS THE CSV FILE AND RETURNS A LIST OF LIST OF THE LINES
    [[LINE0 SPLITED IN COLLUMNS], [LINE1 SPLITED IN COLLUMNS], [LINE2 SPLITED IN COLLUMNS], ...]
    
    append(): THE event_to_write PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ARE GOING TO BE APPENDED TO THE FILE ACCORDING TO THEIR INDEX TO THE SPECIFIC COLUMN ON
    
    change(): THE event_to_replace PARAMETER REQUIRES A LIST OF ELEMENTS: [DATE, HOUR, DURATION, NAME]
    WHICH ALREADY EXISTS IN THE FILE WHICH IS GOING TO BE REPLACED BY THE event_to_write LIST
    """
    def read():
        with open('events.csv', 'r', newline='', encoding='cp1252') as file:
            leading_bytes = file.read(3)

            if (leading_bytes != 'ï»¿'):
                file.seek(0)
            else:
                pass
            reader = csv.reader(file)
            return list(reader)
    def append(event_to_write):
        # TODO
        pass
    def change(event_to_write, event_to_replace):
        # TODO
        pass


def generate_calendar(mm: int, yy: int):
    """Given an input of month number(0 to 12) and year
    it returns a string of the calendar of the month
    including last days of last month and first days of next month
    if they so collide with the calendar

    events is a list of string type elements [Date,Hour,Duration,Title]
    so events = [[date1, hour1, duration1, title1], [date2, hour2, duration2, title2], ...]
    NO DOCTESTS?
    """

    separator = '─'*55
    calendar_string = f"""
    {separator}
       ｜{months[mm]} {yy}｜
    {separator}
    {'｜ '.join(days)}
    """

    last_days_of_last_month = [f"   {x}" for x in list(range(1, int(get_num_of_days(int(mm) -1 + 12*(1 if mm == 1 else 0) , yy)[1]) + 1))[-1 * int(get_num_of_days(mm, yy)[0]):]]

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(range(1, get_num_of_days(mm, yy)[1] + 1))]
    
    first_days_of_next_month_needed_num = [f"    {x}" for x in list(range(1, 6 - datetime.datetime(yy, mm, int(days_of_given_mm[-1].replace('[ ', '').replace(']', ''))).weekday() + 1))]
    days_to_be_printed = last_days_of_last_month + days_of_given_mm + first_days_of_next_month_needed_num

    events = csvrw.read()[1:]
    eventful_days = []
    for event in events:
        month = int(event[0].split('-')[1])
        if month == mm:
            eventful_days.append(int(event[0].split('-')[0]))

    for i in range(len(days_to_be_printed)):
        if '[' in days_to_be_printed[i]: # CHECKS IF DATE IS FROM MONTH SELECTED
            if int(days_to_be_printed[i].replace('[ ', '').replace(']', '')) in eventful_days: #CHECKS IF DAY HAS AT LEAST ONE EVENT
                days_to_be_printed[i] = f"[*{days_to_be_printed[i].replace('[ ', '').replace(']', '')}]" # CHANGES [ DAY] TO [*DAY]

    for line in [days_to_be_printed[x:x+7] for x in range(0, len(days_to_be_printed), 7)]:
        calendar_string += '｜ '.join(line) + "\n    "
    calendar_string += separator

    return calendar_string


# USER END

if __name__=="__main__":

    days = ['  ΔΕΥ', '  ΤΡΙ', '  ΤΕΤ', '  ΠΕΜ', '  ΠΑΡ', '  ΣΑΒ', '  ΚΥΡ']
    months = [None, 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ']
    current_year, current_month, current_day = [int(str(x)) for x in str(date.today()).split('-')]
    current_hour, current_minutes = [int(x) for x in hourtime.now().strftime("%H:%M").split(":")]
    current_time_in_secs = convert_hh_mm_to_seconds(f'{current_hour}:{current_minutes}')

    # TODAY EVENTS NOTIFICATIONS
    events = csvrw.read()[1:]
    coming_event_hours = []
    coming_event_names = []
    for event in events:
        event_year, event_month, event_day, event_hour, event_name = int(event[0].split('-')[2]), int(event[0].split('-')[1]), int(event[0].split('-')[0]), event[1], event[3]
        if event_year == current_year and event_month == current_month and event_day == current_day:
            if int(event_hour.split(':')[0]) >= current_hour:
                if int(event_hour.split(':')[1]) > current_hour:
                    coming_event_hours.append(event_hour)
                    coming_event_names.append(event_name)

    # SORING OF EVENTS
    time_in_sec_of_events = [convert_hh_mm_to_seconds(x) for x in coming_event_hours]
    sorted_time_in_sec_of_events, sorted_event_names = [list(x) for x in list(zip(*sorted(zip(time_in_sec_of_events, coming_event_names))))]
    sorted_time_in_hh_mm_of_events = [':'.join(str(timedelta(seconds=convert_hh_mm_to_seconds(x))).split(':')[:2]) for x in coming_event_hours]

    print('\n')
    print(sorted_time_in_sec_of_events, sorted_event_names)
    for i in range(len(sorted_event_names)):
        hh_till_event, mins_till_event = str(timedelta(seconds=sorted_time_in_sec_of_events[i] - current_time_in_secs)).split(':')[:2]
        print(f"[*] Notification: in {hh_till_event} hour(s) and {mins_till_event} minute(s) the programmed event '{sorted_event_names[i]}' will take place")

    # NAVIGATING MONTHS 

    print('\n')
    print(generate_calendar(1, 2022))
    print('\n')