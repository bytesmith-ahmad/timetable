from tabulate import tabulate, SEPARATING_LINE
from datetime import datetime, time, timedelta
from typing import Type

Time = Type['time']

class Event:
    def __init__(self,_id):
        self.id = _id
        
    def __str__(self):
        return self.id

class TimeSlot:
    def __init__(self, day_of_week: int, start_time: Time, events: list[Event] = []):
        self.day_of_week = day_of_week
        self.start = self.calculate_start_datetime(start_time)
        self.end = self.start + timedelta(minutes=30)
        self.events = events if events is not None else []

    def calculate_start_datetime(self, start_time: Time) -> datetime:
        # Get the current date and time
        current_datetime = datetime.now()

        # Calculate the start datetime for the given day of the week and start time
        start_datetime = current_datetime.replace(hour=start_time.hour, minute=start_time.minute)
        start_of_week = start_datetime - timedelta(days=start_datetime.weekday())
        target_datetime = start_of_week + timedelta(days=self.day_of_week)

        return target_datetime

    def add_event(self, event):
        self.events.append(event)

    def __str__(self):
        return f"Day of the week: {self.day_of_week}, Start: {self.start_time}, End: {self.end_time}, Events: {[str(e) for e in self.events]}"

class Timetable:

    DAYS_OF_THE_WEEK = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
    TIME_FORMAT = "%H%M"
    HALFHOUR = timedelta(minutes=30)
    FAVORITE_FORMAT = "rounded_outline"
    LEFT_FLAG = '>'
    RIGHT_FLAG = '<'
    
    def __init__(self,timeslots: list[TimeSlot] = None, max_size = 48, deltaT=HALFHOUR):
        self.timeslots = timeslots
        self.deltaT = self.HALFHOUR
        self.max_size = max_size
        self._intervals = None
    #~
    
    def generate_interval_list(self) -> list[str]:
        midnight = datetime.combine(datetime.now().date(), datetime.min.time())
        F = self.TIME_FORMAT
        return self.generate_interval([],midnight,F)
    #~
    
    def generate_interval(self,_int,start,F):
        end = start + self.deltaT
        t0 = datetime.strftime(start,F)
        t1 = datetime.strftime(end,F)
        _int += [f"{t0} ~ {t1}"]
        
        # Check if the end time has exceeded midnight
        if end.date() > start.date():
            return _int  # Return the intervals if the end time is in the next day
    
        # Recursively call generate_interval with the updated start time
        return self.generate_interval(_int, end, F)
    #~
    
    def add_timeslots(self,table):
        number_of_intervals = len(table[0])
        for i in range(1,8):
            for j in range(1,number_of_intervals):
                # if start of time timeslot is in interval j, table[i][j] = "event here"  
                    table[i] += [f"TimeSlot({i},{j})"]
        return table
    #~
    
    def transpose(self, tabletime) -> list[list[str]]:
        """Takes a 7 x 48 array and returns a 48 x 7 array"""
        return list(map(list, zip(*tabletime)))
    #~
    
    def build(self):
        W = self.DAYS_OF_THE_WEEK
        intervals = self.generate_interval_list()
        
        tabletime = [[''] + intervals]
        tabletime += [[W[i]] for i in range(1,8)] # table[0] is interval, table[1] is monday, table[2] is tuesday
        tabletime = self.add_timeslots(tabletime)
        timetable = self.transpose(tabletime)

        return tabulate(
            headers='firstrow',
            tabular_data=timetable,
            tablefmt=self.FAVORITE_FORMAT
        )
    #~
    
    def insert_at(time):
        return (time * 2) - 1
    #~

##########################^

# t = Timetable()
# now = datetime.now()
# week = datetime.isoweekday(now)
# _time = now.time()
# timeS = _time.strftime("%H%M")
# delta = timedelta(minutes=30)
# dt = datetime.combine(now,_time)
# later = dt + delta
# hhmm = '%H%M'
# print(f"""
#       week is {t.DAYS_OF_THE_WEEK[week]}
#       now is {_time}
#       delta is {delta}
#       later is {later}
#       {now.strftime(hhmm)} ~ {later.strftime(hhmm)}
#       """)

############################^

ev1 = Event(1343)
ev2 = Event(345)
slot1 = TimeSlot(1,time(19,00),[ev1])
slot2 = TimeSlot(4,time(12,34),[ev1,ev2])
t = Timetable([slot1])
print(t.build())