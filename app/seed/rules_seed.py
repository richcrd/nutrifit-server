from app.db.sessions import SessionLocal
from app.models.catalog import Diagnostic, PhysicActivity, Goal
from app.models.recommendation import Recommendation
from app.models.rule import Rule

def seed():
    db = SessionLocal()

    try:
        create_diagnostics(db)
        create_physic_activity(db)
        create_goals(db)
        create_recommendations(db)
        create_rules(db)

        db.commit()
        print("Seed completed successfully")

    except Exception as error:
        db.rollback()
        print("Error during seed:", error)

    finally:
        db.close()

def create_diagnostics(db):
    names = ["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]

    for name in names:
        exists = db.query(Diagnostic).filter(Diagnostic.name == name).first()
        if exists is None:
            db.add(Diagnostic(name=name))

def create_physic_activity(db):
    names = ["Sedentario", "Ligero", "Moderado", "Intenso"]

    for name in names:
        exists = db.query(PhysicActivity).filter(PhysicActivity.name == name).first()
        if exists is None:
            db.add(PhysicActivity(name=name))

def create_goals(db):
    names = ["Perder peso", "Mantener peso", "Ganar masa muscular"]

    for name in names:
        exists = db.query(Goal).filter(Goal.name == name).first()
        if exists is None:
            db.add(Goal(name=name))

def create_recommendations(db):
    recommendations = [
        {"texto": "Caminar 45 minutos diarios", "categoria": "EJERCICIO"},
        {"texto": "Reducir el consumo de calorias", "categoria": "ALIMENTACION"},
        {"texto": "Evitar bebidas azucaradas", "categoria": "ALIMENTACION"},
        {"texto": "Aumentar el consumo de proteina", "categoria": "ALIMENTACION"},
        {"texto": "Incluir mas frutas y verduras", "categoria": "ALIMENTACION"},
        {"texto": "Mantener rutina de ejercicio actual", "categoria": "EJERCICIO"},
        {"texto": "Realizar ejercicio de fuerza 3 veces por semana", "categoria": "EJERCICIO"},
        {"texto": "Consultar con un nutricionista", "categoria": "ALIMENTACION"},
    ]

    for item in recommendations:
        exists = db.query(Recommendation).filter(Recommendation.text == item["texto"]).first()
        if exists is None:
            db.add(Recommendation(text=item["texto"], category=item["categoria"]))

    db.flush()

def create_rules(db):
    diagnostico_bajo_peso = db.query(Diagnostic).filter(Diagnostic.name == "Bajo peso").first()
    diagnostico_normal = db.query(Diagnostic).filter(Diagnostic.name == "Normal").first()
    diagnostico_sobrepeso = db.query(Diagnostic).filter(Diagnostic.name == "Sobrepeso").first()
    diagnostico_obesidad = db.query(Diagnostic).filter(Diagnostic.name == "Obesidad").first()

    recomendacion_proteina = db.query(Recommendation).filter(Recommendation.text == "Aumentar el consumo de proteina").first()
    recomendacion_nutricionista = db.query(Recommendation).filter(Recommendation.text == "Consultar con un nutricionista").first()
    recomendacion_mantener = db.query(Recommendation).filter(Recommendation.text == "Mantener rutina de ejercicio actual").first()
    recomendacion_frutas = db.query(Recommendation).filter(Recommendation.text == "Incluir mas frutas y verduras").first()
    recomendacion_caminar = db.query(Recommendation).filter(Recommendation.text == "Caminar 45 minutos diarios").first()
    recomendacion_reducir_calorias = db.query(Recommendation).filter(Recommendation.text == "Reducir el consumo de calorias").first()
    recomendacion_evitar_azucar = db.query(Recommendation).filter(Recommendation.text == "Evitar bebidas azucaradas").first()
    recomendacion_fuerza = db.query(Recommendation).filter(Recommendation.text == "Realizar ejercicio de fuerza 3 veces por semana").first()

    regla_bajo_peso = db.query(Rule).filter(Rule.name == "IMC bajo peso").first()
    if regla_bajo_peso is None:
        regla_bajo_peso = Rule(
            name="IMC bajo peso",
            field="imc",
            operator="<",
            min_value=18.5,
            max_value=None,
            diagnostic_id=diagnostico_bajo_peso.id,
            priority=1,
            active=True,
        )
        regla_bajo_peso.recommendations = [recomendacion_proteina, recomendacion_nutricionista]
        db.add(regla_bajo_peso)

    regla_normal = db.query(Rule).filter(Rule.name == "IMC normal").first()
    if regla_normal is None:
        regla_normal = Rule(
            name="IMC normal",
            field="imc",
            operator="BETWEEN",
            min_value=18.5,
            max_value=24.9,
            diagnostic_id=diagnostico_normal.id,
            priority=1,
            active=True,
        )
        regla_normal.recommendations = [recomendacion_mantener, recomendacion_frutas]
        db.add(regla_normal)

    regla_sobrepeso = db.query(Rule).filter(Rule.name == "IMC sobrepeso").first()
    if regla_sobrepeso is None:
        regla_sobrepeso = Rule(
            name="IMC sobrepeso",
            field="imc",
            operator="BETWEEN",
            min_value=25,
            max_value=29.9,
            diagnostic_id=diagnostico_sobrepeso.id,
            priority=1,
            active=True,
        )
        regla_sobrepeso.recommendations = [recomendacion_caminar, recomendacion_reducir_calorias]
        db.add(regla_sobrepeso)

    regla_obesidad = db.query(Rule).filter(Rule.name == "IMC obesidad").first()
    if regla_obesidad is None:
        regla_obesidad = Rule(
            name="IMC obesidad",
            field="imc",
            operator=">",
            min_value=30,
            max_value=None,
            diagnostic_id=diagnostico_obesidad.id,
            priority=1,
            active=True,
        )
        regla_obesidad.recommendations = [recomendacion_caminar, recomendacion_reducir_calorias, recomendacion_evitar_azucar]
        db.add(regla_obesidad)

if __name__ == "__main__":
    seed()