set DATASTORE_DATASET=flowweb
set DATASTORE_EMULATOR_HOST=::1:8329
set DATASTORE_EMULATOR_HOST_PATH=::1:8329/datastore
set DATASTORE_HOST=http://::1:8329
set DATASTORE_PROJECT_ID=flowweb
gcloud beta emulators datastore start  --project flowweb
