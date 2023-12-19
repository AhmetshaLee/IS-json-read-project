import PySimpleGUI as sg
import json

sg.theme('GrayGrayGray')

def display_edit_mode():
    window['-ADD-'].update(disabled=True)
    window['-REMOVE-'].update(disabled=True)

    window['-NAME-'].update(disabled=False)
    window['-SURNAME-'].update(disabled=False)
    window['-BIRTH_DATE-'].update(disabled=False)

def display_save_mode():
    window['-ADD-'].update(disabled=True)
    window['-REMOVE-'].update(disabled=True)

    window['-NAME-'].update(disabled=False)
    window['-SURNAME-'].update(disabled=False)
    window['-BIRTH_DATE-'].update(disabled=False)

def display_read_only():
    input_values = [
        '-REMOVE-',
        '-SAVE-',

        '-NAME-',
        '-SURNAME-',
        '-PATRONYMIC-',
        '-BIRTH_DATE-',
        '-BIRTH_PLACE-',
        '-LIVE_PLACE-',
        '-GENDER-',
        '-MARITAL-',
        '-CHILD_INFO-',
        '-PASSPORT-',
        '-INN-',
        '-PHONE-',
        '-EMAIL-'
    ]
    for value in input_values:
        window[value].update(disabled=True)

menu_layout = [
    ['&Действие', ['Создать json', 'Выбрать json']]
]

toolbar_buttons = [[
    sg.Button('ADD', pad=(0,0), key='-ADD-'),
    sg.Button('EDIT', pad=(0,0), key='-EDIT-'),
    sg.Button('SAVE', pad=(0,0), key='-SAVE-'),
    sg.Button('REMOVE', pad=(0,0), key='-REMOVE-'),
]]

left_col = [
    [sg.Text('Список')],
    [sg.Listbox(values=[''], size=(35, 25), font=('None 12'), key='-LISTBOX-', enable_events=True)],
    [sg.Button('Выбрать', key='-SELECT_BTN-')]
]

right_col = [
    [sg.Text('Фамилия'), sg.Push(), sg.InputText(size=(30,1), key='-SURNAME-')],
    [sg.Text('Имя'), sg.Push(), sg.InputText(size=(30,1), key='-NAME-')],
    [sg.Text('Отчество'), sg.Push(), sg.InputText(size=(30,1), key='-PATRONYMIC-')],
    [sg.Text('Дата рождения'), sg.Push(), sg.InputText(size=(30,1), key='-BIRTH_DATE-')],
    [sg.Text('Место рождения'), sg.Push(), sg.InputText(size=(30,1), key='-BIRTH_PLACE-')],
    [sg.Text('Место фактического проживания'), sg.Push(), sg.InputText(size=(30,1), key='-LIVE_PLACE-')],
    [sg.Text('Пол'), sg.Push(), sg.Combo(['Мужской', 'Женский'], size=(28,1),key='-GENDER-')],
    [sg.Text('Семейное положение'), sg.Push(), sg.Combo(['Женат', 'Замужем', '———'], size=(28,1),key='-MARITAL-')],
    [sg.Text('Сведения о детях'), sg.Push(), sg.Combo(['Присутствуют', 'Нет'], size=(28,1),key='-CHILD_INFO-')],
    [sg.Text('Паспорт (серия и номер)'), sg.Push(), sg.InputText(size=(30,1), key='-PASSPORT-')],
    [sg.Text('ИНН'), sg.Push(), sg.InputText(size=(30,1), key='-INN-')],
    [sg.Text('Номер телефона'), sg.Push(), sg.InputText(size=(30,1), key='-PHONE-')],
    [sg.Text('E-mail (Почта)'), sg.Push(), sg.InputText(size=(30,1), key='-EMAIL-')],
]

main_layout = [
    [sg.Menu(menu_layout,)],
    [sg.Frame('Инструменты', toolbar_buttons)],
    [sg.Column(left_col, element_justification='c'), sg.VSeparator(), sg.Column(right_col, vertical_alignment='t')],
    [sg.StatusBar('Файл не выбран', key='-STATUS_BAR-', auto_size_text=False)]
]

window = sg.Window('работа с JSON', main_layout, resizable=False, finalize=True)

