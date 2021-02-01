import json
import collections
import pandas as pd
import datetime
import csv
import statistics

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
############################# loading weekly, monthly and overall zscore data into dataframes ############################
weekly_df=pd.read_csv("zscore-week.csv") 
monthly_df=pd.read_csv("zscore-month.csv")
overall_df=pd.read_csv("zscore-overall.csv")

########################## calculating weekly top 5 hotspots and coldspots for every district ###########################

with open('top-week.csv','w') as top_week:
	top_week_csv_writer = csv.writer(top_week)
	top_week_csv_writer.writerow(['weekid','method','spot','districtid1','districtid2','districtid3','districtid4','districtid5'])
	week_id =1
	while week_id<=25:
		neighmeth_zscore_dict={}
		statemeth_zscore_dict={}
		for i,j in weekly_df.iterrows():
			temp_ls= list(j)
			#print(temp_ls)
			if int(temp_ls[1])==week_id:
				neighmeth_zscore_dict.update({int(temp_ls[0]):temp_ls[2]})
				statemeth_zscore_dict.update({int(temp_ls[0]):temp_ls[3]})
		neighmeth_values=list(neighmeth_zscore_dict.values())
		statemeth_values=list(statemeth_zscore_dict.values())
		#print(len(neighmeth_values))
		#print(len(statemeth_values))
		neighmeth_values.sort(reverse=True)
		statemeth_values.sort(reverse=True)
		neighmeth_hs_ls=[]
		neighmeth_cs_ls=[]
		statemeth_hs_ls=[]
		statemeth_cs_ls=[]
		for item in neighmeth_zscore_dict:
			## NHS NHS NHS NHS NHS NHS NHS NHS NHS NSH NHS NHS NHS NHS NHS ##
			if len(neighmeth_hs_ls)<5:
				if neighmeth_values[0]==neighmeth_zscore_dict[item]:
					neighmeth_hs_ls.extend([item])
				if neighmeth_values[1]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[2]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[3]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[4]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
			## NCS NCS NCS NCS NCS NCS NCS NCS NCS NCH NCS NCS NCS NCS NCS ##			
			if len(neighmeth_cs_ls)<5:
				if neighmeth_values[626]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[625]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[624]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[623]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[622]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
			if len(neighmeth_hs_ls)>=5 and len(neighmeth_cs_ls)>=5:
				break
		for item in statemeth_zscore_dict:
			## SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS ##
			if len(statemeth_hs_ls)<5:
				if statemeth_values[0]==statemeth_zscore_dict[item]:
					statemeth_hs_ls.extend([item])
				if statemeth_values[1]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[2]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[3]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[4]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
			## SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS ##
			if len(statemeth_cs_ls)<5:
				if statemeth_values[626]==statemeth_zscore_dict[item]:
					statemeth_cs_ls.extend([item])
				if statemeth_values[625]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[624]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[623]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[622]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
			if len(statemeth_hs_ls)>=5 and len(statemeth_cs_ls)>=5:
				break
		##  -------------------------------------------------------------------- ##
		
		neighmeth_hs_d1 = neighmeth_hs_ls[0]
		neighmeth_hs_d2 = neighmeth_hs_ls[1]
		neighmeth_hs_d3 = neighmeth_hs_ls[2]
		neighmeth_hs_d4 = neighmeth_hs_ls[3]
		neighmeth_hs_d5 = neighmeth_hs_ls[4]
			
		neighmeth_cs_d1= neighmeth_cs_ls[0]
		neighmeth_cs_d2= neighmeth_cs_ls[1]
		neighmeth_cs_d3= neighmeth_cs_ls[2]
		neighmeth_cs_d4= neighmeth_cs_ls[3]
		neighmeth_cs_d5= neighmeth_cs_ls[4]
			
		statemeth_hs_d1 = statemeth_hs_ls[0]
		statemeth_hs_d2 = statemeth_hs_ls[1]
		statemeth_hs_d3 = statemeth_hs_ls[2]
		statemeth_hs_d4 = statemeth_hs_ls[3]
		statemeth_hs_d5 = statemeth_hs_ls[4]
			
		statemeth_cs_d1 = statemeth_cs_ls[0]
		statemeth_cs_d2 = statemeth_cs_ls[1]
		statemeth_cs_d3 = statemeth_cs_ls[2]
		statemeth_cs_d4 = statemeth_cs_ls[3]
		statemeth_cs_d5 = statemeth_cs_ls[4]
	
		
		## -------------------------------------------------- ##
		top_week_csv_writer.writerow([week_id,'neighborhood','hot',neighmeth_hs_d1,neighmeth_hs_d2,neighmeth_hs_d3,neighmeth_hs_d4,neighmeth_hs_d5])
		top_week_csv_writer.writerow([week_id,'neighborhood','cold',neighmeth_cs_d1,neighmeth_cs_d2,neighmeth_cs_d3,neighmeth_cs_d4,neighmeth_cs_d5])
		top_week_csv_writer.writerow([week_id,'state','hot',statemeth_hs_d1,statemeth_hs_d2,statemeth_hs_d3,statemeth_hs_d4,statemeth_hs_d5])
		top_week_csv_writer.writerow([week_id,'state','cold',statemeth_cs_d1,statemeth_cs_d2,statemeth_cs_d3,statemeth_cs_d4,statemeth_cs_d5])
		week_id=week_id+1
			


