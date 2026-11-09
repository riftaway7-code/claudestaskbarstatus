# setup instructions for claude

the user wants the claude code status (spinner, verb, timer) in their windows taskbar. you are setting up this repo for them. read this whole file first, then do the steps in order. tell the user what you are doing as you go, and tell them honestly which steps you could not do yourself.

## what you are building

claude code hooks write `status.json`, `status_server.py` serves it as text on `http://127.0.0.1:8765/status`, and the Windhawk "Taskbar Clock Customization" mod shows that text next to the taskbar clock.

## rules

- windows only. if the user is not on windows, stop and tell them.
- never overwrite the user's `~/.claude/settings.json`. read it, merge, write it back, and keep everything that was already there.
- back up `settings.json` to `settings.json.bak` before you touch it.
- do not install anything that is not listed here.
- the mod itself is not in this repo. the user installs it from Windhawk.

## steps

1. check python 3 is installed: `python --version`. if missing, tell the user to install it from python.org and stop until they have.

2. create the folder `%USERPROFILE%\ClaudeTray` and copy `status_server.py` and `verbs.json` from the repo root into it.

3. merge the hooks. read `hooks.json` from the repo root. for each of the three events (`UserPromptSubmit`, `Stop`, `Notification`), append its entry to the matching array under `hooks` in `~/.claude/settings.json`. create the array if it does not exist. do not remove or reorder existing entries. if the user already has an entry with the same command, skip it. validate that the result is valid json.

4. start the server and make it start at login:
   - run it now without a window: `Start-Process pythonw -ArgumentList "$env:USERPROFILE\ClaudeTray\status_server.py" -WindowStyle Hidden`
   - add a shortcut to `shell:startup` that runs `pythonw "%USERPROFILE%\ClaudeTray\status_server.py"`
   - check it works: `Invoke-RestMethod http://127.0.0.1:8765/status` should return `💤 idle`

5. check the hooks fire. tell the user the hooks load on the next claude code session, so after restarting claude code and sending any message, `%USERPROFILE%\ClaudeTray\status.json` should contain `"state":"thinking"`.

6. the Windhawk part. you probably cannot do this for the user because it is a gui and needs a compile, so walk them through it one step at a time and wait for them to confirm each one:
   1. install Windhawk from https://windhawk.net if they do not have it
   2. in Windhawk, search for and install "Taskbar Clock Customization" by m417z. this repo was made against v1.8
   3. open the mod, go to the source code tab, find the line `DWORD seconds = std::max(g_settings.webContentsUpdateInterval, 1) * 60;` (around line 1326) and delete the ` * 60` so it ends in `, 1);` (the same change is in `update-interval-seconds.patch`). if the line looks different in their version, show them what you see and ask before changing anything
   4. click compile, then enable
   5. in the mod settings, add a web content item: url `http://127.0.0.1:8765/status`, content mode `plainText`
   6. set the top line or bottom line to `%web1%`
   7. set the web content update interval to `1`
   8. the taskbar should now show `💤 idle`, and change when claude code is working

7. finish by telling the user exactly what worked, what you skipped, and what they still need to do.

## if something is wrong

- shows nothing: the server is not running. run the check in step 4.
- stuck on idle: claude code needs a restart to load the new hooks, or the hooks were not merged. check `settings.json`.
- updates only once a minute: the one line patch in step 6.3 was not applied or the mod was not recompiled.
- wrong text or garbled spinner characters: the content mode must be `plainText`.
