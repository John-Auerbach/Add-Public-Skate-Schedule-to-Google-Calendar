# **Add Public Skate Schedule to Google Calendar**  

This project is a command-line application that automatically adds **public skating events** from the Pegula Ice Rink calendar to a user's **Google Calendar**.

## **Features**
- Retrieve **only** public skating events from a shared Google Calendar.
- Insert events into a **user-specified** Google Calendar.
- Run **manually or automatically** (e.g., via a scheduled task).
- Uses **OAuth 2.0 authentication** to interact with Google Calendar.

---

## **Prerequisites**
- **Python 3.x** installed on your machine.
- A **Google account** with access to Google Calendar.
- A **Google Cloud Console** project with Calendar API enabled.
- A **credentials.json** file for OAuth2 authentication.

---

## **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/John-Auerbach/Add-Public-Skate-Schedule-to-Google-Calendar
cd Add-Public-Skate-Schedule-to-Google-Calendar
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Google Cloud API**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **new project**.
3. **Enable the Google Calendar API** for your project.
4. **Create OAuth 2.0 credentials**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth Client ID**.
   - Select **Desktop App** and generate credentials.
   - **Download the `credentials.json` file**.
   - Place `credentials.json` in the project root directory.

---

## **Configuration**
### **4️⃣ Create `config.py` for Your Calendar ID**
For security, we store the user's calendar ID in `config.py`, which is **not tracked by Git**.

1. Create a new file named **`config.py`** in the project folder.
2. Add the following code:
   ```python
   # config.py (DO NOT COMMIT THIS FILE)
   USER_CALENDAR_ID = "your-calendar-id@group.calendar.google.com"
   ```
3. Replace `"your-calendar-id@group.calendar.google.com"` with your **Google Calendar ID**:
   - Open Google Calendar.
   - Find your calendar in the left sidebar.
   - Click the **three dots** → `Settings and sharing`.
   - Scroll down to **Integrate Calendar**.
   - Copy the **Calendar ID**.

4. **Add `config.py` to `.gitignore`** to prevent accidental commits:
   ```bash
   echo "config.py" >> .gitignore
   ```

---

## **Usage**
### **5️⃣ Run Manually**
```bash
python auto-add-public-skate.py
```

- The script will **authenticate** with Google.
- It will **fetch public skating events** from Pegula’s calendar.
- It will **add missing events** to your Google Calendar.

### **6️⃣ Running Automatically**
You can schedule the script to run periodically.

#### **Windows (Task Scheduler)**
1. Open **Task Scheduler**.
2. Click **Create Basic Task**.
3. Set:
   - **Trigger**: Daily or Weekly.
   - **Action**: Start a program → `python.exe`.
   - **Arguments**: Full path to `auto-add-public-skate.py`.
4. Click **Finish**.

#### **Mac/Linux (Cron Job)**
1. Open Terminal.
2. Type `crontab -e` to edit cron jobs.
3. Add a line like this to run the script every day at 7 AM:
   ```bash
   0 7 * * * /usr/bin/python3 /path/to/auto-add-public-skate.py
   ```
4. Save and exit.

---

## **Verifying Events**
After running the script, open **Google Calendar** and check if public skate sessions have been added.

---

## **Troubleshooting**
### **Invalid Credentials (`invalid_grant: Bad Request`)**
- **Solution:** Delete the old token file and re-authenticate:
  ```bash
  del token.json  # Windows
  rm token.json   # Mac/Linux
  python auto-add-public-skate.py
  ```

### **Google API Quota Limits**
- If your script runs too frequently, Google might limit API requests.
- Reduce frequency in Task Scheduler/Cron.

---

## **Contributing**
Feel free to fork the repository and submit pull requests!

---

## **License**
This project is licensed under the **MIT License**.