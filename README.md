# Public Skating Scheduler

This project is a command-line application that allows users to automatically add public skating events from a shared Google Calendar to their personal Google Calendar.

## Features

- Retrieve public skating events from a shared calendar.
- Insert events into a user-specified Google Calendar.
- Simple command-line interface for inputting calendar IDs.

## Prerequisites

- Python 3.x installed on your machine.
- A Google account with access to Google Calendar.
- `credentials.json` file from Google Cloud Console for OAuth2 authentication.

## Installation

1. **Clone the Repository**

   Clone the repository to your local machine using Git:

   ```bash
   git clone https://github.com/John-Auerbach/Add-Public-Skate-Schedule-to-Google-Calendar
   cd Add-Public-Skate-Schedule-to-Google-Calendar
   ```

2. **Install Dependencies**

   Use `pip` to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Google Cloud Project**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Enable the Google Calendar API.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place `credentials.json` in the root directory of your project.

## Usage

1. **Run the Script**

   Use the following command to run the application:

   ```bash
   python public-skating-scraper.py
   ```

2. **Input Calendar IDs**

   - When prompted, enter the public skating calendar ID. This can be found on the Pegula website by navigating to `Calendar`, performing a search, then clicking the Google icon next to `Sync Pegula Ice Arena Calendar`. Example: `qq3p7mn8h8dtn10dlaphfrkoaam5sh8p@import.calendar.google.com`
   - Enter your Google Calendar ID where the events will be added. Example: `your-calendar-id@group.calendar.google.com`

3. **Authorize the Application**

   - The application will open a browser window for Google authentication.
   - Log in with your Google account and authorize the application to access your Google Calendar.

4. **Verify Events**

   - After the script runs, check your Google Calendar to see the imported events.

```