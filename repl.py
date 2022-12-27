from datetime import datetime
from re import fullmatch
from calendar_utils import generate_calendar
from calendar import monthrange
from classes import Event, Month, CSV


def getEventInfo():
    while True:
        # Get event date (registration)
        answer = input("[+] Ημερομηνία γεγονότος (yyyy-mm-dd): ")
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
        # Get event time (registrtation)
        answer = input("[+] Ωρα γεγονότος (hh:mm): ")
        if fullmatch(r"\d\d?\:\d\d", answer) == None:
            continue
        hour, minutes = map(
            lambda x: int(x), answer.split(":"))
        if not 0 <= hour <= 23 or not 0 <= minutes < 60:
            continue
        break

    while True:
        # Get event duration (registration)
        answer = input("[+] Διάρκεια γεγονότος: ")
        if answer.isdigit() and int(answer) > 0:
            duration = int(answer)
            break

    while True:
        # Get event name (registration)
        answer = input("[+] Τίτλος γεγονότος: ")
        if "," not in answer and len(answer) > 0:
            title = answer
            break
    return [year, month, day, hour, minutes, duration, title]


def updateEventInfo(event, onlyTime=False):
    while True:
        # Get event's new date
        answer = input(
            f"[+] Ημερομηνία γεγονότος ({event.year}-{event.month}-{event.day}): ") or f"{event.year}-{event.month}-{event.day}"
        if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
            continue
        year, month, day = map(lambda x: int(x), answer.split("-"))
        if year < 2022 or not 0 < month <= 12:
            continue
        months_days = monthrange(year, month)[1]
        if not 0 < day <= months_days:
            continue
        break

    while True:
        # Get event's new time
        answer = input(
            f"[+] Ώρα γεγονότος ({event.hour}:{event.minutes:02d}): ") or f"{event.hour}:{event.minutes:02d}"
        if fullmatch(r"\d\d?\:\d\d", answer) == None:
            continue
        hour, minutes = map(lambda x: int(x), answer.split(":"))
        if not 0 <= hour <= 23 or not 0 <= minutes < 60:
            continue
        break

    duration, title = event.duration, event.title
    if not onlyTime:
        while True:
            # Get event's new duration
            answer = input(
                f"[+] Διάρκεια γεγονότος ({event.duration}): ") or f"{event.duration}"
            if answer.isdigit() and int(answer) > 0:
                duration = int(answer)
                break

        while True:
            # Get event's new name
            answer = input(
                f"[+] Τίτλος γεγονότος ({event.title}): ") or f"{event.title}"
            if "," not in answer and len(answer) > 0:
                title = answer
                break
    return [year, month, day, hour, minutes, duration, title]


def eventSearch(years):
    while True:  # Get event year
        answer = input("[+] Εισάγετε έτος: ")
        if not answer.isdigit():
            continue
        year = int(answer)
        if year >= 2022:
            break

    while True:  # Get event month
        answer = input("[+] Εισάγετε μήνα: ")
        if not answer.isdigit():
            continue
        month = int(answer)
        if 0 < month <= 12:
            break

    print(f"\n{'='*37} Αναζήτηση γεγονότων {'='*37}\n")

    # Check if selected mm/yyyy has events. If events exist print them
    events_len = 0 if year not in years.keys() else len(
        years[year][month].printEvents())
    if events_len == 0:
        print("[-] Κανένα γεγονός αυτόν τον μήνα")

    return years[year][month], events_len


