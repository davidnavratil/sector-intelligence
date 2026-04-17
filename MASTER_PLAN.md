# Sector Intelligence — Master plán
## Česká spořitelna · Sektorová analýza

> Aktualizováno: 23. března 2026
> Stav: Prototyp webové platformy hotový, nasazený na GitHub Pages

---

## 0. Klasifikace položek

Každá položka v plánu je označena jedním ze tří štítků:

| Štítek | Význam | Akce |
|--------|--------|------|
| 🚀 **Quick win** | Lze realizovat rychle (hodiny–dny), jasné zadání, žádné závislosti | Udělat hned |
| 🔧 **Build** | Složitější implementace (týdny), ale víme co a jak | Naplánovat a realizovat |
| 🔍 **Discovery** | Nejdřív ověřit proveditelnost, dostupnost dat, interní procesy, licencování | Prozkoumat před rozhodnutím |

---

## 1. Dekompozice stávajícího procesu

### Současný workflow přípravy sektorového reportu (automotive)

| Krok | Činnost | Čas (odhad) | Automatizovatelnost | Štítek |
|------|---------|-------------|---------------------|--------|
| 1 | Sběr dat z ČSÚ, Eurostatu, ACEA, OICA | 3–4 hod | 🟢 Plně | 🔧 Build |
| 2 | Čištění a konsolidace dat v Excelu | 2–3 hod | 🟢 Plně | 🔧 Build |
| 3 | Tvorba grafů a tabulek | 2–3 hod | 🟢 Plně | ✅ Hotovo (web) |
| 4 | Analýza trendů a komentáře | 3–4 hod | 🟡 Částečně (AI draft + lidská revize) | 🔍 Discovery |
| 5 | Monitoring zpráv a událostí | 1–2 hod | 🟢 Plně | 🔧 Build |
| 6 | Identifikace rizik a příležitostí | 2–3 hod | 🟡 Částečně | 🔍 Discovery |
| 7 | Formátování a finalizace reportu (PDF/PPTX) | 1–2 hod | 🟢 Plně | 🔧 Build |
| 8 | Distribuce | 0.5 hod | 🟢 Plně | 🚀 Quick win |
| **Celkem** | | **15–22 hod** | | |

### Cílový stav po automatizaci

| Krok | Činnost | Čas (odhad) | Změna |
|------|---------|-------------|-------|
| 1–3 | Automatický pipeline + web dashboard | 0 hod (automaticky) | −8–10 hod |
| 4 | AI draft komentářů → revize analytikem | 1–1.5 hod | −2–3 hod |
| 5 | Automatický monitoring + alerty | 0 hod (automaticky) | −1–2 hod |
| 6 | Foresighting framework + AI návrhy | 1 hod | −1–2 hod |
| 7 | Automatický export PDF/PPTX | 0 hod (automaticky) | −1–2 hod |
| 8 | Automatická distribuce | 0 hod (automaticky) | −0.5 hod |
| **Celkem** | | **2–2.5 hod** | **~85 % úspora** |

---

## 2. Architektura datového pipeline

### 2.1 Datové zdroje

| Zdroj | Data | Formát | Frekvence | Štítek | Poznámka |
|-------|------|--------|-----------|--------|----------|
| **ČSÚ API** | Průmyslová produkce NACE 29, registrace, zaměstnanost, mzdy | JSON/XML | Měsíčně | 🔧 Build | Veřejné API, dokumentované |
| **Eurostat API** | EU produkce, obchodní bilance, EV registrace | JSON (SDMX) | Měsíčně/čtvrtl. | 🔧 Build | Veřejné API, SDMX formát |
| **ACEA** | Registrace nových vozidel EU, EV podíly | Web/PDF | Měsíčně | 🔍 Discovery | Nutný scraping nebo ruční stahování PDF, ověřit legálnost |
| **ECB/ČNB** | Úrokové sazby, měnové kurzy | API | Denně | 🚀 Quick win | Jednoduché REST API |
| **UN Comtrade** | Mezinárodní obchod HS 8703 | API | Čtvrtletně | 🔍 Discovery | Komplexní API, rate limits, 3–6 měs. lag dat |
| **OICA** | Globální produkce vozidel | Web/PDF | Ročně | 🔍 Discovery | Pouze roční data, nutný scraping |
| **IEA** | Globální EV data, bateriová data | Různé | Roční + čtvrtl. | 🔍 Discovery | Některá data za paywall |
| **Bloomberg/Reuters** | Finanční data dodavatelů, CDS spready | Terminál/API | Denně | 🔍 Discovery | Vyžaduje licenci — má ČS přístup? |
| **NewsAPI / mediastack** | Monitoring zpráv automotive | JSON API | Realtime | 🚀 Quick win | Freemium, jednoduché API |
| **S&P Global Mobility** | Produkční forecasty, platform plans | Proprietary | Čtvrtletně | 🔍 Discovery | Drahá licence, ale standard v automotive |
| **EuroNCAP** | Bezpečnostní rating nových modelů | Web | Průběžně | 🚀 Quick win | Veřejné, scraping |
| **OECD** | Ekonomické indikátory, PMI | API | Měsíčně | 🔧 Build | Veřejné API |
| **Interní data ČS** | Portfolio exposure, NPL, rating klientů | Interní DB | Denně | 🔍 Discovery | Vyžaduje interní schválení, GDPR, IT security |

