sudo gcloud compute scp /home/projects/Precipitable-Water-Model/data/file.txt thoth:/mnt/ --project tunnel-302420 --zone us-central1-a

sudo gsutil rsync /mnt/ gs://thoth-storage
