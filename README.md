# PyRemoteDesktop
Easy tool to control one of your computers on LAN remotely.

# Used tools
* Client-server communication is based on WebSockets (Tornado framework for python).
* GUI control on server is made by pyautogui, mss and pillow (for screenshots).
* Client part is handled by pure JS.
# Install
* Clone or download zip.
* Run .../venv/bin/python3 server.py on machine you want to control.
# Usage
Print server IP address + port (50000 default) in browser on any machine on LAN and you are good to go!
