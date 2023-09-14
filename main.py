import sys
from database_setup import conn
from func_for_project import create_project, create_dogovor, Dogovor, \
    print_column_names_dogovor, show_projects, Project, count_active_dogovor, show_active_dogovors, \
    show_projects_no_dogovors, projects_with_active_dogovor, return_active_id_dogovors_for_project


def main():
    menu = {
        'Проект': ['Создать', 'Посмотреть проекты', 'Добавить договор в проект', 'Завершить договор для проекта', 'Назад', 'Завершить'],
        'Договор': ['Создать', 'Посмотреть договора', 'Назад', 'Завершить'],
        'Завершить': '',
    }

    while True:
        print("\nОсновное меню:")
        for i, item in enumerate(menu, 1):
            print(f"{i}. {item}")

        choice = int(input("Выберите пункт меню: "))

        try:
            if choice < 1 or choice > len(menu):
                print("Неверный выбор.")
            else:
                main_menu_item = list(menu.keys())[choice - 1]
                sub_menu = menu[main_menu_item]

                if isinstance(sub_menu, list):
                    while True:
                        print(f"\nПодменю для {main_menu_item}:")
                        for j, subitem in enumerate(sub_menu, 1):
                            print(f"{j}. {subitem}")

                        sub_choice = int(input("Выберите подпункт меню: "))

                        if main_menu_item == 'Проект' and sub_choice == 1:
                            active_dogovors = count_active_dogovor()
                            if active_dogovors != 0:
                                while True:
                                    print(f'Создать проект: ')
                                    print('1. Назад')
                                    print('2. Завершить')
                                    choice_internal = input("Введите название проекта или пункт меню: ")
                                    if choice_internal.isdigit():
                                        if int(choice_internal) == 1:
                                            break
                                        elif int(choice_internal) == 2:
                                            sys.exit()
                                        else:
                                            print('Вы ошиблись при вводе')
                                    else:
                                        create_project(choice_internal)
                                        print(f"Проект \"{choice_internal}\" создан.")
                                        # break
                            else:
                                print('В БД должен быть хотя бы один активный договор')
                        elif main_menu_item == 'Проект' and sub_choice == 2:
                            show_projects()

                        elif main_menu_item == 'Проект' and sub_choice == 3:
                            while True:
                                show_projects_no_dogovors()
                                print('b. Назад')
                                print('e. Завершить')
                                some = input('Введите id проект или пункт меню: ')
                                if some == 'b':
                                    break
                                elif some == 'e':
                                    sys.exit()
                                else:

                                    with conn as connection:
                                        number = int(some)
                                        cursor = connection.cursor()
                                        cursor.execute('SELECT * FROM projects WHERE id=?',
                                                       (number,))
                                        row = cursor.fetchone()
                                        if row is not None:
                                            show_active_dogovors()
                                            print('b. Назад')
                                            print('e. Завершить')
                                            s = int(input('Введите id договора: '))
                                            if some == 'b':
                                                break
                                            elif some == 'e':
                                                sys.exit()
                                            else:
                                                d = cursor.execute('SELECT * FROM dogovors WHERE id=?', (s,))
                                                res = d.fetchone()
                                                project = Project(id=number, name=row[1])
                                                project.add_dogovor(res)
                                        else:
                                            print('Проект с указанным ID не найден.')
                        elif main_menu_item == 'Проект' and sub_choice == 4:
                            while True:
                                a = projects_with_active_dogovor()
                                print('b. Назад')
                                print('e. Завершить')
                                some = input('Введите id проект для которого завершить договор или пункт меню: ')
                                if some == 'b':
                                    break
                                elif some == 'e':
                                    sys.exit()
                                elif int(some) in a:
                                    with conn as connection:
                                        b = return_active_id_dogovors_for_project(int(some))
                                        cursor = connection.cursor()
                                        cursor.execute('SELECT * FROM dogovors WHERE id=? ', (b,))
                                        row = cursor.fetchone()
                                        if row is not None:
                                            dogovor = Dogovor(name=row[1], id=row[0])
                                            dogovor.finish()
                                else:
                                    print('Вы ошиблись')
                        elif main_menu_item == 'Проект' and sub_choice == 5:
                            break
                        elif main_menu_item == 'Проект' and sub_choice == 6:
                            sys.exit()

                        elif main_menu_item == 'Договор' and sub_choice == 1:
                            while True:
                                print(f'Создать договор: ')
                                print('1. Назад')
                                print('2. Завершить')
                                choice_internal = input("Введите название проекта или выберите пункт меню: ")
                                if choice_internal.isdigit():
                                    if int(choice_internal) == 1:
                                        break
                                    else:
                                        sys.exit()
                                else:
                                    create_dogovor(choice_internal)
                                    print(f"Договор \"{choice_internal}\" создан.\n")
                        elif main_menu_item == 'Договор' and sub_choice == 2:
                            while True:
                                print('1. Все договора')
                                print('2. Договора в статусе \"Черновик\"')
                                print('3. Договора в статусе \"Активен\"')
                                print('4. Договора в статусе \"Завершен\"')
                                print('5. Назад')
                                print('6. Завершить')
                                choice_dog = int(input("Введите пункт меню: "))
                                if choice_dog == 1:
                                    with conn as connection:
                                        cursor = connection.cursor()
                                        cursor.execute("PRAGMA table_info(dogovors)")
                                        results = cursor.fetchall()
                                        column_names = [result[1] for result in results]
                                        print(column_names)

                                        cursor.execute('SELECT * FROM dogovors')
                                        results = cursor.fetchall()

                                        for row in results:
                                            print(row)
                                elif choice_dog == 2:
                                    with conn as connection:
                                        cursor = connection.cursor()
                                        while True:
                                            print_column_names_dogovor()

                                            cursor.execute('SELECT * FROM dogovors WHERE status=?', ('Черновик',))
                                            results = cursor.fetchall()

                                            for row in results:
                                                print(row)
                                            print('b. Назад')
                                            print('e. Завершить')
                                            choice_internal = input(
                                                "Ввидите id догвора для подтверждения или пункт меню: ")
                                            if choice_internal == 'b':
                                                break
                                            elif choice_internal == 'e':
                                                sys.exit()
                                            else:
                                                with conn as connection:
                                                    number = int(choice_internal)
                                                    cursor = connection.cursor()

                                                    cursor.execute('SELECT * FROM dogovors WHERE id=? AND status=?',
                                                                   (number, 'Черновик',))
                                                    row = cursor.fetchone()
                                                    if row is not None:
                                                        dogovor = Dogovor(name=row[1], id=row[0])
                                                        dogovor.confirm()
                                                    else:
                                                        print('Договор с указанным ID не найден.')
                                elif choice_dog == 3:
                                    with conn as connection:
                                        cursor = connection.cursor()

                                        while True:
                                            print_column_names_dogovor()
                                            cursor.execute('SELECT * FROM dogovors WHERE status=?', ('Активен',))
                                            results = cursor.fetchall()
                                            for row in results:
                                                print(row)
                                            print('b. Назад')
                                            print('e. Завершить')
                                            choice_internal = input(
                                                "Ввидите id догвора для завершения или пункт меню: ")
                                            if choice_internal == 'b':
                                                break
                                            elif choice_internal == 'e':
                                                sys.exit()
                                            else:
                                                with conn as connection:
                                                    number = int(choice_internal)
                                                    cursor = connection.cursor()

                                                    cursor.execute('SELECT * FROM dogovors WHERE id=? AND status=?',
                                                                   (number, 'Активен',))
                                                    row = cursor.fetchone()
                                                    if row is not None:
                                                        dogovor = Dogovor(name=row[1], id=row[0])
                                                        dogovor.finish()
                                                        print(f'Договор с id={row[0]} завершен')
                                                    else:
                                                        print('Договор с указанным ID не найден.')
                                elif choice_dog == 4:
                                    with conn as connection:
                                        cursor = connection.cursor()
                                        print_column_names_dogovor()
                                        cursor.execute('SELECT * FROM dogovors WHERE status=?', ('Завершен',))
                                        results = cursor.fetchall()

                                        for row in results:
                                            print(row)
                                elif choice_dog == 5:
                                    break
                                else:
                                    sys.exit()
                        elif sub_choice == 3:
                            break
                        else:
                            sys.exit()
                else:
                    break
        except ValueError:
            print("Неверный выбор.")


if __name__ == '__main__':
    main()