########################## calculating monthly top 5 hotspots and coldspots for every district ###########################

with open('top-month.csv','w') as top_month:
	top_month_csv_writer = csv.writer(top_month)
	top_month_csv_writer.writerow(['monthid','method','spot','districtid1','districtid2','districtid3','districtid4','districtid5'])
	month_id =1
	while month_id<=6:
		neighmeth_zscore_dict={}
		statemeth_zscore_dict={}
		for i,j in monthly_df.iterrows():
			temp_ls= list(j)
			#print(temp_ls)
			if int(temp_ls[1])==month_id:
				neighmeth_zscore_dict.update({int(temp_ls[0]):temp_ls[2]})
				statemeth_zscore_dict.update({int(temp_ls[0]):temp_ls[3]})
		neighmeth_values=list(neighmeth_zscore_dict.values())
		statemeth_values=list(statemeth_zscore_dict.values())
		neighmeth_values.sort(reverse=True)
		statemeth_values.sort(reverse=True)
		neighmeth_hs_ls=[]
		neighmeth_cs_ls=[]
		statemeth_hs_ls=[]
		statemeth_cs_ls=[]
		for item in neighmeth_zscore_dict:
			## NHS NHS NHS NHS NHS NHS NHS NHS NHS NSH NHS NHS NHS NHS NHS ##
			if len(neighmeth_hs_ls)<5:
				if neighmeth_values[0]==neighmeth_zscore_dict[item]:
					neighmeth_hs_ls.extend([item])
				if neighmeth_values[1]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[2]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[3]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[4]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
			## NCS NCS NCS NCS NCS NCS NCS NCS NCS NCH NCS NCS NCS NCS NCS ##			
			if len(neighmeth_cs_ls)<5:
				if neighmeth_values[626]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[625]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[624]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[623]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[622]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
			if len(neighmeth_hs_ls)>=5 and len(neighmeth_cs_ls)>=5:
				break
		for item in statemeth_zscore_dict:
			## SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS ##
			if len(statemeth_hs_ls)<5:
				if statemeth_values[0]==statemeth_zscore_dict[item]:
					statemeth_hs_ls.extend([item])
				if statemeth_values[1]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[2]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[3]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[4]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
			## SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS ##
			if len(statemeth_cs_ls)<5:
				if statemeth_values[626]==statemeth_zscore_dict[item]:
					statemeth_cs_ls.extend([item])
				if statemeth_values[625]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[624]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[623]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[622]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
			if len(statemeth_hs_ls)>=5 and len(statemeth_cs_ls)>=5:
				break
		##  -------------------------------------------------------------------- ##
		
		neighmeth_hs_d1 = neighmeth_hs_ls[0]
		neighmeth_hs_d2 = neighmeth_hs_ls[1]
		neighmeth_hs_d3 = neighmeth_hs_ls[2]
		neighmeth_hs_d4 = neighmeth_hs_ls[3]
		neighmeth_hs_d5 = neighmeth_hs_ls[4]
			
		neighmeth_cs_d1= neighmeth_cs_ls[0]
		neighmeth_cs_d2= neighmeth_cs_ls[1]
		neighmeth_cs_d3= neighmeth_cs_ls[2]
		neighmeth_cs_d4= neighmeth_cs_ls[3]
		neighmeth_cs_d5= neighmeth_cs_ls[4]
			
		statemeth_hs_d1 = statemeth_hs_ls[0]
		statemeth_hs_d2 = statemeth_hs_ls[1]
		statemeth_hs_d3 = statemeth_hs_ls[2]
		statemeth_hs_d4 = statemeth_hs_ls[3]
		statemeth_hs_d5 = statemeth_hs_ls[4]
			
		statemeth_cs_d1 = statemeth_cs_ls[0]
		statemeth_cs_d2 = statemeth_cs_ls[1]
		statemeth_cs_d3 = statemeth_cs_ls[2]
		statemeth_cs_d4 = statemeth_cs_ls[3]
		statemeth_cs_d5 = statemeth_cs_ls[4]
		## --------------------------------------------------------------------- ##
		
			
		top_month_csv_writer.writerow([month_id,'neighborhood','hot',neighmeth_hs_d1,neighmeth_hs_d2,neighmeth_hs_d3,neighmeth_hs_d4,neighmeth_hs_d5])
		top_month_csv_writer.writerow([month_id,'neighborhood','cold',neighmeth_cs_d1,neighmeth_cs_d2,neighmeth_cs_d3,neighmeth_cs_d4,neighmeth_cs_d5])
		top_month_csv_writer.writerow([month_id,'state','hot',statemeth_hs_d1,statemeth_hs_d2,statemeth_hs_d3,statemeth_hs_d4,statemeth_hs_d5])
		top_month_csv_writer.writerow([month_id,'state','cold',statemeth_cs_d1,statemeth_cs_d2,statemeth_cs_d3,statemeth_cs_d4,statemeth_cs_d5])
		month_id=month_id+1
			
