import zipfile
import os
import traceback


def generate_download_url(version_number: str, base_url: str, file_name: str, connection_check_sub_url: str):
    """This function generates the URL for Chromedriver download and then checks the connection."""
    download_url = ''
    file_name = file_name.replace(r'/', '')
    connection_check_sub_url = connection_check_sub_url.replace(r'/', '')
    updated_version_number = version_number
    try:
        import requests
        google_url = base_url + r'/' + connection_check_sub_url
        latest_chromedriver_version = requests.get(google_url)
        if latest_chromedriver_version.status_code == 200:
            print('Connection to the server Successful!', flush=True)
            if str(version_number).strip().lower() == 'latest':
                download_url = base_url + r'/' + str(latest_chromedriver_version.text).strip() + r'/' + file_name
                updated_version_number = str(latest_chromedriver_version.text).strip()
            else:
                download_url = base_url + r'/' + version_number + r'/' + file_name
        else:
            print(f'Connection to the server Failed! with response code: {str(latest_chromedriver_version.status_code)}', flush=True)
    except Exception as e:
        print('Generate Download URL Failed!', flush=True)
        print(traceback.format_exc(), flush=True)

    return download_url, updated_version_number


def download_and_unzip(download_path: str, download_url: str, path: str) -> bool:
    """This function downloads the actual Chromedriver zip file and unzip it in the user's preferred location."""
    success_status = False
    try:
        import wget
        # download the zip file using the url provided
        latest_driver_zip = wget.download(download_url, download_path)
        # extract the zip file
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            # you can specify the destination folder path here
            archived_file_list = zip_ref.namelist()
            zip_ref.extractall(path)
            success_status = True
            for file in archived_file_list:
                if not os.path.isfile(os.path.join(path, file)):
                    success_status = False
        if not success_status:
            print('\nUnable to extract Chromedriver executable from Zip!', flush=True)
        else:
            print('\nChromedriver executable from Zip extracted!', flush=True)
        # delete the zip file downloaded above
        os.remove(latest_driver_zip)
    except Exception as e:
        print('\nChromedriver download and unzip failed!', flush=True)
        print(traceback.format_exc(), flush=True)
        success_status = False

    return success_status