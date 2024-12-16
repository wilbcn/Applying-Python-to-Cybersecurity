## Overview of Project  

This project showcases an AWS security Tool in Python, allowing the user to check for vulnerabilities in a variety of AWS services including IAM, EC2, and S3. This project was aimed at gaining hands on experiencing working with AWS APIs using boto3, and to improve my understanding of automation in the cloud with a focus on security. I also documented this for my own personal development and growth as I continue to research and experiment with Python, especially with object-oriented programming, and using a variety of modules and libraries like boto3 and pandas. This was also a great opportunity to familiarise myself with the vast amount of methods on offer with boto3. During this project, I reffered to the boto3 documentation from aws to discover and use the listed methods, checking the expected returned syntax to better understand how to access and work with this data. 

## Acknowledgments
Boto3 documentation - https://boto3.amazonaws.com/v1/documentation/api/1.35.8/index.html

### Key Features
### IAM Security
- Generate a IAM credentials report.
- Check for IAM users without MFA enabled.
- Check IAM users with for passwords older than 2 months.
- Check which IAM users have Admin privileges.
- Check when access keys were last used or rotated.

### S3 Compliance
- Check S3 buckets for public access.
- Check if S3 buckets have encryption enabled
- Check if S3 versioning is enabled

### EC2 Security
- Display important information about all EC2 security groups.
- Check for vulnerabilities within EC2 security groups.
- Check for EC2 instances that have public access.
- Check for EC2 instances without key pairs.

## Example screenshots & Using the programme

![Using the Main Menu](<img width="869" alt="image" src="https://github.com/user-attachments/assets/6c26488b-c56e-49f5-9ea7-9e2ac7a68ba1" />)

User-friendly interface with options to explore each aws service we have programmed for checks. All of the menus throughout the programme have exception checks to keep the user on track and avoiding software crashes.

### IAM Class
IAM Sub Menu
<img width="510" alt="image" src="https://github.com/user-attachments/assets/0d00c6ce-a7fd-4665-a8e5-9193b6d6e79d" />

In the IAM Sub Menu, the user is able to explore multiple security checks. Some of these checks require the user to generate a user credentials report. The most recent report date & time is handily returned to the user, should they want to generate a more recent report.

Example Outputs:
<img width="617" alt="image" src="https://github.com/user-attachments/assets/9fd275fd-4630-442d-9d9b-d4abb94b8660" />
<img width="561" alt="image" src="https://github.com/user-attachments/assets/665f0acc-e41e-4ab8-9e4e-a3bd59518c72" />
<img width="1097" alt="image" src="https://github.com/user-attachments/assets/e8e2c741-0482-4148-aea3-50db25190a61" />

Here you can see that some of my test IAM user accounts have been flagged or old passwords, access keys, and a lack of MFA. Then we prompt the user to investigate!

### S3 Class
<img width="523" alt="image" src="https://github.com/user-attachments/assets/aa4a400c-5175-4421-b8d2-976bc5705254" />

In the S3 Sub Menu, the user can check for security concerns with their S3 buckets. This includes public access vulnerabilities, lack of encryption, and bucket versioning.

Example Outputs:
<img width="578" alt="image" src="https://github.com/user-attachments/assets/2fc9213a-0dca-439a-96f3-e380484e2dc6" />

The test-case S3 bucket I made has been flagged for public access concerns due to some ACL rules.

<img width="866" alt="image" src="https://github.com/user-attachments/assets/30631a5e-ae40-42e4-992e-8a1ec46e6371" />

Multiple S3 buckets were flagged without bucket versioning config. This is something I will look into and explore.

### EC2 Class


## Key takeaways and future development












