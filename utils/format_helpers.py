import re

def validate_threshold(value: str, i18n) -> tuple[float | None, str]:
    """Validates and formats a threshold value.
    Returns a tuple of (formatted_value, error_message).
    If validation passes, error_message will be empty.
    If validation fails, formatted_value will be None.
    
    Valid formats:
    - Integers: 1, 99, 101, 10000000
    - 1-2 decimal places: 1.1, 1.01, 2.99, 0.1, 0.77
    - 3 decimal places for values < 1: 0.001, 0.00286
    
    Constraints:
    - Maximum value: 999999999 (9 digits) to fit within database numeric(18,8) field
    """
    # Remove leading/trailing whitespace
    value = value.strip()
    
    try:
        # Try to convert to float first
        float_val = float(value)
        if float_val <= 0:
            return None, i18n.get("error-threshold-must-be-positive")
        
        # Check maximum value constraint (9 digits)
        if float_val >= 1000000000:  # 10^9
            return None, i18n.get("error-threshold-too-large")
            
        # Check if it's an integer
        if value.isdigit():
            return float_val, ""
            
        # Check if it's a decimal number
        if '.' in value:
            # Split into integer and decimal parts
            parts = value.split('.')
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                return None, i18n.get("error-threshold-invalid-format")
            
        # For numbers < 1, allow up to 5 decimal places
        if float_val < 1:
            if not re.match(r'^0\.\d{1,5}$', value):
                decimals = len(value.split('.')[1])
                return None, i18n.get("error-threshold-too-many-decimals-small", decimals=decimals)
        else:
            # For numbers >= 1, allow only 1-2 decimal places
            if not re.match(r'^\d+\.\d{1,2}$', value):
                decimals = len(value.split('.')[1])
                return None, i18n.get("error-threshold-too-many-decimals-large", decimals=decimals)
                
        return float_val, ""
        
    except ValueError:
        return None, i18n.get("error-threshold-generic")

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
