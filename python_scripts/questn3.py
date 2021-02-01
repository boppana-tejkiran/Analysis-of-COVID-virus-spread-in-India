import pandas as pd
import json
import csv
import collections
with open('neighbor-districts-modified.json') as f:
	ordered_data = json.load(f)

for distr in ordered_data:
	temp_ls=ordered_data[distr]
	temp_ls.pop()
	ordered_data[distr]=temp_ls
dict={}
i=101
districts=list(ordered_data.keys())
for lp in districts:
	dict.update({lp:i})
	i=i+1;
df=pd.DataFrame.from_dict(ordered_data,orient='index')
#print(df)
id=[]
col_num=len(df.columns)
for k in range(col_num):
	id.append(str(k))
df.columns=id
z=101
#print(df)

with open('edge-graph.csv','w') as f:
	edge_writer=csv.writer(f, delimiter=',')
	for i,j in df.iterrows():
		temp=list(j)
		for k in temp:
			if k:
				if (dict.get(k)>z):
						
					edge_writer.writerow([z,dict.get(k)])
			else:
				break;
		z=z+1

