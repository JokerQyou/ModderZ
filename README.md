# Modder2
Mod system using plugins written in Python

# Inspiration
There is a program called "Compatibility Telemetry" in Microsoft Windows 10, 
namely the executable "CompatTelRunner.exe". It will be launched sometimes, to 
send data back to Microsoft about something related to software compatibility 
problem (actually I'm not sure about what data it sends).

I'm personally OK to share some data to M$, but this program dramatically 
slow down my computer by continuously reading large amount of data from disk 
and occupying at least one CPU core. All my disks are Intel SSDs and yet I 
cannot even type fluently when this program is running.

So I got this idea that I *WILL* write a script to kill this process upon its 
execution. But I don't want to write the script along. I need a framework, or 
something that notify my script about the events it cares. Basically a sub-pub 
system for various OS and application events. That way I can write a script 
that listen on `process created` events, and kill the newly created process 
if its executable is `CompatTelRunner.exe`.

So I started writing Modder2. It's called Modder2 because I have previously 
named one of my projects "Modder".

# Requirements

You'll need wxPython to run the GUI app.

* On Windows, go to [its official site](http://wxpython.org) to download proper
 installer.
* On macOS, get [Homebrew](https://brew.sh/) and run `brew install wxPython`.
* On Linux, I'm sure you'll find the way by yourself. :P

After installing wxPython, run `pip install -r requirements.txt` to install 
other required Python packages.

# Usage
GUI is not usable at this time. You can run an instance in terminal:

```shell
python -m modder.console_app
```

# Writing mods
A mod is basically a script containing a callale (function / class method). 
You write this function, register it to some events, and when Modder2 trigger 
these events, your function get called.

A simple script would be:

```python
from modder import on


@on('Modder.Started')
def test(event):
    print 'Got event', event
```

If you put it into `modder/mods/xxx.py`, the function `test` will be triggered 
everytime Modder2 starts.

You can also trigger (`modder.trigger`) 
and listen on (`modder.on`) custom events.

Modder2 will eventually support custom mods location, but it currently does not.

# Core events
Core events are defined by Modder2 and  will only be triggered by Modder2. 
Currently there are:

* `Modder.Started`
* `Modder.BeforeQuit`
* `Timer.Interval.Minute`
* `Timer.Interval.Hour`
* `Timer.Interval.Day`

By looking at their name you will be able to tell when they get triggered.

Your registered function will be called in a separate thread. 
Specially, when `Modder.BeforeQuit` event is triggered, functions will be 
called in *current* thread.

# But...

### This is just a stupid event bus
Yes it is. Deal with it.

### It sucks
Deal with it, or contribute. Otherwise go away, you are the one who sucks.
