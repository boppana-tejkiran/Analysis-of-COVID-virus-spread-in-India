import json
import collections
import pandas as pd
import datetime
import csv
import statistics

begin=datetime.datetime(2020, 3, 15)
end = datetime.datetime(2020, 9, 5)
################## loading daily cases file to use covid 19 data ##################
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
	use_neigh_data.update({temp_remove[0]:temp_ls})
############################ making a dictionary of key:id pairs from new-neighbours data ###############################
#print(use_neigh_data)
count=101
distr_dict={}

for item in use_neigh_data.keys():	
	distr_dict.update({item:count})
	count=count+1
#print(distr_dict)

############################ finding weekly avg and standard deviations of neighbour districts for each district in new neighbours file ##########################
neighmeth_weekly_cases={}
neighmeth_overall_cases={}
with open('neighbour-overall.csv','w') as overall_csv:
	overall_csv_writer=csv.writer(overall_csv)
	overall_csv_writer.writerow(['districtid','neighbormean','neighborstdev'])
	with open('neighbour-week.csv','w') as weekly_csv:
		weekly_csv_writer=csv.writer(weekly_csv)
		weekly_csv_writer.writerow(['districtid','weekid','neighbormean','neighborstdev'])
		for distr in use_neigh_data:
			temp_dict={}
			temp_ls=use_neigh_data[distr]
			temp_begin=begin
			temp_end=temp_begin+datetime.timedelta(days=6)
			week_id=1
			overall_cases_ls=[0]*len(temp_ls)
			while temp_end<=datetime.datetime(2020, 9, 5):
				weekly_ls=[] 
				count=0
				for neigh_distr in temp_ls:
					weekly_cases=0
					for date in daily_cases:
						if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
							temp_cases_dict=daily_cases[date]
							if neigh_distr in temp_cases_dict:
								weekly_cases=weekly_cases+temp_cases_dict[neigh_distr]
								
					weekly_ls.extend([weekly_cases])
					overall_cases_ls[count]=overall_cases_ls[count]+weekly_cases
					count=count+1
				weekly_mean=round(statistics.mean(weekly_ls),2)
				if len(weekly_ls)>=2:
					weekly_stdev=round(statistics.pstdev(weekly_ls),2)
				else:
					weekly_stdev=0
				weekly_csv_writer.writerow([distr_dict[distr],week_id,weekly_mean,weekly_stdev])
				temp_dict.update({week_id:weekly_ls})
				week_id=week_id+1
				temp_begin=temp_begin+datetime.timedelta(days=7)
				temp_end=temp_begin+datetime.timedelta(days=6)
			overall_cases_mean=round(statistics.mean(overall_cases_ls),2)
			if len(overall_cases_ls)>=2:
				overall_cases_stdev=round(statistics.pstdev(overall_cases_ls),2)
			else:
				overall_cases_stdev=0
			overall_csv_writer.writerow([distr_dict[distr],overall_cases_mean,overall_cases_stdev])
			neighmeth_weekly_cases.update({distr:temp_dict})
			neighmeth_overall_cases.update({distr:overall_cases_ls})
############################### finding monthly avg and standard deviation of neighbour districts for each district in new neighbours file #############################
neighmeth_monthly_cases={}
#print(use_neigh_data)
with open('neighbor-month.csv','w') as monthly_csv:
		monthly_csv_writer=csv.writer(monthly_csv)
		monthly_csv_writer.writerow(['districtid','monthid','neighbormean','neighborstdev'])
		for distr in use_neigh_data:
			temp_dict={}
			temp_ls=use_neigh_data[distr]
			temp_begin=begin
			temp_end=temp_begin+datetime.timedelta(days=29)
			month_id=1
			#print(distr)
			#print(temp_ls)
			while temp_end<=datetime.datetime(2020, 9, 10):
				monthly_ls=[]
				for neigh_distr in temp_ls:
					monthly_cases=0
					for date in daily_cases:
						if datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")>=temp_begin and datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")<=temp_end:  #converting string date to date time object
				
							temp_cases_dict=daily_cases[date]
							if neigh_distr in temp_cases_dict:
								monthly_cases=monthly_cases+temp_cases_dict[neigh_distr]
				
					monthly_ls.extend([monthly_cases])
				monthly_mean=round(statistics.mean(monthly_ls),2)
				if len(monthly_ls)>=2:
					monthly_stdev=round(statistics.pstdev(monthly_ls),2)				
				else:
					monthly_stdev=round(statistics.pstdev(monthly_ls),2)
				temp_dict.update({month_id:monthly_ls})
				#print('entered near csv writer')
				monthly_csv_writer.writerow([distr_dict[distr],month_id,monthly_mean,monthly_stdev])
				month_id=month_id+1
				temp_begin=temp_begin+datetime.timedelta(days=30)
				temp_end=temp_begin+datetime.timedelta(days=29)
			neighmeth_monthly_cases.update({distr:temp_dict})
###################################################################################################################################################################
################ saving the neighmeth weekly, monthly, overall cases to json files##################
with open('neighmeth_weekly_cases.json','w') as f:
	json.dump(neighmeth_weekly_cases,f,indent=4)

with open('neighmeth_monthly_cases.json','w') as f:
	json.dump(neighmeth_monthly_cases,f,indent=4)

with open('neighmeth_overall_cases.json','w') as f:
	json.dump(neighmeth_overall_cases,f,indent=4)					
								
				
				
				
				
				
