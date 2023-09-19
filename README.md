# FreeEnergyEEG
Codebase underlying Zhang et al.'s 2023  paper about The Neural Correlates of Ambiguity and Risk in Human Decision-Making under an Active Inference Framework.
![image text](https://github.com/andlab-um/FreeEnergyEEG/blob/main/action-perception.png)


# Description
There are "behavioral data" -- 25 participants' behavioral data including action, rewards, and hidden state in each trial, "code for data analysis" -- 'data_fitting.ipynb' applies the active inference framework to fit the behavioral data and outputs the fitted parameters, 'source_localization_and_linear_regression.ipynb' transforms EEG data into source space from sensor space and performs linear regression between the source data and the fitted parameters of the active inference model, 'simulation.' runs the simulation experiment showed in Figure 3, 'sensor_level.ipynb' analyzes the EEG results at the sensor level showed in Figure 5, and 'source_level.ipynb' analyzes the regression results at the source level showed in Figure 6/7/8, "experiment code" -- the code of the contextual two-armed bandit task showed in Figure 4 (a), "preprocessed eeg data" -- 23 participants' EEG data after preprocessing, and "regression data in source space" -- the regression results between the source data and the fitted parameters of the active inference model.
## Introduction
Our study uses the active inference model to investigate the decision-making process in the brain and dissociates the expected free energy and the uncertainty in active inference theory and their neural correlates, suggesting the reliability of active inference in characterizing cognitive processes of human decisions. It provides behavioral and neural evidence of active inference in decision processes and insights into the neural mechanism of human decision under different kinds of uncertainty.
![image text](https://github.com/andlab-um/FreeEnergyEEG/blob/main/generative-model.png)
In my understanding, the active inference framework raises questions about whether the brain encodes the value of resolving uncertainty while encoding the representing of uncertainty. The value of resolving uncertainty is used to balance the exploration-exploitation trade-off during choosing action and uncertainty is encoded to construct the environment model during learning. Our work focuses on investigating where the brain encodes the value of resolving uncertainty.
![image text](https://github.com/andlab-um/FreeEnergyEEG/blob/main/experiment_behavioral%20result.png)
Additionally, our work dissociates the uncertainties into ambiguity, the uncertainty about the model parameter, and risk, the uncertainty about the hidden states. Through experimental settings, we enable subjects to adopt certain strategies to reduce risks or ambiguity and we further investigate where the brain encodes the value of reducing ambiguity and the value of avoiding risk.
## HISTORY
1.04.2021 - Initiation date



## REFERENCES


## Notes
TODO
Task 1: 
