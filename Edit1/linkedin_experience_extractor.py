import os
import json
from datetime import datetime
from linkedin_api import Linkedin
from dotenv import load_dotenv
import time
import random

class LinkedInExperienceExtractor:
    def __init__(self):
        load_dotenv()
        try:
            # Initialize the LinkedIn API client with your app credentials
            self.api = Linkedin(
                os.getenv('LINKEDIN_EMAIL'),
                os.getenv('LINKEDIN_PASSWORD')
            )
            print("Successfully initialized LinkedIn API connection")
        except Exception as e:
            print(f"Error initializing LinkedIn API: {str(e)}")
            raise

    def format_date(self, date_dict):
        """Format date dictionary into a readable string"""
        if not date_dict:
            return "Present"
        
        year = date_dict.get('year', '')
        month = date_dict.get('month', '')
        
        if not year:
            return "Present"
            
        if month:
            try:
                month_name = datetime(2000, month, 1).strftime('%B')
                return f"{month_name} {year}"
            except:
                return str(year)
        return str(year)

    def check_profile_visibility(self, profile_data):
        """Check what information is publicly available on the profile"""
        visibility_info = {
            'is_public': False,
            'available_sections': [],
            'restricted_sections': [],
            'privacy_level': 'unknown'
        }
        
        # Check basic profile sections
        sections = {
            'experience': profile_data.get('experience', []),
            'education': profile_data.get('education', []),
            'skills': profile_data.get('skills', []),
            'birth_date': profile_data.get('birthDate', {}),
            'headline': profile_data.get('headline', ''),
            'summary': profile_data.get('summary', ''),
            'location': profile_data.get('locationName', ''),
            'industry': profile_data.get('industryName', '')
        }
        
        # Check which sections are available
        for section, data in sections.items():
            if data and (isinstance(data, list) and len(data) > 0 or isinstance(data, dict) and data or isinstance(data, str) and data.strip()):
                visibility_info['available_sections'].append(section)
            else:
                visibility_info['restricted_sections'].append(section)
        
        # Determine privacy level
        if len(visibility_info['available_sections']) > 5:
            visibility_info['privacy_level'] = 'public'
            visibility_info['is_public'] = True
        elif len(visibility_info['available_sections']) > 2:
            visibility_info['privacy_level'] = 'semi-public'
        else:
            visibility_info['privacy_level'] = 'private'
        
        return visibility_info

    def get_connection_status(self, profile_id, max_retries=3):
        """Get detailed connection status information with retry mechanism"""
        for attempt in range(max_retries):
            try:
                # Add random delay between retries
                if attempt > 0:
                    delay = random.uniform(2, 5)
                    print(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)

                # Get profile network info
                network_info = self.api.get_profile_network_info(profile_id)
                
                # Get mutual connections
                mutual_connections = []
                try:
                    mutual_data = self.api.get_profile_mutual_connections(profile_id)
                    if mutual_data and 'elements' in mutual_data:
                        mutual_connections = [conn.get('name', '') for conn in mutual_data['elements']]
                except Exception as e:
                    print(f"Warning: Could not get mutual connections: {str(e)}")

                # Determine connection degree based on network info
                degree = 'unknown'
                is_connected = False
                
                if network_info:
                    if network_info.get('firstDegreeSize', 0) > 0:
                        degree = '1'
                        is_connected = True
                    elif network_info.get('secondDegreeSize', 0) > 0:
                        degree = '2'
                    elif network_info.get('thirdDegreeSize', 0) > 0:
                        degree = '3'

                return {
                    'degree': degree,
                    'mutual_connections_count': len(mutual_connections),
                    'mutual_connections': mutual_connections[:5],  # Show first 5 mutual connections
                    'is_connected': is_connected,
                    'network_info': {
                        'first_degree': network_info.get('firstDegreeSize', 0),
                        'second_degree': network_info.get('secondDegreeSize', 0),
                        'third_degree': network_info.get('thirdDegreeSize', 0)
                    }
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    continue
                else:
                    print(f"Warning: Could not determine connection status after {max_retries} attempts")
                    return {
                        'degree': 'unknown',
                        'mutual_connections_count': 0,
                        'mutual_connections': [],
                        'is_connected': False,
                        'network_info': {
                            'first_degree': 0,
                            'second_degree': 0,
                            'third_degree': 0
                        }
                    }

    def get_profile_data(self, profile_url, max_retries=3):
        """Extract profile data with retry mechanism"""
        for attempt in range(max_retries):
            try:
                print(f"Accessing profile (attempt {attempt + 1}/{max_retries})...")
                
                # Extract profile ID from URL
                profile_id = profile_url.split('/in/')[-1].split('/')[0]
                
                # Get profile data
                profile_data = self.api.get_profile(profile_id)
                if not profile_data:
                    raise Exception("Could not get profile data")
                
                # Extract experience
                experience = profile_data.get('experience', [])
                formatted_experience = []
                
                for exp in experience:
                    try:
                        start_date = exp.get('startsAt', {})
                        end_date = exp.get('endsAt', {})
                        
                        formatted_exp = {
                            'title': exp.get('title', ''),
                            'company': exp.get('companyName', ''),
                            'start_date': {
                                'raw': start_date,
                                'formatted': self.format_date(start_date)
                            },
                            'end_date': {
                                'raw': end_date,
                                'formatted': self.format_date(end_date)
                            },
                            'description': exp.get('description', ''),
                            'location': exp.get('locationName', '')
                        }
                        formatted_experience.append(formatted_exp)
                    except Exception as e:
                        print(f"Warning: Error formatting experience entry: {str(e)}")
                        continue
                
                # Get connection status
                connection_info = self.get_connection_status(profile_id)
                
                # Extract birth date with visibility information
                birth_date = profile_data.get('birthDate', {})
                birth_year = birth_date.get('year') if birth_date else None
                
                result = {
                    'full_name': f"{profile_data.get('firstName', '')} {profile_data.get('lastName', '')}",
                    'birth_year': {
                        'value': birth_year,
                        'is_visible': birth_year is not None,
                        'connection_status': connection_info['degree']
                    },
                    'profile_creation_date': profile_data.get('createdAt', {}).get('time'),
                    'experience': formatted_experience,
                    'profile_url': profile_url,
                    'connection_info': connection_info
                }
                
                return result
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    # Add random delay between retries
                    delay = random.uniform(5, 10)
                    print(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Error extracting profile data after {max_retries} attempts: {str(e)}")
                    return None

    def save_to_json(self, data, filename):
        """Save the extracted data to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

def main():
    try:
        extractor = LinkedInExperienceExtractor()
        
        # Example usage
        profile_url = input("Enter LinkedIn profile URL: ")
        data = extractor.get_profile_data(profile_url)
        
        if data:
            filename = f"linkedin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            extractor.save_to_json(data, filename)
            
            # Print detailed information
            print("\nProfile Information:")
            print(f"Name: {data['full_name']}")
            print(f"Profile URL: {data['profile_url']}")
            
            print("\nProfile Visibility:")
            visibility = extractor.check_profile_visibility(data)
            print(f"Privacy Level: {visibility['privacy_level']}")
            print(f"Is Public: {visibility['is_public']}")
            print("\nAvailable Sections:")
            for section in visibility['available_sections']:
                print(f"- {section}")
            print("\nRestricted Sections:")
            for section in visibility['restricted_sections']:
                print(f"- {section}")
            
            print("\nConnection Information:")
            conn_info = data['connection_info']
            print(f"Connection Degree: {conn_info['degree']}")
            print(f"Network Size:")
            print(f"- 1st Degree: {conn_info['network_info']['first_degree']}")
            print(f"- 2nd Degree: {conn_info['network_info']['second_degree']}")
            print(f"- 3rd Degree: {conn_info['network_info']['third_degree']}")
            print(f"Mutual Connections: {conn_info['mutual_connections_count']}")
            
            print("\nBirth Year Information:")
            birth_year_info = data['birth_year']
            print(f"Value: {birth_year_info['value']}")
            print(f"Visible: {birth_year_info['is_visible']}")
            print(f"Connection Status: {birth_year_info['connection_status']}")
        else:
            print("\nCould not extract profile data. Please check:")
            print("1. Your LinkedIn credentials in .env file")
            print("2. The profile URL is correct and accessible")
            print("3. Your LinkedIn account has necessary permissions")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please ensure your LinkedIn credentials are properly configured in .env file")

if __name__ == "__main__":
    main() 