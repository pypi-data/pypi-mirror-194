# stopywatch

Python 3 Simple Stopwatch

This is a simple stopwatch that can be used in Python code to profile the duration of scripts, 

## Table of Contents

1. Requirements
2. Classes / Objects
3. Functions
4. Samples

## 1. Requirements

This package leverages datetime, which is a standard Python package

## 2. Classes

### Stopwatch

This is the main and only class of the package.

#### Attributes

* ```_days```

Number of days since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_hours```

Number of hours since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_minutes```

Number of minutes since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_seconds```

Number of seconds since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_microseconds```

Number of microseconds since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_total_seconds```

Total seconds since the Stopwatch instance was started until it was stopped (if it was stopped)

* ```_started```

True if the Stopwatch is running, False otherwise

* ```_stopped```

True if the Stopwatch is not running, False otherwise

* ```_flags```

List of "times" when the Stopwatch was "paused", includes the stop time as well

#### Methods

* ```start```

Starts the Stopwatch

* ```pause```

Takes the current timestamp and creates a flag

* ```stop```

Stops the Stopwatch and creates a flag with the current timestamp

* ```reset```

Re-initializes the Stopwatch as if the instance was just created

* ```is_started```

Returns `True` if the Stopwatch is running, `False` otherwise

* ```is_stopped```

Returns `True` if the Stopwatch is NOT running, `False` otherwise

* ```print_flags```

Prints all flags to console in `dd:hh:mm:ss.s` format

* ```_calculate_delta```

Calculates the `timedelta` from the start_stamp to the current datetime or a datetime passed as the `stamp` argument

* ```_calculate_all_units```

Caculates each of the timestamp-related attributes days, hours, minutes, etc---

### Sample Code

    from stopywatch import Stopwatch
    from datetime import datetime
    from time import sleep

    timer = Stopwatch()

    timer.start()
    sleep(1)
    timer.pause()
    sleep(1)
    timer.pause()
    sleep(1)
    timer.pause()
    sleep(1)
    timer.pause()
    sleep(1)
    timer.pause()
    sleep(1)
    print(timer.get_start_stamp())
    print(timer.get_stop_stamp())
    timer.stop()
    timer.print_flags()
