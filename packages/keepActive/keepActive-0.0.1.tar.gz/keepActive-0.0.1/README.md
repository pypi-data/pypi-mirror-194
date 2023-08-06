

This library keeps the computer from going idle. It can also keep the user active in apps like MS Teams, Zoom, Slack, etc...  
<br>

**Disclaimer: This package is still under development and effectiveness may vary between OS.**

## Installation
<br>

    pip install keepActive

## Functions

<br>

`.start(time_in_minutes=None)`
<br>
Will start keeping the computer active. The `.start()` function has an optional input parameter, *time_in_minutes*, which can specify the length of time for which the function will run.
If no length of time is specified, the function will run until stopped by the `.stop()` function

`.stop()`
<br>
Will stop the ongoing iteration

<br>

## Quick Start
<br>

    from keepActive import keepActive
    keepActive.start(1) # keep the computer active for 1min 
    keepActive.stop() # end the iteration

---