# Configuración DVC

Después de descargar los CSV:

dvc init
dvc add data/UNSW_NB15_training-set.csv
dvc add data/UNSW_NB15_testing-set.csv
git add data/*.dvc .dvc/config
git commit -m "data: version UNSW-NB15 partitions"

Configurar un remote accesible al docente, sin incluir credenciales:

dvc remote add -d storage <URL-del-almacenamiento>
dvc push

Conservar en la entrega la ubicación del remote y las instrucciones de acceso.
