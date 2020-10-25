import pandas as pd
import numpy as np
dataset1 = pd.read_csv('~/git/DOMAS_groupB09/Lookahead_data.csv', low_memory = False)
dataset2 = pd.read_csv('~/git/DOMAS_groupB09/Proportional_data.csv', low_memory = False)
dataset3 = pd.read_csv('~/git/DOMAS_groupB09/data.csv', low_memory = False)


dataset1.rename(columns={'Unnamed: 0':'step'}, inplace=True)
last_index = dataset1
last_index['step'] = dataset1['step'] % 2000
last_index = last_index.query('step == 1999')
groupedAVG1 = last_index.groupby(['tactic','Spawnrate']).mean()

dataset2.rename(columns={'Unnamed: 0':'step'}, inplace=True)
last_index = dataset2
last_index['step'] = dataset2['step'] % 2000
last_index = last_index.query('step == 1999')
groupedAVG2 = last_index.groupby(['tactic','Spawnrate']).mean()
groupedSTD2 = last_index.groupby(['tactic','Spawnrate']).std()

groupedAVG = pd.concat([groupedAVG1, groupedAVG2])

groupedAVG.to_csv (r'~/git/DOMAS_groupB09/AVG_data.csv')
