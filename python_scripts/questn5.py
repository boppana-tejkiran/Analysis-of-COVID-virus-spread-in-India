import json
import collections
import pandas as pd
import datetime
import csv
import statistics

begin=datetime.datetime(2020, 3, 15)
end = datetime.datetime(2020, 9, 5)
######################### loading daily cases data to a python dictionary from day-wise-cases json file ######################
with open('day-wise-cases.json') as f:
	daily_cases= json.load(f)
######################## loading state - district information json file #######################
with open('state-information.json') as f:  ##here the file we have to load is state-information only // not updated-state-infirmation##
	state_info=json.load(f)
################# loading of new-neighbour-districts json file ###################
with open('neighbor-districts-modified.json') as f:
	neigh_data= json.load(f)
#print(neigh_data)
################## removing id from neighbour districts list of every key in new neighbors json file ####################
for distr in neigh_data:
	temp_ls=neigh_data[distr]
	temp_ls.pop() ## removing id part in value list ##
	new_temp_ls=[]
	for item in temp_ls:  ##removing the Qid part from value list ##
		temp_remove=item.split("/")  
		new_temp_ls.extend([temp_remove[0]])
	neigh_data[distr]=new_temp_ls
use_neigh_data={}
for distr in neigh_data:  ##removing the Qid part from all keys ##
	temp_ls=neigh_data[distr]
	temp_remove=distr.split("/")
	use_neigh_data.update({temp_remove[0]:temp_ls})  ##use_neigh_data is new neighbour json file with Qids and district ids stripped ## 
############################ making a dictionary of key:id pairs from new-neighbours data ###############################
#print(use_neigh_data)
count=101
distr_dict={}

for item in use_neigh_data.keys():	
	distr_dict.update({item:count})
	count=count+1
#print(distr_dict)
############################ modifying the state information to rename same name districts and states with out district data ############################
## =========== adding Telangana as a district to its state code key ============== ##
del state_info['TG']
state_info.update({'TG':['Telangana']})
## =========== adding sikkim as a district to its state code key ============== ##
del state_info['SK']
state_info.update({'SK':['Sikkim']})
## =========== adding assam as a district to its state code key ============== ##
del state_info['AS']
state_info.update({'AS':['Assam']})
## =========== adding goa as a district to its state code key ============== ##
del state_info['GA']
state_info.update({'GA':['Goa']})
## =========== adding manipur as a district to its state code key ============== ##
del state_info['MN']
state_info.update({'MN':['Manipur']})
## =========== updating names of same name districts in uttarpradesh state key ============= ##
temp_ls=state_info['UP']
if 'Pratapgarh' in temp_ls:
	temp_ls.remove('Pratapgarh')
	temp_ls.extend(['Pratapgarh_UP'])
if 'Hamirpur' in temp_ls:
	temp_ls.remove('Hamirpur')
	temp_ls.extend(['Hamirpur_UP'])
if 'Balrampur' in temp_ls:
	temp_ls.remove('Balrampur')
	temp_ls.extend(['Balrampur_UP'])
state_info['UP']=temp_ls
#print(state_info)
## =========== updating names of same name districts in himachalpradesh state key ============= ##
temp_ls=state_info['HP']
if 'Hamirpur' in temp_ls:
	temp_ls.remove('Hamirpur')
	temp_ls.extend(['Hamirpur_HP'])
if 'Bilaspur' in temp_ls:
	temp_ls.remove('Bilaspur')
	temp_ls.extend(['Bilaspur_HP'])
state_info['HP']=temp_ls
## ============= updating names of same name districts in chattisgarh state key =============== ##
temp_ls=state_info['CT']
if 'Balrampur' in temp_ls:
	temp_ls.remove('Balrampur')
	temp_ls.extend(['Balrampur_CT'])
if 'Bilaspur' in temp_ls:
	temp_ls.remove('Bilaspur')
	temp_ls.extend(['Bilaspur_CT'])
state_info['CT']=temp_ls
## ============= updating names of same name districts in bihar state key =============== ##
temp_ls=state_info['BR']
if 'Aurangabad' in temp_ls:
	temp_ls.remove('Aurangabad')
	temp_ls.extend(['Aurangabad_BR'])
state_info['BR']=temp_ls
## ============= updating names of same name districts in maharastra state key =============== ##
temp_ls=state_info['MH']
if 'Aurangabad' in temp_ls:
	temp_ls.remove('Aurangabad')
	temp_ls.extend(['Aurangabad_MH'])
state_info['MH']=temp_ls
## ============= updating names of same districts in Rajasthan state key ===================== ##
temp_ls=state_info['RJ']
if 'Pratapgarh' in temp_ls:
	temp_ls.remove('Pratapgarh')
	temp_ls.extend(['Pratapgarh_RJ'])
state_info['RJ']=temp_ls
############### writing the updated state info to new updated-state information json file ################# 
with open('updated-state-information.json','w') as f:  ## we are writing back for usage in next questions ##
	json.dump(state_info,f,indent=4)

