# 🏆 FPL Liga Dashboard

Et lokalt dashboard til Fantasy Premier League mini-ligaer. Viser ligastilling, point-udvikling, GW-statistikker, chip-brug og meget mere — alt sammen trukket direkte fra FPL's offentlige API via en lokal Python-proxy.

---

## 📁 Projektstruktur

```
fpl-dashboard/
├── backend/
│   ├── app.py            # Flask proxy-server (omgår CORS)
│   └── requirements.txt  # Python-afhængigheder
└── frontend/
    └── index.html        # Hele dashboardet i én fil
```

---

## 🚀 Kom i gang

### 1. Forudsætninger

- Python 3.8+ installeret
- En browser (Chrome, Firefox, Edge)

### 2. Installer Python-afhængigheder

```bash
cd fpl-dashboard/backend
pip install -r requirements.txt
```

### 3. Start backend-serveren

```bash
python app.py
```

Du bør se:
```
🏆  FPL Dashboard Backend
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡  Running at  http://localhost:5000
🌐  Proxying    https://fantasy.premierleague.com/api
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Åbn dashboardet

Åbn filen `frontend/index.html` direkte i din browser:
- **Windows:** Dobbeltklik på filen, eller træk den ind i Chrome
- **Mac:** `open frontend/index.html`
- **Linux:** `xdg-open frontend/index.html`

### 5. Hent data

1. Find dit **Liga-ID** i FPL — det er nummeret i URL'en når du ser din liga:
   `https://fantasy.premierleague.com/leagues/`**`123456`**`/standings/c`
2. Indtast ID'et i feltet øverst i dashboardet
3. Klik **📡 Hent data**

---

## 📊 Dashboard-sektioner

| Sektion | Beskrivelse |
|---|---|
| 🏅 **Ligastilling** | Tabel med alle managers – rank, GW-point, total, ændring siden sidst |
| 📊 **Nøglestatistikker** | Bedste/laveste GW, mest konsistente spiller, afstand top→bund |
| 📈 **Point-udvikling** | Kumuleret linjegraf for alle managers med toggle-mulighed |
| 🎯 **GW-sammenligning** | Søjlediagram for en valgt GW – guldfarve til vinderen |
| 🃏 **Chip-brug** | Overblik over hvornår hver manager har brugt sine chips |
| 😳 **Hall of Shame** | De 3 laveste GW-scores i sæsonen |

---

## ⚙️ Konfiguration

Du kan ændre standard-backends URL direkte i browserens konfig-bar.

For at hardcode et liga-ID, åbn `frontend/index.html` og find:
```js
// Sæt denne værdi for at undgå at taste den manuelt
$('liga-input').value = 'DIT_LIGA_ID';
```

---

## 🛠️ API Endpoints (backend)

| Endpoint | Beskrivelse |
|---|---|
| `GET /api/league/{id}` | Liga-standings (alle sider) |
| `GET /api/manager/{id}/history` | GW-historik + chip-brug |
| `GET /api/bootstrap` | Sæsondata (events/GWs) |
| `GET /api/manager/{id}/picks/{gw}` | Holdvalg for specifik GW |
| `GET /health` | Server-status |

---

## 🐛 Fejlfinding

**"Connection refused" / kan ikke hente data**
→ Sørg for at backend kører (`python app.py`) og at porten matcher (standard: 5000)

**"HTTP 404" for liga**
→ Tjek at liga-ID'et er korrekt. Find det i FPL-URL'en.

**Data loader meget langsomt**
→ FPL's API har rate limits. Med 11 managers henter vi ~11 API-kald. Det tager typisk 10-20 sekunder.

**Ingen chip-data vises**
→ Chips opdateres først efter de er brugt og GW'en er afsluttet.

---

## 📦 Afhængigheder

**Python (backend)**
- `flask` – web-server
- `flask-cors` – tilføjer CORS-headers
- `requests` – HTTP-klient til FPL API

**JavaScript (CDN, ingen installation)**
- [Chart.js 4.4](https://www.chartjs.org/) – grafer og diagrammer

---

*Lavet med ⚽ og for meget FPL-nostalgi.*
