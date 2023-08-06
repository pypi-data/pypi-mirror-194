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
    self._days = 0
    self._hours = 0
    self._minutes = 0
    self._seconds = 0
    self._total_seconds = 0.0
    self._microseconds = 0
    self._started = False
    self._stopped = False
    self._flags = []
    self._start_stamp = None
    self._stop_stamp = None

  """
  Function: __str__

  Returns the timer as a String
  """
  def __str__(self):
    return(f"{self._days}:{self._hours:02}:{self._minutes:02}:{self._seconds:02}.{self._microseconds}")

# Getters and Setters #
  """
  Function: get_days

  Returns the latest days measurement in the stopwatch
  """
  def get_days(self):
    return self._days

  """
  Function: get_hours

  Returns the latest hours measurement in the stopwatch
  """
  def get_hours(self):
    return self._hours

  """
  Function: get_minutes

  Returns the latest minutes measurement in the stopwatch
  """
  def get_minutes(self):
    return self._minutes

  """
  Function: get_seconds

  Returns the latest seconds measurement in the stopwatch
  """
  def get_seconds(self):
    return self._seconds

  """
  Function: get_microseconds

  Returns the latest microseconds measurement in the stopwatch
  """
  def get_microseconds(self):
    return self._microseconds

  """
  Functions: get_flags

  Returns an array of flags when the Stopwatch was paused including the last one when it was stopped
  """
  def get_flags(self):
    return self._flags

  """
  Function: get_start_stamp

  Returns a datetime with the timestamp when the start() method was called
  """
  def get_start_stamp(self):
    return self._start_stamp

  """
  Function: get_stop_stamp

  Returns a datetime with the last timestamp when either stop() or pause() methods were called
  """
  def get_stop_stamp(self):
    return self._stop_stamp

# Public Functions #
  """
  Function: start
  
  Starts the stopwatch.
  Sets the attribute start_stamp to current timestamp
  """
  def start(self):
    self._start_stamp = datetime.now()
    self._started = True

  """
  Function: pause
  
  Pauses the stopwatch, doesn't stop it, 
  just adds a flag at the time of calling and
  sets the attribute stop_stamp to current timestamp
  """
  def pause(self):
    self._stop_stamp = datetime.now()
    self._calculate_delta(stamp=self._stop_stamp)
    flag = {
      "days": self._days,
      "hours": self._hours,
      "minutes": self._minutes,
      "seconds": self._seconds,
      "total_seconds": self._total_seconds,
      "microseconds": self._microseconds
    }
    self._flags.append(flag)

  """
  Function: stop
  
  Stops the stopwatch, adds a final flag at the time of calling and
  sets the attribute stop_stamp to current timestamp
  """
  def stop(self):
    self._stop_stamp = datetime.now()
    self._stopped = True
    self._started = False
    self._calculate_delta(stamp=self._stop_stamp)
    flag = {
      "days": self._days,
      "hours": self._hours,
      "minutes": self._minutes,
      "seconds": self._seconds,
      "total_seconds": self._total_seconds,
      "microseconds": self._microseconds
    }
    self._flags.append(flag)

  """
  Function: reset

  Calls __init__ to re-initialize the stopwatch
  """
  def reset(self):
    self.__init__()

  """
  Function: is_started

  Returns True if the Stopwatch is running or False otherwise
  """
  def is_started(self):
    if self._started:
      if not self._stopped:
        return True
      else:
        return False

  """
  Function: is_stopped

  Returns False if the Stopwatch is running or True otherwise
  """
  def is_stopped(self):
    if not self._started:
      if self._stopped:
        return True
      else:
        return False

  """
  Function: print_flags

  Prints all flags stored in the stopwatch
  """
  def print_flags(self):
    for flag in self._flags:
      print(f"{flag['days']:02}:{flag['hours']:02}:{flag['minutes']:02}:{flag['seconds']:02}.{int(flag['microseconds']*10000)}")

  # Internal Functions #

  def _calculate_delta(self, stamp: datetime):
    if stamp is None:
      if self._stop_stamp is not None:
        delta = self._stop_stamp - self._start_stamp
      else:
        delta = datetime.now() - self._start_stamp
    else:
      delta = stamp - self._start_stamp
    calcs = self._calculate_all_units(delta=delta)
    self._days = calcs["days"]
    self._hours = calcs["hours"]
    self._minutes = calcs["minutes"]
    self._seconds = calcs["seconds"]
    self._microseconds = calcs["microseconds"]
    self._total_seconds = calcs["total_seconds"]

  def _calculate_all_units(self, delta: timedelta):
    total_seconds = delta.total_seconds()
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

