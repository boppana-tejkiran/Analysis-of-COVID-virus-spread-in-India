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
############################ loading data from neighmeth_weekly_cases json file #############################
with open('neighmeth_weekly_cases.json') as f:
	neighmeth_weekly_cases=json.load(f)
############################ loading data from neighmeth_monthly_cases json file ############################
with open('neighmeth_monthly_cases.json') as f:
	neighmeth_monthly_cases=json.load(f)
############################ loading data from neighmeth_overall_cases json file ############################
with open('neighmeth_overall_cases.json') as f:
	neighmeth_overall_cases=json.load(f)
############################ loading data from statemeth_weekly_cases json file #############################
with open('statemeth_weekly_cases.json') as f:
	statemeth_weekly_cases=json.load(f)
############################ loading data from statemeth_monthly_cases json file ############################
with open('statemeth_monthly_cases.json') as f:
	statemeth_monthly_cases=json.load(f)
############################ loading data from statemeth_overall_cases json file ############################
with open('statemeth_overall_cases.json') as f:
	statemeth_overall_cases=json.load(f)
############################ using neighmeth looping over distr_dict and finding weekly and overall hotspots for each district ###############################
neighmeth_spot=""
statemeth_spot=""
with open('method-spot-overall.csv','w') as method_spot_overall:
	method_spot_overall_csv_writer = csv.writer(method_spot_overall)
	method_spot_overall_csv_writer.writerow(['method','spot','districtid'])
	with open('method-spot-week.csv','w') as method_spot_week:
		method_spot_week_csv_writer=csv.writer(method_spot_week)
		method_spot_week_csv_writer.writerow(['weekid','method','spot','districtid'])
		for distr in distr_dict:
			neighmeth_flag=0
			statemeth_flag=0
			temp_begin=begin
			temp_end = temp_begin+datetime.timedelta(days=6)
			week_id =1
			overall_cases=0
			while temp_end <= datetime.datetime(2020, 9, 5):
				weekly_cases=0
				for date in daily_cases:
					temp_ls=daily_cases[date]
					if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
						if distr in temp_ls:
							weekly_cases=weekly_cases+temp_ls[distr]
				overall_cases=overall_cases+weekly_cases
				neighmeth_temp_dict=neighmeth_weekly_cases[distr]
				neighmeth_temp1 = neighmeth_temp_dict[str(week_id)]
				if len(neighmeth_temp1)>=1:
					neighmeth_weekly_mean = round(statistics.mean(neighmeth_temp1),2)
				else:
					neighmeth_weekly_mean = 0
				if len(neighmeth_temp1)>=2:
					neighmeth_weekly_stdev = round(statistics.pstdev(neighmeth_temp1),2)
					
				else:
					neighmeth_weekly_stdev = 0
				
				if weekly_cases>(neighmeth_weekly_mean+neighmeth_weekly_stdev):
					neighmeth_spot = 'hot'
					neighmeth_flag=1
				if weekly_cases<(neighmeth_weekly_mean+neighmeth_weekly_stdev):
					neighmeth_spot='cold'
					neighmeth_flag=-1
				statemeth_temp_dict = statemeth_weekly_cases[distr]
				statemeth_temp1 = statemeth_temp_dict[str(week_id)]
				if len(statemeth_temp1) >=1:
					statemeth_weekly_mean = round(statistics.mean(statemeth_temp1),2)
				else:
					statemeth_weekly_mean = 0
				if len(statemeth_temp1)>=2:
					statemeth_weekly_stdev = round(statistics.pstdev(statemeth_temp1),2)
				else:
					statemeth_weekly_stdev = 0
				if weekly_cases>(statemeth_weekly_mean+statemeth_weekly_stdev):
					statemeth_spot='hot'
					statemeth_flag=1
				if weekly_cases<(statemeth_weekly_mean-statemeth_weekly_stdev):
					statemeth_spot='cold'
					statemeth_flag=-1
				if neighmeth_flag !=0:
					method_spot_week_csv_writer.writerow([week_id,'neighborhood',neighmeth_spot,distr_dict[distr]])
				if statemeth_flag !=0:
					method_spot_week_csv_writer.writerow([week_id,'state',statemeth_spot,distr_dict[distr]])
				week_id =week_id+1
				temp_begin=temp_begin+datetime.timedelta(days=7)
				temp_end=temp_begin+datetime.timedelta(days=6)
				## finding overall zscores for a district ##
				neighmeth_overall_temp_ls = neighmeth_overall_cases[distr]
				if len(neighmeth_overall_temp_ls)>=1:
					neighmeth_overall_mean = round(statistics.mean(neighmeth_overall_temp_ls),2)
				else:
					neighmeth_overall_mean = 0
				if len(neighmeth_overall_temp_ls)>=2:
					neighmeth_overall_stdev = round(statistics.pstdev(neighmeth_overall_temp_ls),2)
				else:
					neighmeth_overall_stdev = 0
				if overall_cases>(neighmeth_overall_mean+neighmeth_overall_stdev):
					neighmeth_spot='hot'
					neighmeth_flag=1
				if overall_cases<(neighmeth_overall_mean-neighmeth_overall_stdev):
					neighmeth_spot='cold'
					neighmeth_flag=-1
				 	
			statemeth_overall_temp_ls = statemeth_overall_cases[distr]
			if len(statemeth_overall_temp_ls)>=1:
				statemeth_overall_mean = round(statistics.mean(statemeth_overall_temp_ls),2)
			else:
				statemeth_overall_mean = 0
			if len(statemeth_overall_temp_ls)>=2:
				statemeth_overall_stdev = round(statistics.pstdev(statemeth_overall_temp_ls),2)
			else:
				statemeth_overall_stdev = 0
			if overall_cases>(statemeth_overall_mean+statemeth_overall_stdev):
				statemeth_spot='hot'
				statemeth_flag=1
			if overall_cases<(statemeth_overall_mean-statemeth_overall_stdev):
				statemeth_spot='cold'
				statemeth_flag=-1
			if neighmeth_flag!=0:
				method_spot_overall_csv_writer.writerow(['neighborhood',neighmeth_spot,distr_dict[distr]])
			if statemeth_flag!=0:
				method_spot_overall_csv_writer.writerow(['state',statemeth_spot,distr_dict[distr]])
		
		
