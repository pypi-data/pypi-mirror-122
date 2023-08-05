# MLE Decathlon

[![Upload Python Package](https://github.com/Pie33000/mle_deacthlon/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Pie33000/mle_deacthlon/actions/workflows/python-publish.yml)


## Description

The repository contains all the exercises of the MLE decathlon test.<br>
The answers to exercises 1 to 3 are in the notebooks folder.<br>
The pipeline construction is in the module forecasting_mle_decathlon.

### Run the code

#### Create conda env and activate it

    conda create -n mle_decathlon python=3.8
    conda activate mle_decathlon
    pip install -r requirements.txt

#### Launch pipeline to train + predict

    python main.py
    
This command launch a training with data in data/inputs directory, then predict forecasting for 8 weeks and save it in data/outputs as a pickle file.

#### Start notebook

    jupyter lab


### Notes

With limited time I couldn't do everything as well as I would have liked. 
The code could be improved, the naming could be revised as well as the processings functions. <br>
We could also add more relevant unit tests with edge case management, integration tests or at least an E2E test.
Model performance monitoring could be managed with mlflow to manage the life cycle of each model, as well as the associated metrics.
Concerning the modeling, many assertions have not been verified. <br>
It would be interesting to do a more thorough study of the data (auto correlation, trend, seasonality etc ...), 
and to use multi-modal models, we could also ask ourselves the question of introducing a more complex modeling 
after a thorough analysis of the data and fine tuning of the basic models.

The construction of the package here does not make any particular sense but it was a request of the exercise.

Regarding exercise 5, I made the effort to use AWS services, even though I am more familiar with Azure.
