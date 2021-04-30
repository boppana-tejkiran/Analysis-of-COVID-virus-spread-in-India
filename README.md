This repository is submission for assignment-1 for DataMIning Course (CS685) at IIT Kanpur in the Autumn semester 2020. In this assignment the trends of COVID Virus spread across India were analyzed as per the questions of assignment. Conclusions were drawn regarding the effect of Lock down imposed in India.

## How to use manual for executing the code

---------------------------
**How to execute the code:**
i) Open the terminal and change the current working directory to the "bash_scripts" sub-folder
ii) This folder contains a script file  “assign1.sh”. This "assign1.sh" has to be executed by using the following commands in terminal:

```sh
$ chmod u+r+x assign1.sh
$ ./assign1.sh
```

iii) The assign1.sh file is the top level script file which contains individual script files (.sh files) which inturn execute the python3 (.py) programs that produce the required outputs as per the requirement of each question in the assignment in .csv format and .json format [It takes around 25-30 minutes for the assign1.sh file to execute]
iv) To execute the report.tex file and convert it into report.pdf perform the follwing commands in order in terminal:

```sh
$ latex report.tex 
$ dvips report.dvi
$ ps2pdf report.ps
```
We will get the report.pdf as output file.

------------------------------------
**Python Modules used in Programs are:**
1) json
2) collections
3) pandas
4) datetime
5) csv
6) statistics
7) difflib
-------------------------------------------

**Contents of the Repository:**

The repository consists of python3 files (.py files) in "python_scripts" folder, bash script files (.sh files) in "bash_scripts" folder and output .csv files in results folder, and report.tex latex file and images needed for it in report folder.

Note : The resulting .csv files generated by executing assign1.sh will be saved into bash_scripts folder. These output files will automatically get rewritten when assign1.sh will be re-executed

----------------------------------------------------------------------
**The data files used for solving the assignment 1 are mentioned below:**

1) data-all.json : This json file contains district wise COVID 19 cases information and is downloaded from https://api.covid19india.org/ website. This file is present in "dataset" folder 
2) neighbor-dictricts.json: This file  is provided with the assignment and it contains information of neighbor districts for districts in India. This file is present in "bash_scripts" folder.

-------------------------------------------------------------------------
**The “.py files” and “.sh files” present in the repository are mentioned below:**

1) questn1.py

	Input files used by the program: 
	1) data-all.json
        2) neighbor-districts.json

	Output files generated by the program: 
	1) neighbor-districts-modified.json
	2) data-all.csv

	Intermediate files generated by the program for use in next programs:
	1) state-information.json

	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn1.py is: neighbor-districts-modified-generator.sh


2) questn2.py

	Input files used by the program: 
	1) data-all.json 
	2) neighbor-districts-modified.json

    	Output files generated by the program: 
	1) cases-week.csv 
	2) cases-month.csv
	3) cases-overall.csv

    	Intermediate files generated by the program for use in next programs:
	1) day-wise-cases.json

    	Functionality of the program: Explained in report.tex file
	
    	Script file which executes questn2.py is: case-generator.sh


3) questn3.py

	Input files used by the program:
	1) neighbor-districts-modified.json
	
	Output files generated by the program:
	1) edge-graph.csv
   
   	Functionality of the program: Explained in report.tex file
	
   	Script file which executes questn3.py is: edge-generator.sh

4) questn4.py

	Input files used by the program:
	1) neighbor-districts-modified.json
	2) day-wise-cases.json
   	
	Output files generated by the program:
	1) neighbor-week.csv
	2) neighbor-month.csv
	3) neighbor-overall.csv
   	
	Intermediate files generated by the program for use in next programs:
	1) neighmeth_weekly_cases.json
	2) neighmeth_monthly_cases.json
	3) neighmeth_overall_cases.json
		
	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn4.py is: neighbor-generator.sh

5) questn5.py

	Input files used by the program:
	1) day-wise-cases.json
	2) neighbor-districts-modified.json
	3) state-information.json
	
   	Output files generated by the program:
	1) state-week.csv
	2) state-month.csv
	3) state-overall.csv
   
   	Intermediate files generated by the program for use in next programs:
	1) statemeth_weekly_cases.json
	2) statemeth_monthly_cases.json
	3) statemeth_overall_cases.json

	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn5.py is:  state-generator.sh

6) question6.py

	Input files used by the program:
	1) neighbor-districts-modified.json
	2) day-wise-cases.json
	3) neighmeth_weekly_cases.json
	4) neighmeth_monthly_cases.json
	5) neighmeth_overall_cases.json
	6) statemeth_weekly_cases.json
	7) statemeth_monthly_cases.json
	8) statemeth_overall_cases.json
	
	Output files generated by the program:
	1) zscore-week.csv
	2) zscore-month.csv
	3) zscore-overall.csv
	
	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn6.py is: zscore-generator.sh

7) questn7.py

	Input files used by the program:
	1) neighbor-districts-modified.json
	2) day-wise-cases.json
	3) neighmeth_weekly_cases.json
	4) neighmeth_monthly_cases.json
	5) neighmeth_overall_cases.json
	6) statemeth_weekly_cases.json
	7) statemeth_monthly_cases.json
	8) statemeth_overall_cases.json
   
   	Output files generated by the program:
	1) method-spot-week.csv
	2) method-spot-month.csv
	3) method-spot-overall.csv
        
    	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn7.py is: method-spot-generator.sh
	
8) questn8.py

	Input files used by the program:
	1) zscore-week.csv
	2) zscore-month.csv
	3) zscore-overall.csv
	4) neighbor-districts-modified.json
   	
	Output files generated by the program:
	1) top-week.csv
	2) top-month.csv
	3) top-overall.csv

	Functionality of the program: Explained in report.tex file
	
	Script file which executes questn8.py is: top-generator.sh
--------------------------------------------

## Note:
1) The above mentoined 8 script files are executed by assign1.sh file and each of these script files execute their respective python3 (.py) programs.

2) The execution time required to execute the 8 python programs and generate the output files when assign1.sh file is executed is around 25-30 minutes

3) The week ids are generated as: A week is counted statring from sunday to saturday from 15-03-2020 to 05-09-2020. A total of 25 week ids were generated between the said dates.

4) The month ids are generated as: A month is counted for every 30 days from 15-03-2020. A total of 6 six month ids are generated from 15-03-2020 to 05-09-2020.

This way of counting month ids for every 30 days from 15-03-2020 is prefered over counting a month ids in the following way. Which is: from (15-03-2020 to 31-03-2020 : month id =1, For April : month id =2, For May : month id =3, For June : month id =4, For July: month id = 5, For August : month id = 6, From 01-09-2020 to 05-09-2020 : month id = 7). Because second method does not give equal size month intervals to compare the growth of COVID cases across months. Because in second method, some month ids (Ex: month id:7 From 01-09-2020 to 05-09-2020) will have very few days
