import json
import collections
import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
with open('../dataset/data-all.json') as f:
	data_all= json.load(f)

df=pd.DataFrame.from_dict(data_all,orient='index')
#print(df)
df.to_csv('data-all.csv')
st_dt_dict={}
distr_names=[]
state_codes=list(df.columns)
#print(state_codes)
for i,j in df.iterrows():
		temp=0
		for lv1 in j:   # j is a panda series
			if type(lv1)!=type(2.0000):
				for lv2 in lv1:
					if lv2=='districts':
						distr_dict= lv1[lv2]
						distr_list=list(distr_dict.keys())
						if state_codes[temp] in st_dt_dict:
							temp_ls=list(st_dt_dict.get(state_codes[temp]))
							temp_ls.extend(distr_list)
							temp_ls=list(set(temp_ls))
							if 'Unknown' in temp_ls:
								temp_ls.remove('Unknown')
							if 'BSF Camp' in temp_ls:
								temp_ls.remove('BSF Camp')
							if 'Italians' in temp_ls:
								temp_ls.remove('Italians')
							if 'Other State' in temp_ls:
								temp_ls.remove('Other State')
							if 'Others' in temp_ls:
								temp_ls.remove('Others')
							if 'Foreign Evacuees' in temp_ls:
								temp_ls.remove('Foreign Evacuees')
							if 'Airport Quarantine' in temp_ls:
								temp_ls.remove('Airport Quarantine')
							if 'Railway Quarantine' in temp_ls:
								temp_ls.remove('Railway Quarantine')
							if 'State Pool' in temp_ls:
								temp_ls.remove('State Pool')
							st_dt_dict[state_codes[temp]]=temp_ls
							distr_names.extend(temp_ls)
							distr_names=list(set(distr_names))
						else:
							st_dt_dict.update({state_codes[temp]:distr_list})
			temp=temp+1
with open('state-information.json','w') as state_info:
	json.dump(st_dt_dict,state_info,indent=4)
###### We have cleaned the data from districts taken from all-data.json in above code ##################################
#print(distr_names)
updated_data_neigh={}
with open('neighbor-districts.json') as f:
	data_neigh = json.load(f)
for distr in data_neigh:
	temp_ls=data_neigh[distr]
	temp=0
	for i in temp_ls:
		temp_ls2=i.split("/")
		if temp_ls2[0].endswith("_district"):
			temp_ls2[0]=temp_ls2[0].replace("_district","")
			#print(temp_ls2[0])
		if temp_ls2[0].find("_")!=-1:
			capital_temp_ls=temp_ls2[0].split("_")
			temp_ls2[0]=" ".join(capital_temp_ls)
		temp_ls2[0]=temp_ls2[0].title()
		for j in distr_names:
			if similar(temp_ls2[0],j)>=0.90:
				temp_ls2[0]=j
				break
		temp_ls2[0]=temp_ls2[0]+str("/")
		temp_ls[temp]="".join(temp_ls2)
		#print(temp_ls[temp])
		temp=temp+1
	temp_str=distr.split("/")
	if temp_str[0].endswith("_district"):
		temp_str[0]=temp_str[0].replace("_district","")
	if temp_str[0].find("_")!=-1:
		capital_temp_str=temp_str[0].split("_")
		temp_str[0]=" ".join(capital_temp_str)
	temp_str[0]=temp_str[0].title()
	for j in distr_names:
		if similar(temp_str[0],j)>=0.90:
			temp_str[0]=j
			break
	temp_str[0]=temp_str[0]+"/"
	temp_distr="".join(temp_str)
	updated_data_neigh.update({temp_distr:temp_ls})
