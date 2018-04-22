# LedgerAsAnAuditingSolutionForMongoDB
This python script captures mongodb related statistics on type of queries that are being run for example and more. This was a group project for cloud computing course and I worked on python script and some research to add to the final report.

Language Used : - Python 3.6
MongoDB was installed on AWS EC2 ubuntu 16.0 instance
In order to stress test MongoDB instance, I used POCdriver.jar - java 7 (https://github.com/johnlpage/POCDriver)

Process : 
1. Ensure MongoDB service is up and running on AWS instance
2. Ensure you move POCdriver.jar from the github link to AWS instance and begin execution of stress test. There are various parameters that could be provided to execute this jar file, however, the following is what I used for example: 
java -jar POCDriver.jar -k 20 -i 20 -u 20 -d 600 -t 2 -e -y 10
The above command will insert, update and query the mongoDB instance by using 2 threads and creating 10 collections. 
3. Run the following command from command prompt on your local machine:
python populateLedger.py
4. In order to visualize data collected, install  Mongo compass and provide IP address on which mongoDB instance is running.
5. In the Mongo compass  click on  Schema  button to visualize ledger data 

Libraries/ Tools  used : -  
For load test  : POcdriver.jar (https://github.com/johnlpage/POCDriver)
Visualize data : Mongo compass 
Python Libraries : pymongo, schedule, time, datetime, trackback

