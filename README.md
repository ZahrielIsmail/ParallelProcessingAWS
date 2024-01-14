HTCondor Cluster built in AWS to do Sentiment Analysis on X (Formerly known as Twitter) data


## **1) Introduction**

 Analyzing Twitter data, with its real-time and dynamic nature, presents a unique set of challenges and opportunities. To efficiently process and extract sentiments from large volumes of tweets, parallel computing becomes essential. This is where High-Throughput Computing (HTC) clusters, such as HTCondor, come into play. HTCondor provides a robust framework for managing and executing parallel and distributed computing tasks across a cluster of machines. Leveraging HTCondor for sentiment analysis on Twitter data not only enhances the speed and efficiency of the analysis but also enables the handling of the massive scale of information generated on social media platforms. This guide explores the utilization of HTCondor clusters for parallel processing of sentiment analysis on Twitter data. By distributing the computational workload across multiple nodes in the cluster, we can significantly reduce the processing time, allowing for near real-time analysis of sentiments expressed in tweets. We will delve into the setup, configuration, and deployment of HTCondor, outlining steps to harness the power of parallel computing for sentiment analysis tasks. 

## **2) Objective**

1) Prepare an HTCondor Infastructure on the AWS instances (Including RDS Server and NFS protocol)
2) Ensure that HTCondor Submission Host is able to distribute the jobs between the Execution Hosts to allow for parallel processing
3) Create a scheduler for HTCondor Submission Host to consistently extract data at fixed intervals from the RDS Database
4) Test the cluster by preparing and utilizing three different Sentiment Analysis Models and verifying the end results via exporting the performance metrics into a file at the end of the process

## **3) Methodology**

![WQD7008](https://github.com/ZahrielIsmail/ParallelProcessingAWS/blob/main/WQD7008.jpg)

Phase 1 Data Scrapping:

1) Scrapping the data from twitter Using tweepy, removal of unnecessary or redundant data as well as any preprocessing steps
2) Load the Data into the RDS Database which also contains the Python files necessary to conduct the modelling

Phase 2 Data Processing:

1) Submission Host extracts the Tweets.csv files from the RDS Database and submits the job via "Condor_submit" to distribute the data among three execution hosts as well as directing which model should be used for the processing
2) Execution Host receives the files and conducts the modelling process, after modelling is complete, certain matrices are noted and exported to the RDS Database
3) Matrices can be exported from the RDS Database for analysis outside of the AWS Ecosystem

## **4.1) Server Setup**

This project has set up various AWS instances for an HTCondor cluster, such as HTCondorManager, SubmissionHost, ExecutionHosts, and an RDS Server. Steps below walks through the installation, configuration, and networking processes. It includes instructions for submitting the jobs, python files. These information serves as a practical roadmap for configuring and managing an HTCondor cluster in a cloud-based environment, with an emphasis on cluster architecture implementation.

**Configuration of the Central Manager**

The Central Manager in the HTCondor cluster is set up in a series of steps that began with HTCondor installation. This is accomplished by first updating the system packages before installing the HTCondor package.
```
sudo apt-get update
```
Then, to proceed with the HTCondor installation 
```
sudo apt-get install condor -y
```
Following installation, the HTCondor is configured to define its role within the cluster, including assigning it the roles of Master, Collector, and Negotiator. 
```
echo "DAEMON_LIST = MASTER, COLLECTOR, NEGOTIATOR" | sudo tee -a /etc/condor/condor_config.local
echo "CONDOR_HOST = <central_manager_hostname>" | sudo tee -a /etc/condor/condor_config.local
```
After that, restart the HTCondor to apply the changes.
```
sudo systemctl restart condor
```
Furthermore, the NFS is set in HTCondor for shared file access across different nodes in the distributed computing environment.
The NFS configuration on the Central Manager is stated below: 

Step 1: Create a Shared Directory on the Central Manager

This step is necessary for data sharing and efficient cluster operation.
```
sudo mkdir -p /home/condor_shared
```
Step 2: Apply the changes by running
```
sudo exportfs -ra
```
Step 3: Verify that the export was successful by running
```
sudo exportfs -v
```
Steo 4: Ensure that the NFS server is running
```
sudo systemctl enable --now nfs-server
```
These configuration enables seamless communication and file sharing between the HTCondor cluster's various components. Finally, the HTCondor service is needed to get restarted again to ensure that the Central Manager is properly configured and operational.
```
sudo systemctl restart condor
```

