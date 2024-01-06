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

The project has set up various AWS instances for an HTCondor cluster, such as HTCondorManager, SubmissionHost, ExecutionHosts, and an RDS Server. It walks through the installation, configuration, and networking processes. It includes instructions for submitting the jobs, python files. This information serves as a practical roadmap for configuring and managing an HTCondor cluster in a cloud-based environment, with an emphasis on cluster architecture implementation.

**Configuration of the Central Manager**
The Central Manager in our HTCondor cluster was set up in a series of steps that began with HTCondor installation. This was accomplished by first updating the system packages before installing the HTCondor package with the **sudo apt-get** command, then install the condor with  **install htcondor -y** command. Following installation, the HTCondor was configured to define its role within the cluster, including assigning it the roles of Master, Collector, and Negotiator. The necessary configuration lines were added to the condor_config.local file. 
Furthermore, the 'CONDOR_HOST' was set to the Central Manager's hostname to ensure proper identification within the cluster network. Besides, steps were taken to create and configure a shared NFS directory, which is necessary for data sharing and efficient cluster operation. This configuration enables seamless communication and file sharing between the HTCondor cluster's various components. Finally, the HTCondor service was restarted to ensure that the Central Manager was properly configured and operational.

The Central Manager includes steps for creating and configuring a shared directory in the HTCondor cluster setup. This procedure begins with the command **'sudo mkdir -p /home/condor_shared**'. Following that, command **'sudo exportfs -ra'** to apply the changes,**'sudo exportfs -v'** to verify the export's success, and **'sudo systemctl enable --now nfs-server'** to ensure the NFS server is operational. These steps are critical for creating a shared environment for efficient data access and management throughout the cluster.

**Configuration of Submission Host**
HTCondor cluster setup on AWS includes a series of steps that begin with HTCondor installation. This entails first updating the system's packages and then installing HTCondor. Following installation, the HTCondor configuration is customized, specifically by adding MASTER and SCHEDD to the 'DAEMON_LIST' and identifying the central manager via the 'CONDOR_HOST' setting. The HTCondor service is restarted to ensure that these changes take effect. Establishing a shared NFS directory is also an important part of the setup. Installing NFS common tools, creating a designated mount point on the system, and then mounting the shared directory from the Central Manager to this point accomplishes this. These steps are critical for setting up the cluster for efficient task scheduling and resource sharing.

**Configuration of the Execution Host**
The process of configuring the HTCondor cluster's Execution Hosts begins with updating the system and installing HTCondor. Following that, HTCondor is configured specifically for the execution host, including MASTER and STARTD in the 'DAEMON_LIST' and defining the 'CONDOR_HOST' with the hostname of the central manager. Mounting the NFS shared directory, which involves creating a local mount point and then linking it to the shared directory on the Central Manager, is a critical step in this setup. Finally, the HTCondor service on the Execution Host is restarted to apply these settings and ensure proper functionality.

Once all instances are ready, 'condor_status' command should be used to validate the status and ensure that everything is working properly.

**Submitting Jobs**
Following that, a job submission file job.submit is ready, with the executable script, output, error, and log files, as well as a queue command. Finally, the job is sent to the cluster to be processed. This step demonstrates the HTCondor setup's functionality and ability to manage and execute distributed computing tasks.

## **5) Results and Discussions**
