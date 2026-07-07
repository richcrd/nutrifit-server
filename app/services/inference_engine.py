from app.services.calculations import calculate_imc, calculate_recommended_water_ml
from app.respositories.rule_repository import get_active_rules

def matches_rule(evaluated_value, operator, min_value, max_value):
  if operator == ">":
    return evaluated_value > float(min_value)
  elif operator == "<":
    return evaluated_value < float(min_value)
  elif operator == ">=":
    return evaluated_value >= float(min_value)
  elif operator == "<=":
    return evaluated_value <= float(min_value)
  elif operator == "BETWEEN":
    return float(min_value) <= evaluated_value <= float(max_value)
  else:
    return False

def get_value_by_field(field, calculated_values):
  if field in calculated_values:
    return calculated_values[field]
  else:
    return None

def evaluate_rules(rules, calculated_values):
  diagnostic_found = None
  recommendations_found = []

  for rule in rules:
    evaluated_value = get_value_by_field(rule.field, calculated_values)

    if evaluated_value is None:
      continue

    matches = matches_rule(evaluated_value, rule.operator, rule.min_value, rule.max_value)

    if matches:
      diagnostic_found = rule.found
      recommendations_found = rule.recommendations
      break

  return diagnostic_found, recommendations_found

def process_consultation(db, weight_kg, height_cm, age, genre):
  imc = calculate_imc(weight_kg, height_cm)
  recommended_water_ml = calculate_recommended_water_ml(weight_kg, genre)

  calculated_values = {
    "imc": imc,
    "age": age,
    "recommended_water_ml": recommended_water_ml,
  }

  rules = get_active_rules(db)
  diagnostic, recommendations = evaluate_rules(rules, calculated_values)

  result = {
    "imc_calculated": imc,
    "recommended_water_ml": recommended_water_ml,
    "diagnostic": diagnostic,
    "recommendations": recommendations,
  }

  return result