def repl(years):
    mm, yyyy = datetime.now().month, datetime.now().year

    while True:
        print(f"\n{'='*95}\n{generate_calendar(mm, yyyy, years)}")

        choice = input('''
Πατήστε ENTER για προβολή του επόμενου μήνα, "q" για έξοδο ή κάποια από τις παρακάτω επιλογές:
    "-" για πλοήγηση στον προηγούμενο μήνα
    "+" για διαχείριση των γεγονότων του ημερολογίου
    "*" για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα
    -> ''')

        match choice:  # requires Py3.10
            # First menu [calendar and choice for function(navigate months, edit events, print events)]
            case "":    # User enters ENTER
                mm, yyyy = mm % 12 + 1, yyyy + 1*(mm == 12)
            case "-":   # User enters "-"
                mm, yyyy = mm - 1 + 12*(mm == 1), yyyy - 1*(mm == 1)
            case "+":   # User enters "+"
                while True:  # Always expect user input
                    choice = input('''
Διαχείριση γεγονότων ημερολογίου, επιλέξτε ενέργεια:
    1 Καταγραφή νέου γεγονότος
    2 Διαγραφή γεγονότος
    3 Ενημέρωση γεγονότος
    0 Επιστροφή στο κυρίως μενού
    -> ''')
                    match choice:
                        case "0":   # If user enters 0 go to main menu
                            break

                        case "1":   # If user enters 1 get input for event registration
                            event = Event(getEventInfo())
                            if event.year not in years.keys():
                                years[event.year] = {
                                    x: Month(x, event.year) for x in range(1, 13)}
                            # Check if event (to be registered) is overlapping with another event
                            overlap = event.checkOverlap()
                            # If overlapping: loop until event is not overlapping
                            while overlap[0]:
                                print(
                                    "[+] Γεγονός έχει επικάλυψη με άλλα γεγονότα")
                                print(overlap[1])
                                event = Event(updateEventInfo(
                                    event, onlyTime=True))
                                overlap = event.checkOverlap()
                            # Register event
                            if event.year not in years.keys():
                                years[event.year] = {
                                    x: Month(x, event.year) for x in range(1, 13)}
                            years[event.year][event.month].addEvent(event)
                            print(
                                f"[+] Το γεγονός προστέθηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "2":   # If user enters 2 get input for event deletion
                            events, events_len = eventSearch(years)
                            if events_len == 0:
                                continue

                            # If events exist in selected mm/yyyy select event (for deletion)
                            while True:
                                answer = input(
                                    "[+] Επιλέξτε γεγονός προς διαγραφή: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events.events[event]
                            # Delete selected event
                            events.removeEvent(event)
                            print(
                                f"[+] Το γεγονός διαγράφηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "3":   # If user enters 3 get input for event update
                            # Print events registered in that mm/yyyy (if any)
                            events, events_len = eventSearch(years)
                            if events_len == 0:
                                continue

                            # If events exist in selected mm/yyyy select event (for update)
                            while True:
                                answer = input(
                                    "[+] Επιλέξτε γεγονός προς ενημέρωση: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events.events[event]
                            new_event = Event(updateEventInfo(event))
                            # Remove event temporarily so there are no overhead overlaps
                            years[event.year][event.month].removeEvent(event)

                            # Check if event (to be registered) is overlapping with another event
                            overlap = new_event.checkOverlap()

                            # If overlapping: loop until event is not overlapping
                            while overlap[0]:
                                print(
                                    "[-] Γεγονός έχει επικάλυψη με άλλα γεγονότα")
                                print(overlap[1])

                                new_event = Event(updateEventInfo(
                                    new_event, onlyTime=True))
                                overlap = new_event.checkOverlap()

                            # Register edited event
                            if new_event.year not in years.keys():
                                years[new_event.year] = {
                                    x: Month(x, new_event.year) for x in range(1, 13)}
                            years[new_event.year][new_event.month].addEvent(
                                new_event)
                            print(
                                f"[*] Το γεγονός ενημερώθηκε: <[{new_event.title}] -> Date: {new_event.year}-{new_event.month}-{new_event.day}, Time: {new_event.hour}:{new_event.minutes:02d}, Duration: {new_event.duration}>")
                            break

            case "*":   # If user enters "*" Then print events of entered month
                eventSearch(years)
                input(
                    "[+] Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού: ")

            case "q":
                CSV.write("events.csv", years)
                raise SystemExit(0)
