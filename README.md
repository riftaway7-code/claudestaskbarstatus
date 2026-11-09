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
   - set the web content update interval to 1 (see the patch below, otherwise it means 1 minute)

windows only. the server only listens on localhost.

## the one-line mod patch

the stock mod treats the web content update interval as minutes, which is too slow for a live spinner. the fix is one line. in the mod's source editor in Windhawk (v1.8, around line 1326), change

```
DWORD seconds = std::max(g_settings.webContentsUpdateInterval, 1) * 60;
```

to

```
DWORD seconds = std::max(g_settings.webContentsUpdateInterval, 1);
```

then compile the mod. the interval is now in seconds. the same change is in `update-interval-seconds.patch`. i don't redistribute the mod itself, all credit for it goes to [m417z](https://github.com/m417z) and the [windhawk-mods](https://github.com/ramensoftware/windhawk-mods) repo. newer versions may already differ around that line.
