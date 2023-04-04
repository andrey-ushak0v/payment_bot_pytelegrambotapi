def change_keys(data: dict):
    replacements = ['Номер карты', 'срок действия', 'CVV']
    new_list = list(data.values())
    new_list.pop(4)
    new_list[2] = f'{new_list[2]}/{str(new_list[3])[2:]}'
    new_list.pop(3)
    new_list[1], new_list[2] = new_list[2], new_list[1]
    new_dict = dict(zip(replacements, new_list))
    return new_dict
