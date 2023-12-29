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

## **5) Results and Discussions**
