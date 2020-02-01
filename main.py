import brunch_thaad as bts
import time

logfile = str(time.time()) + "txt"
id = "<brunch id>"
ps = "<password>"
Kill_keywords = ["keywords here"]
thaad = bts.THAAD("kill_pages.txt", logfile, id, ps, Kill_keywords)

while True:
    thaad.run_thaad()
