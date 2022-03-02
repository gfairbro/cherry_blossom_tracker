import pandas as pd

#import tables
trees = pd.read_csv('../data/raw_trees.csv', sep=';') 
bloom_range = pd.read_csv('../data/bloom_range.csv')

#set cultivar list to drop. These are not the right tree type
drop = ['SEIBOLDI', 'SWEETHEART', 'MIYAKO']

#join the two tables to add defined bloom periods
bloom_include = pd.merge(left = trees, right = bloom_range, on="CULTIVAR_NAME", how='left')
#drop inappropriate cultivars
trees_upload = bloom_include[~bloom_include['CULTIVAR_NAME'].isin(drop)]

#save new data
trees_upload.to_csv('../data/processed_trees.csv')