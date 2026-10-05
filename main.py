"""Command-line interface for the duplicate remover.

Examples
--------
python main.py data/sample.csv
python main.py data/sample.csv -o data/clean.csv --subset email
python main.py data/sample.csv --subset name email --keep last --case-sensitive
python main.py data/sample.csv --report-duplicates data/dupes.csv
"""
import argparse
import sys

from dedup import (find_duplicates, load_data, remove_duplicates,
                   save_data, summarize)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Remove duplicate entries from CSV/Excel/JSON files.")
    p.add_argument("input", help="Input file (.csv, .xlsx, .json)")
    p.add_argument("-o", "--output", help="Output file (default: <input>_clean.<ext>)")
    p.add_argument("-s", "--subset", nargs="+",
                   help="Column(s) that define a duplicate (default: all columns)")
    p.add_argument("-k", "--keep", choices=["first", "last", "none"], default="first",
                   help="Which occurrence to keep; 'none' drops all duplicated rows")
    p.add_argument("--case-sensitive", action="store_true",
                   help="Treat 'John' and 'john' as different (default: ignore case)")
    p.add_argument("--no-strip", action="store_true",
                   help="Do not trim whitespace before comparing")
    p.add_argument("--report-duplicates", metavar="FILE",
                   help="Also save every duplicated row to FILE for review")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    keep = False if args.keep == "none" else args.keep
    opts = dict(subset=args.subset, case_insensitive=not args.case_sensitive,
                strip_whitespace=not args.no_strip)

    try:
        df = load_data(args.input)
        if args.report_duplicates:
            dupes = find_duplicates(df, keep=keep, **opts)
            save_data(dupes, args.report_duplicates)
            print(f"Duplicate report saved to {args.report_duplicates} ({len(dupes)} rows)")
        clean = remove_duplicates(df, keep=keep, **opts)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    out = args.output
    if not out:
        stem, dot, ext = args.input.rpartition(".")
        out = f"{stem}_clean.{ext}" if dot else f"{args.input}_clean"
    save_data(clean, out)

    s = summarize(df, clean)
    print(f"Rows before : {s['rows_before']}")
    print(f"Rows after  : {s['rows_after']}")
    print(f"Removed     : {s['duplicates_removed']} ({s['percent_removed']}%)")
    print(f"Saved to    : {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
