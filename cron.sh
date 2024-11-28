# Création de la tâche cron dans le crontab pour lancer le script run.sh

# Variables
run_path=$(realpath "run.sh")

# Création du cron avec le script de run 
cron_job="0 2 * * * $run_path"

# Ajout de la tâche cron au crontab
(crontab -l 2>/dev/null; echo "$cron_job") | crontab -

echo "La tâche cron a été ajoutée avec succès."