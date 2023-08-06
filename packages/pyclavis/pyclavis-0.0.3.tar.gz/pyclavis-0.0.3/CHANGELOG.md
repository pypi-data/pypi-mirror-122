
# Changelog


## first official release v0.0.3 - 20211010

- selected info text 
- double click on credit starts open in browser action
- fix credit name in info string
- download check in own background task (non-blocking)
- added logging
- added `--export` cmd_line command. prints tab separated credit information to stdout
- documentation
- fix delete credit
- 


## release v0.0.2 - 20211009

- ui rework
- added support for storing the master password in a `.pyclavis_key` file 
 (not recommended) in case your computer is already "protected" enough and
 pyclavis should start without the prompt
- passwort generator added
- bug fix, add password. overwrite last entry. resolved by copy values.
- listbox set_index() added
- provider data reload from disk (useful after manual external modification)
- python binary setting in config, defaults to python3
- update check on downloads tab will trigger pip install -U pyclavis
- double click in history start open in browser action
- switch to history tab after app start when history available
- single instance check, only one pyclavis is allowed to run at the same time
- 


## release v0.0.1 - 20211006 

- first unofficial release, tested on linux
- 
