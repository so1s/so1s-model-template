#!/bin/bash

# options:
FILE_URL=""
INPUT_TYPE=""
OUTPUT_TYPE=""
MODEL_NAME=""
TAG=""
USERNAME=""
PASSWORD=""
REGISTRY=""

# 0. parsed options
while [ "$#" != 0 ]; do
    case "$1" in
        -f|--file) # download files
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                FILE_URL=$2
                shift 2
            else
                echo "Error : please input '-f|--file {FILE_URL}' Argument." >&2
                exit 1
            fi
            ;;
        -i|--input) # set input type
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                INPUT_TYPE=$2
                shift 2
            else
                echo "Error : please input '-i|--input {INPUT_TYPE}' Argument." >&2
                exit 1
            fi
            ;;
        -o|--output) # set output type
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                OUTPUT_TYPE=$2
                shift 2
            else
                echo "Error : please input '-o|--output {OUTPUT_TYPE}' Argument." >&2
                exit 1
            fi
            ;;
        -n|--name) # set image name
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                MODEL_NAME=$2
                shift 2
            else
                echo "Error : please input '-n|--name {MODEL_NAME}' Argument." >&2
                exit 1
            fi
            ;;
        -t|--tag) # set image tag
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                TAG=$2
                shift 2
            else
                echo "Error : please input '-t|--tag {IMAGE_TAG}' Argument." >&2
                exit 1
            fi
            ;;
        -u|--user) # set image registry password
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                USERNAME=$2
                shift 2
            else
                echo "Error : please input '-u|--user {USERNAME}' Argument." >&2
                exit 1
            fi
            ;;
        -p|--password) # set image registry password
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                PASSWORD=$2
                shift 2
            else
                echo "Error : please input '-p|--password {PASSWORD}' Argument." >&2
                exit 1
            fi
            ;;
        -r|--registry) # set image registry name
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                REGISTRY=$2
                shift 2
            else
                echo "Error : please input '-r|--registry {REGISTRY}' Argument." >&2
                exit 1
            fi
            ;;
        -h|--help) # help
            echo "Usage: $0 -i <input_type>" >&2
            echo "      -f | --file       (set custom file url)" >&2
            echo "      -i | --input      (set inference input type)" >&2
            echo "      -o | --output     (set inference output type)" >&2
            echo "      -n | --name       (set model name)" >&2
            echo "      -t | --tag        (set image tag)" >&2
            echo "      -u | --user       (set image registry username)" >&2
            echo "      -p | --password   (set image registry password)" >&2
            exit 0
            ;;
        -*|--*) # unsupported flags
            echo "Error: Unsupported flag: $1" >&2
            echo "$0 -h for help message" >&2
            exit 1
            ;;
        *) # error
            echo "Error: Arguments with not proper flag: $1" >&2
            echo "$0 -h for help message" >&2
            exit 1
            ;;
    esac
done

IMAGE_TAG=""
if [ -z $REGISTRY ]; then
    IMAGE_TAG="${USERNAME}/${MODEL_NAME}:${TAG}"
else
    IMAGE_TAG="${REGISTRY}/${USERNAME}/${MODEL_NAME}:${TAG}"
fi

echo "===============================parsed options===============================" >&1
echo "FILE_URL     : ${FILE_URL}" >&1
echo "INPUT_TYPE   : $INPUT_TYPE" >&1
echo "OUTPUT_TYPE  : ${OUTPUT_TYPE}" >&1
echo "NAME         : ${MODEL_NAME}" >&1
echo "TAG          : ${TAG}" >&1
echo "USERNAME     : ${USERNAME}" >&1
echo "REGISTRY     : ${REGISTRY}" >&1
echo "IMAGE_TAG     : ${IMAGE_TAG}" >&1
echo ""
echo ""

# option validation check
if [ -z $FILE_URL ]; then
    echo "Please Input [ -f | --file ] Options" >&2
    exit 1
fi
if [ -z $INPUT_TYPE ];  then
    echo "Please Input [ -i | --input ] Options" >&2
    exit 1
fi
if [ -z $OUTPUT_TYPE ]; then
    echo "Please Input [ -o | --output ] Options" >&2
    exit 1
fi
if [ -z $MODEL_NAME ]; then 
    echo "Please Input [ -n | --name ] Options" >&2
    exit 1
fi
if [ -z $TAG ];then 
    echo "Please Input [ -t | --tag ] Options" >&2
    exit 1
fi
if [ -z $USERNAME ]; then
    echo "Please Input [ -u | --user ] Options" >&2
    exit 1
fi
if [ -z $PASSWORD ]; then
    echo "Please Input [ -p | --password ] Options" >&2
    exit 1
fi



# 1. move workdir & set ENV
cd /apps

# 2. download files & unzip & summing
FILE_NAME=$(basename "$FILE_URL")
FILE_TYPE=`echo $FILE_NAME | rev | cut -d '.' -f1 | rev`
echo "FILE_NAME     : ${FILE_NAME}" >&1
echo "FILE_TYPE     : ${FILE_TYPE}" >&1
echo "wget ${FILE_URL}" >&1

wget $FILE_URL
case "$FILE_TYPE" in
    tar|gz)
        tar -zxvf $FILE_NAME
        ;;
    zip)
        unzip -o $FILE_NAME
        ;;
esac

echo "=========================Python Dependencies Install==========================" >&1
if [ -e "requirements.txt" ]; then
    pip3 install -r requirements.txt
    cat requirements.txt >> bento_requirements.txt
fi

# 3. bentoml model save
echo "============================Model SAVE to BentoML============================" >&1
export INPUT_TYPE
export OUTPUT_TYPE
export MODEL_NAME
python3.8 save.py

# 4. bentoml build
echo "=============================BENTOML BUILD SCRIPT=============================" >&1
sed "s/{input_type}/$INPUT_TYPE/g;s/{output_type}/$OUTPUT_TYPE/g;s/{model_name}/$MODEL_NAME/g" bentofile.template > bentofile.yaml
cat bentofile.yaml >&1
echo "=============================BENTOML BUILD START==============================" >&1
bentoml build

# 5. bentoml containerizing
echo "============================CONTAINERIZATION START============================" >&1
echo "bentoml containerize $MODEL_NAME:latest -t ${IMAGE_TAG} --network host --verbose --platform=linux/amd64" >&1
bentoml containerize $MODEL_NAME:latest -t ${IMAGE_TAG} --network host --verbose --platform=linux/amd64

# 6. docker push
echo "============================CONTAINERIZATION PUSH=============================" >&1
echo "$PASSWORD" | docker login --username $USERNAME --password-stdin
echo "docker push ${IMAGE_TAG}"
docker push ${IMAGE_TAG}

exit 0