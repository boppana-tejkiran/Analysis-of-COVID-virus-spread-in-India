import json
import collections
import pandas as pd
import datetime
import csv

begin=datetime.datetime(2020, 3, 15)
end = datetime.datetime(2020, 9, 5)
################### Creating a data frame of covid19 data using data-all json file #####################
with open('../dataset/data-all.json') as f:
	data_all= json.load(f)

df=pd.DataFrame.from_dict(data_all,orient='index')
#print(df)
################### Creating a dictionary of districts with ids from new-neghbors jason file #####################
with open('neighbor-districts-modified.json') as f:
	temp_data= json.load(f)

count=101
distr_dict={}

for item in temp_data.keys():
	temp_ls=item.split("/")	
	distr_dict.update({temp_ls[0]:count})
	count=count+1
#print(distr_dict)
######## Creating a dictionary of dialy cases for all keys of neighbor districts using covid data frame #########
daily_cases={}
for i,j in df.iterrows():
	i=datetime.datetime.strptime(i,"%Y-%m-%d")
	temp_dict={}
	if i>=begin and i<=end:
		for state in j:   #looping across states
			if type(state)!=type(2.0000):
				for item in state:    #looping with in a state
					if item=='districts':
						temp1=state[item] 
						for distr in temp1:    #looping with in districts list
							#print(distr)
							if distr in distr_dict:
								temp2=temp1[distr]
								for diff in temp2:   #looping with in a single district
									if diff=='delta':
										temp3=temp2[diff]
										flag=0
										for cases in temp3:  #looping with in delta dict of single district
											if cases=='confirmed':
												temp_dict.update({distr:temp3['confirmed']})
												flag=1
										if flag==0:
											temp_dict.update({distr:0})
		daily_cases.update({i:temp_dict})
#print(daily_cases)
## %%%%%%%%%%%%%%%%%%%% the above code does not capture the cases data of districts with same name and data of state->districts %%%%%%%%%%%%%%%%%% ##
################# adding the covid data of districts with same name and state->districts to daily_cases dictionary #####################
## ================================= Adding Telangana state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['TG'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Telangana':confirmed})
## ================================== Adding Delhi state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['DL'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Delhi':confirmed})
## ================================== Adding Sikkim state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['SK'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Sikkim':confirmed})
## ================================== Adding Assam state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['AS'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Assam':confirmed})
## ================================== Adding Goa state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['GA'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Goa':confirmed})
## ================================== Adding Manipur state daily confirmed cases to our daily_cases dictionary ================================= #
for ind in df.index:
	state=df['MN'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='delta':
				temp1=state[item]
				if 'confirmed' in temp1:
					confirmed=temp1['confirmed']
					flag=1
	if flag==0:
		confirmed=0
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Manipur':confirmed})
## ================================== adding aurangabad_BH daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['BR'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Aurangabad' in temp1:
					temp2=temp1['Aurangabad']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Aurangabad_BR':confirmed})
## ================================== adding aurangabad_MH daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['MH'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Aurangabad' in temp1:
					temp2=temp1['Aurangabad']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Aurangabad_MH':confirmed})
## ================================== adding balrampur_CT daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['CT'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Balrampur' in temp1:
					temp2=temp1['Balrampur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Balrampur_CT':confirmed})
## ================================== adding balrampur_UP daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['UP'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Balrampur' in temp1:
					temp2=temp1['Balrampur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Balrampur_UP':confirmed})
## ================================== adding bilaspur_CT daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['CT'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Bilaspur' in temp1:
					temp2=temp1['Bilaspur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Bilaspur_CT':confirmed})
## ================================== adding bilaspur_HP daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['HP'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Bilaspur' in temp1:
					temp2=temp1['Bilaspur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Bilaspur_HP':confirmed})
## ================================== adding hamirpur_HP daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['HP'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Hamirpur' in temp1:
					temp2=temp1['Hamirpur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Hamirpur_HP':confirmed})
## ================================== adding hamirpur_UP daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['UP'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Hamirpur' in temp1:
					temp2=temp1['Hamirpur']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Hamirpur_UP':confirmed})
## ================================== adding prathapgarh_RJ daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['RJ'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Prathapgarh' in temp1:
					temp2=temp1['Prathapgarh']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Prathapgarh_RJ':confirmed})
## ================================== adding pratapgarh_UP daily confirmed cases to our daily cases dictionary ================================== #
for ind in df.index:
	state=df['UP'][ind]
	flag=0
	if type(state)!=type(2.0000):
		for item in state:
			if item=='districts':
				temp1=state[item]
				if 'Pratapgarh' in temp1:
					temp2=temp1['Pratapgarh']
					if 'delta' in temp2:
						temp3=temp2['delta']
						if 'confirmed' in temp3:
							confirmed=temp3['confirmed']
							flag=1
	if flag==0:
		confirmed=0;
	ind=datetime.datetime.strptime(ind,"%Y-%m-%d")
	if(ind>=begin) and (ind<=end):
		daily_cases[ind].update({'Pratapgarh_UP':confirmed})		
########### Calculating weekly cases, overall cases for every district key in new neighbours json file using above covid data dictnry ############
with open('cases-overall.csv','w') as overall_csv:
		overall_csv_writer=csv.writer(overall_csv)
		overall_csv_writer.writerow(['districtid','cases'])
		with open('cases-week.csv','w') as weekly_csv:
			csv_writer=csv.writer(weekly_csv)
			csv_writer.writerow(['districtid','weekid','cases'])
			for distr in distr_dict:
				overall_cases=0
				temp_begin=begin
				temp_end=temp_begin+datetime.timedelta(days=6)
				week_id=1
				while temp_end<=datetime.datetime(2020, 9, 5):
					weekly_cases=0
					for date in daily_cases:
						if date>=temp_begin and date<=temp_end:
							temp_dict=daily_cases[date]
							if distr in temp_dict:
								weekly_cases= weekly_cases+temp_dict[distr]
					csv_writer.writerow([distr_dict[distr],week_id,weekly_cases])		
					week_id=week_id+1
					temp_begin=temp_begin+datetime.timedelta(days=7)
					temp_end=temp_begin+datetime.timedelta(days=6)
					overall_cases=overall_cases+weekly_cases
				overall_csv_writer.writerow([distr_dict[distr],overall_cases])
			
########### Calculating monthly cases for every district key in new neighbours json file using above covid data dictnry ############			
with open('cases-month.csv','w') as monthly_csv:
	csv_writer=csv.writer(monthly_csv)
	csv_writer.writerow(['districtid','monthid','cases'])
	for distr in distr_dict:
		temp_begin=begin
		temp_end=temp_begin+datetime.timedelta(days=29)
		month_id=1
		while temp_end<=datetime.datetime(2020, 9, 10):
			monthly_cases=0
			for date in daily_cases:
				if date>=temp_begin and date<=temp_end:
					temp_dict=daily_cases[date]
					if distr in temp_dict:
						monthly_cases=monthly_cases+temp_dict[distr]
			csv_writer.writerow([distr_dict[distr],month_id,monthly_cases])
			month_id=month_id+1
			temp_begin=temp_begin+datetime.timedelta(days=30)
			temp_end=temp_begin+datetime.timedelta(days=29)
					
					
					
########################### Save daily cases dictionary as json file for next questions ################################### 					
#print(daily_cases)
dict_store={}

for date in daily_cases:
	temporary_dict=daily_cases[date]
	dict_store.update({str(date):temporary_dict})  ##only for storing the result for next problems##

with open('day-wise-cases.json','w') as f:
	json.dump(dict_store,f,indent=4)		
					
					
					
					
				
			
							
		

