# app/services/rule_service.py

from app.models.ast_node import Node

def create_rule(rule_string):
    tokens = rule_string.split()
    if len(tokens) == 3:  # This handles simple expressions like 'age > 30'
        left_operand = tokens[0]
        operator = tokens[1]
        right_operand = tokens[2]

        return {
            'type': 'operand',
            'left': {
                'type': 'variable',
                'value': left_operand
            },
            'operator': operator,
            'right': {
                'type': 'value',
                'value': right_operand
            }
        }
    elif len(tokens) > 3:  # Handle expressions with logical operators like AND/OR
        operator_index = tokens.index('AND') if 'AND' in tokens else tokens.index('OR')
        left_part = ' '.join(tokens[:operator_index])
        right_part = ' '.join(tokens[operator_index + 1:])
        logical_operator = tokens[operator_index]

        return {
            'type': 'operator',
            'value': logical_operator,
            'left': create_rule(left_part),
            'right': create_rule(right_part)
        }
    else:
        raise ValueError("Invalid rule format")


def combine_rules(rules):
    combined_root = Node("operator", value="OR")
    left_rule = create_rule(rules[0])
    right_rule = create_rule(rules[1])
    combined_root.left = Node("operand", value=left_rule)
    combined_root.right = Node("operand", value=right_rule)
    return combined_root.to_dict()

def evaluate_rule(rule_ast, data):
    if rule_ast['type'] == 'operator':
        if rule_ast['value'] == 'AND':
            return evaluate_rule(rule_ast['left'], data) and evaluate_rule(rule_ast['right'], data)
        elif rule_ast['value'] == 'OR':
            return evaluate_rule(rule_ast['left'], data) or evaluate_rule(rule_ast['right'], data)
    elif rule_ast['type'] == 'operand':
        if 'value' in rule_ast and isinstance(rule_ast['value'], dict):
            return evaluate_rule(rule_ast['value'], data)
        else:
            left = rule_ast['left']['value']
            operator = rule_ast['operator']
            right = rule_ast['right']['value']

            # Convert `right` to the same type as `data[left]`
            if left in data:
                left_value = data[left]
                if isinstance(left_value, int):
                    right = int(right)
                elif isinstance(left_value, float):
                    right = float(right)
                elif isinstance(left_value, str):
                    right = str(right)

            # Perform the comparison
            if operator == '>':
                return left_value > right
            elif operator == '<':
                return left_value < right
            elif operator == '=':
                return left_value == right
    return False



def evaluate_condition(data, key, operator, value):
    if key not in data:
        return False
    if operator == '>':
        return data[key] > int(value)
    elif operator == '<':
        return data[key] < int(value)
    elif operator == '=':
        return data[key] == value
    else:
        return False
