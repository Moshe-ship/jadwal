# jadwal (جدول) — Arabic Synthetic Data Generator

> Generate culturally accurate Arabic test data. Names, addresses, phones, IDs — all region-specific.

---

## Why

Every Arabic app needs test data. Random generators give you "John Smith" — jadwal gives you "محمد بن عبدالله القحطاني" with a real Saudi phone number and Riyadh address.

Region-specific: Gulf, Egypt, Levant, Maghreb. Real patterns. Real formats. No APIs. No internet.

## Install

```bash
pip install jadwal
```

## Quick Start

```bash
# Generate 100 records for Gulf region
jadwal generate --count 100 --region gulf --output data.jsonl

# Preview a single sample from Egypt
jadwal sample --region egypt

# List all available fields
jadwal fields
```

## Commands

| Command | Description |
|---------|-------------|
| `generate` | Generate synthetic records to file. Supports `--count`, `--region`, `--output`, `--format`. |
| `sample` | Preview a single record in the terminal. Quick way to see what data looks like. |
| `fields` | List all available fields with descriptions and examples. |
| `regions` | Show supported regions with countries, phone formats, and ID patterns. |
| `explain` | Learn how jadwal generates data — patterns, sources, methodology. |

## Available Fields

26 fields, all region-aware:

| Field | Example (Gulf) |
|-------|---------------|
| `full_name` | محمد بن عبدالله القحطاني |
| `first_name` | محمد |
| `family_name` | القحطاني |
| `email` | m.alqahtani@gmail.com |
| `phone` | +966 55 123 4567 |
| `national_id` | 1087654321 |
| `city` | الرياض |
| `address` | حي النرجس، شارع الأمير سلطان، الرياض |
| `company` | شركة النور للتقنية |
| `job_title` | مهندس برمجيات |
| `date_hijri` | 1446/03/15 |
| `date_gregorian` | 2025-03-15 |
| `paragraph` | فقرة كاملة بالعربية |
| `sentence` | جملة واحدة بالعربية |
| `age` | 32 |
| `gender` | ذكر |

## Regions

| Region | Countries | Phone Format | ID Pattern |
|--------|-----------|-------------|------------|
| **Gulf** | SA, UAE, QA, BH, KW, OM | +966 5x xxx xxxx | 10-digit national ID |
| **Egypt** | EG | +20 1x xxxx xxxx | 14-digit national ID |
| **Levant** | JO, LB, SY, PS | +962 7x xxx xxxx | Country-specific |
| **Maghreb** | MA, TN, DZ, LY | +212 6xx xxxxxx | Country-specific |

## Output Formats

- **JSONL** (default) — one JSON object per line, streaming-friendly
- **CSV** — standard CSV with headers
- **JSON** — single JSON array

```bash
jadwal generate --count 50 --region egypt --format csv --output egypt.csv
jadwal generate --count 50 --region gulf --format json --output gulf.json
```

## Fully Offline

No API calls. No internet required. All data patterns are built-in. Runs anywhere Python runs.

---

<p align="center" dir="rtl">
مقدمة من <a href="https://x.com/i/communities/2032184341682643429">مجتمع الذكاء الاصطناعي السعودي</a> للعرب أولا وللعالم أجمع
</p>

<p align="center">
Brought to you by the <a href="https://x.com/i/communities/2032184341682643429">Saudi AI Community</a> — for Arabs first, and the world at large.
</p>

## License

MIT — [Musa the Carpenter](https://github.com/Moshe-ship)

---

<p align="center">
<sub>
<a href="https://github.com/Moshe-ship/artok">artok</a> ·
<a href="https://github.com/Moshe-ship/bidi-guard">bidi-guard</a> ·
<a href="https://github.com/Moshe-ship/arabench">arabench</a> ·
<a href="https://github.com/Moshe-ship/majal">majal</a> ·
<a href="https://github.com/Moshe-ship/khalas">khalas</a> ·
<a href="https://github.com/Moshe-ship/safha">safha</a> ·
<a href="https://github.com/Moshe-ship/raqeeb">raqeeb</a> ·
<a href="https://github.com/Moshe-ship/sarih">sarih</a> ·
<a href="https://github.com/Moshe-ship/qalam">qalam</a> ·
<a href="https://github.com/Moshe-ship/naql">naql</a> ·
<a href="https://github.com/Moshe-ship/samt">samt</a> ·
<b>jadwal</b>
</sub>
</p>