########################## calculating overall top 5 hotspots and coldspots districts ###########################
with open('top-overall.csv','w') as top_overall:
		top_overall_csv_writer = csv.writer(top_overall)
		top_overall_csv_writer.writerow(['method','spot','districtid1','districtid2','districtid3','districtid4','districtid5'])
		neighmeth_zscore_dict={}
		statemeth_zscore_dict={}
		for i,j in overall_df.iterrows():
			temp_ls= list(j)
			#print(temp_ls)
			neighmeth_zscore_dict.update({int(temp_ls[0]):temp_ls[1]})
			statemeth_zscore_dict.update({int(temp_ls[0]):temp_ls[2]})
		#print(neighmeth_zscore_dict)
		neighmeth_values=list(neighmeth_zscore_dict.values())
		statemeth_values=list(statemeth_zscore_dict.values())
		neighmeth_values.sort(reverse=True)
		statemeth_values.sort(reverse=True)
		#print(neighmeth_values)
		neighmeth_hs_ls=[]
		neighmeth_cs_ls=[]
		statemeth_hs_ls=[]
		statemeth_cs_ls=[]
		for item in neighmeth_zscore_dict:
			## NHS NHS NHS NHS NHS NHS NHS NHS NHS NSH NHS NHS NHS NHS NHS ##
			if len(neighmeth_hs_ls)<5:
				if neighmeth_values[0]==neighmeth_zscore_dict[item]:
					neighmeth_hs_ls.extend([item])
				if neighmeth_values[1]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[2]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[3]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
				if neighmeth_values[4]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_hs_ls:
						neighmeth_hs_ls.extend([item])
			## NCS NCS NCS NCS NCS NCS NCS NCS NCS NCH NCS NCS NCS NCS NCS ##			
			if len(neighmeth_cs_ls)<5:
				if neighmeth_values[626]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[625]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[624]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[623]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
				if neighmeth_values[622]==neighmeth_zscore_dict[item]:
					if item not in neighmeth_cs_ls:
						neighmeth_cs_ls.extend([item])
			if len(neighmeth_hs_ls)>=5 and len(neighmeth_cs_ls)>=5:
				break
		for item in statemeth_zscore_dict:
			## SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS SHS ##
			if len(statemeth_hs_ls)<5:
				if statemeth_values[0]==statemeth_zscore_dict[item]:
					statemeth_hs_ls.extend([item])
				if statemeth_values[1]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[2]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[3]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
				if statemeth_values[4]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_hs_ls.extend([item])
			## SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS SCS ##
			if len(statemeth_cs_ls)<5:
				if statemeth_values[626]==statemeth_zscore_dict[item]:
					statemeth_cs_ls.extend([item])
				if statemeth_values[625]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[624]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[623]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
				if statemeth_values[622]==statemeth_zscore_dict[item]:
					if item not in statemeth_hs_ls:
						statemeth_cs_ls.extend([item])
			if len(statemeth_hs_ls)>=5 and len(statemeth_cs_ls)>=5:
				break
		##  -------------------------------------------------------------------- ##
		
		neighmeth_hs_d1 = neighmeth_hs_ls[0]
		neighmeth_hs_d2 = neighmeth_hs_ls[1]
		neighmeth_hs_d3 = neighmeth_hs_ls[2]
		neighmeth_hs_d4 = neighmeth_hs_ls[3]
		neighmeth_hs_d5 = neighmeth_hs_ls[4]
			
		neighmeth_cs_d1= neighmeth_cs_ls[0]
		neighmeth_cs_d2= neighmeth_cs_ls[1]
		neighmeth_cs_d3= neighmeth_cs_ls[2]
		neighmeth_cs_d4= neighmeth_cs_ls[3]
		neighmeth_cs_d5= neighmeth_cs_ls[4]
			
		statemeth_hs_d1 = statemeth_hs_ls[0]
		statemeth_hs_d2 = statemeth_hs_ls[1]
		statemeth_hs_d3 = statemeth_hs_ls[2]
		statemeth_hs_d4 = statemeth_hs_ls[3]
		statemeth_hs_d5 = statemeth_hs_ls[4]
			
		statemeth_cs_d1 = statemeth_cs_ls[0]
		statemeth_cs_d2 = statemeth_cs_ls[1]
		statemeth_cs_d3 = statemeth_cs_ls[2]
		statemeth_cs_d4 = statemeth_cs_ls[3]
		statemeth_cs_d5 = statemeth_cs_ls[4]
		## --------------------------------------------------------------------- ##
		'''
		for distr in distr_dict:   ## code to convert distrrict ids back to district names
			if distr_dict[distr]==neighmeth_hs_ls[0]:
				neighmeth_hs_d1=distr
			if distr_dict[distr]==neighmeth_hs_ls[1]:
				neighmeth_hs_d2=distr
			if distr_dict[distr]==neighmeth_hs_ls[2]:
				neighmeth_hs_d3=distr
			if distr_dict[distr]==neighmeth_hs_ls[3]:
				neighmeth_hs_d4=distr
			if distr_dict[distr]==neighmeth_hs_ls[4]:
				neighmeth_hs_d5=distr
			
			if distr_dict[distr]==neighmeth_cs_ls[0]:
				neighmeth_cs_d1=distr
			if distr_dict[distr]==neighmeth_cs_ls[1]:
				neighmeth_cs_d2=distr
			if distr_dict[distr]==neighmeth_cs_ls[2]:
				neighmeth_cs_d3=distr
			if distr_dict[distr]==neighmeth_cs_ls[3]:
				neighmeth_cs_d4=distr
			if distr_dict[distr]==neighmeth_cs_ls[4]:
				neighmeth_cs_d5=distr
			## --------------------------------------- ##
			
			if distr_dict[distr]==statemeth_hs_ls[0]:
				statemeth_hs_d1=distr
			if distr_dict[distr]==statemeth_hs_ls[1]:
				statemeth_hs_d2=distr
			if distr_dict[distr]==statemeth_hs_ls[2]:
				statemeth_hs_d3=distr
			if distr_dict[distr]==statemeth_hs_ls[3]:
				statemeth_hs_d4=distr
			if distr_dict[distr]==statemeth_hs_ls[4]:
				statemeth_hs_d5=distr
			
			if distr_dict[distr]==statemeth_cs_ls[0]:
				statemeth_cs_d1=distr
			if distr_dict[distr]==statemeth_cs_ls[1]:
				statemeth_cs_d2=distr
			if distr_dict[distr]==statemeth_cs_ls[2]:
				statemeth_cs_d3=distr
			if distr_dict[distr]==statemeth_cs_ls[3]:
				statemeth_cs_d4=distr
			if distr_dict[distr]==statemeth_cs_ls[4]:
				statemeth_cs_d5=distr
				'''
		## ------------------------------------------------------- ##	
		top_overall_csv_writer.writerow(['neighborhood','hot',neighmeth_hs_d1,neighmeth_hs_d2,neighmeth_hs_d3,neighmeth_hs_d4,neighmeth_hs_d5])
		top_overall_csv_writer.writerow(['neighborhood','cold',neighmeth_cs_d1,neighmeth_cs_d2,neighmeth_cs_d3,neighmeth_cs_d4,neighmeth_cs_d5])
		top_overall_csv_writer.writerow(['state','hot',statemeth_hs_d1,statemeth_hs_d2,statemeth_hs_d3,statemeth_hs_d4,statemeth_hs_d5])
		top_overall_csv_writer.writerow(['state','cold',statemeth_cs_d1,statemeth_cs_d2,statemeth_cs_d3,statemeth_cs_d4,statemeth_cs_d5])


##############################################################################################################################################################
