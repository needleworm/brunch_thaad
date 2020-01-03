import brunch_thaad as bts
import time

logfile = str(time.time()) + "txt"
thaad = bts.THAAD("kill_pages.txt", logfile)

while True:
    thaad.run_thaad()
    time.sleep(3)
