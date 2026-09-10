import pandas as pd 

""" 
Generally for pairs trading if the z-score is above 2 std, 
this would mean that the spread is too high, which meants 
that it will eventually come back down prompting a short of the spread. 
Conversely if the z-score is below 2 std, the spread is lower than usual, 
and there is an expectation for price to go back up which prompts 
a long of the spread. When z-score cross back toward 0, this would be 
a signal that it is time to exit the trade as the reversion would have happened.

Signal = -1 for a short 
Signal = 1 for a long  
"""

def get_signal(z_score): 
    signal = pd.Series(0, index=z_score.index)
    signal.loc[z_score > 2] = -1 
    signal.loc[z_score < -2] = 1 

    return signal 

def get_stateful_signal(z_score): 
    signal = pd.Series(0, index=z_score.index)

    position = 0 

    for i in range(len(z_score)): 
        z = z_score.iloc[i]

        if position == 0: 
            if z > 2: 
                position = -1 
            elif z < -2: 
                position = 1
        elif position == -1: 
            # Exit short when spread returns toward the mean 
            if z < 0.5: 
                position = 0 

        elif position == 1: 
            # Exit long when spread returns toward the mean 
            if z > -0.5: 
                position = 0

        signal.iloc[i] = position 

    return signal 
