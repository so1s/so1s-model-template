# 1. bentoml bundle
python3.8 /apps/src/main.py

# 2. bentoml build
cd /apps
echo "bentoml build ---"
bentoml build

# 2. bentoml containerize
echo "bentoml containerize ---"
bentoml containerize iris_classifier:latest -t $1:$2 --network host --verbose --platform=linux/amd64

# 3. docker push
echo "$3" | docker login --username so1s --password-stdin
docker tag $1:$2 so1s/$1:$2
docker push so1s/$1:$2