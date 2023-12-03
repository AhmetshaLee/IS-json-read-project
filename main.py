import json

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