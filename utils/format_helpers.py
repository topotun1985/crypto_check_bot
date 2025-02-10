def format_crypto_price(price: float) -> str:
    """
    Форматирует цену криптовалюты, обеспечивая отображение значащих цифр.
    
    Правила:
    1. Если число >= 1, показываем 2 знака после запятой (например, 1.23)
    2. Если число < 1, показываем первые три значащие цифры
    
    Примеры:
    >>> format_crypto_price(1.23456)     # -> "1.23"
    >>> format_crypto_price(0.00287500)  # -> "0.00287"
    >>> format_crypto_price(0.00000123)  # -> "0.00000123"
    """
    if price >= 1:
        return f"{price:.2f}"
    
    # Преобразуем в строку с большим количеством знаков после запятой
    price_str = f"{price:.10f}"
    
    # Удаляем конечные нули
    price_str = price_str.rstrip('0')
    
    # Находим первую значащую цифру после нуля
    significant_digits = 0
    decimal_pos = price_str.find('.')
    
    for i, char in enumerate(price_str[decimal_pos + 1:], 1):
        if char != '0':
            significant_digits = i
            break
    
    # Добавляем еще 2 знака после первой значащей цифры
    return f"{price:.{significant_digits + 2}f}".rstrip('0').rstrip('.')