FILE_PATH = None
display_read_only()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'Создать json':

        while True:
            FILENAME = sg.popup_get_text('Введите название для файла', default_text='users') # сменить диалоговое окно на свое (отсуствует ru перевод)
            if FILENAME is None:
                print('closed')
                break
            elif FILENAME == '': # улучшить проверку на пробелы
                sg.popup('Название файла не может быть пустым!')
            else:
                JSON_FILENAME = f'{FILENAME}.json'
                print(JSON_FILENAME)
                try:
                    with open(JSON_FILENAME, 'x', encoding='utf-8') as file:
                        users_data = {'users': []}
                        json.dump(users_data, file, indent=4, ensure_ascii=False)
                    sg.popup('created')
                    break
                except FileExistsError:
                    sg.popup('Файл с таким именем уже существует!')


    elif event == 'Выбрать json':

        try:
            FILE_PATH = sg.popup_get_file('Выбрать json файл', no_window=True, file_types=(('JSON Files', '*.json'),))
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
                if len(users_data) == 0:
                    print(f'файл пустой')
                else:
                    print(f'файл что-то содержит внутри')
                    print(f'{users_data} {type(users_data)}') # печатаем содержимое файла (проверка)

                if isinstance(users_data.get('users'), list) and 'users' in users_data:
                    if len(users_data['users']) > 0: # дополнить проверкой если внутри users отсутствуют ключи surname name patronymic (навсякий)
                        users_list = [f"{user['surname']} {user['name']} {user['patronymic']}" for user in users_data['users']]
                        window['-LISTBOX-'].update(values=users_list)
                    else:
                        window['-LISTBOX-'].update(values=['Список пользователей пуст'])
                else:
                    sg.popup(f'Файл не содержит поля [users]')

        except json.JSONDecodeError:
            sg.popup(f'Неверный формат файла JSON!')
        except FileNotFoundError:
            window['-STATUS_BAR-'].update('Вы отменили выбор файла')


    elif event == '-SELECT_BTN-':

        text_inputs = {
        'name': window['-NAME-'],
        'surname': window['-SURNAME-'],
        'birth_date': window['-BIRTH_DATE-'],
        }

        selected_users = values['-LISTBOX-']
        user_index = window['-LISTBOX-'].get_indexes()[0]

        for key, input_elem in text_inputs.items():
            input_elem.update(users_data['users'][user_index][key])


    elif event == '-ADD-':
        # позже добавить в виде функций смены режимов просмотра
        if not FILE_PATH: 
            sg.popup('Чтобы начать добавлять данные, выберите JSON файл!', title='Ошибка') 
        else: 
            print('вызов режима добавления')


    elif event == '-EDIT-':
        display_edit_mode()


    elif event == '-SAVE-':
        window['-ADD-'].update(disabled=False)
        window['-REMOVE-'].update(disabled=False)

window.close()

# try:
#     with open('users.json', 'r', encoding='utf-8') as json_data:
#         users = json.load(json_data)
# except json.decoder.JSONDecodeError:
#     users = {}
# except (FileExistsError, OSError):
#     with open('users.json', 'w', encoding='utf-8') as file:
#         users = {}
#         json.dump(users, file)

# while True:
    # print('Заполните следующие данные: ')

    # last_name = input('Фамилия: ')
    # first_name = input('Имя: ')
    # patronymic = input('Отчество: ')

    # birth_date = input('Дата рождения (ДД.ММ.ГГГГ): ')
    # birth_place = input('Место рождения (Город — Регион — Страна): ')

    # live_place = input('Место фактического проживания (Регион — Город — Адрес): ')

    # gender = input('Пол (М/Ж): ')
    # marital_status = input('Семейное положение (Женат/Замужем): ')
    # child_info = input('Сведения о детях (Есть/Нет): ')

    # passport = input('Паспортные данные (Серия и №): ')
    # inn_number = input('ИНН: ')

    # phone = input('Номер телефона (Если несколько, то перечислить): ')
    # email = input('E-mail (Почта): ')

    # city = input('Город: ')
    # address = input('Улица: ')
    # b_day, b_month, b_year = birth_date.split('.')
    # birth_city, birth_region, birth_country = birth_place.replace(',', ' ').split()
    # birth_place = ', '.join([birth_city, birth_region, birth_country])

    # live_region, live_city, live_address = live_place.split(', ')
    # live_place = ', '.join([live_region, live_city, live_address])

    # pass_series, pass_num = passport.replace(',', ' ').split()
    # passport = ' '.join([pass_series, pass_num])

    # user = {
    #     'last_name': last_name,
    #     'first_name': first_name,
    #     'patronymic': patronymic,
    #     'birth_date': birth_date,
    #     'gender': gender,
    #     'marital_status': marital_status,
    #     'child_info': child_info,
    #     'passport_data': passport,
    #     'INN': inn_number,
    #     'birth_place': birth_place,
    #     'address': live_place,
    #     'phone': [phone],
    #     'other_data': {
    #         'e-mail': [email]
    #     }

    # }

#     if 'users' not in users:
#         users['users'] = []
#     users['users'].append(user)

#     users['count'] = len(users['users'])

#     choice = input('Добавить ещё пользователя? (Да/Нет): ')
#     if choice.lower() in ['нет', 'no', 'n']:
#         break

# with open('users.json', 'r+', encoding='utf-8') as file:
#     json.dump(users, file, indent=4, ensure_ascii=False)