import os
import requests
import subprocess
import wget
import zipfile


def download_latest_version(version_number, driver_directory):
    print("Attempting to download latest driver online......")
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    print(download_url)
    # downloads driver as a zip file to specified folder
    latest_driver_zip = wget.download(download_url, out=os.path.dirname(driver_directory))
    # read & extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
        # zip file will be extracted to specified folder path
        downloaded_zip.extractall(path=driver_directory)
        print(f"\nSuccessfully downloaded version {version_number} to:\n{driver_directory}")
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)
    return


def check_driver(driver_directory):
    latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    # check for latest chromedriver version online
    response = requests.get(latest_release_url)
    online_driver_version = response.text
    print(f"Latest online chromedriver version: {online_driver_version}")
    # executes cmd line entry to check for existing web-driver version locally
    try:
        cmd_run = subprocess.run("chromedriver --version",
                                 capture_output=True,
                                 text=True)
    except FileNotFoundError:
        print("No local chromedriver.exe found in specified path")
        download_latest_version(online_driver_version, driver_directory)
    else:
        # Extract driver version number as string from terminal output
        local_driver_version = cmd_run.stdout.split()[1]
        print(f"Local chromedriver version: {local_driver_version}")
        if local_driver_version == online_driver_version:
            return True
        else:
            download_latest_version(online_driver_version, driver_directory)