#################### finding of weekly and overall cases for all other districts for a district in its state #####################
##### ==============  we will use distr_dict , daily_cases, state info and loop over them to get daily, monthly and overall cases ============= #####
state_info2=state_info
temp_state_info1=state_info

statemeth_weekly_cases={}
statemeth_overall_cases={}

#################
#print(temp_state_info1)
with open('state-overall.csv','w') as state_overall:
	state_overall_csv_writer=csv.writer(state_overall)
	state_overall_csv_writer.writerow(['districtid','statemean','statestdev'])
	with open('state-week.csv','w') as state_week:
		state_week_csv_writer=csv.writer(state_week)
		state_week_csv_writer.writerow(['districtid','weekid','statemean','statestdev'])
		for distr in distr_dict:
			temp_dict={}
			for state in temp_state_info1:
				temp_ls=list(temp_state_info1[state])
				if distr in temp_ls:
					temp_ls.remove(distr)
					temp_begin=begin
					temp_end=temp_begin+datetime.timedelta(days=6)
					week_id=1
					overall_ls=[0]*len(temp_ls)
					while temp_end<=datetime.datetime(2020, 9, 5):
						weekly_ls=[]
						count=0
						for item in temp_ls:
							weekly_cases=0
							if item in distr_dict:  ##we added this becauses some districts in state-info may not be in neighbor file##
								for date in daily_cases:
									if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
										temp_cases_ls=daily_cases[date]
										if item in temp_cases_ls:
											weekly_cases=weekly_cases+temp_cases_ls[item]
							
								weekly_ls.extend([weekly_cases])
								overall_ls[count]=overall_ls[count]+weekly_cases
								count=count+1
						
						if len(weekly_ls)>=1:
							weekly_mean=round(statistics.mean(weekly_ls),2)
						else:
							weekly_mean=0
						if len(weekly_ls)>=2:
							weekly_stdev=round(statistics.pstdev(weekly_ls),2)
						else:
							weekly_stdev=0
						state_week_csv_writer.writerow([distr_dict[distr],week_id,weekly_mean,weekly_stdev])
						temp_dict.update({week_id:weekly_ls})
						week_id=week_id+1
						temp_begin=temp_begin+datetime.timedelta(days=7)
						temp_end=temp_begin+datetime.timedelta(days=6)
					if len(overall_ls)>=1:
						overall_mean=round(statistics.mean(overall_ls),2)
					else:
						overall_mean=0
					if len(overall_ls)>=2:
						overall_stdev=round(statistics.pstdev(overall_ls),2)
					else:
						overall_stdev=0;
					statemeth_weekly_cases.update({distr:temp_dict})
					statemeth_overall_cases.update({distr:overall_ls})
					state_overall_csv_writer.writerow([distr_dict[distr],overall_mean,overall_stdev])
	

#################### finding of monthly cases for all other districts for a district in its state ##################### 
#print(state_info2)

statemeth_monthly_cases={}
with open('state-month.csv','w') as state_month:
	state_month_csv_writer=csv.writer(state_month)
	state_month_csv_writer.writerow(['districtid','monthid','statemean','statestdev'])
	for distr in distr_dict:
		temp_dict={}
		for state in state_info2:
			temp_distr_ls2=state_info2[state]
			#print(distr)
			#print(temp_distr_ls2)
			if distr in temp_distr_ls2:
				temp_distr_ls2.remove(distr)
				temp_begin=begin
				temp_end=temp_begin+datetime.timedelta(days=29)
				month_id =1
				
				while temp_end<=datetime.datetime(2020, 9, 10):
					monthly_ls=[]
					for item in temp_distr_ls2:
						monthly_cases=0
						if item in distr_dict:
							for date in daily_cases:
								if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
									temp_cases_ls=daily_cases[date]
									if item in temp_cases_ls:
										monthly_cases=monthly_cases+temp_cases_ls[item]
				
							monthly_ls.extend([monthly_cases])
					if len(monthly_ls)>=1:
						monthly_mean=round(statistics.mean(monthly_ls),2)
					else:
						monthly_mean=0
					if len(monthly_ls)>=2:
						monthly_stdev=round(statistics.mean(monthly_ls),2)
					else:
						monthly_stdev=0
					temp_dict.update({month_id:monthly_ls})
					
					state_month_csv_writer.writerow([distr_dict[distr],month_id,monthly_mean,monthly_stdev])
					month_id=month_id+1
					temp_begin=temp_begin+datetime.timedelta(days=30)
					temp_end=temp_begin+datetime.timedelta(days=29)
				statemeth_monthly_cases.update({distr:temp_dict})
################ saving the statemeth weekly, monthly, overall cases to json files##################
with open('statemeth_weekly_cases.json','w') as f:
	json.dump(statemeth_weekly_cases,f,indent=4)

with open('statemeth_monthly_cases.json','w') as f:
	json.dump(statemeth_monthly_cases,f,indent=4)

with open('statemeth_overall_cases.json','w') as f:
	json.dump(statemeth_overall_cases,f,indent=4)					
					
					
					
					
					
					
					
					
					
					
					



