# APEXPOSE LinkedIn Data Extractor

A comprehensive tool to extract job application data from LinkedIn, including resumes, application questions, LinkedIn scores, and job descriptions.

## Features

- ✅ **Job Description Extraction**: Saves job description to `JD.txt`
- ✅ **Resume Downloads**: Downloads all resumes as `firstname_lastname.pdf` to `FSD_resume/` folder
- ✅ **Application Data**: Extracts all application data including 5 questions and answers
- ✅ **LinkedIn Scores**: Captures LinkedIn-generated match scores
- ✅ **Profile Links**: Extracts LinkedIn profile URLs
- ✅ **CSV Export**: Saves all data to `application.csv` with structured format

## Files Created

1. **JD.txt** - Job description
2. **application.csv** - All applicant data with questions, scores, and profile links
3. **FSD_resume/** - Folder containing all downloaded resumes named as `firstname_lastname.pdf`

## CSV Structure

The `application.csv` file contains the following columns:

| Column | Description |
|--------|-------------|
| Index | Candidate number |
| Name | Full name |
| First_Name | First name |
| Last_Name | Last name |
| Headline | LinkedIn headline |
| Location | Location |
| LinkedIn_Score | LinkedIn match percentage |
| Profile_Link | LinkedIn profile URL |
| Resume_File | Resume filename |
| Question_1 to Question_5 | Application questions |
| Answer_1 to Answer_5 | Candidate answers |

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Set your LinkedIn credentials as environment variables:

```bash
export LINKEDIN_EMAIL="your_email@example.com"
export LINKEDIN_PASSWORD="your_password"
```

Or run with inline credentials:

```bash
LINKEDIN_EMAIL="your_email" LINKEDIN_PASSWORD="your_password" python run_extractor.py
```

### 3. Install Chrome Driver

Make sure you have Chrome browser installed and the ChromeDriver is in your PATH.

## Usage

### Quick Start

```bash
python run_extractor.py
```

### Advanced Usage

```bash
python apexpose_data_extractor.py
```

## Configuration

### Job ID

The script is configured for job ID `4254395344`. To change this, edit the `job_id` variable in the `ApexposeDataExtractor` class:

```python
self.job_id = "YOUR_JOB_ID"  # Replace with your job ID
```

### Download Folder

Resumes are saved to the `FSD_resume/` folder by default. You can change this in the constructor:

```python
self.download_folder = "YOUR_FOLDER_NAME"
```

## Output Files

### JD.txt
Contains the complete job description extracted from LinkedIn.

### application.csv
CSV file with all applicant data including:
- Basic information (name, headline, location)
- LinkedIn match scores
- Profile links
- Resume file names
- 5 application questions and answers

### FSD_resume/
Folder containing all downloaded resumes named as `firstname_lastname.pdf`.

## Error Handling

The script includes comprehensive error handling:
- Login failures
- Network issues
- Missing elements
- Download failures

All errors are logged to:
- `apexpose_extractor.log` - Main extraction log
- `extractor_run.log` - Runner script log

## Anti-Detection Features

The script includes several anti-detection measures:
- Random delays between actions
- Human-like typing behavior
- Random user agents
- Disabled automation indicators
- Enhanced Chrome options

## Troubleshooting

### Common Issues

1. **Login Failed**
   - Check your LinkedIn credentials
   - Ensure 2FA is disabled or use app passwords
   - Try logging in manually first

2. **No Candidates Found**
   - Verify the job ID is correct
   - Ensure you have access to the job posting
   - Check if the job has applicants

3. **Resume Download Failed**
   - Some resumes may not be downloadable
   - Check network connectivity
   - Verify file permissions

4. **Chrome Driver Issues**
   - Update Chrome browser
   - Download matching ChromeDriver version
   - Ensure ChromeDriver is in PATH

### Debug Mode

For debugging, you can modify the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Security Notes

- Never commit credentials to version control
- Use environment variables for sensitive data
- Consider using LinkedIn app passwords
- Regularly update dependencies

## Performance

- Processing time: ~2-3 seconds per candidate
- Total time for 52 candidates: ~3-4 minutes
- Memory usage: ~200-300MB
- Network usage: ~50-100MB per resume

## Limitations

- Requires LinkedIn account with job posting access
- Some resumes may not be downloadable
- LinkedIn may rate-limit excessive requests
- Job ID must be accessible to your account

## Support

For issues or questions:
1. Check the log files for detailed error messages
2. Verify your LinkedIn credentials and permissions
3. Ensure Chrome and ChromeDriver are up to date
4. Check network connectivity

## License

This tool is for educational and legitimate business use only. Please respect LinkedIn's terms of service and rate limits. 