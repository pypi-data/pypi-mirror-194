from datetime import datetime, timedelta

"""
Class: Stopwatch

This class aims to mimic the behavior of a regular stopwatch
"""
class Stopwatch:
# Overrides #
  """
  Function: __init__

  Initialization of the instance
  """
  def __init__(self):
    self.days = 0
    self.hours = 0
    self.minutes = 0
    self.seconds = 0
    self.total_seconds = 0.0
    self.microseconds = 0
    self.started = False
    self.stopped = False
    self.flags = []
    self.start_stamp = None

  """
  Function: __str__

  Returns the timer as a String
  """
  def __str__(self):
    return(f"{self.days}:{self.hours:02}:{self.minutes:02}:{self.seconds:02}.{self.microseconds}")

# Public Functions #
  """
  Function: start
  
  Starts the stopwatch.
  Sets the attribute start_stamp to current timestamp
  """
  def start(self):
    self.start_stamp = datetime.now()
    self.started = True

  """
  Function: pause
  
  Pauses the stopwatch, doesn't stop it, 
  just adds a flag at the time of calling and
  sets the attribute stop_stamp to current timestamp
  """
  def pause(self):
    self.stop_stamp = datetime.now()
    self.calculateDelta(stamp=self.stop_stamp)
    flag = {
      "days": self.days,
      "hours": self.hours,
      "minutes": self.minutes,
      "seconds": self.seconds,
      "total_seconds": self.total_seconds,
      "microseconds": self.microseconds
    }
    self.flags.append(flag)
    print(flag)

  """
  Function: stop
  
  Stops the stopwatch, adds a final flag at the time of calling and
  sets the attribute stop_stamp to current timestamp
  """
  def stop(self):
    self.stop_stamp = datetime.now()
    self.stopped = True
    self.started = False
    self.calculateDelta(stamp=self.stop_stamp)
    flag = {
      "days": self.days,
      "hours": self.hours,
      "minutes": self.minutes,
      "seconds": self.seconds,
      "total_seconds": self.total_seconds,
      "microseconds": self.microseconds
    }
    self.flags.append(flag)

  """
  Function: reset

  Calls __init__ to re-initialize the stopwatch
  """
  def reset(self):
    self.__init__()

  """
  Function: print_flags

  Prints all flags stored in the stopwatch
  """
  def print_flags(self):
    for flag in self.flags:
      print(f"{flag['days']:02}:{flag['hours']:02}:{flag['minutes']:02}:{flag['seconds']:02}.{int(flag['microseconds']*10000)}")

  # Internal Functions #

  def calculateDelta(self, stamp: datetime):
    if stamp is None:
      if self.stop_stamp is not None:
        delta = self.stop_stamp - self.start_stamp
      else:
        delta = datetime.now() - self.start_stamp
    else:
      delta = stamp - self.start_stamp
    calcs = self.calculateAllUnits(delta=delta)
    self.days = calcs["days"]
    self.hours = calcs["hours"]
    self.minutes = calcs["minutes"]
    self.seconds = calcs["seconds"]
    self.microseconds = calcs["microseconds"]
    self.total_seconds = calcs["total_seconds"]

  def calculateAllUnits(self, delta: timedelta):
    total_seconds = delta.total_seconds()
    print(f"THIS IS TOTAL_SECONDS {total_seconds}")
    days = int( delta.total_seconds() // (60*60*24))
    if days > 0:
      hours = int((delta.total_seconds() - (days*24*60*60)) % (60*60))
    else:
      hours = int(delta.total_seconds() // (60*60))
    if hours > 0:
      minutes = int((delta.total_seconds() - (days*24*60*60) - (hours*60*60)) % (60))
    else:
      minutes = int(delta.total_seconds() // 60)
    if minutes > 0:
      seconds = int((delta.total_seconds() - (days*24*60*60) - (hours*60*60) - (minutes*60)))
    else:
      seconds = int(delta.total_seconds())
    microseconds = (total_seconds - delta.total_seconds())
    return {
      "total_seconds": total_seconds,
      "days": days,
      "hours": hours,
      "minutes": minutes,
      "seconds": seconds,
      "microseconds": microseconds
    }