### 2.2 Technická architektura

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                             │
│  ČSÚ │ Eurostat │ ACEA │ ECB/ČNB │ NewsAPI │ OICA │ IEA    │
└──┬───────┬────────┬──────┬────────┬────────┬──────┬─────────┘
   │       │        │      │        │        │      │
   ▼       ▼        ▼      ▼        ▼        ▼      ▼
┌──────────────────────────────────────────────────────────────┐
│                  PYTHON DATA PIPELINE                         │
│  fetch_*.py → validate.py → clean_transform.py →              │
│  generate_data_js.py                                          │
│  + ai_commentary.py (Claude API)                              │
│  + detect_anomalies.py                                        │
│  + news_classifier.py                                         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                GITHUB ACTIONS (scheduled)                      │
│  Týdně/měsíčně: run pipeline → validate → commit data.js →   │
│  deploy to GitHub Pages → notify (email/Slack)                │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                WEB PLATFORM (GitHub Pages)                     │
│  index.html + app.js + data.js                                │
│  ✅ HOTOVO — https://davidnavratil.github.io/                 │
│              sector-intelligence/                              │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼ (Fáze 5)
┌──────────────────────────────────────────────────────────────┐
│            INTERNÍ PLATFORMA ČS (budoucnost)                  │
│  Backend (Python/Node) + Auth + interní data ČS               │
│  🔍 Discovery: infrastruktura, security, schválení            │
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Klíčové skripty

| Skript | Účel | Štítek | Poznámka |
|--------|------|--------|----------|
| `pipeline/fetch_csu.py` | Stahování dat z ČSÚ API | 🔧 Build | Dobře dokumentované API |
| `pipeline/fetch_eurostat.py` | Stahování dat z Eurostatu | 🔧 Build | SDMX, složitější queries |
| `pipeline/fetch_ecb_cnb.py` | Kurzy a sazby | 🚀 Quick win | Jednoduché REST |
| `pipeline/fetch_acea.py` | ACEA data scraping | 🔍 Discovery | Ověřit, zda povolují scraping |
| `pipeline/fetch_news.py` | Monitoring zpráv | 🚀 Quick win | NewsAPI free tier |
| `pipeline/validate.py` | Validace stažených dat | 🔧 Build | Kontrola kompletnosti, outlierů |
| `pipeline/clean_transform.py` | Čištění a transformace | 🔧 Build | Pandas, standardizace |
| `pipeline/generate_data_js.py` | Generování data.js | 🔧 Build | Jinja2 templating |
| `pipeline/ai_commentary.py` | AI komentáře k datům | 🔍 Discovery | Claude API — cost, kvalita, prompt engineering |
| `pipeline/detect_anomalies.py` | Detekce anomálií | 🔧 Build | z-score, IQR, sezónní adjustace |
| `pipeline/news_classifier.py` | AI klasifikace zpráv | 🔍 Discovery | Kvalita klasifikace, false positives |
| `pipeline/export_pdf.py` | Generování PDF reportu | 🔧 Build | WeasyPrint nebo Puppeteer |
| `pipeline/export_pptx.py` | Generování PPTX | 🔧 Build | python-pptx |
| `.github/workflows/update.yml` | GitHub Actions schedule | 🚀 Quick win | Cron + pipeline orchestrace |

---

## 3. Vylepšení analytického obsahu

### 3.1 Forward-looking sekce

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Predikce na 4Q dopředu | Extrapolace trendů s confidence intervaly | 🔧 Build | Jednoduché stat. modely (ARIMA, lin. regrese) |
| Leading indicators | PMI, nové objednávky, consumer confidence | 🔧 Build | Data z OECD, ČSÚ |
| Benchmark ČR vs. peers | Srovnání s DE, SK, PL, HU | 🔧 Build | Eurostat data, stejné metriky |
| ML predikční modely | Sofistikovanější forecasting (XGBoost, Prophet) | 🔍 Discovery | Dostatek historických dat? Přidaná hodnota vs. jednoduché modely? |
| Sentiment analýza trhu | NLP nad automotive zprávami | 🔍 Discovery | Kvalita českých NLP modelů, noise ratio |

### 3.2 Automatické komentáře

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| AI draft ke každé metrice | Claude API: trend, kontext, implikace | 🔍 Discovery | Prompt engineering, testování kvality, cost per run |
| Human-in-the-loop workflow | Analytik reviduje, schvaluje, edituje | 🔧 Build | UI pro review + approve |
| Komentáře pro RM | Doporučení pro relationship managery | 🔍 Discovery | Formát, relevance, interní procesy RM |
| Feedback loop | Schválené komentáře jako few-shot examples | 🔧 Build | Ukládání do JSON/DB |

