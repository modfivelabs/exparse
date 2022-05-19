import re

class __Symbols:
    FROZEN = '~'
    FINISH = ';'
    REPEAT = 'x'
    SERIES = '...'

class __Patterns:
    SUM = r'^(sum=|\+=)(\d+(\.\d+)?):(.*)'
    COUNT = r'^(count=|\*=)(\d+):(.*)'
    BRACKETS = r'\({1}[\d,x~_. ]+\){1}'
    REPEAT = r'(.*)x(\d+?)'
    SERIES = r',?(\d+(\.\d+)?\.{3})|(\([(\d+(\.\d)*)\(\)x,~_ ]+\)\.{3});?,?'
    INTERNAL = r'[\d~]'

def _pattern_match(pattern, expression):
    match_result = re.match(pattern, expression)
    return match_result is not None, match_result

def _clean_output(expression):
    return expression.replace(__Symbols.FROZEN, ',')

def _parse_repetition_expression(expression):

    pattern = []
    result, match = _pattern_match(__Patterns.REPEAT, expression)

    while result:
        value, multiplier = match.groups()
        if multiplier.isdigit():
            for i in range(int(multiplier)):
                pattern.append(value)
        expression = __Symbols.FROZEN.join(pattern)
        result, match = _pattern_match(__Patterns.REPEAT, expression)

    return expression

def _parse_expression(expression):

    expanded_expression = expression.split(',')
    parsed_expression = []

    for exp in expanded_expression:

        if exp == '_':
            parsed_expression.append('null')

        elif __Symbols.REPEAT in exp:
            parsed_expression.append(_parse_repetition_expression(exp))

        elif _pattern_match(__Patterns.INTERNAL, exp)[0]:
            parsed_expression.append(exp.replace(__Symbols.SERIES, ''))

        elif exp != '':
            raise ValueError('Expression: {}\nContains unexpected characters.'.format(exp))
    
    expression = __Symbols.FROZEN.join(parsed_expression)
    return expression

def clean_expression(expression):
    return ','.join([val for val in expression.replace(' ','').split(',') if val != ''])

def parse(expression):
    expression = clean_expression(expression)
    expression = _parse_expression(expression)
    
    return _clean_output(expression)

def parse_to_numbers(expression, replace_empty=0.0):
    parsed_expression = parse(expression)
    number_list = []
    for value in parsed_expression.split(','):
        if value == 'null':
            number_list.append(replace_empty)
        elif value.isdigit():
            number_list.append(float(value))
    return number_list
