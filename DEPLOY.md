# How to Deploy to Google Cloud — Step by Step

---

## Before you start — things you need

| What | Where to get it | Cost |
|------|----------------|------|
| Google account | gmail.com | Free |
| OpenAI API key | platform.openai.com | Pay per use |

---

## PHASE 1 — Set up Google Cloud (do this once, ever)

### Step 1: Create a Google Cloud Account

1. Open your browser and go to: https://cloud.google.com/
2. Click the big blue button **"Get started for free"**
3. Sign in with your Gmail account
4. It will ask for a credit card
   - DON'T WORRY — you get **$300 free credit**
   - You will NOT be charged for a small hobby app
   - Cloud Run charges only when someone uses your app
5. Click through the setup wizard until you reach the Google Cloud Console

---

### Step 2: Create a Project

Think of a Project like a **folder** in Google Cloud.
Everything your app needs lives inside this folder.

1. Go to: https://console.cloud.google.com/
2. At the very top, click the dropdown that might say "My First Project" or "Select a project"
3. A popup appears — click **"New Project"** (top right of the popup)
4. Fill in:
   - **Project name:** `my-crew-ai-app`
   - Leave everything else as default
5. Click **"Create"**
6. Wait 10 seconds, then select your new project from the dropdown at the top

---

### Step 3: Install Google Cloud CLI on your computer

The CLI (Command Line Interface) lets you control Google Cloud
from your terminal (the black box you type commands in).

1. Go to: https://cloud.google.com/sdk/docs/install-sdk
2. Under **Windows**, click **"Google Cloud CLI installer"**
3. Download and run the installer (.exe file)
4. During install:
   - Keep all defaults checked
   - Check "Run gcloud init" at the end — OR do it manually after

5. After install, **open a brand new terminal** (Command Prompt or PowerShell)
   - Windows: Press `Win + R`, type `cmd`, press Enter

6. Type this and press Enter:
   ```
   gcloud --version
   ```
   You should see something like: `Google Cloud SDK 460.0.0`
   If you see this, the install worked!

---

### Step 4: Log in and connect to your project

```bash
gcloud init
```

This will:
1. Open a browser window asking you to sign into Google
2. Sign in with the same Gmail you used for Google Cloud
3. Come back to the terminal — it asks "Pick cloud project to use"
4. Type the number next to `my-crew-ai-app` and press Enter

Then run this to double-check:
```bash
gcloud config get-value project
```
It should print: `my-crew-ai-app`

---

### Step 5: Turn on the required Google Cloud services

Google Cloud has hundreds of services. You need to "turn on" the ones you'll use.
Think of it like installing apps on a new phone.

Copy and paste these 3 commands one by one:

```bash
gcloud services enable run.googleapis.com
```
(This enables Cloud Run — where your app will live)

```bash
gcloud services enable cloudbuild.googleapis.com
```
(This enables Cloud Build — it builds your app before deploying)

```bash
gcloud services enable secretmanager.googleapis.com
```
(This enables Secret Manager — a safe vault for your API keys)

Each command takes about 10-30 seconds. You'll see "Operation finished successfully."

---

## PHASE 2 — Store your API key safely

NEVER put your API key directly in the code.
Instead, we store it in Google's **Secret Manager** — think of it like a safe/locker.

### Step 6: Save your OpenAI API key

Replace `PASTE_YOUR_OPENAI_KEY_HERE` with your actual key (starts with `sk-`):

```bash
echo -n "PASTE_YOUR_OPENAI_KEY_HERE" | gcloud secrets create OPENAI_API_KEY --data-file=-
```

You should see: `Created version [1] of the secret [OPENAI_API_KEY].`

---

## PHASE 3 — Deploy your app!

### Step 7: Navigate to your app folder

```bash
cd "C:\Users\Prasanth Sahoo\Downloads\CrewAI\my_crew_app"
```

---

### Step 8: THE BIG DEPLOY COMMAND

Copy and paste this entire command:

```bash
gcloud run deploy my-crew-app ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest ^
  --memory 2Gi ^
  --timeout 300
```

NOTE: The `^` at the end of each line is Windows' way of continuing a long command.
On Mac/Linux you'd use `\` instead.

What this command does (explained simply):
- `gcloud run deploy my-crew-app` → Name your app "my-crew-app"
- `--source .`                    → Use the code in THIS folder (the dot means "here")
- `--platform managed`            → Let Google manage the server for you
- `--region us-central1`          → Put the server in USA (choose closest to you)
- `--allow-unauthenticated`       → Anyone can visit your app URL (no login needed)
- `--set-secrets ...`             → Give your app access to the saved API key
- `--memory 2Gi`                  → Give the app 2GB of memory (AI needs this)
- `--timeout 300`                 → Wait up to 5 minutes for a response (AI is slow)

---

### Step 9: Wait and watch

The command will:
1. Upload your code to Google Cloud (~30 seconds)
2. Build it using your Dockerfile (~2-3 minutes)
3. Deploy it to a server (~30 seconds)

At the very end you'll see something like:

```
Service [my-crew-app] revision [my-crew-app-00001-abc] has been deployed
Service URL: https://my-crew-app-abcdefghij-uc.a.run.app
```

**COPY THAT URL — that is your app's address on the internet!**

---

### Step 10: Open your app!

1. Open your browser
2. Paste the URL you copied
3. You should see your Streamlit app!
4. Type a topic, click Research, wait ~60 seconds, see the result!

---

## PHASE 4 — Useful commands after deployment

### See your app URL again (if you forgot it):
```bash
gcloud run services describe my-crew-app --region us-central1 --format="value(status.url)"
```

### See live logs (what's happening on the server):
```bash
gcloud run services logs read my-crew-app --region us-central1 --limit 50
```

### Update your app after changing code:
Just run the deploy command again from Step 8!
Google Cloud will update without any downtime.

### Update your OpenAI key (if you get a new one):
```bash
echo -n "YOUR_NEW_KEY" | gcloud secrets versions add OPENAI_API_KEY --data-file=-
```

### Stop your app (so it doesn't cost money):
```bash
gcloud run services delete my-crew-app --region us-central1
```

---

## Estimated Costs

| Service | Free Tier | After Free Tier |
|---------|-----------|-----------------|
| Cloud Run | 2M requests/month free | ~$0.40/million requests |
| Cloud Build | 120 min/day free | Very cheap |
| Secret Manager | 6 versions free | Nearly free |
| **OpenAI gpt-4o** | None | ~$0.01–0.03 per research task |

For a hobby project used occasionally: **expect $0–2/month total**

---

## Something went wrong? Common fixes

| Problem | Fix |
|---------|-----|
| `gcloud: command not found` | Restart your terminal after installing gcloud |
| `Permission denied` | Run: `gcloud auth login` |
| `Project not found` | Run: `gcloud config set project my-crew-ai-app` |
| App crashes on startup | Run the logs command above to see the error |
| `Secret not found` | Make sure you ran Step 6 first |
| App times out | The 300s timeout is already set — AI just needs time, wait for it |
