# claudestaskbarstatus

claude code's thinking spinner, live in your windows taskbar next to the clock.

- working: `✻ Pontificating… (0:12)`
- needs you: `✽ needs you (0:42)`
- done: `💤 idle`

## how it works

1. three claude code hooks write a tiny `status.json` (thinking / waiting / idle, a random verb, a start time)
2. `status_server.py` reads that file and serves it as plain text at `http://127.0.0.1:8765/status`, with an animated spinner and an elapsed timer
3. the [Windhawk](https://windhawk.net) "Taskbar Clock Customization" mod polls that url and shows it in the taskbar

## instructions

**using claude code? just tell it:** `set this up for me, follow forclaude/SETUP.md` (clone this repo first). it does the file and hook parts for you and walks you through the Windhawk part.

**doing it by hand (windows, python 3 required):**

1. make the folder `%USERPROFILE%\ClaudeTray` and put `status_server.py` and `verbs.json` in it.
2. open `%USERPROFILE%\.claude\settings.json` and merge the `hooks` section from `hooks.json` into it. if you already have hooks for `UserPromptSubmit`, `Stop` or `Notification`, add these next to yours instead of replacing them.
3. start the server: open a terminal and run `pythonw "%USERPROFILE%\ClaudeTray\status_server.py"`. to have it start at login, put a shortcut to that command in `shell:startup`.
4. check it: open `http://127.0.0.1:8765/status` in a browser. you should see `💤 idle`.
5. install [Windhawk](https://windhawk.net), then install the mod "Taskbar Clock Customization".
6. apply the one-line patch below in the mod's source tab, compile, and enable it.
7. in the mod settings:
   - add a web content item, url `http://127.0.0.1:8765/status`, content mode `plainText`
   - set the top line or bottom line to `%web1%`
   - set the web content update interval to `1`
8. restart claude code so it loads the hooks, send a message, and watch the taskbar.

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