### 3.3 Anomálie a alerty

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Statistická detekce | z-score > 2, IQR, sezónní adjustace | 🔧 Build | Standardní statistika |
| Traffic light přechody | Notifikace při změně 🟢→🟡 nebo 🟡→🔴 | 🚀 Quick win | Logika v pipeline |
| Kontextuální alerty | AI vysvětlí příčinu anomálie | 🔍 Discovery | Kvalita vysvětlení, false positives |
| Email notifikace | Automatický email s alertem | 🚀 Quick win | GitHub Actions + sendgrid/mailgun |
| Slack integrace | Alert do Slack kanálu | 🚀 Quick win | Webhook |
| Eskalační matice | Kdo dostane jaký alert (kritický vs. informativní) | 🔍 Discovery | Interní procesy, kdo je stakeholder |

### 3.4 Historické srovnání

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| YoY / QoQ toggle | Přepínač v grafech | 🚀 Quick win | Chart.js dataset switching |
| Timeline slider | Výběr období pro zobrazení | 🔧 Build | Nový UI komponent |
| Krizová srovnání | Overlay: COVID, energetická krize, chip shortage | 🔧 Build | Referenční data v data.js |
| Heatmapa měsíc × rok | Matice pro sezónní vzorce | 🚀 Quick win | Chart.js matrix plugin |

---

## 4. Foresighting framework

### 4.1 Trend Radar ✅ prototyp hotový

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Vizualizace radaru | 14 trendů, dopad × horizont | ✅ Hotovo | Na webu |
| Pravidelná aktualizace | Měsíčně signály, čtvrtletně pozice | 🔍 Discovery | Kdo bude aktualizovat? Workflow? |
| AI screening nových trendů | Claude prochází zprávy a navrhuje nové trendy | 🔍 Discovery | Kvalita návrhů, false positives |
| Expert validation | Pololetní validace s externími experty | 🔍 Discovery | Kdo jsou experti? Budget? |
| Trend detail drill-down | Klik na trend → detail s historií, zdroji | 🔧 Build | Nová UI sekce |

**Mechanismus pravidelné aktualizace:**

| Frekvence | Činnost | Kdo | Štítek |
|-----------|---------|-----|--------|
| Měsíčně | Review signálů a monitoring | Analytik + AI screening | 🔧 Build (AI), 🔍 Discovery (proces) |
| Čtvrtletně | Aktualizace pozic na radaru | Analytický tým | 🔍 Discovery (kdo, jak) |
| Pololetně | Přidání/odebrání trendů, validace | Tým + externí | 🔍 Discovery (experti) |
| Ročně | Kompletní revize radaru | Management + tým | 🔍 Discovery (governance) |

**Kategorie trendů:**
- Regulatorní (EU emisní limity, CBAM, ESG reporting, Euro 7)
- Technologické (EV, autonomní řízení, SDV, solid-state baterie, V2G)
- Tržní (čínská konkurence, konsolidace OEM, subscription modely, fleet management)
- Geopolitické (nearshoring, trade wars, supply chain diverzifikace, CBAM)
- Sociální (car sharing, urbanizace, demografické změny, remote work)
- Finanční (zelené dluhopisy, ESG investice, stranded assets ICE)

### 4.2 Scénářová matice ✅ prototyp hotový

**2×2 matice — osy:**
- X: Rychlost EV tranzice (pomalá ↔ rychlá)
- Y: Globální obchodní prostředí (protekcionismus ↔ otevřenost)

**4 scénáře:**
1. 🟡 **Evoluce** — pomalá tranzice + otevřenost → graduální adaptace
2. 🟢 **Zelený boom** — rychlá tranzice + otevřenost → příležitost pro early adopters
3. ⚪ **Stagnace** — pomalá tranzice + protekcionismus → regionalizace
4. 🔵 **Disruption** — rychlá tranzice + protekcionismus → chaotická transformace

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Matice vizualizace | 2×2 grid s detaily | ✅ Hotovo | Na webu |
| Signpost tracking | Měřitelné indikátory pro každý scénář | 🔧 Build | Definovat KPI, prahy |
| Pravděpodobnosti scénářů | Dynamické přiřazení % | 🔍 Discovery | Metodika, kdo rozhoduje |
| Monte Carlo simulace | Kvantitativní modelování scénářů | 🔍 Discovery | Má smysl? Data pro kalibraci? |
| Impakt na portfolio ČS | Dopad každého scénáře na bankovní metriky | 🔍 Discovery | Propojení s interními daty |
| Automatická revize | AI navrhuje přehodnocení na základě signpostů | 🔍 Discovery | Prompt engineering, validace |

### 4.3 Wild cards a černé labutě

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Wild card register | Nízká pravděp., vysoký dopad (válka, technol. průlom, regulatorní šok) | 🔧 Build | Statický seznam + UI |
| Contingency playbook | Připravené akce pro každou wild card | 🔍 Discovery | Interní procesy, kdo rozhoduje |
| Stress testing | Dopad wild cards na portfolio | 🔍 Discovery | Propojení s risk modely ČS |

