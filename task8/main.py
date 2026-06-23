from logic import read_from_file, simplify_polynomial, save_to_file, output_polynomial


def show_menu():
    print("\n" + "=" * 60)
    print("   РАБОТА С МНОГОЧЛЕНАМИ")
    print("=" * 60)
    print("1. Вывести многочлен из файла (input.txt)")
    print("2. Привести подобные члены и сохранить результат")
    print("3. Выйти из программы")
    print("=" * 60)


def main():
    """Главная функция с меню."""
    filename = "input.txt"
    
    while True:
        show_menu()
        choice = input("Выберите пункт меню (1-3): ").strip()
        
        if choice == '1':
            print("\n--- Чтение многочлена из файла ---")
            poly, error = read_from_file(filename)
            
            if error:
                print("ОШИБКА: " + error)
            else:
                print("Исходный многочлен: " + output_polynomial(poly))
                print("Для приведения подобных используйте пункт 2.")
        
        elif choice == '2':
            print("\n--- Приведение подобных членов ---")
            
            poly, error = read_from_file(filename)
            
            if error:
                print("ОШИБКА: " + error)
                continue
            
            print("Исходный многочлен: " + output_polynomial(poly))
            
            poly = simplify_polynomial(poly)
            print("Результат упрощения: " + output_polynomial(poly))
            
            success, message = save_to_file(poly, filename)
            if success:
                print("ГОТОВО: " + message + " в файл '" + filename + "'")
            else:
                print("ОШИБКА: " + message)
        
        elif choice == '3':
            print("\nДо свидания!")
            break
        
        else:
            print("\nОШИБКА: Неверный пункт. Выберите 1, 2 или 3.")


if __name__ == "__main__":
    main()
