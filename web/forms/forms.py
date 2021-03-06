#!/usr/bin/env python
# coding=utf-8

from web.forms import fileds


class BaseForm:
    def __init__(self):
        self._value_dict = {}
        self._error_dict = {}
        self._valid_status = True

    def valid(self, handler):

        for field_name, field_obj in self.__dict__.items():
            if field_name.startswith('_'):
                continue

            if type(field_obj) == fileds.CheckBoxField:
                post_value = handler.get_arguments(field_name, None)
            elif type(field_obj) == fileds.FileField:
                post_value = []
                file_list = handler.request.files.get(field_name, [])
                for file_item in file_list:
                    post_value.append(file_item['filename'])
            else:
                post_value = handler.get_argument(field_name, None)

            field_obj.match(field_name, post_value)
            if field_obj.is_valid:
                self._value_dict[field_name] = field_obj.value
            else:
                self._error_dict[field_name] = field_obj.error
                self._valid_status = False
        return self._valid_status
