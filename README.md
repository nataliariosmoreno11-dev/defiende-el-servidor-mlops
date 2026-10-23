# Defiende el servidor · Taller evaluable MLOps

Repositorio para versionar código, datos, experimentos y modelos en la clasificación binaria de UNSW-NB15 (normal vs. ataque).

## Trazabilidad obligatoria

commit Git → referencia DVC → run MLflow → revisión Hugging Face

## Estructura

- src/: auditoría, preparación, entrenamiento y predicción.
- configs/: configuraciones reproducibles v1 y v2.
- evidencias/: auditoría, experimentos, selección, test y predicciones.
- recuperacion/: prueba en un entorno nuevo.
- mlflow/: exportación estructurada de los cuatro runs.
- data/: referencias DVC; no subir CSV masivos.

## Inicio

python -m venv .venv
pip install -r requirements.txt
dvc pull

El modelo y el umbral se eligen usando validación. El test se reserva para la evaluación final.