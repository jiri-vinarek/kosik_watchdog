# About
The script checks availability of delivery slots at https://www.kosik.cz/ and sends an email when a free slot is present.

# Installation
The setup below is for Windows 10.

## Selenium
- Find used Chrome version - `Help > About Google Chrome`.
- Install Selenium chrome driver from https://chromedriver.chromium.org/downloads.

## Python
- Download and install Anaconda from https://www.anaconda.com/distribution/#download-section.
- Run _Anaconda Prompt_ application
  - Install pip - run `conda install -c anaconda pip`.
  - Navigate with `cd` to the directory with repository and install packages - run `pip install -r requirements.txt`.

## Script configuration
- Create and setup a gmail email account used for sending emails. See _Option 1_ at https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development.
- Update configuration in `kosik_watchdog.py`. Change variables `PATH_TO_CHROMEWEBDRIVER`, `ADDRESSES`, `WATCHDOG_EMAIL` and `WATCHDOG_PASSWORD`.

## Periodic script execution
- Change paths in `run_script.bat`
- Add chromedriver to run at startup. See https://www.howtogeek.com/228467/how-to-make-a-program-run-at-startup-on-any-computer/.
- Setup windows Task scheduler to run `run_script.bat` periodically. See https://stackoverflow.com/a/4250516/11238203.
  - In _General_ set _Run whether user is logged on or not_
  - _Triggers_ - _At system startup_, repeat every 15 minutes. Please, be reasonable with the periodic execution and do not abuse the system.
