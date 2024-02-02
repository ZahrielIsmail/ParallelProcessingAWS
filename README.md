HTCondor Cluster built in AWS to do Sentiment Analysis on X (Formerly known as Twitter) data


## **1) Introduction**

 Analyzing Twitter data, with its real-time and dynamic nature, presents a unique set of challenges and opportunities. To efficiently process and extract sentiments from large volumes of tweets, parallel computing becomes essential. This is where High-Throughput Computing (HTC) clusters, such as HTCondor, come into play. HTCondor provides a robust framework for managing and executing parallel and distributed computing tasks across a cluster of machines. Leveraging HTCondor for sentiment analysis on Twitter data not only enhances the speed and efficiency of the analysis but also enables the handling of the massive scale of information generated on social media platforms. This guide explores the utilization of HTCondor clusters for parallel processing of sentiment analysis on Twitter data. By distributing the computational workload across multiple nodes in the cluster, we can significantly reduce the processing time, allowing for near real-time analysis of sentiments expressed in tweets. We will delve into the setup, configuration, and deployment of HTCondor, outlining steps to harness the power of parallel computing for sentiment analysis tasks. 

## **2) Objective**

1) Prepare an HTCondor Infastructure on the AWS instances (Including RDS Server and NFS protocol)
2) Ensure that HTCondor Submission Host is able to distribute the jobs between the Execution Hosts to allow for parallel processing
3) Create a scheduler for HTCondor Submission Host to consistently extract data at fixed intervals from the RDS Database
4) Test the cluster by preparing and utilizing three different Sentiment Analysis Models and verifying the end results via exporting the performance metrics into a file at the end of the process

## **3) Methodology**

![WQD7008](https://github.com/ZahrielIsmail/ParallelProcessingAWS/assets/155151831/19a37449-954e-4b07-9a51-57fe9949a38a)

Phase 1 Data Scrapping:

1) Scrapping the data from twitter Using tweepy, removal of unnecessary or redundant data as well as any preprocessing steps
2) Load the Data into the RDS Database which also contains the Python files necessary to conduct the modelling

Phase 2 Data Processing:

1) Submission Host extracts the Tweets.csv files from the RDS Database and submits the job via "Condor_submit" to distribute the data among three execution hosts as well as directing which model should be used for the processing
2) Execution Host receives the files and conducts the modelling process, after modelling is complete, certain matrices are noted and exported to the RDS Database
3) Matrices can be exported from the RDS Database for analysis outside of the AWS Ecosystem

## **4) Server Setup**

This project focuses on only Phase 2 of the methodology listed in the previous mentioned table. The components that require being setup on the AWS environment are 6 Instances of sizes stated Below.

- HTCondorManager
- SubmissionHost   // Requires setup of an NFS Kernel in this instance
- ExeuctionHost    //Requires At least two instances, used within this proejct is 3 Instances, all three instances require NFS Common and mounting folders from SubmissionHost instance
- RDS Server     

This section focuses on the infrastructure setup for the HTCondor cluster, the following table is the number of instances required for the function of this study:
Name	Role	Size	Required(?)
Central_Manager	HTCondor Central Manger	Micro	Yes
Submission_Host	HTCondor Submission Host	Nano	Yes
Execution_Host_1	HTCondor Execution Host	Small	Yes
Execution_Host_2	HTCondor Execution Host	Small	No
Execution_Host_3	HTCondor Execution Host	Small	No

 The following are the requirements for the systems to function. The declaration of roles within the HTCondor system must be done during the setup of the instances and will be covered in the following section.

**************
## 4.1 Central Manager
**************
 The central managers role in the cluster is to manage the system resources as well as assigning jobs according to free execution hosts, the overall memory needed in this role is low, which provides a reason for the small memory size allocated to the instance. After the Central Manager node is created, it can be accessed via the EC2 terminal to initiate the setup phase. The following code is required to install HTCondor and set the role as central manager:


**************

HTCondor

**************
sudo apt-get update

curl -fsSL https://get.htcondor.org | sudo /bin/bash -s -- --no-dry-run --password "abc123" --central-manager <Private IP Address>

sudo systemctl restart condor

NFS Setup

sudo apt install nfs-kernel-server

mkdir condor_shared

sudo vim /etc/exports # add /home/ubuntu/condor_shared *(rw,sync,no_subtree_check)

sudo exportfs -ra	
**************
Github Clone
**************
git clone <repository https>

git config credential.helper store

git pull
**************
Create commit.sh file
git add .

git commit -m “Committed from EC2” 

git push
 **************
## 4.2 Submission Host
**************
The submission host will create the job request to be submitted to the execution hosts. It requires the central mangers private IP to form the cluster and also requires a job.sub file to submit the jobs.
HTCondor
**************
sudo apt-get update

curl -fsSL https://get.htcondor.org | sudo /bin/bash -s -- --no-dry-run --password "abc123" --submit <Central Manager IP>

sudo systemctl restart condor

NFS Setup
sudo apt install nfs-common

mkdir mounter

sudo mount 172.31.54.189:/home/ubuntu/condor_shared /home/ubuntu/mounter

Create job.sub file
vim job.sub

**************
executable = $(filename)

output = output_$(Process).txt

error = error_$(Process).txt

log = log.txt
requirements = True
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = /home/ubuntu/mounter/local_dataset.xlsx

filename = script1.py

queue

filename = script2.py

queue

filename = script3.py

queue
****************
 
## 4.3 Execution Host

**************

The execution host are the workers of the cluster and will do the bulk of the processes. It requires the Central Managers IP to connect to the cluster.
HTCondor
**************
sudo apt-get update

curl -fsSL https://get.htcondor.org | sudo /bin/bash -s -- --no-dry-run --password "abc123" --execute <Central Manager IP>

sudo systemctl restart condor

NFS Setup
sudo apt install nfs-common

mkdir mounter

sudo mount 172.31.54.189:/home/ubuntu/condor_shared /home/ubuntu/mounter
**************

Python Setup
**************
Due to the scripts being built for Python3, some python packages are required to be installed on the execution hosts before being able to run.
sudo apt install python3-pip
**************

sudo pip3 install nltk
sudo pip3 install nltk
sudo pip3 install seaborn
sudo pip3 install wordcloud
sudo pip3 install sklearn
sudo pip3 install scikit-learn
sudo pip3 install xgboost
**************

sudo mount 172.31.54.189:/home/ubuntu/condor_shared /home/ubuntu/mounter