---

## 5. Supply chain analýza ✅ prototyp hotový

### 5.1 Value chain mapping

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| 4-tier vizualizace | Suroviny → Komponenty → Systémy → OEM | ✅ Hotovo | Na webu |
| Interaktivní drill-down | Klik na tier → detail | 🚀 Quick win | Rozšířit existující `showTierDetail()` |
| Geografická mapa dodavatelů | Mapa ČR/EU s pozicemi klíčových dodavatelů | 🔧 Build | Leaflet.js nebo podobné |
| Real-time risk scoring | Automatické hodnocení rizik per dodavatel | 🔍 Discovery | Zdroj dat? Metodika? |

### 5.2 Risk heatmap ✅ prototyp hotový

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| 5×5 matice | Pravděpodobnost × dopad, 12 rizik | ✅ Hotovo | Na webu |
| Čtvrtletní aktualizace pozic | Přehodnocení rizik | 🔍 Discovery | Kdo hodnotí? Workshop? |
| Historický vývoj rizik | Jak se pozice rizik mění v čase | 🔧 Build | Ukládání historických dat |
| Risk mitigation tracking | Stav mitigačních opatření | 🔍 Discovery | Interní procesy |

### 5.3 Rozšířená supply chain analýza

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Supplier financial health | Propojení s bankovními daty ČS | 🔍 Discovery | Interní schválení, GDPR, data quality |
| Concentration risk | Závislost na single-source dodavatelích | 🔍 Discovery | Kde vzít data o závislostech? |
| Nearshoring monitor | Tracking přesunů výroby do/z ČR | 🔧 Build | Monitoring zpráv + CzechInvest data |
| ESG supply chain scoring | Hodnocení dodavatelů dle ESG | 🔍 Discovery | Metodika, data, regulatorní požadavky |
| Sanctions screening | Kontrola dodavatelů vs. sankční seznamy | 🔍 Discovery | Interní compliance, nástroje |
| Semiconductor dependency | Tracking čipové závislosti per OEM | 🔧 Build | Veřejná data + odhady |
| Battery supply chain | Detailní mapping lithium → cell → pack → EV | 🔧 Build | IEA data, veřejné zdroje |
| Critical raw materials | EU CRM list monitoring, zásoby, ceny | 🔧 Build | EU/USGS data, commodity feeds |

---

## 6. Webová platforma ✅ hotovo

### Aktuální stav
- **URL:** https://davidnavratil.github.io/sector-intelligence/
- **Technologie:** HTML + Tailwind CSS + Chart.js (static site, no build step)
- **Design:** Elegantní světlý theme, ČS brand barvy
- **Stránky:** Dashboard, Data Explorer, Foresighting, Supply Chain, News, Banking, Dokumenty

### Plánovaná vylepšení

| Vylepšení | Štítek | Poznámka |
|-----------|--------|----------|
| Drill-down v grafech (klik → detail) | 🚀 Quick win | Chart.js onClick handler |
| Srovnání období (YoY toggle) | 🚀 Quick win | Dataset switching |
| Fullscreen mód pro grafy | 🚀 Quick win | CSS + JS |
| Print-friendly layout | 🚀 Quick win | CSS @media print |
| Responsivní design (tablet/mobil) | 🔧 Build | Tailwind responsive classes |
| Animated transitions mezi stránkami | 🚀 Quick win | CSS transitions |
| Bookmark/share konkrétní stránky | 🚀 Quick win | URL hash routing |
| Uživatelská nastavení (oblíbené metriky) | 🔧 Build | LocalStorage |
| Dark/light mode toggle | 🚀 Quick win | CSS variables + toggle |
| Keyboard shortcuts | 🚀 Quick win | Event listeners |
| Search across all data | 🔧 Build | Full-text search v datech |
| Data download (CSV/Excel export z grafů) | 🔧 Build | Chart.js export + SheetJS |
| Accessibility (WCAG 2.1) | 🔧 Build | ARIA labels, contrast, keyboard nav |
| Embedding / iframe support | 🚀 Quick win | Responsive iframe friendly |
| PWA (offline mode) | 🔧 Build | Service worker, manifest.json |

---

## 7. Executive summary s traffic lights ✅ hotovo

### Dashboard obsahuje:
- **Sector Health Score** (0–10) s barevným indikátorem
- **8 klíčových metrik** s traffic lights (🟢🟡🔴) — aktuální stav + výhled
- **4 KPI karty** — produkce, registrace, EV podíl, zaměstnanost
- **Alert banner** — automatické upozornění na kritické události

### Rozšíření

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| Sparkline u Health Score (poslední rok) | 🚀 Quick win | Mini chart v kartě |
| Cross-sector srovnání | 🔧 Build | Až budou další sektory |
| Management one-pager PDF | 🔧 Build | Automatická generace top 5 zjištění |
| Konfigurovatelné prahové hodnoty TL | 🔧 Build | Admin UI nebo config.json |
| Historický log změn TL | 🔧 Build | Changelog: kdy se co změnilo |
| Komentář analytika u každé metriky | 🚀 Quick win | Textové pole v data.js |
| Sektor comparison spider chart | 🔧 Build | Radar chart — automotive vs. energetika |