**Configuration of Submission Host**

HTCondor cluster setup on AWS for the Submission Host includes a series of steps that begin with HTCondor installation. Submission Host is responsible in submmiting the jobs. This entails first updating the system's packages and then installing HTCondor. 
```
sudo apt-get update
sudo apt-get install htcondor -y
```
Following that, the HTCondor configuration is applied, specifically by adding MASTER and SCHEDD to the 'DAEMON_LIST' and identifying the central manager via the 'CONDOR_HOST' setting. 
```
echo "DAEMON_LIST = MASTER, SCHEDD" | sudo tee -a /etc/condor/condor_config.local
echo "CONDOR_HOST = <central_manager_hostname>" | sudo tee -a /etc/condor/condor_config.local
```
The HTCondor service is restarted to ensure that these changes take effect. 
```
sudo systemctl restart condor
```
Establishing a shared NFS directory is also an important part of the setup. Installing NFS common tools, creating a designated mount point on the system.
```
# Mount the NFS shared directory
sudo apt-get update
sudo apt-get install nfs-common
sudo mkdir -p /local/mount/point
```
Then, mount the shared directory from the Central Manager to this point accomplishes the steps.
```
sudo mount 172.31.54.189:/home/condor_shared /local/mount/point
```
Lastly, to restart the condor to ensure all changes are applied accordingly.
```
sudo systemctl restart condor
```
These steps are critical for setting up the cluster for efficient task scheduling and resource sharing.

**Configuration of the Execution Host**

The process of configuring the HTCondor cluster's Execution Hosts begins with updating the system and installing HTCondor. 
```
sudo apt-get update
sudo apt-get install htcondor -y
```
Following that, HTCondor is configured specifically for the execution host, including MASTER and STARTD in the 'DAEMON_LIST' and defining the 'CONDOR_HOST' with the hostname of the central manager. 
```
echo "DAEMON_LIST = MASTER, STARTD" | sudo tee -a /etc/condor/condor_config.local
echo "CONDOR_HOST = <central_manager_hostname>" | sudo tee -a /etc/condor/condor_config.local
```
Mounting the NFS shared directory, which involves creating a local mount point and then linking it to the shared directory on the Central Manager, is an important step in this setup. 
```
# Mount the NFS shared directory
sudo mkdir -p /local/mount/point
sudo mount 172.31.54.189:/home/condor_shared /local/mount/point
```
Finally, the HTCondor service on the Execution Host is restarted to apply these settings and ensure proper functionality.
```
sudo systemctl restart condor
```
Once all instances are ready, 'condor_status' command should be used to validate the status and ensure that everything is working properly.
```
condor status 
```

**Submitting Jobs**

Following that, a job submission file job.submit is ready, with the executable script, output, error, and log files, as well as a queue command. Finally, the job is sent to the cluster to be processed. This step demonstrates the HTCondor setup's functionality and ability to manage and execute distributed computing tasks.

In detail, to submit three Python files concurrently in AWS using HTCondor, typically by using a HTCondor submit file with the queue directive. 
```
executable = $(filename)
output = output_$(Process).txt
error = error_$(Process).txt
log = log.txt

filename = script1.py
queue

filename = script2.py
queue

filename = script3.py
queue
```
Submit the jobs using HTCondor
```
condor_submit submit_jobs.condor
```

## **4.2) Setup Github Connection

To create a connection to Github to act as an external repository to the cluster, the user is required to create a user access token from their github account with the following permissions:
- repo
- write:packages
- project

Once the token has been generated, retrieve the clone HTTPS link for the github repository which can be acquired within the repository. After the token is generated and the HTTPS is acquired, utilize the EC2 Terminal for the Submission Host and use the following code:

```
git clone <repository https>
```

Once the code is run, the terminal will request the Username and Password associated with the repository, the username can be found in the first section of the HTTPS, example:https://github.com/JohnDoe/Parallel.git, the username should be JohnDoe, for the password request, utilize the User Access Token as the password functionality has been deprecated. To store the credentials for future push/pull requests use the following code:

```
git config credential.helper store
git pull 
```

 To export data back into the repository use the following code:
```
git add .
git commit -m "Committed from EC2" ##This is the comment for the commit
git push 
```

## **5) Results and Discussions**
