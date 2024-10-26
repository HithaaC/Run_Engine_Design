from app.services.rule_service import create_rule, combine_rules, evaluate_rule

# Original rule strings
rule1 = "age > 30 AND department = Sales"
rule2 = "salary > 50000 OR experience > 5"

# Generate ASTs for each rule
ast1 = create_rule(rule1)
ast2 = create_rule(rule2)

# Display the ASTs for verification
print("AST for Rule 1:", ast1)
print("AST for Rule 2:", ast2)

# Combine the rules using the original strings, not the ASTs
combined_ast = combine_rules([rule1, rule2])
print("Combined AST:", combined_ast)

# Example data for evaluation
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

# Evaluate the combined rule against the data
result = evaluate_rule(combined_ast, data)
print("Evaluation Result:", result)