---

## 8. Export reportů

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| PDF export z dashboardu | Tlačítko → PDF s metrikami, grafy, komentáři | 🔧 Build | jsPDF client-side nebo WeasyPrint server-side |
| PPTX šablona ČS | Brand barvy, loga, layout | 🔍 Discovery | Existuje brand book / šablona? |
| PPTX generátor | python-pptx v pipeline | 🔧 Build | 10–15 slidů |
| Word/DOCX export | Pro formální reporty | 🔧 Build | python-docx |
| Excel export surových dat | Download tabulek | 🚀 Quick win | SheetJS v prohlížeči |
| Automatická distribuce email | Email s PDF přílohou | 🚀 Quick win | Sendgrid/mailgun + cron |
| Slack notifikace | Shrnutí + odkaz na web | 🚀 Quick win | Incoming webhook |
| Teams notifikace | Pro interní komunikaci ČS | 🔍 Discovery | Má ČS Teams? Webhook access? |
| SharePoint archivace | Ukládání reportů do SharePointu | 🔍 Discovery | Přístup, API, governance |
| Scheduled delivery | Automatický report 1. pondělí v měsíci | 🔧 Build | GitHub Actions cron |
| Custom report builder | Analytik vybere sekce → custom PDF | 🔧 Build | UI + templating |

---

## 9. Multi-sector architektura

### Datový model
```
sectors/
  automotive/
    data.js          ← metriky, grafy, trendy, scénáře, supply chain
    config.json      ← specifické nastavení (zdroje, metriky, prahové hodnoty)
    pipeline/        ← fetch skripty specifické pro sektor
  energetika/
    data.js
    config.json
    pipeline/
  ...
```

### Plánované sektory

| Sektor | NACE | Štítek | Poznámka |
|--------|------|--------|----------|
| 🚗 Automotive | 29 | ✅ Hotovo | Prototyp na webu |
| ⚡ Energetika | 35 | 🔧 Build | Dostatek veřejných dat, jasné metriky |
| 💻 IT & Telco | 61–63 | 🔍 Discovery | Specifická data — kde je vzít? ČTÚ? |
| 🏗️ Stavebnictví | 41–43 | 🔧 Build | ČSÚ stavební produkce, hypotéky |
| 🧪 Chemie & farma | 20–21 | 🔍 Discovery | Heterogenní sektor, specifické zdroje |
| 🌾 Zemědělství & potravinářství | 01–03, 10–11 | 🔍 Discovery | SZIF, EAGRI — dostupnost API? |
| 🚚 Logistika & doprava | 49–53 | 🔍 Discovery | Specifické metriky, fragmentovaná data |
| 🏨 Turismus & hospitality | 55–56 | 🔍 Discovery | Sezónnost, COVID dopady, ČSÚ cestovní ruch |

### Sdílené vs. sektorově specifické komponenty

| Komponenta | Sdílená | Specifická |
|------------|---------|------------|
| Web layout (sidebar, header, navigace) | ✅ | |
| Chart.js rendering engine | ✅ | |
| Traffic light system | ✅ | |
| Foresighting framework (radar, matice) | ✅ | |
| Risk heatmap | ✅ | |
| News monitoring engine | ✅ | |
| Datové zdroje a fetch skripty | | ✅ |
| Metriky a KPI definice | | ✅ |
| Scénáře a signposty | | ✅ |
| Supply chain mapping | | ✅ |
| Prahové hodnoty pro TL | | ✅ |

### Refaktoring pro multi-sector 🔧 Build

| Krok | Popis |
|------|-------|
| 1 | Extrahovat `data.js` do `sectors/automotive/data.js` |
| 2 | Vytvořit `config.json` se seznamem metrik, prahů, zdrojů |
| 3 | Upravit `app.js` — dynamické načítání dat dle vybraného sektoru |
| 4 | Sidebar selector → skutečné přepínání sektorů |

---

## 10. Uživatelské role a přístupy

| Role | Potřeby | Přístup | Štítek |
|------|---------|---------|--------|
| **Sektorový analytik** | Plný přístup, editace scénářů, správa dat | Vše + admin | 🔧 Build (UI), 🔍 Discovery (autorizace) |
| **Management** | Executive dashboard, traffic lights, PDF | Dashboard + export | 🚀 Quick win (view-only) |
| **Relationship manager** | Banking implications, příležitosti, alerty | Banking + News + Dashboard | 🔍 Discovery (co přesně potřebují?) |
| **Risk manager** | Supply chain rizika, NPL scénáře, stress testy | Supply Chain + Banking | 🔍 Discovery (propojení s risk modely) |
| **Ekonomický výzkum** | Makro data, cross-sector srovnání | Data Explorer + cross-sector | 🔍 Discovery (overlap s existujícími nástroji?) |

