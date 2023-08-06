from locale import getdefaultlocale

locale, _ = getdefaultlocale()
strings = {
    "pl_PL": {
        "pause": "Wstrzymaj",
        "pause_label": "Wstrzymanie działania na czas: ",
        "settings": "Ustawienia",
        "tr": "Czas przypomnienia: ",
        "tn": "Czas nękania: ",
        "ing": "Zwiększaj głośność nękania",
        "exit": "Zakończ",
        "resume": "Wznów",
        "suffix_minutes": " minut(y)",
        "suffix_seconds": " sekund(y)",
        "auto": "automatycznie",
        "lin_autostart": "Uruchamiaj wraz ze startem Linuksa",
        "win_autostart": "Uruchamiaj wraz ze startem Windows",
        "hint": "Kliknij aby wstrzymać/wznowić działanie",
        "woitm": "Działaj tylko w przedziale czasowym",
        "time_from": "Od ",
        "time_to": " do ",
    }
}
TITLE = "AwakeGuardian"
HINT = strings.get(locale, {}).get("hint", "Click to pause/resume")
PAUSE = strings.get(locale, {}).get("pause", "Pause")
PAUSE_LABEL = strings.get(locale, {}).get("pause_label", "Pause for")
SETTINGS = strings.get(locale, {}).get("settings", "Settings")
TR = strings.get(locale, {}).get("tr", "Time of reminder")
TN = strings.get(locale, {}).get("tn", "Time of nagging")
ING = strings.get(locale, {}).get("ing", "Increment volume when nagging")
EXIT = strings.get(locale, {}).get("exit", "Exit")
RESUME = strings.get(locale, {}).get("resume", "Resume")
SUFFIX_MINUTES = strings.get(locale, {}).get("suffix_minutes", " minute(s)")
SUFFIX_SECONDS = strings.get(locale, {}).get("suffix_seconds", " second(s)")
STR_AUTO = strings.get(locale, {}).get("auto", "automatically")
LIN_AUTOSTART = strings.get(locale, {}).get("lin_autostart", "Run on Linux startup")
WIN_AUTOSTART = strings.get(locale, {}).get("win_autostart", "Run on Windows startup")
WOITM = strings.get(locale, {}).get("woitm", "Work only in a time range")
TIME_FROM = strings.get(locale, {}).get("time_from", "From ")
TIME_TO = strings.get(locale, {}).get("time_to", " to ")
