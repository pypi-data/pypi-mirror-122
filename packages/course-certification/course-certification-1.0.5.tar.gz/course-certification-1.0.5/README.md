# Course Certification

## Setting up

1. Installation:

    1. Install wkhtmltopdf from https://wkhtmltopdf.org/
    2. (only for Windows OS users)Add wkhtmltopdf to PATH:
        add **C:\Program Files\wkhtmltopdf\bin** to Path variable([video demo](https://gitlab.com/karthik49/course-certification/-/blob/master/how_to_add_wkhtmltopdf_to__windows_path.mov))
        1. Control panel -> System and Security -> System --> Advanced System Settings -> Advanced -> Environment variables... -> System variables -> Path(select this and click edit) -> Add C:\Program Files\wkhtmltopdf\bin
    3. Install course_certification:
        `pip install course_certification`


2. Get Google Spreadsheet API Json key file:
    Here’s how to get one:
    1. Enable API Access for a Project if you haven’t done it yet.
        1. Head to Google Developers Console and create a new project (or select the one you already have).
        2. In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
        3. In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.
    2. Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
    3. Fill out the form
    4. Click “Create” and “Done”.
    5. Press “Manage service accounts” above Service Accounts.
    6. Press on ⋮ near recenlty created service account and select “Manage keys” and then click on “ADD KEY > Create new key”.
    7. Select JSON key type and press “Create”.
    You will automatically download a JSON file with credentials. It may look like this:
    ```
    {
        "type": "service_account",
        "project_id": "api-project-XXX",
        "private_key_id": "2cd … ba4",
        "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
        "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
        "client_id": "473 … hd.apps.googleusercontent.com",
        ...
    }
    ```
    8. Remember the path to the downloaded credentials file. Also, in the next step you’ll need the value of client_email from this file.
    9. Very important! Go to your spreadsheet and share it with a client_email from the step above. Just like you do with any other Google account. If you don’t do this, you’ll get a gspread.exceptions.SpreadsheetNotFound exception when trying to access this spreadsheet from your application or a script.


## Usage

    `certificate_generator --key _the_path_of_key_file_ --output _output_folder_  --spreadsheet _spreadsheet_name_ --worksheet _worksheet_name_ --resources _folder_containing_resources_such_as_templates_ --html --pdf --image`

The above line will create the certificates in HTML, PDF and Image(jpg).

