import winreg

def get_installed_software():
    """
    Сбор информации о установленном программном обеспечении из реестра Windows.
    
    Возвращает список строк, каждая из которых содержит информацию о программном обеспечении:
    название производителя, название программы и версия.
    """
    # Инициализация пустого списка для хранения информации о программах
    software_list = []
    
    # Пути к ключам реестра для 32-битных и 64-битных приложений
    keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # Ключ для 64-битных приложений
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"  # Ключ для 32-битных приложений на 64-битной ОС
    ]
    
    # Перебираем пути к ключам реестра
    for key_path in keys:
        # Пытаемся открыть ключ реестра
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        except WindowsError:
            # Если ключ не существует, продолжаем с другим ключом
            continue

        # Получаем количество подключей в текущем ключе
        num_subkeys = winreg.QueryInfoKey(key)[0]
        
        # Перебираем все подключи
        for i in range(num_subkeys):
            try:
                # Получаем имя подключа (подключа ключа реестра)
                subkey_name = winreg.EnumKey(key, i)
                
                # Открываем подключ с именем subkey_name
                subkey = winreg.OpenKey(key, subkey_name)
                
                # Получаем название производителя
                try:
                    vendor = winreg.QueryValueEx(subkey, "Publisher")[0]
                except FileNotFoundError:
                    vendor = "Неизвестно"
                
                # Получаем название программы
                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                except FileNotFoundError:
                    # Если имя программы отсутствует, пропускаем подключ
                    continue
                
                # Получаем версию программы
                try:
                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                except FileNotFoundError:
                    version = "Неизвестно"
                
                # Формируем строку с информацией о программе
                software_info = f"{vendor}\t{name}\t{version}"
                
                # Добавляем информацию о программе в список
                software_list.append(software_info)
                
            except WindowsError:
                # Если возникла ошибка при обработке подключа, продолжаем со следующим
                continue

    return software_list

if __name__ == "__main__":
    # Получаем список установленного программного обеспечения
    installed_software = get_installed_software()
    
    # Выводим список установленных программ на экран
    for software in installed_software:
        print(software)
