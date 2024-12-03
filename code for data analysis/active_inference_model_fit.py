import numpy as np
import math
import random
import csv
import pystan
import pandas as pd

def read_behavioral_data(n):
    result_stay_cue = []
    result_safe_risk = []
    action_stay_cue = []
    action_safe_risk = []
    if_can_ask = []
    fname = '/home/ncclab/zhangshuo/active_inference/behavioral_data/uncertainty_' + str(n+1) + '_2022.csv'
    with open(fname,'r') as f :
        for line in f.readlines():
            if line.split(',')[0]=='0' or line.split(',')[0]=='1':
                if int(line.split(',')[3])==0:
                    action_stay_cue.append(1)
                elif int(line.split(',')[3])==1 or int(line.split(',')[3])==2:
                    action_stay_cue.append(2)
                else :
                    print('ERROR')
                result_stay_cue.append(int(line.split(',')[3]))
                result_safe_risk.append(int(float(line.split(',')[6])))
                action_safe_risk.append(int(line.split(',')[4])+1)
                if line.split(',')[1]==' ':
                    if_can_ask.append(0)
                else :
                    if_can_ask.append(1)

    return if_can_ask,action_stay_cue,result_stay_cue,action_safe_risk,result_safe_risk
trial_num = 120
subject_num = 25
if_can_ask_sub = []
action_stay_cue_sub = []
result_stay_cue_sub = []
action_safe_risk_sub = []
result_safe_risk_sub = []
for i in range(subject_num):
    if_can_ask,action_stay_cue,result_stay_cue,action_safe_risk,result_safe_risk = read_behavioral_data(i)
    if_can_ask_sub.append(if_can_ask)
    action_stay_cue_sub.append(action_stay_cue)
    result_stay_cue_sub.append(result_stay_cue)
    action_safe_risk_sub.append(action_safe_risk)
    result_safe_risk_sub.append(result_safe_risk)
if_can_ask_sub = np.array(if_can_ask_sub)
action_stay_cue_sub = np.array(action_stay_cue_sub)
result_stay_cue_sub = np.array(result_stay_cue_sub)
action_safe_risk_sub = np.array(action_safe_risk_sub)
result_safe_risk_sub = np.array(result_safe_risk_sub)