###################################### Clubbing of all Districts in Telangana to a single District Telangana ########################### 
Telangana=['Adilabad/Q15211', 'Bhadradri Kothagudem/Q28169767', 'Hyderabad/Q15340', 'Jagtial/Q28169780', 'Jangaon/Q28170170', 'Jayashankar Bhupalapally/Q28169775', 'Jogulamba Gadwal/Q27897618', 'Kamareddy/Q27956125', 'Karimnagar/Q15373', 'Khammam/Q15371', 'Komram Bheem/Q28170184', 'Mahabubabad/Q28169761', 'Mahabubnagar/Q15380', 'Mancherial/Q28169747', 'Medak/Q15386', 'Medchal–Malkajgiri/Q27614841', 'Mulugu/Q61746006', 'Nagarkurnool/Q28169773', 'Narayanpet/Q61746013', 'Nalgonda/Q15384', 'Nirmal/Q28169750', 'Nizamabad/Q15391', 'Peddapalli/Q27614797', 'Rajanna Sircilla/Q28172781', 'Rangareddy/Q15388', 'Sangareddy/Q28169753', 'Siddipet/Q28169756', 'Suryapet/Q28169770', 'Vikarabad/Q28170173', 'Wanaparthy/Q28172504', 'Warangal Urban/Q213077', 'Warangal Rural/Q28169759', 'Yadadri Bhuvanagiri/Q28169764']
Telangana_neigh_ls=[]

for distr in updated_data_neigh:
	if distr in Telangana:
		Telangana_neigh_ls.extend(updated_data_neigh[distr])
	
Telangana_neigh_ls=list(set(Telangana_neigh_ls))
#print(Telangana_neigh_ls)
#print(len(Telangana_neigh_ls))
Telangana_neigh_ls=[x for x in Telangana_neigh_ls if x not in  Telangana]
for distr in Telangana:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Telangana:
			temp_ls[temp]='Telangana/Q15211'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))
updated_data_neigh.update({'Telangana/Q15211':Telangana_neigh_ls})

###################################### Clubbing of all Districts in Delhi to a single District Delhi ###########################
Delhi=['Central Delhi/Q107941', 'East Delhi/Q107960', 'North East Delhi/Q429329', 'North Delhi/Q693367', 'North West Delhi/Q766125', 'West Delhi/Q549807', 'New Delhi/Q987', 'South East Delhi/Q25553535', 'South West Delhi/Q2379189', 'South Delhi/Q2061938', 'Shahdara/Q83486']
Delhi_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Delhi:
		Delhi_neigh_ls.extend(updated_data_neigh[distr])
		
Delhi_neigh_ls=list(set(Delhi_neigh_ls))
Delhi_neigh_ls=[x for x in Delhi_neigh_ls if x not in  Delhi]

for distr in Delhi:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Delhi:
			temp_ls[temp]='Delhi/Q107960'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Delhi/Q107960':Delhi_neigh_ls})
###################################### Clubbing of all Districts in Sikkim to a single District Sikkim ###########################
Sikkim=['East Sikkim/Q1772832', 'West Sikkim/Q611357', 'North Sikkim/Q1784149', 'South Sikkim/Q1805051']
Sikkim_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Sikkim:
		Sikkim_neigh_ls.extend(updated_data_neigh[distr])
		
Sikkim_neigh_ls=list(set(Sikkim_neigh_ls))
Sikkim_neigh_ls=[x for x in Sikkim_neigh_ls if x not in  Sikkim]

for distr in Sikkim:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Sikkim:
			temp_ls[temp]='Sikkim/Q1772832'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Sikkim/Q1772832':Sikkim_neigh_ls})
