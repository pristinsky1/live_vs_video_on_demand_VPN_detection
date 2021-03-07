# Live_vs_Vod_Project
## Group Name: Live

Due to the variety, affordability and convenience of online video streaming, there are more subscribers than ever to video streaming platforms. Moreover, the decreased operation of non-essential businesses and increase in the number of people working from home in this past year has further compounded this effect. More people are streaming live lectures, sports, news, and video calls via the internet at home today than we have ever seen before. Internet Service Providers, such as Viasat, are tasked with optimizing  internet connections and tailoring their allocation of resources to fit each unique customer’s needs. With this increase in internet activity, it would be especially beneficial for Viasat to understand what issues arise when customers stream various forms of video. In general, different internet activities require different resources to optimize the connection. For example, if a customer watches a lot of live video they may prefer a connection with lower latency and higher bandwidth. Although we are able to identify the genre of an activity when a user is not using a VPN, the challenge arises when a user chooses to surf the web through a VPN. When it comes to VPN use cases we can’t identify a user’s unique activity when they experience issues, thus making us unable to successfully troubleshoot  those problems. This is where a tool that could identify various internet activities, specifically live or uploaded video streaming, within a VPN tunnel would be extremely useful for an Internet Service Provider. 

## Project Report: 
Found within the **references** folder. The file name is DSC180B_Report.

## Guide for Launching this Project:
Note: These instructions assume that the user has access to the DSMLP server to be able to run this project. Open terminal, run these commands in the associated order:

1.) **ssh user@dsmlp-login.ucsd.edu** (user refers to your school username). Enter credentials.

2.) **launch-180.sh -G B05_VPN_XRAY -P Always -i apristin99/live_vs_vod_project**

3.) **git clone https://github.com/pristinsky1/live_vs_video_on_demand_VPN_detection.git**

4.) **cd live_vs_video_on_demand_VPN_detection**

Now you are within the right directory with the environment already set up! Start running the files!

5.) For files needed to be predict, you have to put them in the "data/in" directory. Acceptable files are files generated network-stats tool provided by Viasat.

6.) If you wish to train a new classifier based on new data or new type of model and parameters, you have to change the location of training data and other settings in the "config/train-parmas.json". Otherwise, you can directly run **python run.py predict** using the trained model contained in the project.


## Guide for Pipeline Testing:
Run **python run.py test** and the results will be in **test/out**. Within that folder, it contains the output dataframes, model, and reports of accuracies for the test data.


## Contents:
There are three parts of contents:
1. src folder - Contains all library code.
2. config folder - Contains directory of each target.
3. run.py - Main Program for this project.
4. notebooks folder - stores notebooks for this project.
5. data/out folder - stores results of this project.

The two files to look at for results under data/out:

training_report.json: Json file contains the report of model's basic information and its performance on validation set.
predictions.csv: DataFrame contains basic information of one record generated by network-stats and its prediction result.



## How to run it?
Warning: The feature, train and predict has to be run in fixed order. If you want to run everything at once, you can use the all script.

Use console to run **python run.py eda** as a script. This will run the eda notebook and store the html version for easy accessibility under "/notebooks". 

Use console to run **python run.py feature** as a script. This will create the features. The output dataframe will be stored in "data/out" directory in csv format.

Use console to run **python run.py train** as a script. This will train the model. The output model and report will be stored in "data/out" directory in csv format.

Use console to run **python run.py predict** as a script. This will classify the input dataset as live or streaming. The output dataframe will be stored in "data/out" directory in csv format.

Use console to run **python run.py all** as a script. This will run everything listed above. The output dataframes and model and report will be stored in "data/out" directory in csv format.


## Description of Each Params Files
"feature-params.json" -- "indir: the input directory of training set, outdir: the output directory of generated dataframe, output: 1 means output dataframe containing features information, 0 means only return it as a dataframe(Must be 1 in feature-params.json)"

"train-params.json" -- 
    :param: indir: file directory where extracted features stored.
    :param: outdir: file directory where output of this funcition stored.
    :param: testsize: the portion of train dataset used for validation.
    :param: randomstate: the randomstate number to random split train and valid set.
    :param: method: the classifier name used for training.
    :param: method_parameters: the parameter used for training.

"predict-params.json" -- "indir: the input directory of stored model, indir2: the input directory of testset, outdir: the output directory of test result."



```
### Responsibilities

* Da Gong developed the structure of this project.
* Zishun Jin worked on the prediction model and the model features of this project.
* Tianran Qiu worked on the prediction model and the model features of this project.
* Andrey developed the environment and the model feature creation for this project.
* Mariam worked on the final report and model feature creation for this project. 
```




### Website

Link to the webpage: https://pristinsky1.github.io/live_vs_video_on_demand_VPN_detection/
