from tkinter import *
import requests
from datetime import date

def get_holidays():
    try:
        today = date.today()
        year = today.year
        month = today.month
        day = today.day

        url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/RU'
        response = requests.get(url, timeout=5)
        data = response.json()  # получаем список праздников в виде словарей

        # Ищем праздники именно сегодня
        today_str = f'{year}-{month:02d}-{day:02d}'
        found = []
        for holiday in data:
            if holiday['date'] == today_str:
                found.append(holiday['localName'])

        if found:
            result = f"Праздники сегодня ({day}.{month:02d}.{year}):\n\n"
            for h in found:
                result += f"• {h}\n"
        else:
            result = f"Сегодня ({day}.{month:02d}.{year}) официальных\nпраздников нет."

        output_label['text'] = result

    except Exception as e:
        output_label['text'] = f'Ошибка: {e}'

def get_next_holiday():
    try:
        today = date.today()
        url = f'https://date.nager.at/api/v3/PublicHolidays/{today.year}/RU'
        response = requests.get(url, timeout=5)
        data = response.json()

        today_str = str(today)
        # Ищем следующий праздник после сегодня
        for holiday in data:
            if holiday['date'] > today_str:
                name = holiday['localName']
                hdate = holiday['date']
                output_label['text'] = f"Ближайший праздник:\n\n• {name}\n  Дата: {hdate}"
                return

        output_label['text'] = "Праздников до конца года не найдено"

    except Exception as e:
        output_label['text'] = f'Ошибка: {e}'


root = Tk()
root.title('Праздники России')
root['bg'] = '#1a1a2e'
root.geometry('400x320')
root.resizable(False, False)

Label(root, text='Праздники России', bg='#1a1a2e',
      fg='#e94560', font=('Arial', 15, 'bold')).pack(pady=15)

Label(root, text='Источник: date.nager.at (открытое API, без ключа)',
      bg='#1a1a2e', fg='#888', font=('Arial', 8)).pack()

btn_frame = Frame(root, bg='#1a1a2e')
btn_frame.pack(pady=12)

Button(btn_frame, text='Какой сегодня праздник', command=get_holidays,
       bg='#e94560', fg='white', font=('Arial', 11, 'bold'),
       padx=8, pady=5).pack(side=LEFT, padx=5)

Button(btn_frame, text='Следующий праздник', command=get_next_holiday,
       bg='#0f3460', fg='white', font=('Arial', 11, 'bold'),
       padx=8, pady=5).pack(side=LEFT, padx=5)

frame_out = Frame(root, bg='#16213e', bd=2, relief='ridge')
frame_out.pack(padx=20, pady=5, fill='both', expand=True)

output_label = Label(frame_out, text='Нажмите кнопку!',
                     bg='#16213e', fg='#e0e0e0', font=('Arial', 11),
                     wraplength=340, justify='left', anchor='nw')
output_label.pack(padx=10, pady=10, fill='both', expand=True)

root.mainloop()