###################################### Clubbing of all Districts in Assam to a single District Assam ###########################
Assam=['Kokrajhar/Q42618', 'Dhubri/Q42485', 'Bongaigaon/Q42197', 'Chirang/Q2574898', 'Barpeta/Q41249', 'Goalpara/Q42522', 'Nalbari/Q42779', 'Kamrup/Q2247441', 'Baksa/Q2360266', 'Darrang/Q42461', 'Marigaon/Q42737', 'Sonitpur/Q42765', 'Udalguri/Q321998', 'Kamrup Metropolitan/Q2464674', 'South Salmara-Mankachar/Q24907599', 'Nagaon/Q42686', 'West Karbi Anglong/Q24949218','East Karbi Anglong/Q42558', 'Dima Hasao/Q42774', 'Golaghat/Q42517', 'Hojai/Q24699407', 'Cachar/Q42209', 'Hailakandi/Q42505', 'Karimganj/Q42542', 'Bishwanath/Q28110722', 'Jorhat/Q42611', 'Lakhimpur/Q42743', 'Majuli/Q28110729', 'Sivasagar/Q42768', 'Dhemaji/Q42473', 'Dibrugarh/Q42479', 'Tinsukia/Q42756', 'Charaideo/Q24039029']
Assam_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Assam:
		Assam_neigh_ls.extend(updated_data_neigh[distr])
		
Assam_neigh_ls=list(set(Assam_neigh_ls))
Assam_neigh_ls=[x for x in Assam_neigh_ls if x not in  Assam]

for distr in Assam:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Assam:
			temp_ls[temp]='Assam/Q42558'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Assam/Q42558':Assam_neigh_ls})
###################################### Clubbing of all Districts in Goa to a single District Goa ###########################
Goa=['North Goa/Q108234','South Goa/Q108244']
Goa_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Goa:
		Goa_neigh_ls.extend(updated_data_neigh[distr])
		
Goa_neigh_ls=list(set(Goa_neigh_ls))
Goa_neigh_ls=[x for x in Goa_neigh_ls if x not in Goa]

for distr in Goa:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Goa:
			temp_ls[temp]='Goa/Q108234'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Goa/Q108234':Goa_neigh_ls})
###################################### Clubbing of all Districts in Manipur to a single District Manipur ###########################
Manipur=['Tamenglong/Q2301717', 'Jiribam/Q28419387', 'Pherzawl/Q28173809', 'Churachandpur/Q2577281', 'Bishnupur/Q938190', 'Chandel/Q2301769', 'Noney/Q28419389', 'Kakching/Q28173825', 'Imphal East/Q1916666', 'Imphal West/Q1822188', 'Thoubal/Q2086198', 'Kangpokpi/Q28419386', 'Senapati/Q2301706', 'Ukhrul/Q735101', 'Tengnoupal/Q28419388', 'Kamjong/Q28419390']
Manipur_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Manipur:
		Manipur_neigh_ls.extend(updated_data_neigh[distr])
		
Manipur_neigh_ls=list(set(Manipur_neigh_ls))
Manipur_neigh_ls=[x for x in Manipur_neigh_ls if x not in Manipur]

for distr in Manipur:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Manipur:
			temp_ls[temp]='Manipur/Q938190'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Manipur/Q938190':Manipur_neigh_ls})
################################## Clubbing of Mumbai city and Mumbai subarban in to a single District Mumbai ########################
Mumbai=['Mumbai Suburban/Q2085374','Mumbai City/Q2341660']
Mumbai_neigh_ls=[]
for distr in updated_data_neigh:
	if distr in Mumbai:
		Mumbai_neigh_ls.extend(updated_data_neigh[distr])
		
Mumbai_neigh_ls=list(set(Mumbai_neigh_ls))
Mumbai_neigh_ls=[x for x in Mumbai_neigh_ls if x not in Mumbai]

for distr in Mumbai:
	if distr in updated_data_neigh:
		del updated_data_neigh[distr]

for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in Mumbai:
			temp_ls[temp]='Mumbai/Q2341660'
		temp=temp+1
	updated_data_neigh[distr]=list(set(temp_ls))

