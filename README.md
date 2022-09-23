cd C:\Xumin\Loisaida_Energy

gcloud builds submit --tag gcr.io/loisaida/energy-emission --project=loisaida
gcloud config set run/region us-east4
gcloud run deploy --image gcr.io/loisaida/energy-emission --platform managed --project=loisaida --allow-unauthenticated
