# claudestaskbarstatus

claude code's thinking spinner, live in your windows taskbar next to the clock.

- working: `✻ Pontificating… (0:12)`
- needs you: `✽ needs you (0:42)`
- done: `💤 idle`

## how it works

1. three claude code hooks write a tiny `status.json` (thinking / waiting / idle, a random verb, a start time)
2. `status_server.py` reads that file and serves it as plain text at `http://127.0.0.1:8765/status`, with an animated spinner and an elapsed timer
3. the [Windhawk](https://windhawk.net) "Taskbar Clock Customization" mod polls that url and shows it in the taskbar

## setup

1. put `status_server.py` and `verbs.json` in `%USERPROFILE%\ClaudeTray` and run `python status_server.py` (needs python 3, nothing else)
2. merge `hooks.json` into your `~/.claude/settings.json` (the `hooks` section)
3. install Windhawk and the Taskbar Clock Customization mod, then in the mod settings:
   - add a web content item with url `http://127.0.0.1:8765/status`, content mode `plainText`
   - set the clock's top or bottom line to `%web1%`
   - set the web content update interval low (1 to 2 seconds) so the spinner and timer feel live

windows only. the server only listens on localhost.
