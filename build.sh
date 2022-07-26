# 1.bentoml bundling
while :
do
    if [ ! -d /root/bentoml/repository ]; 
    then
        echo "bentoml bundling..."
        python3.8 /apps/src/main.py
    else
        echo "bentoml bundle is created."
        break
    fi
    sleep 1
done

# 2. bentoml containerizing
bentoml containerize TransformerService:latest -t $1:$2

# 3. docker push
echo "$3" | docker login --username so1s --password-stdin
docker tag $1:$2 so1s/$1:$2
docker push so1s/$1:$2