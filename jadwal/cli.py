"""CLI entry point for jadwal."""

from __future__ import annotations

import argparse
import sys
from typing import NoReturn

from jadwal.display import (
    console,
    display_explain,
    display_export,
    display_json,
    display_sample,
)


# ── Subcommand handlers ──────────────────────────────────────────


def _cmd_generate(args: argparse.Namespace) -> int:
    """Generate synthetic data."""
    from jadwal.generator import GeneratorConfig, generate_dataset, to_jsonl, to_csv, to_json

    region = args.region if args.region != "mixed" else None
    config = GeneratorConfig(
        count=args.count,
        region=region,
        seed=args.seed,
        fields=_parse_fields(args.fields),
    )
    rows = generate_dataset(config)

    if args.output:
        fmt = args.format
        if fmt == "csv":
            to_csv(rows, args.output)
        elif fmt == "json":
            to_json(rows, args.output)
        else:
            to_jsonl(rows, args.output)
        display_export(len(rows), fmt, args.output)
    elif args.json:
        display_json(rows)
    else:
        display_sample(rows[:10])

    return 0


def _cmd_sample(args: argparse.Namespace) -> int:
    """Show 5 sample rows."""
    from jadwal.generator import GeneratorConfig, generate_dataset

    region = args.region if args.region != "mixed" else None
    config = GeneratorConfig(
        count=5,
        region=region,
        seed=args.seed,
        fields=_parse_fields(args.fields),
    )
    rows = generate_dataset(config)
    display_sample(rows)
    return 0


def _cmd_fields(_args: argparse.Namespace) -> int:
    """List all available fields."""
    from jadwal.generator import AVAILABLE_FIELDS
    from rich.table import Table

    table = Table(show_header=True, header_style="bold cyan", border_style="dim", padding=(0, 1))
    table.add_column("Field", style="bold white")
    table.add_column("Example", style="dim")

    # Show a sample for each field
    from jadwal.generator import generate_row
    sample = generate_row(AVAILABLE_FIELDS, "gulf")
    for f in AVAILABLE_FIELDS:
        table.add_row(f, str(sample.get(f, "")))

    console.print()
    console.print("[bold magenta]jadwal[/bold magenta] [dim]- Available Fields[/dim]")
    console.print()
    console.print(table)
    console.print()
    return 0


def _cmd_regions(_args: argparse.Namespace) -> int:
    """Show all supported regions."""
    from jadwal.generator import generate_row, AVAILABLE_FIELDS
    from jadwal.data import REGIONS
    from rich.table import Table

    console.print()
    console.print("[bold magenta]jadwal[/bold magenta] [dim]- Supported Regions[/dim]")
    console.print()

    for region in REGIONS:
        console.print(f"  [bold cyan]{region.upper()}[/bold cyan]")
        sample = generate_row(["full_name", "phone", "city", "email"], region)
        for k, v in sample.items():
            console.print(f"    {k}: {v}")
        console.print()

    return 0


def _cmd_explain(_args: argparse.Namespace) -> int:
    """Explain the tool."""
    display_explain()
    return 0


# ── Helpers ──────────────────────────────────────────────────────


def _parse_fields(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    parts = [f.strip() for f in raw.split(",") if f.strip()]
    return parts or None


# ── Argument parser ──────────────────────────────────────────────


def _common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--region", choices=["gulf", "egypt", "levant", "maghreb", "mixed"], default="mixed")
    parser.add_argument("--fields", default=None, help="Comma-separated fields")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jadwal", description="Generate realistic Arabic synthetic data.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {_get_version()}")

    sub = parser.add_subparsers(dest="command")

    gen_p = sub.add_parser("generate", help="Generate synthetic data (default)")
    gen_p.add_argument("--count", type=int, default=10, help="Number of rows")
    gen_p.add_argument("--output", default=None, help="Output file path")
    gen_p.add_argument("--format", choices=["jsonl", "csv", "json"], default="jsonl")
    gen_p.add_argument("--json", action="store_true")
    _common_args(gen_p)

    sam_p = sub.add_parser("sample", help="Show 5 sample rows")
    _common_args(sam_p)

    sub.add_parser("fields", help="List all available fields")
    sub.add_parser("regions", help="Show supported regions with examples")
    sub.add_parser("explain", help="Explain what jadwal does")

    return parser


def _get_version() -> str:
    from jadwal import __version__
    return __version__


# ── Entry point ──────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> NoReturn:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        args = parser.parse_args(["generate", *(argv or sys.argv[1:])])

    dispatch = {
        "generate": _cmd_generate,
        "sample": _cmd_sample,
        "fields": _cmd_fields,
        "regions": _cmd_regions,
        "explain": _cmd_explain,
    }

    try:
        code = dispatch[args.command](args)
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/dim]")
        code = 130
    except BrokenPipeError:
        code = 0

    sys.exit(code)
