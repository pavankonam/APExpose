# APEXPOSE Candidate Extractor

This tool extracts candidate data from APEXPOSE job postings, including resumes, LinkedIn profiles, and application questions.

## Features

- Downloads all candidate resumes and saves them as `firstname_lastname.pdf`
- Extracts LinkedIn profile data and scores
- Saves application questions and responses
- Creates a comprehensive CSV file with all candidate data
- Downloads and saves the job description

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your LinkedIn credentials:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## Usage

1. Run the script:
```bash
python apexpose_candidate_extractor.py
```

2. Enter your APEXPOSE job ID when prompted.

3. The script will create:
   - `JD.txt` - Job description
   - `application.csv` - All candidate data
   - `FSD_resume/` folder - All downloaded resumes

## Output Files

### JD.txt
Contains the complete job description.

### application.csv
CSV file with the following columns:
- First_Name
- Last_Name
- Email
- LinkedIn_Profile
- LinkedIn_Score
- Question_1 through Question_5
- Resume_Filename
- Profile_Data (JSON string with LinkedIn profile details)

### FSD_resume/
Folder containing all downloaded resumes named as `firstname_lastname.pdf`

## Notes

- Make sure you have proper access to the APEXPOSE API
- LinkedIn API credentials are required for profile extraction
- The script will create necessary directories automatically
- All files are saved with UTF-8 encoding for proper character handling

## API Endpoints

The script uses these APEXPOSE API endpoints:
- `GET /jobs/{job_id}` - Get job description
- `GET /jobs/{job_id}/candidates` - Get all candidates data

Make sure these endpoints are accessible with your API credentials.

## Edit 1 
Trying to extract the information for linkedin pages using OAuth Linkedin API
- Failed to extract dates and DOB

## Edit 2
Extracting data from the fake job post 
We are extracting - Resume, Application details and linkedIN profiles

