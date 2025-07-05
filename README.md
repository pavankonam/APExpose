# LinkedIn Experience Extractor

This tool extracts experience and birth year information from LinkedIn profiles using the LinkedIn API.

## Prerequisites

- Python 3.7 or higher
- LinkedIn account credentials

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your LinkedIn credentials:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## Usage

1. Run the script:
```bash
python linkedin_experience_extractor.py
```

2. When prompted, enter the LinkedIn profile URL you want to extract data from.

3. The script will create a JSON file with the extracted data in the following format:
```json
{
    "full_name": "John Doe",
    "birth_year": {
        "value": 1990,
        "is_visible": true,
        "connection_status": "1",
        "possible_reasons": []
    },
    "profile_creation_date": "2020-01-15",
    "profile_url": "https://www.linkedin.com/in/johndoe",
    "connection_info": {
        "degree": "1",
        "mutual_connections_count": 42,
        "mutual_connections": ["Alice Smith", "Bob Johnson", "Carol White"],
        "is_connected": true,
        "network_info": {
            "first_degree": 500,
            "second_degree": 10000,
            "third_degree": 50000
        }
    },
    "experience": [
        {
            "title": "Software Engineer",
            "company": "Example Corp",
            "location": "San Francisco, CA",
            "start_date": {
                "raw": {"year": 2020, "month": 1},
                "formatted": "January 2020"
            },
            "end_date": {
                "raw": null,
                "formatted": "Present"
            },
            "description": "Job description..."
        }
    ]
}
```

## Notes

- The tool requires a LinkedIn account with access to the profiles you want to extract data from
- Birth year information visibility depends on:
  - User's privacy settings
  - Your connection status with the user
  - Whether the user has made their birth year public
- Connection status information includes:
  - Connection degree (1st, 2nd, or 3rd-degree connection)
  - Network size (number of connections at each degree)
  - Number of mutual connections
  - List of top mutual connections
  - Whether you are directly connected
- Profile creation date is extracted from the profile's metadata
- Dates are provided in both raw and formatted versions for flexibility
- Make sure to comply with LinkedIn's terms of service and usage guidelines
- The tool uses the unofficial LinkedIn API, so it might need updates if LinkedIn changes their website structure 

## Edit 1 
Trying to extract the information for linkedin pages using OAuth Linkedin API
- Failed to extract dates and DOB

## Edit 2
Extracting data from the fake job post 
We are extracting - Resume, Application details and linkedIN profiles

