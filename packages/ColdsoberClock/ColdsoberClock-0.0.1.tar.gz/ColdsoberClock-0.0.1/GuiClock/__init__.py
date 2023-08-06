from time import strftime
class clock:
    def __init__(self,label):
        self.label = label
        self.real_clock()

    def real_clock(self):
        hour = strftime("%H")
        minute = strftime("%M")
        secs = strftime("%S")
        self.label.config(text = hour +":"+minute+":"+secs)
        self.label.after(1000, self.real_clock)

    def dates(self):
        year = strftime("%Y")
        month = strftime("%b")
        day = strftime("%d")
        today_date = strftime("%a")
        output_date = year + "-" + month + "-" + day + " " + today_date
        return output_date


