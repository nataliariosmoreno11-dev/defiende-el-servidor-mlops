# Ejecutar desde la raíz del repositorio
$ErrorActionPreference = "Stop"
python -m src.audit data/UNSW_NB15_training-set.csv data/UNSW_NB15_testing-set.csv
python -m src.train --config configs/v1.yaml --data data/UNSW_NB15_training-set.csv
python -m src.train --config configs/v2.yaml --data data/UNSW_NB15_training-set.csv
Write-Host "Completar dos configuraciones adicionales y registrar sus run_id en evidencias/experimentos.csv"
