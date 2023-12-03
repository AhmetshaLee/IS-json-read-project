import PySimpleGUI as sg
import json

sg.theme('GrayGrayGray')

def display_edit_mode():
    window['-ADD-'].update(disabled=True)
    window['-REMOVE-'].update(disabled=True)

    window['-NAME-'].update(disabled=False)
    window['-SURNAME-'].update(disabled=False)
    window['-BIRTHDATE-'].update(disabled=False)

def display_save_mode():
    window['-ADD-'].update(disabled=True)
    window['-REMOVE-'].update(disabled=True)

    window['-NAME-'].update(disabled=False)
    window['-SURNAME-'].update(disabled=False)
    window['-BIRTHDATE-'].update(disabled=False)

menu_layout = [
    ['&Действие', ['Создать json', 'Выбрать json']]
]

toolbar_buttons = [[
    sg.Button('ADD', button_color=(sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-ADD-'),
    sg.Button('EDIT', button_color=(sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-EDIT-'),
    sg.Button('SAVE', button_color=(sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-SAVE-'),
    sg.Button('REMOVE', button_color=(sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-REMOVE-'),
]]

left_col = [
    [sg.Text('Список')],
    [sg.Listbox(values=['Текст для проверки'], size=(35, 25), font=('None 12'), key='-LISTBOX-', enable_events=True)],
    [sg.Button('Выбрать', key='-SELECT_BTN-')]
]

right_col = [
    [sg.Text('Имя'), sg.Push(), sg.InputText(size=(30,1), key='-NAME-', disabled=True)],
    [sg.Text('Фамилия'), sg.Push(), sg.InputText(size=(30,1), key='-SURNAME-', disabled=True)],
    [sg.Text('Дата рождения'), sg.Push(), sg.InputText(size=(30,1), key='-BIRTHDATE-', disabled=True)],
]

main_layout = [
    [sg.Menu(menu_layout,)],
    [sg.Frame('Инструменты', toolbar_buttons)],
    [sg.Column(left_col, element_justification='c'), sg.VSeparator(), sg.Column(right_col, vertical_alignment='t')],
    [sg.StatusBar(f'file1, file2')]
]

window = sg.Window('работа с JSON', main_layout, resizable=False)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Создать json':
        default_file_name = 'users1.json'
        with open(default_file_name, 'w', encoding='utf-8') as file:
            users = {}
            json.dump(users, file)
        sg.popup(f'Файл с именем по умолчанию {default_file_name} создан!')


    elif event == 'Выбрать json':
        file_path = sg.popup_get_file('Выбрать json файл', no_window=True, file_types=(('JSON Files', '*.json'),))

        with open(file_path, 'r', encoding='utf-8') as json_data:
            users_data = json.load(json_data)

        if 'users' not in users_data:
            users_data['users'] = []
            print('add')
        

        users_list = [f"{user['first_name']} {user['last_name']}" for user in users_data['users']]
        window['-LISTBOX-'].update(users_list)

        with open(file_path, 'r+', encoding='utf-8') as file:
            json.dump(users_data, file, indent=4, ensure_ascii=False)


    elif event == '-SELECT_BTN-':

        text_inputs = {
        'first_name': window['-NAME-'],
        'last_name': window['-SURNAME-'],
        'birth_date': window['-BIRTHDATE-'],
        }

        selected_users = values['-LISTBOX-']
        user_index = window['-LISTBOX-'].get_indexes()[0]

        for key, input_elem in text_inputs.items():
            input_elem.update(users_data['users'][user_index][key])


    elif event == '-EDIT-':
        display_edit_mode()

    elif event == '-SAVE-':
        window['-ADD-'].update(disabled=False)
        window['-REMOVE-'].update(disabled=False)

window.close()

try:
    with open('users.json', 'r', encoding='utf-8') as json_data:
        users = json.load(json_data)
except json.decoder.JSONDecodeError:
    users = {}
except (FileExistsError, OSError):
    with open('users.json', 'w', encoding='utf-8') as file:
        users = {}
        json.dump(users, file)

while True:
    print('Заполните следующие данные: ')

    last_name = input('Фамилия: ')
    first_name = input('Имя: ')
    patronymic = input('Отчество: ')

    birth_date = input('Дата рождения (ДД.ММ.ГГГГ): ')
    birth_place = input('Место рождения (Город — Регион — Страна): ')

    live_place = input('Место фактического проживания (Регион — Город — Адрес): ')

    gender = input('Пол (М/Ж): ')
    marital_status = input('Семейное положение (Женат/Замужем): ')
    child_info = input('Сведения о детях (Есть/Нет): ')

    passport = input('Паспортные данные (Серия и №): ')
    inn_number = input('ИНН: ')

    phone = input('Номер телефона (Если несколько, то перечислить): ')
    email = input('E-mail (Почта): ')

    # city = input('Город: ')
    # address = input('Улица: ')
    # b_day, b_month, b_year = birth_date.split('.')
    birth_city, birth_region, birth_country = birth_place.replace(',', ' ').split()
    birth_place = ', '.join([birth_city, birth_region, birth_country])

    live_region, live_city, live_address = live_place.split(', ')
    live_place = ', '.join([live_region, live_city, live_address])

    pass_series, pass_num = passport.replace(',', ' ').split()
    passport = ' '.join([pass_series, pass_num])

    user = {
        'last_name': last_name,
        'first_name': first_name,
        'patronymic': patronymic,
        'birth_date': birth_date,
        'gender': gender,
        'marital_status': marital_status,
        'child_info': child_info,
        'passport_data': passport,
        'INN': inn_number,
        'birth_place': birth_place,
        'address': live_place,
        'phone': [phone],
        'other_data': {
            'e-mail': [email]
        }

    }

    if 'users' not in users:
        users['users'] = []
    users['users'].append(user)

    users['count'] = len(users['users'])

    choice = input('Добавить ещё пользователя? (Да/Нет): ')
    if choice.lower() in ['нет', 'no', 'n']:
        break

with open('users.json', 'r+', encoding='utf-8') as file:
    json.dump(users, file, indent=4, ensure_ascii=False)