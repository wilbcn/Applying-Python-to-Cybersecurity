# Overview of Project

I am currently undertaking a certificate programme called BlueTeam Level 1, which covers a massive amount of domains within Cybersecurity such as phishing analysis, threat intelligence, SIEM monitoring, and more. Within the phishing analysis segment, I learned how to investigate suspicious emails, particularly with tools such as VirusTotal. I am always looking for new ideas and projects to help develop myself as a programmer, whilst also implementing what I have learned through my MSc, and various certificate programmes.

This programme allows the user to make various API calls to VirusTotal, in order to get a Filereport on a Hash (MD5, SHA-1, or SHA-256), or a URL. This programme introduced me to modules like hashlib, and dotenv, which I used to generate hash files and also securely load in my VT API Key.

## Acknowledgements

VT documentation on URL File reports - https://docs.virustotal.com/reference/analysis
VT documentation on Hash File reports - https://docs.virustotal.com/reference/file-info
VT documentation, working with objects - https://docs.virustotal.com/reference/objects
Python docs - Using OS Module - https://docs.python.org/3/library/os.html

## Project Structure
/VT-ThreatScan/
Contains the README.md file for the Project Documentation and Overview.

/VT-ThreatScan/src
This folder contains the code for running the programme.

## Key Features
- Insert a hash file manually and generate a file report.
- Generate a hash file from a local file, and generate a file report.
- Insert a URL manually, and generate a file report.
- Log searches in a neatly formatted CSV file, creating an audit trail and permanent log.
- The log information then provides the user with the necessary information that may warrant a deeper investigation.

## Example screenshots and outputs
## Main Menu

<img width="1065" alt="image" src="https://github.com/user-attachments/assets/25534d1d-0b2d-491b-9d7e-5dd0d7186126" />

- Users are provided a clean user menu, which they can interact with via the CLI.

<img width="472" alt="image" src="https://github.com/user-attachments/assets/e7c5fa6b-2ca0-44ff-96d6-cbf37d40ebbf" />

- Typing 1 takes you to the Hash Sub-Menu, where we can investigate hashes either by manual upload via the CLI or by checking a local file.

## Manual hash check

<img width="501" alt="image" src="https://github.com/user-attachments/assets/861451b2-88a6-4bd2-a5cf-4f5ab4bfa8aa" />

- First, the user must specify which hash type they would like to check. This helps validate the inserted hash as we compare the user input to the expected hash length for each type.

<img width="520" alt="image" src="https://github.com/user-attachments/assets/89b6e58b-2d66-490a-bee7-f69759d03d77" />

- After specifying MD5, I then pasted a known testing md5 hash to generate a file report. You can see the output in the console, as well as the option to peform another search.

<img width="1639" alt="image" src="https://github.com/user-attachments/assets/6251af22-60b7-4f75-9166-d708ca10a44b" />

- This search was then added to our saved searches log. With this information, an analyst may be prompted to investigate the hash further.

## Checking a local file








