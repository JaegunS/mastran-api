# MASTRAN Sheet API

## Introduction
To get started, go to the [Google Cloud console](https://console.cloud.google.com/welcome?hl=en) and create a new project. Name it whatever you'd like. Your organization should be **umich.edu** and your location should be **self-created**.

Then, select your project and search for the **Google Sheets API**. Enable it. Then, click **Create Credentials**.

Select **User data** and fill out the fields. Then, download the JSON file. Rename it to `credentials.json` and place it in **src**.

Run the following command to install the required packages:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You should be all set up! Try running `example.py`.
