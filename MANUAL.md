# AIRA-ONE Farm Plot Directory — View App Manual

## Overview

The view app is a read-only version of the farm plot manager for sharing with farm members. It connects live to the admin app's data — no separate database.

- **URL:** https://aira-view.onrender.com
- **Access:** Members login with shared username/password
- **GitHub:** https://github.com/damu1966/aira-view

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python / Flask + Gunicorn |
| Data source | Proxies from admin app API (PythonAnywhere) |
| Map | Leaflet.js |
| Frontend | Vanilla JS, CSS |
| Hosting | Render.com (free tier) |

### Key Files

```
aira_view/
├── app.py                  # Flask backend — proxy routes + login/logout
├── requirements.txt        # Python dependencies (flask, requests, gunicorn)
├── Procfile                # Render start command
├── MANUAL.md               # This file
├── static/
│   └── farm_map.png        # Farm map image
└── templates/
    ├── index.html          # Main read-only map + panel UI
    └── login.html          # Login page
```

---

## Features (Read-Only)

- Login page with username/password
- Farm map with colour-coded plot boundaries
- Click any plot polygon → popup shows owner name, mobile, email
- **Owners tab:** Browse all owners, search by name/mobile/plot, click 📍 to locate on map
- **Plots tab:** Browse all plots, filter undrawn/unassigned, click plot ID to jump on map
- Stats in header: total plots, owners, assigned, mapped
- Sign out button

### What members CANNOT do
- Add, edit, or delete owners or plots
- Draw or modify plot boundaries
- Assign owners to plots

---

## How Data Flows

```
Member's browser
     │
     ▼
Render (aira-view.onrender.com)
     │  /api/data
     ▼
PythonAnywhere (airafoads.pythonanywhere.com)
     │  reads farm.db
     ▼
Returns plots + owners JSON
```

Data is always live — any changes made in the admin app appear immediately in the view app.

---

## Login Credentials

Credentials are set as **environment variables** on Render (not hardcoded):

| Variable | Purpose |
|----------|---------|
| `APP_USERNAME` | Shared username for all members |
| `APP_PASSWORD` | Shared password for all members |
| `SECRET_KEY` | Flask session encryption key |

### To Change the Password
1. Go to [render.com](https://render.com) → **aira-view** → **Environment** tab
2. Update `APP_PASSWORD` value
3. Click **Save Changes** — app redeploys automatically (~1 min)

---

## Deployment

The app auto-deploys from GitHub whenever code is pushed to the `main` branch.

### To Update Code
```bash
# Make changes to files in aira_view/ folder
cd /Users/damodaransubramanian/AiraFoads/aira_view
git add .
git commit -m "Description of change"
git push
```
Render detects the push and redeploys automatically.

### Manual Redeploy (without code changes)
Render dashboard → **aira-view** → **Manual Deploy** → **Deploy latest commit**

---

## Render Settings

| Setting | Value |
|---------|-------|
| Runtime | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |
| Instance type | Free |
| Region | Singapore |
| Auto-deploy | Yes (on GitHub push) |

### Environment Variables (set in Render dashboard)
```
APP_USERNAME=<your username>
APP_PASSWORD=<your password>
SECRET_KEY=<random string>
```

---

## Render Free Tier — Important Notes

| Behaviour | Detail |
|-----------|--------|
| **Sleep** | App sleeps after 15 min of no traffic |
| **Wake time** | First load after sleep takes ~30 seconds |
| **Hours** | 750 free hours/month (enough for 1 app) |
| **Disk** | Ephemeral — no local DB (by design, data comes from PythonAnywhere) |

**Tell members:** If the page takes long to load, wait 30 seconds and try again — it is waking up.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Login page shows but no data after login | PythonAnywhere admin app is sleeping | Open `airafoads.pythonanywhere.com` to wake it, then reload |
| Slow first load | Render instance sleeping | Wait 30 seconds, refresh |
| "Invalid username or password" | Wrong credentials | Check `APP_USERNAME` / `APP_PASSWORD` in Render Environment |
| Map shows but no polygons | Plots have no boundaries drawn yet | Draw them in admin app |
| Blank page / JS error | Code bug or failed deploy | Check Render Logs tab |

### View Logs
Render dashboard → **aira-view** → **Logs** tab

---

## Updating the Farm Map Image

If the farm map image changes:
1. Copy new `farm_map.png` to `aira_view/static/farm_map.png`
2. Run:
```bash
cd /Users/damodaransubramanian/AiraFoads/aira_view
git add static/farm_map.png
git commit -m "Update farm map image"
git push
```

---

## Dependencies

```
flask>=2.3.0       # Web framework
requests>=2.31.0   # HTTP proxy calls to admin API
gunicorn>=21.2.0   # Production WSGI server for Render
```
