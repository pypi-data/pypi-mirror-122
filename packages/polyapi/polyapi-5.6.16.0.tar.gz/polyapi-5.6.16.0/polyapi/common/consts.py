#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Описание типов и констант, использующихся в PPL.
"""

from typing import NewType

# типы данных
business_logic = NewType('BusinessLogic', str)
graph = NewType('Graph', str)
time_type = NewType('Time', str)
json_type = NewType('JSON', str)
datetime_type = NewType('Datetime', str)
responce = NewType('Responce', str)

# коды различных типов модулей
MULTISPHERE_ID = 500
GRAPH_ID = 600
MAP_ID = 700
ASSOCIATION_RULES_ID = 800
CLUSTERING_ID = 900
FORECAST_ID = 1000

# маппинг "код модуля - наименование модуля"
CODE_NAME_MAP = {
    MULTISPHERE_ID: 'Мультисфера',
    GRAPH_ID: 'Графика',
    MAP_ID: 'Карты',
    ASSOCIATION_RULES_ID: 'Ассоциативные правила',
    CLUSTERING_ID: 'Кластеризация',
    FORECAST_ID: 'Прогнозирование'
}

# соответствие типов, используемых Полиматикой, с типами данных Python Core
TYPES_MAP = {
    'uint8': 'integer',
    'uint16': 'integer',
    'uint32': 'integer',
    'uint64': 'integer',
    'double': 'float',
    'string': 'string',
    'date': 'date',
    'time': 'time',
    'datetime': 'datetime',
    'date_year': 'integer',
    'date_quarter': 'integer',
    'date_month': 'string',
    'date_day': 'integer',
    'date_week': 'integer',
    'date_wday': 'string',
    'time_hour': 'integer',
    'time_minute': 'integer',
    'time_second': 'integer'
}

# месяцы
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декабрь"]

# дни недели
WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

# константы, использующиеся для создания вычислимых фактов
OPERANDS = ["=", "+", "-", "*", "/", "<", ">", "!=", "<=", ">="]
LOGIC_FUNCS = ["or", "and", "not"]
FUNCS = ["top", "total", "corr"]

# прочие
ISO_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
