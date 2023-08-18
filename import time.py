from datetime import datetime

now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)