**Discovery otázky:**
- Kolik uživatelů reálně bude platformu používat?
- Jaké jsou existující nástroje pro jednotlivé role? Duplikace?
- Je potřeba autentizace v první fázi, nebo stačí interní URL?
- Integrace s AD/SSO České spořitelny?

---

## 11. AI-powered funkce

### 11.1 Automatické komentáře

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| Claude API integrace | 🔧 Build | API klíč, prompt design |
| Prompt engineering pro sektorové komentáře | 🔍 Discovery | Testování kvality, iterace na promptech |
| Komentář ke každé metrice (trend, kontext, implikace) | 🔧 Build | Template-based prompting |
| Human-in-the-loop review UI | 🔧 Build | Approve/edit/reject workflow |
| Few-shot learning z předchozích reportů | 🔍 Discovery | Dostatek historických reportů? Formát? |
| Cost management | 🔍 Discovery | Kolik stojí 1 run? Budget? |
| Fallback pro offline/bez API | 🚀 Quick win | Zobrazit "komentář není k dispozici" |

### 11.2 Detekce anomálií

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| z-score detekce | 🔧 Build | Standardní statistika, scipy |
| Sezónní adjustace (STL decomposition) | 🔧 Build | statsmodels |
| Kontextuální AI vysvětlení | 🔍 Discovery | Claude: "Proč produkce klesla?" — kvalita? |
| False positive rate tuning | 🔍 Discovery | Kolik alertů je OK? Alert fatigue? |
| Prioritizace dle dopadu na portfolio | 🔍 Discovery | Váhy metrik, interní data |

### 11.3 Automatický monitoring zpráv

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| NewsAPI / mediastack integrace | 🚀 Quick win | Free tier, jednoduché API |
| Klíčová slova per sektor | 🚀 Quick win | Config soubor |
| AI klasifikace (typ + dopad) | 🔍 Discovery | Kvalita klasifikace, český vs. anglický obsah |
| Automatické propojení se scénáři | 🔍 Discovery | Matching logika: zpráva → relevantní scénář |
| Sentiment scoring | 🔍 Discovery | NLP nad českými texty — kvalita? |
| Deduplikace zpráv | 🔧 Build | Similarity hashing |
| RSS feed monitoring | 🚀 Quick win | MPO, CzechInvest, AutoSAP, ČNB blogy |

### 11.4 Q&A nad daty

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| Chat interface na webu | 🔧 Build | Chatbox komponent |
| RAG nad data.js + historickými reporty | 🔍 Discovery | Embedding modely, vector store, hosting |
| Přirozené dotazy → SQL/filtry | 🔍 Discovery | Text-to-query, přesnost |
| Konverzační paměť | 🔧 Build | Session-based context |
| Guardrails (odpovídá jen na sektorové dotazy) | 🔍 Discovery | Prompt engineering, safety |

### 11.5 Automatické generování scénářů

| Prvek | Štítek | Poznámka |
|-------|--------|----------|
| AI navrhne nové scénáře na základě trendů | 🔍 Discovery | Kvalita, kreativita vs. relevance |
| Automatické přehodnocení pravděpodobností | 🔍 Discovery | Na základě čeho? Signpostů? |
| What-if modelování | 🔍 Discovery | "Co když cena lithia vzroste o 50 %?" |

---

## 12. Banking-specifické funkce

| Prvek | Popis | Štítek | Poznámka |
|-------|-------|--------|----------|
| Portfolio exposure dashboard | Expozice ČS vůči automotive dle NACE | ✅ Hotovo (demo data) | Reálná data = 🔍 Discovery |
| NPL monitoring | Vývoj NPL ratio automotive | ✅ Hotovo (demo data) | Reálná data = 🔍 Discovery |
| Stress test scénáře | Dopad scénářů na NPL, LGD, PD | 🔍 Discovery | Propojení s interními risk modely |
| Early warning signals | Predikce zhoršení kvality portfolia | 🔍 Discovery | ML modely, interní data |
| Obchodní příležitosti | Identifikace potenciálních klientů | ✅ Hotovo (statické) | Dynamické = 🔍 Discovery |
| Competitor benchmarking | Srovnání expozice ČS vs. KB, ČSOB | 🔍 Discovery | Veřejné výroční zprávy, ČNB data |
| Regulatorní dopady | DORA, CRR III, ESG disclosure | 🔧 Build | Monitoring regulace |
| Green finance příležitosti | EV financování, ESG úvěry, zelené dluhopisy | 🔍 Discovery | Interní produkty ČS, trh |
| Klientský profil × sektorový výhled | Propojení sektorového ratingu s klientským | 🔍 Discovery | CRM data, schválení |

---

## 13. Rizika implementace