updated_data_neigh.update({'Mumbai/Q2341660':Mumbai_neigh_ls})
################################## Updating dissimilar district names ###################################################################
unmatched_distr={'The Nilgiris/Q15188':'Nilgiris/Q15188', 'Palghat/Q1535742':'Palakkad/Q1535742', 'Kochbihar/Q2728658':'Cooch Behar/Q2728658', 'Purba Champaran/Q49159':'East Champaran/Q49159', 'Pashchim Champaran/Q100124':'West Champaran/Q100124', 'Rae Bareilly/Q1321157':'Rae Bareli/Q1321157','Tirunelveli Kattabo/Q15200':'Tirunelveli/Q15200', 'Pattanamtitta/Q634935':'Pathanamthitta/Q634935', 'Kanchipuram/Q15157':'Kancheepuram/Q15157', 'Sri Potti Sriramulu Nellore/Q15383':'S.P.S. Nellore/Q15383', 'Rajauri/Q544279':'Rajouri/Q544279', 'Firozpur/Q172385':'Ferozepur/Q172385', 'Sri Ganganagar/Q1419696':'Ganganagar/Q1419696', 'Dhaulpur/Q1207709':'Dholpur/Q1207709', 'Jyotiba Phule Nagar/Q1891677': 'Amroha/Q1891677', 'Kheri/Q1755447':'Lakhimpur Kheri/Q1755447', 'Sait Kibir Nagar/Q1945445': 'Sant Kabir Nagar/Q1945445', 'Mahesana/Q2019694':'Mehsana/Q2019694','The Dangs/Q1135616': 'Dang/Q1135616', 'Faizabad/Q1814132':'Ayodhya/Q1814132', 'Sant Ravidas Nagar/Q127533':'Bhadohi/Q127533' , 'Kaimur (Bhabua)/Q77367':'Kaimur/Q77367', 'Kodarma/Q2085480':'Koderma/Q2085480', 'Purbi Singhbhum/Q2452921':'East Singhbhum/Q2452921', 'Seraikela Kharsawan/Q2362658':'Saraikela-Kharsawan/Q2362658', 'Baleshwar/Q2022279':'Balasore/Q2022279', 'Pashchimi Singhbhum/Q1950527':'West Singhbhum/Q1950527', 'Bemetara/Q16254159':'Bametara/Q16254159','Kabirdham/Q2450255':'Kabeerdham/Q2450255', 'Dantewada/Q100211':'Dakshin Bastar Dantewada/Q100211', 'Narsimhapur/Q2341616':'Narsinghpur/Q2341616', 'Sonapur/Q1473957':'Subarnapur/Q1473957', 'Baudh/Q2363639':'Boudh/Q2363639', 'Debagarh/Q2269639':'Deogarh/Q2269639', 'Bid/Q814037':'Beed/Q814037', 'Belgaum/Q815464':'Belagavi/Q815464', 'Shimoga/Q2981389':'Shivamogga/Q2981389', 'Tumkur/Q1301635':'Tumakuru/Q1301635', 'Bellary/Q1791926':'Ballari/Q1791926', 'Yadagiri/Q1786949':'Yadgir/Q1786949', 'Ysr/Q15342':'Y.S.R. Kadapa/Q15342', 'Aizwal/Q1947322':'Aizawl/Q1947322', 'Sahibzada Ajit Singh Nagar/Q2037672': 'S.A.S. Nagar/Q2037672','Bangalore Rural/Q806464':'Bengaluru Rural/Q806464','Bangalore Urban/Q806463':'Bengaluru Urban/Q806463','Panch Mahal/Q1781463':'Panchmahal/Q1781463','Ri-Bhoi/Q1884672':'Ribhoi/Q1884672', 'Banas Kantha/Q806125':'Banaskantha/Q806125', 'Muktsar/Q1947359':'Sri Muktsar Sahib/Q1947359', 'Badgam/Q2594218':'Budgam/Q2594218','Sabar Kantha/Q1772856':'Sabarkantha/Q1772856','Nav Sari/Q1797349':'Navsari/Q1797349','Siddharth Nagar/Q1815339':'Siddharthnagar/Q1815339','Ashok Nagar/Q2246416':'Ashoknagar/Q2246416','Hugli/Q548518':'Hooghly/Q548518','Bijapur/Q1727570':'Vijayapura/Q1727570'}
final_neigh={}
for distr in updated_data_neigh:
	temp_ls=updated_data_neigh[distr]
	temp=0
	for neigh_distr in temp_ls:
		if neigh_distr in unmatched_distr:
			temp_ls[temp]=unmatched_distr[neigh_distr]
		temp=temp+1
	if distr in unmatched_distr:
		distr=unmatched_distr[distr]
	final_neigh.update({distr:temp_ls}) 
