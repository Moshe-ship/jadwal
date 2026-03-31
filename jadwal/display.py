"""Rich terminal display for jadwal output."""

from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table

console = Console()

BRANDING = "[bold magenta]jadwal[/bold magenta] [dim]- Arabic Synthetic Data Generator[/dim]"


# ---------------------------------------------------------------------------
# Sample table
# ---------------------------------------------------------------------------


def display_sample(rows: list[dict[str, str]], console: Console = console) -> None:
    """Show generated sample rows in a Rich table with RTL alignment for Arabic columns."""
    if not rows:
        console.print("[dim]No rows to display.[/dim]")
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        padding=(0, 1),
    )

    headers = list(rows[0].keys())
    for header in headers:
        table.add_column(header, style="white")

    for row in rows:
        table.add_row(*[str(row.get(h, "")) for h in headers])

    console.print()
    console.print(BRANDING)
    console.print()
    console.print(table)
    console.print()


# ---------------------------------------------------------------------------
# Fields listing
# ---------------------------------------------------------------------------


def display_fields(
    fields: dict[str, str],
    console: Console = console,
) -> None:
    """Show all available fields with descriptions."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        padding=(0, 1),
    )

    table.add_column("Field", style="bold white", min_width=20)
    table.add_column("Description", style="dim white")

    for name, description in fields.items():
        table.add_row(name, description)

    console.print()
    console.print(BRANDING)
    console.print()
    console.print(table)
    console.print()


# ---------------------------------------------------------------------------
# Regions listing
# ---------------------------------------------------------------------------


def display_regions(
    regions: dict[str, dict[str, str]],
    console: Console = console,
) -> None:
    """Show all supported regions with example data."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        padding=(0, 1),
    )

    table.add_column("Region", style="bold white", min_width=12)
    table.add_column("Example Name", style="white", min_width=20)
    table.add_column("Example City", style="white", min_width=16)
    table.add_column("Phone Format", style="dim white", min_width=16)

    for region, examples in regions.items():
        table.add_row(
            region,
            examples.get("name", ""),
            examples.get("city", ""),
            examples.get("phone", ""),
        )

    console.print()
    console.print(BRANDING)
    console.print()
    console.print(table)
    console.print()


# ---------------------------------------------------------------------------
# Export confirmation
# ---------------------------------------------------------------------------


def display_export(
    count: int,
    fmt: str,
    path: str,
    console: Console = console,
) -> None:
    """Print export confirmation message."""
    console.print()
    console.print(
        f"[green]Generated {count} rows[/green] [dim]\u2192[/dim] "
        f"[bold]{path}[/bold] [dim]({fmt})[/dim]"
    )
    console.print()


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------


def display_json(data: list[dict[str, str]], console: Console = console) -> None:
    """Print data as formatted JSON to the terminal."""
    console.print(json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Explain
# ---------------------------------------------------------------------------


def display_explain(console: Console = console) -> None:
    """Explain what jadwal does, data sources, regions, and field types."""
    console.print()
    console.print(BRANDING)
    console.print()

    console.print("[bold]What is jadwal?[/bold]")
    console.print()
    console.print(
        "  jadwal (\u062c\u062f\u0648\u0644) generates realistic Arabic synthetic data for testing,\n"
        "  prototyping, and development. It produces culturally accurate names,\n"
        "  addresses, phone numbers, and other fields across multiple Arabic\n"
        "  dialect regions \u2014 all offline, no API calls needed.\n"
    )

    console.print("[bold]Supported regions:[/bold]")
    console.print()
    console.print("  [cyan]gulf[/cyan]      Saudi Arabia, UAE, Kuwait, Qatar, Bahrain, Oman")
    console.print("  [cyan]egypt[/cyan]     Egypt")
    console.print("  [cyan]levant[/cyan]    Syria, Lebanon, Jordan, Palestine")
    console.print("  [cyan]maghreb[/cyan]   Morocco, Algeria, Tunisia, Libya")
    console.print("  [cyan]mixed[/cyan]     Random mix from all regions")
    console.print()

    console.print("[bold]Field types:[/bold]")
    console.print()
    console.print("  Names, emails, phone numbers, addresses, cities, national IDs,")
    console.print("  dates, companies, job titles, and more \u2014 all region-appropriate.")
    console.print()

    console.print("[bold]Data sources:[/bold]")
    console.print()
    console.print("  All data is generated from curated name lists, regional phone")
    console.print("  formats, and address patterns. No real personal data is used.")
    console.print()

    console.print("[bold]Usage examples:[/bold]")
    console.print()
    console.print("  [bold cyan]jadwal generate[/bold cyan]                       Generate 10 rows (all fields, mixed regions)")
    console.print("  [bold cyan]jadwal generate --count 100 --region gulf[/bold cyan]  100 Gulf-region rows")
    console.print("  [bold cyan]jadwal generate --format csv -o data.csv[/bold cyan]  Export as CSV")
    console.print("  [bold cyan]jadwal sample --region egypt[/bold cyan]            Preview 5 Egyptian rows")
    console.print("  [bold cyan]jadwal fields[/bold cyan]                          List all available fields")
    console.print("  [bold cyan]jadwal regions[/bold cyan]                         Show region examples")
    console.print()
