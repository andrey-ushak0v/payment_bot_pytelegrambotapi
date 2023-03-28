def change_keys(data: dict):
    replacements = ['Номер карты', 'Код безопасности', 'Месяц', 'Год', 'Имя']
    list_val_data = list(data.values())
    data = dict(zip(replacements, list_val_data))
    return data
