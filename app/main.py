# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.rule_service import create_rule, combine_rules, evaluate_rule

app = FastAPI()

class RuleRequest(BaseModel):
    rule_string: str

class CombineRulesRequest(BaseModel):
    rules: list

class EvaluationRequest(BaseModel):
    json_data: dict
    rule_ast: dict

@app.post("/create_rule")
async def create_rule_endpoint(request: RuleRequest):
    try:
        rule_ast = create_rule(request.rule_string)
        return {"rule_ast": rule_ast}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules")
async def combine_rules_endpoint(request: CombineRulesRequest):
    try:
        combined_rule_ast = combine_rules(request.rules)
        return {"combined_rule_ast": combined_rule_ast}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate_rule")
async def evaluate_rule_endpoint(request: EvaluationRequest):
    try:
        result = evaluate_rule(request.rule_ast, request.json_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