| Riziko | Pravděp. | Dopad | Mitigace | Štítek |
|--------|----------|-------|----------|--------|
| API změny u ČSÚ/Eurostatu | Střední | Vysoký | Verzování API calls, fallback na CSV, monitoring | 🔧 Build |
| Kvalita dat (chybějící, revize) | Vysoká | Střední | Validační pipeline, historické srovnání, alerty | 🔧 Build |
| AI halucinace v komentářích | Střední | Vysoký | Human-in-the-loop, fact-checking, few-shot | 🔍 Discovery |
| Kapacita týmu pro údržbu | Vysoká | Vysoký | Max automatizace, dokumentace, jednoduchost | 🔧 Build |
| Bezpečnost (interní data) | Nízká | Kritický | Separace: GH Pages (veřejná) vs. interní server | 🔍 Discovery |
| Adopce uživateli | Střední | Vysoký | Zapojení od začátku, iterace, user testing | 🔍 Discovery |
| Licenční náklady (Bloomberg, S&P) | Střední | Střední | Začít s free zdroji, licenci řešit až po PoC | 🔍 Discovery |
| GDPR / data governance | Nízká | Vysoký | Žádná PII v první fázi, interní data až po schválení | 🔍 Discovery |
| Vendor lock-in (Claude API) | Nízká | Střední | Abstrakce AI vrstvy, fallback na jiné LLM | 🔧 Build |
| Scope creep | Vysoká | Střední | Jasné fáze, MVP přístup, říkat "ne" | Průběžně |

---

## 14. Roadmap a prioritizace

### Fáze 0: Quick wins (dny) 🚀
🎯 **Cíl:** Okamžité vylepšení stávajícího prototypu

- [ ] YoY toggle v grafech
- [ ] Drill-down v grafech (onClick handler)
- [ ] Fullscreen mód pro grafy
- [ ] Print-friendly CSS
- [ ] Sparkline u Health Score
- [ ] Komentář analytika u metrik (textové pole v data.js)
- [ ] URL hash routing (bookmarkable stránky)
- [ ] RSS feed monitoring (AutoSAP, MPO, CzechInvest)
- [ ] Dark/light mode toggle

### Fáze 1: Data Pipeline (4–6 týdnů) 🔧
🎯 **Cíl:** Web zobrazuje reálná data místo demo dat

- [ ] Python skripty pro ČSÚ API (produkce, registrace, zaměstnanost)
- [ ] Python skripty pro Eurostat API (EU data, EV registrace)
- [ ] ECB/ČNB kurzy a sazby
- [ ] Transformační logika → generování data.js
- [ ] Validační pipeline (completeness, outliers, freshness)
- [ ] GitHub Actions workflow — měsíční automatická aktualizace
- [ ] Error handling a notifikace při selhání pipeline
- [ ] Historická data archivace (pro srovnání)

### Fáze 2: Export + alerty (3–4 týdny) 🔧
🎯 **Cíl:** Automatické reporty a notifikace

- [ ] PDF export z dashboardu (jsPDF nebo WeasyPrint)
- [ ] PPTX generátor (python-pptx)
- [ ] Excel export dat z grafů
- [ ] Email notifikace při traffic light změnách
- [ ] Slack webhook notifikace
- [ ] Anomálie detection (z-score + sezónní adjustace)
- [ ] Scheduled delivery (měsíční automatický report)

### Fáze 3: News + foresighting revize (2–3 týdny) 🔧
🎯 **Cíl:** Automatický monitoring a živý foresighting

- [ ] NewsAPI integrace + klíčová slova
- [ ] Deduplikace a ukládání zpráv
- [ ] Signpost tracking dashboard
- [ ] Historické srovnání (timeline, krizové periody)
- [ ] Trend radar drill-down (detail per trend)

### Fáze 4: AI funkce (4–6 týdnů) 🔍 → 🔧
🎯 **Cíl:** AI-powered komentáře a klasifikace

**Discovery (1–2 týdny):**
- [ ] Testování Claude API pro sektorové komentáře — kvalita, cost
- [ ] Testování AI klasifikace zpráv — přesnost, false positives
- [ ] Prompt engineering iterace
- [ ] Definice human-in-the-loop workflow

**Build (2–4 týdny po discovery):**
- [ ] Claude API integrace do pipeline
- [ ] AI komentáře ke každé metrice
- [ ] AI klasifikace zpráv (typ, dopad)
- [ ] Review UI (approve/edit/reject)

### Fáze 5: Multi-sector (4–6 týdnů per sektor) 🔧
🎯 **Cíl:** Rozšíření na další sektory

- [ ] Refaktoring na sektorově agnostický data model
- [ ] config.json per sektor (metriky, zdroje, prahy)
- [ ] Energetika — metriky, zdroje, scénáře, supply chain
- [ ] Stavebnictví — metriky, zdroje, scénáře
- [ ] Cross-sector srovnávací dashboard

### Fáze 6: Produkční nasazení (6–8 týdnů) 🔍 → 🔧
🎯 **Cíl:** Interní server s autentizací a bankovními daty

**Discovery (2–3 týdny):**
- [ ] Interní infrastruktura ČS — co je k dispozici?
- [ ] Security review a schválení
- [ ] GDPR posouzení pro interní data
- [ ] Integrace s AD/SSO
- [ ] Dostupnost interních dat (portfolio, NPL, CRM)

