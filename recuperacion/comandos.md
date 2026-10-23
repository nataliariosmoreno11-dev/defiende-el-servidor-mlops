# Comandos de recuperación

Ejecutar en una carpeta nueva:

1. git clone --no-checkout <URL>
2. git checkout <commit final o commit elegido>
3. python -m venv .venv && activar el entorno
4. pip install -r requirements.txt
5. dvc pull
6. verificar SHA-256 de los CSV contra evidencias/auditoria.json
7. descargar v1 y v2 de Hugging Face por SHA completo
8. ejecutar src/predict.py sobre la misma muestra fija de validación
9. comparar salidas con recuperacion/predicciones-v1.csv y recuperacion/predicciones-v2.csv
10. registrar comandos, hashes, diferencias y logs

No reutilizar cachés de datos o modelos de la ejecución original.
