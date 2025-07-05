# LinkedIn Resume Downloader for APEXPOSE

This script automates the process of downloading resumes from job applicants on your LinkedIn APEXPOSE page. It navigates through your LinkedIn job postings and downloads applicant resumes to a local folder.

## Features

- 🔐 Secure LinkedIn authentication
- 🚀 Automated navigation through APEXPOSE admin pages
- 📥 Automatic resume downloads from job applicants
- 📁 Organized file storage in `FSD_resume` folder
- 📝 Comprehensive logging for debugging
- 🔄 Retry mechanisms and error handling
- 🛡️ Anti-detection measures for LinkedIn

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (will be installed automatically)
- LinkedIn account with access to APEXPOSE admin

## Installation

1. **Clone or download the files to your local machine**

2. **Install dependencies:**
   ```bash
   python setup.py
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your credentials:**
   - Edit the `.env` file created by setup.py
   - Add your LinkedIn email and password:
   ```
   LINKEDIN_EMAIL=your_linkedin_email@example.com
   LINKEDIN_PASSWORD=your_linkedin_password
   ```

## Usage

1. **Run the script:**
   ```bash
   python linkedin_resume_downloader.py
   ```

2. **The script will:**
   - Log in to your LinkedIn account
   - Navigate to APEXPOSE admin page
   - Go to posted jobs
   - Access the specific job posting
   - Find and click "View Applicants"
   - Download resumes for each applicant
   - Save files in `FSD_resume` folder with applicant names

## File Structure

```
Edit2/
├── linkedin_resume_downloader.py    # Main script
├── setup.py                         # Setup script
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── .env                            # Your credentials (create this)
├── FSD_resume/                     # Downloaded resumes folder
└── linkedin_downloader.log         # Log file
```

## How It Works

1. **Authentication:** Logs into LinkedIn using your credentials
2. **Navigation:** Follows the exact path you specified:
   - APEXPOSE admin page
   - Posted jobs page
   - Specific job detail page
3. **Applicant Discovery:** Finds and clicks "View Applicants" button
4. **Resume Download:** For each applicant:
   - Clicks on their profile
   - Looks for download buttons
   - Downloads resume to `FSD_resume` folder
   - Renames file to applicant name

## Troubleshooting

### Common Issues

1. **"Chrome driver not found"**
   - Install Chrome browser
   - Run `python setup.py` to check driver

2. **"Login failed"**
   - Check your credentials in `.env` file
   - Ensure 2FA is disabled or use app password

3. **"No applicants found"**
   - LinkedIn may have changed the page structure
   - Check the log file for detailed error messages
   - The script includes multiple fallback selectors

4. **"Download button not found"**
   - Some applicants may not have uploaded resumes
   - Check the log for specific applicant details

### Logging

The script creates detailed logs in `linkedin_downloader.log`. Check this file for:
- Navigation progress
- Applicant discovery
- Download success/failure
- Error details

### Manual Steps (if automation fails)

If the script encounters issues, you can manually:

1. Log into LinkedIn
2. Navigate to: `https://www.linkedin.com/company/107037579/admin/`
3. Go to "Posted Jobs" → "Paused"
4. Click on your job posting
5. Click "View Applicants"
6. Manually download resumes

## Security Notes

- Your credentials are stored locally in `.env` file
- Never commit `.env` file to version control
- The script uses secure browser automation
- No data is sent to external servers

## LinkedIn Limitations

- LinkedIn may detect automation and block access
- The script includes anti-detection measures
- If blocked, wait 24 hours before retrying
- Consider using LinkedIn Recruiter for bulk operations

## Customization

You can modify the script to:
- Change download folder name
- Add more applicant data extraction
- Modify file naming conventions
- Add email notifications
- Integrate with other systems

## Support

If you encounter issues:
1. Check the log file for detailed error messages
2. Ensure all prerequisites are installed
3. Verify your LinkedIn credentials
4. Check if LinkedIn has changed their interface

## Legal Compliance

- This tool is for personal use with your own LinkedIn account
- Respect LinkedIn's Terms of Service
- Do not use for commercial purposes without proper licensing
- Ensure compliance with data protection regulations

---

**Note:** This tool is designed to work with your own LinkedIn APEXPOSE page and job postings. Use responsibly and in accordance with LinkedIn's terms of service. 