################################## looping over distr_dict and finding monthly hot and cold for every district ####################################
neighmeth_spot=""
statemeth_spot=""
with open('method-spot-month.csv','w') as method_spot_month:	
	method_spot_month_csv_writer=csv.writer(method_spot_month)
	method_spot_month_csv_writer.writerow(['monthid','method','spot','districtid'])
	for distr in distr_dict:
		neighmeth_flag=0
		statemeth_flag=0
		temp_begin=begin
		temp_end = temp_begin+datetime.timedelta(days=29)
		month_id =1	
		while temp_end <= datetime.datetime(2020, 9, 10):
			monthly_cases=0
			for date in daily_cases:
				temp_ls=daily_cases[date]
				if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
					if distr in temp_ls:
						monthly_cases=monthly_cases+temp_ls[distr]
			neighmeth_temp_dict=neighmeth_monthly_cases[distr]
			neighmeth_temp1 = neighmeth_temp_dict[str(month_id)]
			if len(neighmeth_temp1)>=1:
				neighmeth_monthly_mean = round(statistics.mean(neighmeth_temp1),2)
			else:
				neighmeth_monthly_mean = 0
			if len(neighmeth_temp1)>=2:
				neighmeth_monthly_stdev = round(statistics.pstdev(neighmeth_temp1),2)
				
			else:
				neighmeth_monthly_stdev = 0
			
			if monthly_cases>(neighmeth_monthly_mean+neighmeth_monthly_stdev):
				neighmeth_spot='hot'
				neighmeth_flag=1
			if monthly_cases<(neighmeth_monthly_mean-neighmeth_monthly_stdev):
				neighmeth_spot='cold'
				neighmeth_flag=-1
			
			statemeth_temp_dict = statemeth_monthly_cases[distr]
			statemeth_temp1 = statemeth_temp_dict[str(month_id)]
			if len(statemeth_temp1) >=1:
				statemeth_monthly_mean = round(statistics.mean(statemeth_temp1),2)
			else:
				statemeth_monthly_mean = 0
			if len(statemeth_temp1)>=2:
				statemeth_monthly_stdev = round(statistics.pstdev(statemeth_temp1),2)
			else:
				statemeth_monthly_stdev = 0
			if monthly_cases>(statemeth_monthly_mean+statemeth_monthly_stdev):
				statemeth_spot='hot'
				statemeth_flag=1
			if monthly_cases<(statemeth_monthly_mean-statemeth_monthly_stdev):
				statemeth_spot='cold'
				statemeth_flag=-1
			if neighmeth_flag!=0:
				method_spot_month_csv_writer.writerow([month_id,'neighborhood',neighmeth_spot,distr_dict[distr]])
			if statemeth_flag!=0:
				method_spot_month_csv_writer.writerow([month_id,'state',statemeth_spot,distr_dict[distr]])
			month_id =month_id+1
			temp_begin=temp_begin+datetime.timedelta(days=30)
			temp_end=temp_begin+datetime.timedelta(days=29)
		
