import tkinter as tk
import json
import requests
from time import strftime
from datetime import datetime

def get_prayer_times(city, country):
    apiRequest = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}")
    api = json.loads(apiRequest.content)

    fajr = "الفجر : " + api["data"]["timings"]["Fajr"]
    zuhr = "الظهر : " + api["data"]["timings"]["Dhuhr"]
    asr = "العصر : " + api["data"]["timings"]["Asr"]
    maghrib = "المغرب : " + api["data"]["timings"]["Maghrib"]
    eisha = "العشاء : " + api["data"]["timings"]["Isha"]

    HijriWeekDay = api["data"]["date"]["hijri"]["weekday"]["ar"]
    HijriDay = api["data"]["date"]["hijri"]["day"]
    HijriMonth = api["data"]["date"]["hijri"]["month"]["ar"]
    HijriYear = api["data"]["date"]["hijri"]["year"]
    HijriDateAR = HijriWeekDay + " " + HijriDay + " " + HijriMonth + " " + HijriYear
    #HijriDateInArabic= HijriDateAR

    WeekDay = api["data"]["date"]["gregorian"]["weekday"]["en"]
    Day = api["data"]["date"]["gregorian"]["day"]
    Month = api["data"]["date"]["gregorian"]["month"]["en"]
    Year = api["data"]["date"]["gregorian"]["year"]
    Gregorian = WeekDay + " " + Day + " " + Month + " " + Year
    GregorianDate = Gregorian

    return fajr, zuhr, asr, maghrib, eisha, HijriDateAR, GregorianDate

def customize():
    global button_switch
    if button_switch:
        button.config(image=off, bg="#2a2a2a", activebackground="#2a2a2a")
        root.config(bg="#2a2a2a")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#2a2a2a")
        button_switch = False
    else:
        button.config(image=on, bg="#dbdbdb", activebackground="#dbdbdb")
        root.config(bg="#dbdbdb")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#dbdbdb")
        button_switch = True

def countdown(t):
    if t >= -1:
        hrs, rest = divmod(t, 3600)
        mins, secs = divmod(rest, 60)
        timer_label.config(text='{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs))
        timer_label.after(1000, countdown, t - 1)
        if hrs == 00 and mins == 00:
            timer_label.config(text='{:02d}'.format(secs))
        if t == 0: 
            timer_label.config(text="حان موعد الصلاة", font=('Digistyle Unicode', 20), padx=75)
        if t==-1:
            timer_label.after(4000)
    else:
        list_next_of_salat = [(datetime.strptime(prayer_times[0].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[1].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[2].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[3].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[4].split(": ")[1], '%H:%M') - datetime.now()).seconds]
        timer_label.config(font=("ds-digital", 24), padx=20, pady=20, width=7)
        countdown(min(list_next_of_salat))

def get_weather():
    api_key = "9da2fc92c5b469c44b1f47be532ee721"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data["main"]["temp"]
    temperature_rounded = round(temperature)
    weather_label["text"] = f"{temperature_rounded}°C"
    weather_label.after(900000, get_weather) #Bug : after it call(15 min) weather info, never back to call again.
    
def clock():
    tick = strftime('%H:%M:%S %p')
    clock_label.config(text=tick)
    clock_label.after(1000, clock)

root = tk.Tk()
root.title('Times Of Salaty')
root.config(bg="#dbdbdb")
root.minsize(400, 400)

city = "El Oued"
country = "dz"
prayer_times = get_prayer_times(city, country)

on = tk.PhotoImage(file="light.png")
off = tk.PhotoImage(file="dark.png")

button_switch = True

button = tk.Button(root, image=on, bd=0, bg="#dbdbdb", activebackground="#dbdbdb", command=lambda: customize())
button.pack(pady=5, padx=5)

space = tk.Label(root, bg="#dbdbdb").pack()

clock_label = tk.Label(root, font=('ds-digital', 40, 'bold'), pady=8, foreground='red', bg="#dbdbdb")
clock_label.pack(anchor='center')

space = tk.Label(root, bg="#dbdbdb").pack()
space = tk.Label(root, bg="#dbdbdb").pack()

hijrilabel = tk.Label(root, text=prayer_times[5], font=('Digistyle Unicode', 20, 'bold'), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
egualLabel = tk.Label(root, text="الموافق لِ", font=('Digistyle Unicode', 20, 'bold'), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
englislabel = tk.Label(root, text=prayer_times[6], font=('Digistyle Unicode', 20, 'bold'), pady=5, padx=5, fg='red',bg="#dbdbdb").pack()

space = tk.Label(root, bg="#dbdbdb").pack()
space = tk.Label(root, bg="#dbdbdb").pack()

awkatlabel = tk.Label(root, text="｡ﾟ☆. أوقات الصلاة ｡ﾟ☆.", font=('Digistyle Unicode', 20, 'bold'), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()

space = tk.Label(root, bg="#dbdbdb").pack()

fajrLabel = tk.Label(root, text=prayer_times[0], font=('Digistyle Unicode', 20), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
zuhrLabel = tk.Label(root, text=prayer_times[1], font=('Digistyle Unicode', 20), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
asrLabel = tk.Label(root, text=prayer_times[2], font=('Digistyle Unicode', 20), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
maghribLabel = tk.Label(root, text=prayer_times[3], font=('Digistyle Unicode', 20), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()
eishaLabel = tk.Label(root, text=prayer_times[4], font=('Digistyle Unicode', 20), pady=5, padx=5, fg='red', bg="#dbdbdb").pack()

space = tk.Label(root, bg="#dbdbdb").pack()
space = tk.Label(root, bg="#dbdbdb").pack()

list_next_of_salat = [(datetime.strptime(prayer_times[0].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[1].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[2].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[3].split(": ")[1], '%H:%M') - datetime.now()).seconds,
                      (datetime.strptime(prayer_times[4].split(": ")[1], '%H:%M') - datetime.now()).seconds]

timer_label = tk.Label(root, font=("ds-digital", 24), padx=20, pady=20, width=7, foreground='red', bg="#dbdbdb")
timer_label.pack(side=tk.RIGHT)

weather_label = tk.Label(root, font=("ds-digital", 24), padx=20, pady=20, width=7, foreground='red', bg="#dbdbdb")
weather_label.pack(side=tk.LEFT)

countdown(min(list_next_of_salat))
get_weather()
clock()

root.mainloop()