#print(final_neigh)
####################### Removing Naklak and Konkan division districts from neighbours json file as they are not present in covid data ############

remove_distr=['Konkan Division/Q6268840','Noklak/Q48731903']
for distr in final_neigh: ##loop to remove districts in value lists
	temp_neigh_ls=final_neigh[distr]
	for neigh_distr in temp_neigh_ls:
		if neigh_distr in remove_distr:
			temp_neigh_ls.remove(neigh_distr)
	final_neigh[distr]=temp_neigh_ls
		
for distr in remove_distr:
	if distr in final_neigh:
		del final_neigh[distr]
######################## separating districts with same names and adding state codes to them ###########################################
same_name_distr={'Aurangabad/Q592942':'Aurangabad_MH/Q592942', 'Aurangabad/Q43086':'Aurangabad_BR/Q43086', 'Balrampur/Q16056268':'Balrampur_CT/Q16056268', 'Balrampur/Q1948380':'Balrampur_UP/Q1948380', 'Hamirpur/Q2019757':'Hamirpur_UP/Q2019757', 'Hamirpur/Q2086180':'Hamirpur_HP/Q2086180', 'Bilaspur/Q1478939':'Bilaspur_HP/Q1478939','Bilaspur/Q100157':'Bilaspur_CT/Q100157', 'Pratapgarh/Q1585433':'Pratapgarh_RJ/Q1585433', 'Pratapgarh/Q1473962':'Pratapgarh_UP/Q1473962'}
for distr in final_neigh:  #updating district names at value level
	temp_neigh_ls=final_neigh[distr]
	temp=0
	for  neigh_distr in temp_neigh_ls:
		if neigh_distr in same_name_distr:
			temp_neigh_ls[temp]=same_name_distr[neigh_distr]	
		temp=temp+1
	final_neigh[distr]=temp_neigh_ls

for distr in same_name_distr:  #updating district names at key level
	if distr in final_neigh:
		temp_neigh_ls=final_neigh[distr]
		del final_neigh[distr]
		final_neigh.update({same_name_distr[distr]:temp_neigh_ls})
#print(final_neigh)
####### ========== adjusting mismatch occured due to string match function =========== #########
stringmatch_issue={'Gondia/Q1937857':'Gonda/Q1937857'}
for distr in final_neigh:
	temp_neigh_ls=final_neigh[distr]
	temp=0
	for neigh_distr in temp_neigh_ls:
		if neigh_distr in stringmatch_issue:
			temp_neigh_ls[temp]=stringmatch_issue[neigh_distr]
		temp=temp+1
	final_neigh[distr]=temp_neigh_ls
	
for distr in stringmatch_issue:
	if distr in final_neigh:
		temp_neigh_ls=final_neigh[distr]
		del final_neigh[distr]
		final_neigh.update({stringmatch_issue[distr]:temp_neigh_ls})
############################# This is to find mismatches between json districts and covid 19 data districts ##############################################################
#print(final_neigh)
neigh_keys=final_neigh.keys()
temp_ls=[]
for i in neigh_keys:
	count=0
	temp_str=i.split("/")
	for j in distr_names:
		if temp_str[0]==j:
			count=1
			break
	if count==0:
		temp_ls.append(i)
#print(len(temp_ls))	
#print((temp_ls))

############################################# Sorting districts and adding ids to districts ########################################################
ordered_data = collections.OrderedDict(sorted(final_neigh.items()))
i=101
for distr in ordered_data:
	temp_ls=ordered_data[distr]
	temp_ls.extend([i])
	ordered_data[distr]=temp_ls
	i=i+1
with open('neighbor-districts-modified.json','w') as f:
	json.dump(ordered_data,f,indent=4)		
