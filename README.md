# KBJ-preterm

## Overall Architecture

## Requirements
python: 3.7
```
pip install -r requirements.txt
```
## How to feature selection

## How to model selection and training

## How to make docker image for submission
Frist download baseline image
```
docker pull docker.synapse.org/syn26133770/ptb-dream-example
```
And make docker image for two tasks
```
docker build -t preterm:v1 -f Dockerfile_preterm
```
or
```
docker build -t early_preterm:v1 -f Dockerfile_early_preterm
```
