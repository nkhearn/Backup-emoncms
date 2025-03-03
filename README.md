# Backup-emoncms
# EmonCMS Google Drive Backup

This project provides a simple script to automate the backup of your EmonCMS data to Google Drive. It performs the following actions:

1.  **Backs up EmonCMS data:** Creates a local backup of your EmonCMS database.
2.  **Uploads to Google Drive:** Uploads the backup file to your specified Google Drive folder.
3.  **Deletes local backup:** Removes the local backup file to save disk space.

## Prerequisites

* **EmonCMS Installation:** You must have a working EmonCMS installation.
* **Python 3:** Python 3 must be installed on your system.
* **Google Cloud Project:** You'll need a Google Cloud project with the Google Drive API enabled.
* **Google Cloud Service Account:** You'll need to create a service account and download its credentials as a JSON file.

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/nkhearn/Backup-emoncms.git
    cd backup-emoncms
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```


3.  **Create Google Cloud Service Account Credentials:**

    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Create or select a project.
    * Enable the "Google Drive API" for your project.
    * Navigate to "APIs & Services" -> "Credentials."
    * Click "Create Credentials" -> "Service account."
    * Give your service account a name and description.
    * Grant the service account the "Storage Object Creator" role (or a more specific role if needed) to allow it to upload files to Google Drive.
    * Click "Continue" and then "Create Key."
    * Select "JSON" as the key type and click "Create."
    * Save the downloaded JSON file as `service_credentials.json` in the same directory as your Python script.
    * **Important:** Keep this `service_credentials.json` file secure. Do not commit it to version control.

4.  **Configure the Script:**
    * Configure the `backup.py` script.
    * Near the bottom of the script is a path.join.  it uses the default path of `/var/opt/emoncms/backup`
    * Change this to your backup file location.

    * To get your google drive folder ID, open google drive in your browser, and navigate to the folder you wish to use. The ID is in the url. For example: `https://drive.google.com/drive/folders/YOUR_FOLDER_ID`

5.  **Run the Script:**

    ```bash
    ./backup.sh
    ```

## Scheduling

You can schedule the script to run automatically using cron (Linux/macOS) or Task Scheduler (Windows).

**Example Cron Job (Linux/macOS):**

To run the script daily at 2:00 AM, add the following line to your crontab:

```bash
0 2 * * * /path/to/backup.sh
```

To edit your crontab, run crontab -e.
Example Task Scheduler (Windows):
 * Open Task Scheduler.
 * Create a new basic task.
 * Set the trigger to run daily at your desired time.
 * Set the action to "Start a program."
 * Browse to your executable and add the path to your backup.sh script as an argument.
Security
 * Secure your service_credentials.json file. Do not share it or commit it to version control.
 * Use strong passwords for your EmonCMS database.
 * Restrict the service account's permissions to only what is necessary.
Disclaimer
This script is provided as-is, without any warranty. Use it at your own risk. Always test backups thoroughly.
