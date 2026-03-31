"""Arabic synthetic data generator."""
from __future__ import annotations

import csv
import json
import random
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .data import (
    ARABIC_SENTENCES,
    ARABIC_TO_LATIN,
    CITIES_EGYPT,
    CITIES_GULF,
    CITIES_LEVANT,
    CITIES_MAGHREB,
    COMPANY_CORES,
    COMPANY_PREFIXES,
    COMPANY_SUFFIXES,
    EG_GOVERNORATE_CODES,
    EMAIL_DOMAINS_GLOBAL,
    EMAIL_DOMAINS_LOCAL,
    FAMILY_NAMES_EGYPT,
    FAMILY_NAMES_GULF,
    FAMILY_NAMES_LEVANT,
    FAMILY_NAMES_MAGHREB,
    FEMALE_NAMES_EGYPT,
    FEMALE_NAMES_GULF,
    FEMALE_NAMES_LEVANT,
    FEMALE_NAMES_MAGHREB,
    GREGORIAN_MONTHS,
    HIJRI_MONTHS,
    JOB_TITLES,
    MALE_NAMES_EGYPT,
    MALE_NAMES_GULF,
    MALE_NAMES_LEVANT,
    MALE_NAMES_MAGHREB,
    NEIGHBORHOODS_EGYPT,
    NEIGHBORHOODS_GULF,
    NEIGHBORHOODS_LEVANT,
    NEIGHBORHOODS_MAGHREB,
    PHONE_FORMATS,
    REGION_COUNTRIES,
    REGIONS,
    STREETS_EGYPT,
    STREETS_GULF,
    STREETS_LEVANT,
    STREETS_MAGHREB,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class GeneratorConfig:
    """Configuration for a data generation run."""

    count: int = 100
    region: str | None = None  # None = mixed (random per row)
    seed: int | None = None
    fields: list[str] | None = None  # None = all fields


# ---------------------------------------------------------------------------
# Region-keyed data pools
# ---------------------------------------------------------------------------

_MALE_NAMES: dict[str, list[str]] = {
    "gulf": MALE_NAMES_GULF,
    "egypt": MALE_NAMES_EGYPT,
    "levant": MALE_NAMES_LEVANT,
    "maghreb": MALE_NAMES_MAGHREB,
}

_FEMALE_NAMES: dict[str, list[str]] = {
    "gulf": FEMALE_NAMES_GULF,
    "egypt": FEMALE_NAMES_EGYPT,
    "levant": FEMALE_NAMES_LEVANT,
    "maghreb": FEMALE_NAMES_MAGHREB,
}

_FAMILY_NAMES: dict[str, list[str]] = {
    "gulf": FAMILY_NAMES_GULF,
    "egypt": FAMILY_NAMES_EGYPT,
    "levant": FAMILY_NAMES_LEVANT,
    "maghreb": FAMILY_NAMES_MAGHREB,
}

_CITIES: dict[str, list[str]] = {
    "gulf": CITIES_GULF,
    "egypt": CITIES_EGYPT,
    "levant": CITIES_LEVANT,
    "maghreb": CITIES_MAGHREB,
}

_STREETS: dict[str, list[str]] = {
    "gulf": STREETS_GULF,
    "egypt": STREETS_EGYPT,
    "levant": STREETS_LEVANT,
    "maghreb": STREETS_MAGHREB,
}

_NEIGHBORHOODS: dict[str, list[str]] = {
    "gulf": NEIGHBORHOODS_GULF,
    "egypt": NEIGHBORHOODS_EGYPT,
    "levant": NEIGHBORHOODS_LEVANT,
    "maghreb": NEIGHBORHOODS_MAGHREB,
}


def _resolve_region(region: str | None) -> str:
    """Return a concrete region — pick randomly if *region* is ``None``."""
    if region is not None:
        return region
    return random.choice(REGIONS)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _rand_digits(n: int) -> str:
    """Return a string of *n* random decimal digits."""
    return "".join(random.choices(string.digits, k=n))


def _transliterate(arabic: str) -> str:
    """Transliterate an Arabic string to a simplified Latin form.

    Used for generating plausible email local parts.  This is intentionally
    rough — real transliteration is more nuanced, but this is good enough
    for synthetic data.
    """
    result: list[str] = []
    for ch in arabic:
        mapped = ARABIC_TO_LATIN.get(ch)
        if mapped is not None:
            result.append(mapped)
        elif ch == " ":
            result.append(".")
        # Skip characters without a mapping (diacritics, etc.).
    return "".join(result).strip(".")


# ---------------------------------------------------------------------------
# Field generators
# ---------------------------------------------------------------------------


def gen_first_name(region: str | None = None, gender: str | None = None) -> str:
    """Return a random first name for *region* and *gender*.

    *gender*: ``"male"`` / ``"ذكر"`` or ``"female"`` / ``"أنثى"``.
    When ``None``, chosen randomly.
    """
    region = _resolve_region(region)

    if gender is None:
        gender = random.choice(["male", "female"])

    is_male = gender in ("male", "ذكر")
    pool = _MALE_NAMES[region] if is_male else _FEMALE_NAMES[region]
    return random.choice(pool)


def gen_family_name(region: str | None = None) -> str:
    """Return a random family name for *region*."""
    region = _resolve_region(region)
    return random.choice(_FAMILY_NAMES[region])


def gen_full_name(region: str | None = None) -> str:
    """Return a full Arabic name: first + patronymic/middle + family.

    Gulf names may include 'بن' (son of) between components.
    """
    region = _resolve_region(region)
    gender = random.choice(["male", "female"])

    first = gen_first_name(region, gender)
    middle = gen_first_name(region, "male")  # Patronymic is always male.
    family = gen_family_name(region)

    if region == "gulf" and random.random() < 0.5:
        connector = "بن" if gender == "male" else "بنت"
        return f"{first} {connector} {middle} {family}"

    return f"{first} {middle} {family}"


def gen_email(region: str | None = None) -> str:
    """Return a plausible email address with transliterated Arabic name."""
    region = _resolve_region(region)
    gender = random.choice(["male", "female"])

    first = gen_first_name(region, gender)
    family = gen_family_name(region)

    local_first = _transliterate(first)
    local_family = _transliterate(family)

    # Strip the "al" prefix articles that may appear in family names.
    local_family = local_family.lstrip(".")

    separator = random.choice([".", "_", ""])
    local = f"{local_first}{separator}{local_family}"

    # Sometimes append digits.
    if random.random() < 0.3:
        local += _rand_digits(random.randint(1, 3))

    # Pick a domain — 70% global, 30% local.
    if random.random() < 0.7 or region not in EMAIL_DOMAINS_LOCAL:
        domain = random.choice(EMAIL_DOMAINS_GLOBAL)
    else:
        domain = random.choice(EMAIL_DOMAINS_LOCAL[region])

    return f"{local}@{domain}".lower()


def gen_phone(region: str | None = None) -> str:
    """Return a random phone number formatted for a country in *region*."""
    region = _resolve_region(region)
    country = random.choice(REGION_COUNTRIES[region])
    fmt = random.choice(PHONE_FORMATS[country])

    # Replace placeholders: {d1}=1 digit, {d2}=2 digits, etc.
    result = fmt
    for n in range(9, 0, -1):
        tag = f"{{d{n}}}"
        while tag in result:
            result = result.replace(tag, _rand_digits(n), 1)

    return result


def gen_national_id(region: str | None = None) -> str:
    """Return a synthetic national ID for a country in *region*.

    Currently supports Saudi, Egyptian, and Emirati formats.
    """
    region = _resolve_region(region)

    if region == "gulf":
        # Saudi ID format.
        prefix = random.choice(["1", "2"])
        return f"{prefix}{_rand_digits(9)}"

    if region == "egypt":
        century = random.choice(["2", "3"])  # 2=1900s, 3=2000s
        yy = f"{random.randint(0, 99):02d}"
        mm = f"{random.randint(1, 12):02d}"
        dd = f"{random.randint(1, 28):02d}"
        gov = random.choice(EG_GOVERNORATE_CODES)
        seq = _rand_digits(4)
        check = _rand_digits(1)
        return f"{century}{yy}{mm}{dd}{gov}{seq}{check}"

    if region == "levant":
        # Jordanian national number: 10 digits.
        return _rand_digits(10)

    # Maghreb — Moroccan CIN-style: 1-2 letters + 6 digits.
    letters = random.choice(["A", "B", "BE", "BH", "BJ", "BK", "D", "E"])
    return f"{letters}{_rand_digits(6)}"


def gen_city(region: str | None = None) -> str:
    """Return a random city name for *region*."""
    region = _resolve_region(region)
    return random.choice(_CITIES[region])


def gen_address(region: str | None = None) -> str:
    """Return a plausible Arabic street address for *region*."""
    region = _resolve_region(region)

    street = random.choice(_STREETS[region])
    neighborhood = random.choice(_NEIGHBORHOODS[region])
    city = random.choice(_CITIES[region])
    postal = _rand_digits(5)

    return f"{street}، {neighborhood}، {city} {postal}"


def gen_company(region: str | None = None) -> str:
    """Return a random Arabic company name."""
    _resolve_region(region)  # Validate but company names are pan-Arab.
    prefix = random.choice(COMPANY_PREFIXES)
    core = random.choice(COMPANY_CORES)
    suffix = random.choice(COMPANY_SUFFIXES)
    return f"{prefix} {core} {suffix}"


def gen_job_title() -> str:
    """Return a random Arabic job title."""
    return random.choice(JOB_TITLES)


def gen_date_hijri() -> str:
    """Return a random Hijri date string."""
    day = random.randint(1, 30)
    month = random.choice(HIJRI_MONTHS)
    year = random.randint(1440, 1450)
    return f"{day} {month} {year}"


def gen_date_gregorian() -> str:
    """Return a random Gregorian date string in Arabic."""
    day = random.randint(1, 28)
    month = random.choice(GREGORIAN_MONTHS)
    year = random.randint(2020, 2030)
    return f"{day} {month} {year}"


def gen_paragraph(region: str | None = None) -> str:
    """Return 2-3 Arabic sentences on a random topic."""
    _resolve_region(region)  # Validate.
    topic = random.choice(list(ARABIC_SENTENCES.keys()))
    sentences = random.sample(
        ARABIC_SENTENCES[topic],
        k=min(random.randint(2, 3), len(ARABIC_SENTENCES[topic])),
    )
    return " ".join(sentences)


def gen_sentence(region: str | None = None) -> str:
    """Return one random Arabic sentence."""
    _resolve_region(region)  # Validate.
    topic = random.choice(list(ARABIC_SENTENCES.keys()))
    return random.choice(ARABIC_SENTENCES[topic])


def gen_age() -> str:
    """Return a random age between 18 and 80 (as string for consistency)."""
    return str(random.randint(18, 80))


def gen_gender() -> str:
    """Return a random gender in Arabic."""
    return random.choice(["ذكر", "أنثى"])


# ---------------------------------------------------------------------------
# Field registry
# ---------------------------------------------------------------------------

# Each generator is called with (region,) except for field-specific ones.
# We normalise them all to accept ``(region)`` via lambdas where needed.

FIELD_GENERATORS: dict[str, Callable[[str], Any]] = {
    "full_name": gen_full_name,
    "first_name": gen_first_name,
    "family_name": gen_family_name,
    "email": gen_email,
    "phone": gen_phone,
    "national_id": gen_national_id,
    "city": gen_city,
    "address": gen_address,
    "company": gen_company,
    "job_title": lambda _r: gen_job_title(),
    "date_hijri": lambda _r: gen_date_hijri(),
    "date_gregorian": lambda _r: gen_date_gregorian(),
    "paragraph": gen_paragraph,
    "sentence": gen_sentence,
    "age": lambda _r: gen_age(),
    "gender": lambda _r: gen_gender(),
}

AVAILABLE_FIELDS: list[str] = sorted(FIELD_GENERATORS.keys())


# ---------------------------------------------------------------------------
# Row / dataset generation
# ---------------------------------------------------------------------------


def generate_row(
    fields: list[str] | None = None,
    region: str | None = None,
) -> dict[str, Any]:
    """Generate a single row of synthetic data.

    When *fields* is ``None`` all available fields are produced.
    When *region* is ``None`` a random region is chosen **per row** so that
    a mixed-region dataset is produced.
    """
    if fields is None:
        fields = AVAILABLE_FIELDS

    row_region = _resolve_region(region)
    row: dict[str, Any] = {}

    for name in fields:
        generator = FIELD_GENERATORS.get(name)
        if generator is None:
            raise ValueError(f"Unknown field: {name!r}. Choose from {AVAILABLE_FIELDS}")
        row[name] = generator(row_region)

    return row


def generate_dataset(config: GeneratorConfig) -> list[dict[str, Any]]:
    """Generate *config.count* rows of synthetic Arabic data."""
    if config.seed is not None:
        random.seed(config.seed)

    rows: list[dict[str, Any]] = []
    for _ in range(config.count):
        rows.append(generate_row(fields=config.fields, region=config.region))

    return rows


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------


def to_jsonl(data: list[dict[str, Any]], path: str | Path) -> None:
    """Write *data* as newline-delimited JSON (JSONL)."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as fh:
        for row in data:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def to_csv(data: list[dict[str, Any]], path: str | Path) -> None:
    """Write *data* as a UTF-8 CSV file with BOM for Excel compatibility."""
    if not data:
        Path(path).write_text("", encoding="utf-8")
        return

    path = Path(path)
    fieldnames = list(data[0].keys())

    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def to_json(data: list[dict[str, Any]], path: str | Path) -> None:
    """Write *data* as a JSON array."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
