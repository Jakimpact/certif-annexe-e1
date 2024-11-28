cd "$(dirname "$0")"
mkdir logs
LOG_FILE="logs/run_log.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" >> $LOG_FILE
}

mkdir -p extracts/bdd_tables
mkdir -p extracts/blobs

log "Initialisation et installations"
bash install.sh

log "Lancement du script pour l'extraction des tables de la base de données"
python3 scripts/extract_bdd.py

log "Lancement du script pour l'extraction des blobs du data lake" 
python3 scripts/extract_blobs.py

log "Lancement du script pour la décompression des fichiers zip" 
python3 scripts/transform_zip.py

log "Lancement du script pour la récupération des informations des fichiers parquet"
python3 scripts/transform_parquet.py

log "Extraction terminée"