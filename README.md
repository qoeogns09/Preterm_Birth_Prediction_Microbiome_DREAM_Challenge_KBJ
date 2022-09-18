# KBJ-preterm

## Overall Architecture

## Requirements
python: 3.7
```
pip install -r requirements.txt
```
```
Before implement these codes, you should download data. 
data
├── alpha_diversity
│   └── alpha_diversity.csv
├── community_state_types
│   ├── cst_valencia.csv
│   └── cst_valencia_w_taxons.csv
├── metadata
│   └── metadata.csv
├── pairwise_distance
│   ├── krd_distance_long.csv
│   └── krd_distance_wide.csv
├── phylotypes
│   ├── phylotype_nreads.1e0.csv
│   ├── phylotype_nreads.1e_1.csv
│   ├── phylotype_nreads.5e_1.csv
│   ├── phylotype_relabd.1e0.csv
│   ├── phylotype_relabd.1e_1.csv
│   ├── phylotype_relabd.5e_1.csv
│   ├── pt.1e-1.csv
│   ├── pt.1e0.csv
│   └── pt.5e-1.csv
├── sv_counts
│   └── sp_sv_long.csv
└── taxonomy
    ├── sv_taxonomy.csv
    ├── taxonomy_nreads.family.csv
    ├── taxonomy_nreads.genus.csv
    ├── taxonomy_nreads.species.csv
    ├── taxonomy_relabd.family.csv
    ├── taxonomy_relabd.genus.csv
    └── taxonomy_relabd.species.csv
```
## How to feature selection
Simply run all cell in each notebook files

## How to model selection and training
Simply run all cell in each notebook files

## How to make docker image for submission
Frist download baseline image
```
docker pull docker.synapse.org/syn26133770/ptb-dream-example
```
And make docker image for two tasks

Task 1
```
docker build -t preterm:v1 -f Dockerfile_preterm
```
Task 2
```
docker build -t early_preterm:v1 -f Dockerfile_early_preterm
```
