def calculate_imc(weight_kg: float, height_cm: float) -> float:
  height_cm = height_cm / 100
  imc = weight_kg / (height_cm * height_cm)
  return round(imc, 2)

def calculate_recommended_water_ml(weight_kg: float, genre: str) -> int:
  ml_per_kg = 35

  if genre == "M":
    ml_per_kg = 35
  elif genre == "F":
    ml_per_kg = 31
  else:
    ml_per_kg = 33

  return int(weight_kg * ml_per_kg)
