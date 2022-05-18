import re

class Symbols:

    FROZEN = '~'
    FINISH = ';'
    REPEAT = 'x'
    SERIES = '...'

class Patterns:

    SUM = r'^(sum=|\+=)(\d+(\.\d+)?):(.*)'
    COUNT = r'^(count=|\*=)(\d+):(.*)'
    BRACKETS = r'\({1}[\d,x~_. ]+\){1}'
    REPEAT = r'(.*)x(\d+?)'
    SERIES = r',?(\d+(\.\d+)?\.{3})|(\([(\d+(\.\d)*)\(\)x,~_ ]+\)\.{3});?,?'
    INTERNAL = r'[\d~]'

def pattern_match(pattern : str, expression : str):
    match_result = re.match(pattern, expression)
    return match_result is not None, match_result

def clean_expression(expression : str):
    return ','.join([val for val in expression.replace(' ','').split(',') if val != ''])

def clean_output(expression : str):
    return expression.replace(Symbols.FROZEN, ',')

def parse_repetition_expression(expression : str):

    pattern = []
    result, match = pattern_match(Patterns.REPEAT, expression)

    while result:
        value, multiplier = match.groups()
        if multiplier.isdigit():
            for i in range(int(multiplier)):
                pattern.append(value)
        expression = Symbols.FROZEN.join(pattern)
        result, match = pattern_match(Patterns.REPEAT, expression)

    return expression

def parse_simple_expression(expression : str):

    expanded_expression = expression.split(',')
    parsed_expression = []

    for exp in expanded_expression:

        if exp == '_':
            parsed_expression.append('null')

        elif Symbols.REPEAT in exp:
            parsed_expression.append(parse_repetition_expression(exp))

        elif pattern_match(Patterns.INTERNAL, exp)[0]:
            parsed_expression.append(exp.replace(Symbols.SERIES, ''))

        elif exp != '':
            raise ValueError('Expression: {}\nContains unexpected characters.'.format(exp))
    
    expression = Symbols.FROZEN.join(parsed_expression)
    return expression

def parse_expression(expression : str, clean : bool = True):

    expression = clean_expression(expression)
    expression = parse_simple_expression(expression)
    
    return expression if not clean else clean_output(expression)

def parse_to_numbers(expression : str, empty : str = 0):
    parsed_expression = parse_expression(expression)
    number_list = []
    for value in parsed_expression.split(','):
        if value == 'null':
            number_list.append(empty)
        elif value.isdigit():
            number_list.append(float(value))
    return number_list
