from pprint import pprint
import inspect

def introspection_info(obj) -> dict:
    object_info = {'Вызываем ли объект?': callable(obj),
                   'Модуль': inspect.getmodule(obj)}

    if type(obj) is type:  # тип объекта
        object_info['Тип объекта'] = obj
    else:
        object_info['Тип объекта'] = type(obj)

    for attr_name in dir(obj):
        if '__' in attr_name:  # атрибут является магическим методом
            if object_info.get('Магические методы'):
                object_info['Магические методы'].append(attr_name)
            else:
                object_info['Магические методы'] = [attr_name]
            continue

        if callable(getattr(obj, attr_name)):  # атрибут является функцией
            if object_info.get('Функции'):
                object_info['Функции'].append(attr_name)
            else:
                object_info['Функции'] = [attr_name]
            continue

        if object_info.get('Атрибуты'):
            object_info['Атрибуты'].append(attr_name)
        else:
            object_info['Атрибуты'] = [attr_name]

    return object_info


pprint(introspection_info(str))
pprint(introspection_info(float))