**Build (4–6 týdnů po discovery):**
- [ ] Migrace na interní server
- [ ] Autentizace a role-based přístup
- [ ] Integrace s interními bankovními daty
- [ ] Supply chain propojení s klientskými daty
- [ ] Q&A chat interface

### Fáze 7: Advanced analytics (průběžně) 🔍
🎯 **Cíl:** Pokročilé analytické funkce

- [ ] ML predikční modely (Prophet, XGBoost)
- [ ] Stress testing propojení s risk modely
- [ ] Early warning signals
- [ ] Monte Carlo simulace scénářů
- [ ] What-if modelování
- [ ] Sentiment analýza českých médií

---

## 15. Metriky úspěchu

| Metrika | Baseline (teď) | Fáze 1 | Fáze 3 | Fáze 6 |
|---------|----------------|--------|--------|--------|
| Čas přípravy reportu | 15–22 hod | 5–8 hod | 3–4 hod | 2–2.5 hod |
| Frekvence aktualizace dat | Čtvrtletně | Měsíčně (auto) | Měsíčně (auto) | Týdně (auto) |
| Počet sledovaných metrik | ~10 (manuálně) | 20+ (auto) | 30+ (auto) | 50+ (auto) |
| Pokrytí sektorů | 1 (automotive) | 1 | 1 | 3–5 |
| Aktivní uživatelé | 0 | 3–5 (analytici) | 5–10 | 20+ |
| Čas od události po alert | Dny | Hodiny | Hodiny | Minuty |
| Podíl automatizovaného obsahu | 0 % | 60 % (data) | 75 % (+ news) | 90 % (+ AI) |
| Uživatelská spokojenost (NPS) | N/A | Měřit | > 30 | > 50 |

---

## 16. Discovery backlog

Položky, které vyžadují průzkum/ověření před rozhodnutím o implementaci:

### Vysoká priorita (ověřit v Fázi 1–2)
| # | Otázka | Koho se zeptat | Deadline |
|---|--------|----------------|----------|
| D1 | Má ČS přístup k Bloomberg/Reuters API? | Treasury / IT | Před Fází 4 |
| D2 | Existuje brand book / PPTX šablona ČS? | Marketing / PR | Před Fází 2 |
| D3 | Kdo bude reálně platformu používat? Počet uživatelů? | Management sekt. analýzy | ASAP |
| D4 | Jaké existující nástroje tým používá? Překryv? | Analytický tým | ASAP |
| D5 | Budget pro AI API (Claude/OpenAI) a datové licence? | Management | Před Fází 4 |

### Střední priorita (ověřit v Fázi 3–4)
| # | Otázka | Koho se zeptat | Deadline |
|---|--------|----------------|----------|
| D6 | ACEA — povolují scraping? Alternativní zdroj? | Legal / ACEA | Před Fází 1 |
| D7 | Interní infrastruktura — co je k dispozici pro hosting? | IT oddělení | Před Fází 6 |
| D8 | GDPR posouzení pro propojení s klientskými daty | Legal / DPO | Před Fází 6 |
| D9 | AD/SSO integrace — technické možnosti? | IT Security | Před Fází 6 |
| D10 | Má ČS Teams nebo Slack? Webhook přístup? | IT / komunikace | Před Fází 2 |

### Nižší priorita (ověřit v Fázi 5+)
| # | Otázka | Koho se zeptat | Deadline |
|---|--------|----------------|----------|
| D11 | Propojení s risk modely (PD, LGD, stress testy) | Risk oddělení | Před Fází 7 |
| D12 | CRM data pro klientský profil × sektor | CRM tým | Před Fází 6 |
| D13 | Cross-sector: jaké sektory prioritizovat? | Management | Před Fází 5 |
| D14 | Expert panel pro validaci scénářů — kdo? Budget? | Management | Před Fází 4 |
| D15 | NLP pro české texty — kvalita, dostupné modely? | AI/ML tým (pokud existuje) | Před Fází 7 |

---

## 17. Poznámky k implementaci

### Co funguje dobře (lessons learned z prototypu):
- **Statický web bez build stepu** — rychlý vývoj, snadný deploy na GitHub Pages
- **Chart.js** — dostatečně flexibilní pro všechny typy grafů
- **Tailwind CSS via CDN** — rychlé styling bez toolchainu
- **Oddělení dat (data.js) od logiky (app.js) od layoutu (index.html)** — čistá architektura pro automatickou aktualizaci dat bez zásahu do kódu

### Principy pro další vývoj:
- **MVP first** — každá fáze dodá fungující produkt, ne prototyp
- **Automate everything** — pokud to lze automatizovat, automatizovat
- **Human-in-the-loop pro AI** — nikdy nepublikovat AI výstup bez lidské revize
- **Start with free data** — placené licence až po prokázání hodnoty
- **Measure adoption** — sledovat, zda to někdo používá, než přidáme další funkce
- **Keep it simple** — odolat scope creep, říkat "ne" nice-to-have
