#!/usr/bin/env python3
"""
Runner script for Improved Resume Downloader
"""

import os
import sys
from improved_resume_downloader import ImprovedResumeDownloader
import logging
import glob

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('improved_downloader_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the improved resume downloader"""
    print("=" * 60)
    print("Improved Resume Downloader for LinkedIn")
    print("=" * 60)
    
    # Load credentials from environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    if not linkedin_email or not linkedin_password:
        print("❌ Error: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        print("\nTo set environment variables:")
        print("export LINKEDIN_EMAIL='your_email@example.com'")
        print("export LINKEDIN_PASSWORD='your_password'")
        print("\nOr run with:")
        print("LINKEDIN_EMAIL='your_email' LINKEDIN_PASSWORD='your_password' python run_improved_downloader.py")
        return
    
    print(f"✅ Using LinkedIn account: {linkedin_email}")
    print("Starting improved resume download process...")
    print()
    
    downloader = ImprovedResumeDownloader(linkedin_email, linkedin_password)
    
    try:
        # Setup driver
        print("🔧 Setting up Chrome driver...")
        downloader.setup_driver()
        
        # Login to LinkedIn
        print("🔐 Logging into LinkedIn...")
        if not downloader.login_to_linkedin():
            print("❌ Failed to login to LinkedIn")
            return
        
        # Download all resumes
        print("📥 Downloading all resumes with improved click handling...")
        print("   • Will check for additional pages and process them all")
        print("   • Uses the same download logic for each page")
        success = downloader.check_and_process_all_pages()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Improved resume download process completed!")
            print("=" * 60)
            print("\n📁 Files downloaded to FSD_resume/ folder")
            print("\n📊 Summary:")
            print("   • Resumes downloaded with proper naming (firstname_lastname.pdf)")
            print("   • Bypassed LinkedIn's click interception errors")
            print("   • Used JavaScript execution for problematic clicks")
            print("   • Multiple fallback strategies for downloading")
            print("   • Files saved to FSD_resume/ folder")
        else:
            print("❌ Resume download process failed")
            
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        print("🔒 Closing browser...")
        downloader.close_driver()
        print("✅ Process completed")

if __name__ == "__main__":
    main() 