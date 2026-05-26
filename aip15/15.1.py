from tkinter import *
import requests

def get_weather():
    city = city_field.get()   
    api_key = 'fd01e11ebca52d140576efcec8ba353a'

    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': api_key, 'q': city, 'units': 'metric', 'lang': 'ru'}

    try:
        result = requests.get(url, params=params)  
        weather = result.json()                    # превращаем ответ в словарь Python

        if weather.get('cod') != 200:
            info_label['text'] = 'Город не найден!'
            return
        
        # Извлекаем нужные данные из словаря
        name  = weather['name']
        temp  = weather['main']['temp']
        feels = weather['main']['feels_like']
        desc  = weather['weather'][0]['description']
        hum   = weather['main']['humidity']

        info_label['text'] = (
            f"Город: {name}\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels}°C\n"
            f"Погода: {desc}\n"
            f"Влажность: {hum}%"
        )
    except Exception as e:
        info_label['text'] = f'Ошибка: {e}'


root = Tk()                                # Tk() — создаёт главное окно приложения
root['bg'] = '#f0f4f8'                     # цвет фона окна
root.title('Погодное приложение')          # заголовок в верхней панели окна
root.geometry('350x300')                   # размер окна: 350 пикселей шириной, 300 высотой
root.resizable(False, False)               # запрещаем изменять размер окна

# ВЕРХНИЙ ФРЕЙМ (рамка для поля ввода и кнопки)
frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.3)

Label(frame_top, text='Введите город:', bg='#ffb700').pack(pady=2)

# Entry — поле для ввода текста
city_field = Entry(frame_top, bg='white', font=16, justify='center')
city_field.pack(pady=2, fill='x', padx=5)

# Button — кнопка; command= указывает, какую функцию вызвать при нажатии
Button(frame_top, text='Узнать погоду', command=get_weather,
       bg='#e65c00', fg='white').pack(pady=4)

# НИЖНИЙ ФРЕЙМ (для вывода результата)
frame_bottom = Frame(root, bg='white', bd=3, relief='groove')
frame_bottom.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.52)

# Label — текстовая метка
info_label = Label(frame_bottom, text='Введите город и нажмите кнопку',
                   bg='white', font=('Arial', 10), justify='left',
                   wraplength=250, anchor='nw')
info_label.pack(padx=10, pady=10, fill='both')

root.mainloop()  # запускаем главный цикл
