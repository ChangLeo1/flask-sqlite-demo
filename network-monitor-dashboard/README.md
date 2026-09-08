# Small Business Network Monitor

A lightweight Python network-monitoring dashboard built with **Flask + SQLite + HTML/CSS/JavaScript**.

It is designed as a practical portfolio project that shows **networking, Python, dashboard development and troubleshooting** in one place.

## What it checks

For every device or host you add, the app can show:

- **Availability** — whether the host replies to ping
- **Latency** — average ping response time in milliseconds
- **Packet loss** — percentage of ping packets that do not return
- **DNS resolution** — the IP address returned for a hostname such as `google.com`
- **TCP port status** — whether one configured service port accepts a connection
- **Recent uptime** — percentage of successful checks from the latest stored measurements
- **History** — measurements saved in SQLite for later analysis

The dashboard automatically rechecks targets every 30 seconds while the page is open.

## Example use

A small office could add:

| Device | Host | Optional port | What it tells you |
|---|---|---:|---|
| Router | `192.168.1.1` | — | Is the gateway reachable? |
| NAS | `192.168.1.10` | `445` | Is the NAS online and is SMB reachable? |
| Printer | `192.168.1.20` | `9100` | Is the printer online and is its print service reachable? |
| Website | `google.com` | `443` | Do DNS, internet access and HTTPS connectivity work? |

> Local addresses such as `192.168.x.x` can only be checked when this app is running on a computer connected to that same network.

## How it works

```text
Browser Dashboard
       |
       v
Flask Web App
       |
       +--> DNS lookup (Python socket)
       +--> Ping test (system ping command)
       +--> TCP port check (Python socket)
       |
       v
SQLite Database
       |
       +--> targets
       +--> measurement history
```

## Run it on Windows / macOS / Linux

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install packages and start the dashboard:

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically on first run.

## Test it

```bash
pytest -q
```

## Project structure

```text
network-monitor-dashboard/
├── app.py              # Flask routes and API
├── monitor.py          # ping, DNS and TCP checks
├── db.py               # SQLite operations
├── schema.sql          # database schema
├── templates/
│   └── index.html      # dashboard page
├── static/
│   ├── app.js          # live refresh logic
│   └── style.css       # responsive UI
├── tests/
│   └── test_app.py
├── requirements.txt
└── README.md
```

## What I learned / demonstrated

- Python networking with `socket`
- ICMP-style reachability testing through the operating system `ping` utility
- TCP connectivity checks
- DNS troubleshooting
- Flask backend and JSON API development
- SQLite data storage
- Basic frontend JavaScript for live dashboard updates
- Turning raw network measurements into an interface useful for troubleshooting

## Good next upgrades

- Latency and packet-loss charts
- Email/Slack alerts after repeated failures
- SNMP monitoring for switches and routers
- Export measurements to CSV
- Authentication for business use
- Docker deployment
