docker build . -t so1s/torch-build:v1
docker push so1s/torch-build:v1

kubectl delete -f pod.yaml
kubectl apply -f pod.yaml