# app/tests/test_rules.py

import pytest
from app.services.rule_service import create_rule, combine_rules, evaluate_rule

def test_create_rule():
    rule_string = "age > 30 AND department = Sales"
    ast = create_rule(rule_string)

    assert ast['type'] == 'operator'
    assert ast['value'] == 'AND'
    assert ast['left']['type'] == 'operand'
    assert ast['left']['left']['value'] == 'age'
    assert ast['left']['operator'] == '>'
    assert ast['left']['right']['value'] == '30'
    assert ast['right']['type'] == 'operand'
    assert ast['right']['left']['value'] == 'department'
    assert ast['right']['operator'] == '='
    assert ast['right']['right']['value'] == 'Sales'


# app/services/rule_service.py

def combine_rules(rules):
    """
    Combines multiple rule ASTs into a single AST using the AND operator by default.
    :param rules: List of AST nodes
    :return: Root node of the combined AST
    """
    if not rules:
        return None

    # Start with the first AST node
    combined_ast = rules[0]

    # Combine the rest of the rules into a single AST
    for rule in rules[1:]:
        combined_ast = {
            "type": "operator",
            "value": "AND",
            "left": combined_ast,
            "right": rule
        }

    return combined_ast


def test_evaluate_rule():
    rule_ast = {
        "type": "operator",
        "value": "AND",
        "left": {"type": "operand", "value": "age > 30"},
        "right": {"type": "operand", "value": "department = Sales"}
    }
    data = {"age": 35, "department": "Sales"}
    result = evaluate_rule(rule_ast, data)
    assert result == True
