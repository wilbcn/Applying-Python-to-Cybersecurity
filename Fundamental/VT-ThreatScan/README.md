# Overview of Project

VT-ThreatScan is a Python tool that enables users to analyze file hashes (MD5, SHA-1, SHA-256) and URLs using the VirusTotal API. The tool allows for manual hash input, file-based hash scanning, and URL analysis, while maintaining a permanent log for audit purposes.

I developed VT-ThreatScan while studying phishing analysis and threat intelligence as part of my BlueTeam Level 1 certification, aiming to apply my knowledge of cybersecurity investigations while also improving my Python skills.

This project allows me to reinforce what I have learned through my MSc studies, certifications, and personal development by integrating real-world cybersecurity analysis techniques into code.

## Acknowledgements

- VT documentation on URL File reports - https://docs.virustotal.com/reference/analysis
- VT documentation on Hash File reports - https://docs.virustotal.com/reference/file-info
- VT documentation, working with objects - https://docs.virustotal.com/reference/objects
- Python docs - Using OS Module - https://docs.python.org/3/library/os.html

## Project Structure
- 📂 VT-ThreatScan/ (Root Project Directory)
- 📄 README.md – Project documentation & usage guide
- 📂 src/ (Source Code Directory)
- 📄 main.py – Entry point of the program
- 📄 hash_check.py – Hash scanning logic
- 📄 url_check.py – URL analysis logic
- 📄 utils.py – Utility functions & CSV logging
- 📄 .env – Environment file for storing API key (not included for security reasons)
- 📄 requirements.txt – Dependencies for running the project

## Key Features
- 🔍 Manual Hash Lookup – Enter an MD5, SHA-1, or SHA-256 hash and fetch a VirusTotal report.
- 🖥️ File-Based Hash Analysis – Generate a hash from a local file and analyze it.
- 🌐 URL Investigation – Submit a URL and retrieve its VirusTotal scan results.
- 📊 Audit Logging – Automatically log all searches in a CSV file for investigation tracking.
- 📌 Customizable API Handling – Uses .env file to store API keys securely.

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

<img width="408" alt="image" src="https://github.com/user-attachments/assets/be11efde-10d9-435f-9cd8-c8b82229d151" />

- Typing 2 now in the Hash Sub Menu, we can check a local file, generate a hash for it, and get a file report on that hash. For testing purposes we will be looking up known test file 'eicar.com.txt'

<img width="663" alt="image" src="https://github.com/user-attachments/assets/e096d0e4-20b8-4fb9-87fb-d0001b69211b" />

- Results show that this is only a test file, however we still have plenty of useful information. This is also logged to our CSV file.

## Checking a URL

<img width="681" alt="image" src="https://github.com/user-attachments/assets/dd7d8f06-e353-46a1-892d-756937a38407" />

- Once again, we are testing our programme using the known testing souce 'Eicar'. I have inserted this test URL via the CLI, and generated a file report on it.

<img width="1621" alt="image" src="https://github.com/user-attachments/assets/d0354105-6290-414e-b6bf-0992e044bca1" />

- We can now see that all 3 entries from our programme showcase have been added to the log. Our URL scan identifies and counts the engines which flagged the URL as harmless, malicious, and so fourth.

## Key takeaways and future development
- Automated Alerts: Notify users if a malicious hash or URL is found.
- Integration with More Threat Intelligence APIs: Extend beyond VirusTotal to sources like AbuseIPDB or AlienVault OTX.
- Enhanced User Interface: Add a simple GUI instead of CLI-only interaction.

As I continue my BlueTeam Level 1 certification, I hope to expand on these ideas and further improve the project.