bandit_model = """
functions {
  matrix dir(matrix a) {

    matrix[8,8] A;
    vector[8] a_0 = [0,0,0,0,0,0,0,0]';

    for (j in 1:8) {
      for (i in 1:8) {
        a_0[j]  += a[i,j];
      }
    }
    for (i in 1:8) {
      for (j in 1:8) {
        A[i,j] = a[i,j]/a_0[j];
      }
    }
    return A;
  }

  matrix cum(matrix a) {
    matrix[8,8] a_cum = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]];
    vector[8] a_0 = [0,0,0,0,0,0,0,0]';

    for (j in 1:8) {
      for (i in 1:8) {
        a_0[j] += a[i,j];
      }
    }

    for (i in 1:8) {
      for (j in 1:8) {
        a_cum[i,j] = a_0[j];
      }
    }
    return a_cum;
  }
  
  vector H_entropy(matrix A) {
    vector[8] H = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]';
    real h = 0.0;
    for (j in 1:8) {
      h = 0.0;
      for (i in 1:8) {
        h += A[i,j] * log(A[i,j] + exp(-16));
      }
      H[j] = -h;
    }
    return H;
  }
  
  real G_ExperctedFreeEnergy(matrix A, matrix a, vector s, int action_stay_cue, real p_al, real p_ai, real p_ex) {
    vector[8] o = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]';
    matrix[8,8] w = [[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0],[0.0,0,0,0,0,0,0,0]];
    matrix[8,8] a_nonzero = [[1,1,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]];
    real AL = 0.0;
    real AI = 0.0;
    real EX = 0.0;
    real discount = 0.1;
    vector[8] preference = [1, 2, 1.5, 0.5, 0, 0, -0.167, -0.167]';
    vector[8] H = H_entropy(A);

    for (i in 1:8) {
      for (j in 1:8) {
        o[i] += A[i,j] * s[j];
      }
    }
    
    for (i in 1:8) {
      for (j in 1:8) {
        w[i,j] = 1.0/cum(a)[i,j] - 1.0/(a[i,j]+exp(-16));
        w[i,j] *= a_nonzero[i,j];
      }
    }
  
    for (i in 1:8) {
      for (j in 1:8) {
        AL += o[i] * w[i,j] *s[j];
      }
    }

    for (i in 1:8) {
      AI += o[i] * log(o[i] + exp(-16));
    }
    
    for (i in 1:8) {
      EX += o[i] * preference[i];
    }

    if (action_stay_cue == 0) {
      return discount * (p_al * AL + p_ai * AI) - p_ex * EX;
    } 
    else if (action_stay_cue == 1) {
      return p_al * AL + p_ai * AI - p_ex * EX;
    } 
    else {
      return 0.0;
    }
  }

}


data {
  int<lower=1> subjects;
  int<lower=1> trials;
  int<lower=1,upper=2> action_stay_cue[subjects,trials];
  int<lower=1,upper=2> action_safe_risk[subjects,trials];
  int<lower=0,upper=1> if_can_ask[subjects,trials];
  int<lower=0,upper=2> result_stay_cue[subjects,trials];
  int<lower=0,upper=12> result_safe_risk[subjects,trials];    
}

transformed data {
  real<lower=0,upper=1> discount;
  
  discount = 0.1;
  
}

parameters{
  real<lower=0.001,upper=100> prior;
  real<lower=0.001,upper=20> rate;
  real<lower=0,upper=10> p_al;
  real<lower=0,upper=10> p_ai;
  real<lower=0,upper=10> p_ex;
}

model {
  for (s in 1:subjects){
    matrix[8,8] a = [[100.0, 100, prior, prior, 0, 0, 0, 0],[0, 0, prior, prior, 0, 0, 0, 0],[0, 0, prior, prior, 0, 0, 0, 0],[0, 0, prior, prior, 0, 0, 0, 0],[0, 0, prior, prior, 0, 0, 0, 0],[0, 0, 0, 0, 100, 100, 0, 0],[0, 0, 0, 0, 0, 0, 100, 0],[0, 0, 0, 0, 0, 0, 0, 100]];
    vector[8] s1;
    vector[8] s2;
    vector[8] s3;
    vector[8] s4;
    vector[8] ss;
    vector[8] o;
    vector[8] preference = [1, 2, 1.5, 0.5, 0, 0, -0.167, -0.167]';
    real G_stay_safe;
    real G_stay_risk;
    real G_cue_HR;
    real G_cue_HR_0;
    real G_cue_HR_1;
    real G_cue_LR;
    real G_cue_LR_0;
    real G_cue_LR_1;
    real G_safe;
    real G_risk;
    
    vector[2] G_stay_cue;
    vector[2] G_safe_risk;
    matrix[8,8] A;
    
    
    
    for (j in 1:trials) {
      A = dir(a);
      if (if_can_ask[s][j] != 0) {
        s1 = [0, 0, 0, 0, 0.5, 0.5, 0, 0]';
        s2 = [0.5, 0.5, 0, 0, 0, 0, 0, 0]';
        G_stay_safe = (G_ExperctedFreeEnergy(A, a, s1, 0, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s2, 0, p_al, p_ai, p_ex));
        s3 = [0, 0, 0, 0, 0.5, 0.5, 0, 0]';
        s4 = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        G_stay_risk = (G_ExperctedFreeEnergy(A, a, s3, 0, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s4, 0, p_al, p_ai, p_ex));

        s1 = [0, 0, 0, 0, 0, 0, 0.5, 0.5]';
        s2 = [1, 0, 0, 0, 0, 0, 0, 0]';
        s3 = [0, 0, 0, 0, 0, 0, 0.5, 0.5]';
        s4 = [0, 0, 1, 0, 0, 0, 0, 0]';
        G_cue_HR_0 = G_ExperctedFreeEnergy(A, a, s1, 1, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s2, 1, p_al, p_ai, p_ex);
        G_cue_HR_1 = G_ExperctedFreeEnergy(A, a, s3, 1, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s4, 1, p_al, p_ai, p_ex);

        if (G_cue_HR_0 > G_cue_HR_1) {
         G_cue_HR = G_cue_HR_1;
        } else {
         G_cue_HR = G_cue_HR_0;
        }



        s1 = [0, 0, 0, 0, 0, 0, 0.5, 0.5]';
        s2 = [0, 1, 0, 0, 0, 0, 0, 0]';
        s3 = [0, 0, 0, 0, 0, 0, 0.5, 0.5]';
        s4 = [0, 0, 0, 1, 0, 0, 0, 0]';
        G_cue_LR_0 = G_ExperctedFreeEnergy(A, a, s1, 1, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s2, 1, p_al, p_ai, p_ex);
        G_cue_LR_1 = G_ExperctedFreeEnergy(A, a, s3, 1, p_al, p_ai, p_ex) + G_ExperctedFreeEnergy(A, a, s4, 1, p_al, p_ai, p_ex);

        if (G_cue_LR_0 > G_cue_LR_1) {
         G_cue_LR = G_cue_LR_1;
        } else {
         G_cue_LR = G_cue_LR_0;
        }



        G_stay_cue[1] = -G_stay_safe - G_stay_risk;
        G_stay_cue[2] = -G_cue_HR - G_cue_LR;
        if (is_nan(G_stay_cue[1])) {
          G_stay_cue[1] = 1;
          G_stay_cue[2] = 1;
        }
        if (is_nan(G_stay_cue[2])) {
          G_stay_cue[1] = 1;
          G_stay_cue[2] = 1;
        }
        action_stay_cue[s,j] ~ categorical_logit(G_stay_cue);
      }
      
      if (result_stay_cue[s][j] == 0) {
        ss = [0.5, 0.5, 0, 0, 0, 0, 0, 0]';
        G_safe = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        G_risk = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        G_safe_risk[1] = -G_safe;
        G_safe_risk[2] = -G_risk;
      } else if (result_stay_cue[s][j] == 1) {
        ss = [1, 0, 0, 0, 0, 0, 0, 0]';
        G_safe = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        G_risk = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        G_safe_risk[1] = -G_safe;
        G_safe_risk[2] = -G_risk;
      } else {
        ss = [0, 1, 0, 0, 0, 0, 0, 0]';
        G_safe = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        G_risk = G_ExperctedFreeEnergy(A, a, ss, action_stay_cue[s][j], p_al, p_ai, p_ex);
        G_safe_risk[1] = -G_safe;
        G_safe_risk[2] = -G_risk;
      }

      if (is_nan(G_safe_risk[1])) {
        G_safe_risk[1] = 1;
        G_safe_risk[2] = 1;
      }
      if (is_nan(G_safe_risk[2])) {
        G_safe_risk[1] = 1;
        G_safe_risk[2] = 1;
      }

      action_safe_risk[s,j] ~ categorical_logit(G_safe_risk);
      
      if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 0) {
        ss = [0.5, 0.5, 0, 0, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 0) {
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        o = [0, 0, 0, 0, 1, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 3) {
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        o = [0, 0, 0, 1, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 1) {
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 9) {
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        o = [0, 0, 1, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 0 && result_safe_risk[s][j] == 12) {
        ss = [0, 0, 0.5, 0.5, 0, 0, 0, 0]';
        o = [0, 1, 0, 0, 0, 0, 0, 0]';
      
      
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 0) {
        ss = [1, 0, 0, 0, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 0) {
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        o = [0, 0, 0, 0, 1, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 3) {
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        o = [0, 0, 0, 1, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 1) {
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 9) {
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        o = [0, 0, 1, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 1 && result_safe_risk[s][j] == 12) {
        ss = [0, 0, 1, 0, 0, 0, 0, 0]';
        o = [0, 1, 0, 0, 0, 0, 0, 0]';
      
      
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 0) {
        ss = [0, 1, 0, 0, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 0) {
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        o = [0, 0, 0, 0, 1, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 3) {
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        o = [0, 0, 0, 1, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 6 && action_safe_risk[s][j] == 1) {
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        o = [1, 0, 0, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 9) {
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        o = [0, 0, 1, 0, 0, 0, 0, 0]';
      } else if (result_stay_cue[s][j] == 2 && result_safe_risk[s][j] == 12) {
        ss = [0, 0, 0, 1, 0, 0, 0, 0]';
        o = [0, 1, 0, 0, 0, 0, 0, 0]';
      } 
      
      
      if(action_stay_cue[s][j] == 1) {
        for(n in 1:8) {
          for(m in 1:8) {
            a[n,m] += rate * discount * o[n] * ss[m];
          }
        }
      } else if (action_stay_cue[s][j] == 2) {
        for(n in 1:8) {
          for(m in 1:8) {
            a[n,m] += rate * o[n] * ss[m];
          }
        }
      }
      
    }
  }
}


"""

bandit_data = {"subjects":subject_num,
               "trials":trial_num,
               "if_can_ask":if_can_ask_sub,
               "action_stay_cue":action_stay_cue_sub,
               "result_stay_cue":result_stay_cue_sub,
               "action_safe_risk":action_safe_risk_sub,
               "result_safe_risk":result_safe_risk_sub}
sm = pystan.StanModel(model_code=bandit_model)
fit = sm.sampling(data=bandit_data,iter=20000,chains=4,warmup=16000,control={'adapt_delta':0.8 ,'max_treedepth':20})
summary_dict = fit.summary()
df = pd.DataFrame(summary_dict['summary'],columns=summary_dict['summary_colnames'],index=summary_dict['summary_rownames'])
df.to_csv('active_inference_fitted_parameter.csv')