# OpenWrt AdGuard Home Scheduler 🕒

A lightweight, professional web dashboard to manage multiple enable/disable schedules for **AdGuard Home** running on **OpenWrt** routers.

This tool bypasses the limitation of the single schedule in the official AdGuard Home interface by leveraging OpenWrt's native **Cron** system via a simple web interface.

![Dashboard Preview](https://via.placeholder.com/800x400?text=AdGuard+Scheduler+Dashboard)

## Features
- ✅ **Clean UI**: Modern, responsive HTML5 dashboard.
- ✅ **Unlimited Schedules**: Add as many On/Off timers as you need.
- ✅ **Native Integration**: Uses OpenWrt's built-in `crontab` system.
- ✅ **No Dependencies**: Pure HTML/JS frontend and Shell Script backend. No PHP/Python required.

## Installation

### 1. Requirements
- OpenWrt Router
- AdGuard Home installed and running
- `curl` installed on the router (usually pre-installed or `opkg install curl`)

### 2. Copy Files
Upload the files to your router using **SCP** (WinSCP) or basic file creation commands.

- **`adguard_api.cgi`** -> `/www/cgi-bin/adguard_api.cgi`
- **`adguard_dashboard.html`** -> `/www/adguard_dashboard.html`

### 3. Set Permissions (Important!)
You must make the backend script executable:

```bash
chmod +x /www/cgi-bin/adguard_api.cgi
```

## Usage

1. Open your browser and navigate to:
   `http://192.168.1.1/adguard_dashboard.html`
   *(Replace with your router's IP address)*

2. Select the **Action** (ON/OFF), **Hour**, and **Minute**.
3. Click **Add Schedule**.

The script will automatically create the necessary Cron job to toggle AdGuard Home's filtering status via its API.

## Configuration (Optional)
If your AdGuard Home is running on a different port than `3000` or requires authentication, edit `adguard_api.cgi`:

```bash
# Line 55: Update the URL or add credentials (-u user:pass)
cmd="curl -X POST ..."
```

## License
MIT License - Feel free to modify and share!
