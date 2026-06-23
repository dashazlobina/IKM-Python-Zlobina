from logic20 import build_tree, tree_to_string, simplify_tree


def main():
    print("УПРОЩЕНИЕ ФОРМУЛ")
    print("Пример: (a * b + a * c)")
    print("=" * 60)
    
    expr = input("Введите формулу: ").strip()
    
    if not expr:
        print("ОШИБКА: Вы не ввели формулу.")
        return
    
    try:
        tree = build_tree(expr)
        if tree is None:
            print("ОШИБКА: Не удалось построить дерево.")
            return
        
        print("\nИсходная формула: " + tree_to_string(tree))
        
        simplified = simplify_tree(tree)
        print("Упрощенная формула: " + tree_to_string(simplified))
        
    except Exception as e:
        print("ОШИБКА: " + str(e))


if __name__ == "__main__":
    main()
  
