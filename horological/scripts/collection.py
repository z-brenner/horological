#!/usr/bin/env python3
"""collection: a local, append-only log of a user's watch collection.

Standard library only. Data stays in one JSON file on the user's machine.

File location, in order of precedence:
  1. --file PATH
  2. $HOROLOGICAL_HOME/collection.json
  3. ~/.horological/collection.json

Commands
  path      Print the file location.
  init      Create an empty collection file.
  profile   Show or set collector profile fields.
  add       Add a watch you own, want, or are considering.
  update    Change fields on a watch.
  acquire   Mark a wishlist watch as bought.
  dispose   Record a sale, trade, gift or loss.
  service   Record a service or repair.
  note      Add a dated note to a watch.
  wear      Record that a watch was worn on a date.
  rotation  Show owned watches by how recently and how often they were worn.
  list      List watches, optionally by status.
  show      Show one watch with its history.
  log       Show the event log.
  summary   Counts, styles, spend and a profile digest.
  export    Export as Markdown or JSON.
  import    Import a previously exported JSON file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 1
STATUSES = ["owned", "wishlist", "considering", "sold", "traded", "gifted", "lost"]
ACTIVE = {"owned"}
WANTED = {"wishlist", "considering"}
DISPOSED = {"sold", "traded", "gifted", "lost"}
PROFILE_KEYS = [
    "name", "experience", "interests", "styles", "budget", "wrist_mm",
    "goals", "dislikes", "preferred_sizes", "notes",
]
EXPERIENCE_LEVELS = ["curious", "beginner", "enthusiast", "collector", "expert", "watchmaker"]
WATCH_FIELDS = [
    "brand", "model", "reference", "caliber", "movement_type", "year", "size_mm",
    "style", "condition", "box_papers", "serial", "notes", "tags",
]


# ---------------------------------------------------------------- storage

def default_path() -> Path:
    home = os.environ.get("HOROLOGICAL_HOME")
    base = Path(home).expanduser() if home else Path.home() / ".horological"
    return base / "collection.json"


def empty_store() -> dict:
    return {"schema_version": SCHEMA_VERSION, "profile": {}, "watches": [], "events": []}


def load(path: Path) -> dict:
    if not path.exists():
        return empty_store()
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("profile", {})
    data.setdefault("watches", [])
    data.setdefault("events", [])
    return data


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def today() -> str:
    return dt.date.today().isoformat()


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "watch"


def new_id(data: dict, brand: str, model: str) -> str:
    base = slug(f"{brand} {model}")
    existing = {w["id"] for w in data["watches"]}
    if base not in existing:
        return base
    n = 2
    while f"{base}-{n}" in existing:
        n += 1
    return f"{base}-{n}"


def find(data: dict, key: str) -> dict:
    key_l = key.lower()
    exact = [w for w in data["watches"] if w["id"] == key_l]
    if exact:
        return exact[0]
    matches = [w for w in data["watches"] if key_l in w["id"]]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"no watch matches '{key}'. Use `list` to see ids.")
    ids = ", ".join(w["id"] for w in matches)
    raise SystemExit(f"'{key}' matches several watches: {ids}")


def log_event(data: dict, kind: str, watch_id: str | None, details: dict) -> None:
    data["events"].append({
        "at": now(), "type": kind, "watch_id": watch_id,
        "details": {k: v for k, v in details.items() if v not in (None, "", [])},
    })


def money(amount, currency) -> dict | None:
    if amount is None:
        return None
    return {"amount": amount, "currency": (currency or "USD").upper()}


def parse_list(value: str | None) -> list[str] | None:
    if value is None:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


# ---------------------------------------------------------------- commands

def cmd_path(args, data, path):
    print(path)
    return False


def cmd_init(args, data, path):
    if path.exists() and not args.force:
        print(f"Collection already exists at {path}")
        return False
    data.clear()
    data.update(empty_store())
    log_event(data, "init", None, {})
    print(f"Created {path}")
    return True


def cmd_profile(args, data, path):
    changed = False
    for pair in args.set or []:
        if "=" not in pair:
            raise SystemExit("profile --set expects key=value")
        key, value = pair.split("=", 1)
        key = key.strip()
        if key not in PROFILE_KEYS:
            raise SystemExit(f"unknown profile key '{key}'. Allowed: {', '.join(PROFILE_KEYS)}")
        if key == "experience" and value not in EXPERIENCE_LEVELS:
            raise SystemExit(f"experience must be one of: {', '.join(EXPERIENCE_LEVELS)}")
        if key in {"interests", "styles", "dislikes"}:
            value = parse_list(value)
        old = data["profile"].get(key)
        data["profile"][key] = value
        log_event(data, "profile", None, {"field": key, "from": old, "to": value})
        changed = True
    if changed:
        data["profile"]["updated"] = today()
    print(json.dumps(data["profile"], indent=2, ensure_ascii=False))
    return changed


def apply_fields(watch: dict, args) -> dict:
    changes = {}
    for field in WATCH_FIELDS:
        value = getattr(args, field, None)
        if value is None:
            continue
        if field == "tags":
            value = parse_list(value)
        if watch.get(field) != value:
            changes[field] = value
            watch[field] = value
    return changes


def cmd_add(args, data, path):
    status = args.status
    if status not in STATUSES:
        raise SystemExit(f"status must be one of: {', '.join(STATUSES)}")
    watch = {"id": new_id(data, args.brand, args.model), "status": status, "added": today()}
    apply_fields(watch, args)
    if status == "owned":
        watch["acquired"] = {
            "date": args.date or None, "price": money(args.price, args.currency),
            "source": args.source,
        }
    elif status in WANTED:
        watch["target_price"] = money(args.price, args.currency)
        watch["priority"] = args.priority
    data["watches"].append(watch)
    log_event(data, "add", watch["id"], {"status": status, "brand": args.brand, "model": args.model})
    print(f"Added {watch['id']} as {status}")
    return True


def cmd_update(args, data, path):
    watch = find(data, args.id)
    changes = apply_fields(watch, args)
    if args.status:
        if args.status not in STATUSES:
            raise SystemExit(f"status must be one of: {', '.join(STATUSES)}")
        changes["status"] = args.status
        watch["status"] = args.status
    if not changes:
        print("No changes.")
        return False
    log_event(data, "update", watch["id"], changes)
    print(f"Updated {watch['id']}: {', '.join(changes)}")
    return True


def cmd_acquire(args, data, path):
    watch = find(data, args.id)
    previous = watch["status"]
    watch["status"] = "owned"
    watch["acquired"] = {
        "date": args.date or today(), "price": money(args.price, args.currency),
        "source": args.source,
    }
    log_event(data, "acquire", watch["id"], {"from_status": previous, **watch["acquired"]})
    print(f"{watch['id']} is now owned")
    return True


def cmd_dispose(args, data, path):
    watch = find(data, args.id)
    if args.how not in DISPOSED:
        raise SystemExit(f"--how must be one of: {', '.join(sorted(DISPOSED))}")
    watch["status"] = args.how
    watch["disposed"] = {
        "date": args.date or today(), "price": money(args.price, args.currency),
        "to": args.to, "reason": args.reason,
    }
    log_event(data, args.how, watch["id"], watch["disposed"])
    print(f"{watch['id']} recorded as {args.how}")
    return True


def cmd_service(args, data, path):
    watch = find(data, args.id)
    record = {
        "date": args.date or today(), "by": args.by, "work": args.work,
        "cost": money(args.cost, args.currency),
    }
    watch.setdefault("services", []).append(record)
    watch["last_service"] = record["date"]
    log_event(data, "service", watch["id"], record)
    print(f"Service recorded for {watch['id']}")
    return True


def cmd_note(args, data, path):
    watch = find(data, args.id)
    watch.setdefault("journal", []).append({"date": today(), "text": args.text})
    log_event(data, "note", watch["id"], {"text": args.text})
    print(f"Note added to {watch['id']}")
    return True


def cmd_wear(args, data, path):
    watch = find(data, args.id)
    date = args.date or today()
    dt.date.fromisoformat(date)
    worn = watch.setdefault("worn", [])
    if date in worn:
        print(f"{watch['id']} already logged as worn on {date}")
        return False
    worn.append(date)
    worn.sort()
    log_event(data, "wear", watch["id"], {"date": date})
    print(f"Logged {watch['id']} worn on {date}")
    return True


def build_rotation(data: dict) -> list[dict]:
    rows = []
    for w in data["watches"]:
        if w["status"] not in ACTIVE:
            continue
        worn = w.get("worn", [])
        last = worn[-1] if worn else None
        days = (dt.date.today() - dt.date.fromisoformat(last)).days if last else None
        price = ((w.get("acquired") or {}).get("price") or {})
        cost_per_wear = round(price["amount"] / len(worn), 2) if price.get("amount") and worn else None
        rows.append({
            "id": w["id"], "watch": describe(w), "times_worn": len(worn),
            "last_worn": last, "days_since_worn": days, "cost_per_wear": cost_per_wear,
        })
    rows.sort(key=lambda r: (r["days_since_worn"] is not None, -(r["days_since_worn"] or 0)))
    return rows


def cmd_rotation(args, data, path):
    print(json.dumps(build_rotation(data), indent=2, ensure_ascii=False))
    return False


def describe(w: dict) -> str:
    bits = [w.get("brand", ""), w.get("model", "")]
    if w.get("reference"):
        bits.append(f"ref. {w['reference']}")
    if w.get("year"):
        bits.append(f"({w['year']})")
    return " ".join(b for b in bits if b)


def cmd_list(args, data, path):
    watches = data["watches"]
    if args.status:
        wanted = set(args.status.split(","))
        watches = [w for w in watches if w["status"] in wanted]
    if not watches:
        print("No watches recorded.")
        return False
    for w in watches:
        print(f"{w['id']:<32} {w['status']:<12} {describe(w)}")
    return False


def cmd_show(args, data, path):
    watch = find(data, args.id)
    out = dict(watch)
    if out.get("serial") and not args.reveal_serial:
        out["serial"] = "stored, hidden; use --reveal-serial"
    out["history"] = [e for e in data["events"] if e["watch_id"] == watch["id"]]
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return False


def cmd_log(args, data, path):
    events = data["events"][-args.limit:] if args.limit else data["events"]
    for e in events:
        detail = ", ".join(f"{k}={v}" for k, v in e["details"].items())
        print(f"{e['at']}  {e['type']:<8} {e.get('watch_id') or '':<28} {detail}")
    return False


def totals(watches: list[dict], key: str, sub: str) -> dict:
    sums: dict[str, float] = {}
    for w in watches:
        price = (w.get(key) or {}).get(sub)
        if price:
            sums[price["currency"]] = sums.get(price["currency"], 0) + price["amount"]
    return sums


def build_summary(data: dict) -> dict:
    ws = data["watches"]
    by_status = {s: sum(1 for w in ws if w["status"] == s) for s in STATUSES}
    owned = [w for w in ws if w["status"] in ACTIVE]
    styles: dict[str, int] = {}
    brands: dict[str, int] = {}
    movements: dict[str, int] = {}
    for w in owned:
        for bucket, field in ((styles, "style"), (brands, "brand"), (movements, "movement_type")):
            if w.get(field):
                bucket[w[field]] = bucket.get(w[field], 0) + 1
    overdue = []
    year_now = dt.date.today().year
    for w in owned:
        if (w.get("movement_type") or "").lower() in {"mechanical", "automatic", "manual", "hand-wound", "spring drive"}:
            last = w.get("last_service")
            if not last or year_now - int(last[:4]) >= 7:
                overdue.append(w["id"])
    return {
        "profile": data["profile"],
        "counts": {k: v for k, v in by_status.items() if v},
        "owned_by_brand": brands,
        "owned_by_style": styles,
        "owned_by_movement": movements,
        "spent_on_owned": totals(owned, "acquired", "price"),
        "received_from_disposals": totals([w for w in ws if w["status"] in DISPOSED], "disposed", "price"),
        "wishlist": [describe(w) for w in ws if w["status"] in WANTED],
        "service_check_suggested": overdue,
        "most_worn": [
            f"{r['watch']}: {r['times_worn']}" for r in
            sorted(build_rotation(data), key=lambda r: -r["times_worn"])[:3] if r["times_worn"]
        ],
    }


def cmd_summary(args, data, path):
    print(json.dumps(build_summary(data), indent=2, ensure_ascii=False))
    return False


def to_markdown(data: dict, include_serials: bool) -> str:
    s = build_summary(data)
    lines = ["# Watch Collection", "", f"Exported {today()}", ""]
    if data["profile"]:
        lines += ["## Collector profile", ""]
        for k, v in data["profile"].items():
            v = ", ".join(v) if isinstance(v, list) else v
            lines.append(f"- {k.replace('_', ' ').title()}: {v}")
        lines.append("")
    for title, statuses in (("Owned", ACTIVE), ("Wishlist and considering", WANTED),
                            ("Former watches", DISPOSED)):
        group = [w for w in data["watches"] if w["status"] in statuses]
        if not group:
            continue
        lines += [f"## {title}", "", "| Watch | Caliber | Status | Notes |", "|---|---|---|---|"]
        for w in group:
            notes = w.get("notes") or ""
            if include_serials and w.get("serial"):
                notes = f"{notes} Serial {w['serial']}".strip()
            lines.append(f"| {describe(w)} | {w.get('caliber') or ''} | {w['status']} | {notes} |")
        lines.append("")
    if s["service_check_suggested"]:
        lines += ["## Service check suggested", ""]
        lines += [f"- {i}" for i in s["service_check_suggested"]]
        lines.append("")
    return "\n".join(lines)


def cmd_export(args, data, path):
    if args.format == "json":
        out = json.loads(json.dumps(data))
        if not args.include_serials:
            for w in out["watches"]:
                w.pop("serial", None)
        text = json.dumps(out, indent=2, ensure_ascii=False)
    else:
        text = to_markdown(data, args.include_serials)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)
    return False


def cmd_import(args, data, path):
    incoming = json.loads(Path(args.source).read_text(encoding="utf-8"))
    if args.replace:
        data.clear()
        data.update(empty_store())
    data["profile"].update(incoming.get("profile", {}))
    existing = {w["id"] for w in data["watches"]}
    added = 0
    for w in incoming.get("watches", []):
        if w["id"] in existing:
            continue
        data["watches"].append(w)
        added += 1
    seen = {(e["at"], e["type"], e.get("watch_id")) for e in data["events"]}
    for e in incoming.get("events", []):
        if (e["at"], e["type"], e.get("watch_id")) not in seen:
            data["events"].append(e)
    data["events"].sort(key=lambda e: e["at"])
    log_event(data, "import", None, {"source": str(args.source), "watches_added": added})
    print(f"Imported {added} watches")
    return True


# ---------------------------------------------------------------- cli

def add_watch_fields(p, required: bool):
    p.add_argument("--brand", required=required)
    p.add_argument("--model", required=required)
    p.add_argument("--reference")
    p.add_argument("--caliber")
    p.add_argument("--movement-type", dest="movement_type",
                   help="automatic, manual, quartz, solar, spring drive, smart")
    p.add_argument("--year")
    p.add_argument("--size-mm", dest="size_mm", type=float)
    p.add_argument("--style", help="diver, dress, field, pilot, chronograph, GMT, sports, etc.")
    p.add_argument("--condition")
    p.add_argument("--box-papers", dest="box_papers", help="full set, watch only, box only, papers only")
    p.add_argument("--serial", help="optional; stored only in the local file")
    p.add_argument("--notes")
    p.add_argument("--tags", help="comma-separated")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="collection", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", help="path to collection.json")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("path").set_defaults(func=cmd_path)
    s = sub.add_parser("init")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("profile")
    s.add_argument("--set", action="append", metavar="KEY=VALUE")
    s.set_defaults(func=cmd_profile)

    s = sub.add_parser("add")
    add_watch_fields(s, required=True)
    s.add_argument("--status", default="owned")
    s.add_argument("--date")
    s.add_argument("--price", type=float, help="price paid, or target price for wishlist")
    s.add_argument("--currency", default="USD")
    s.add_argument("--source", help="where bought: AD, grey dealer, forum, auction, gift")
    s.add_argument("--priority", help="for wishlist: high, medium, low")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("update")
    s.add_argument("id")
    add_watch_fields(s, required=False)
    s.add_argument("--status")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("acquire")
    s.add_argument("id")
    s.add_argument("--date")
    s.add_argument("--price", type=float)
    s.add_argument("--currency", default="USD")
    s.add_argument("--source")
    s.set_defaults(func=cmd_acquire)

    s = sub.add_parser("dispose")
    s.add_argument("id")
    s.add_argument("--how", required=True, help="sold, traded, gifted, lost")
    s.add_argument("--date")
    s.add_argument("--price", type=float)
    s.add_argument("--currency", default="USD")
    s.add_argument("--to")
    s.add_argument("--reason")
    s.set_defaults(func=cmd_dispose)

    s = sub.add_parser("service")
    s.add_argument("id")
    s.add_argument("--date")
    s.add_argument("--by")
    s.add_argument("--work")
    s.add_argument("--cost", type=float)
    s.add_argument("--currency", default="USD")
    s.set_defaults(func=cmd_service)

    s = sub.add_parser("note")
    s.add_argument("id")
    s.add_argument("text")
    s.set_defaults(func=cmd_note)

    s = sub.add_parser("wear")
    s.add_argument("id")
    s.add_argument("--date", help="YYYY-MM-DD, default today")
    s.set_defaults(func=cmd_wear)

    sub.add_parser("rotation").set_defaults(func=cmd_rotation)

    s = sub.add_parser("list")
    s.add_argument("--status", help="comma-separated statuses")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("show")
    s.add_argument("id")
    s.add_argument("--reveal-serial", action="store_true")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("log")
    s.add_argument("--limit", type=int, default=0)
    s.set_defaults(func=cmd_log)

    sub.add_parser("summary").set_defaults(func=cmd_summary)

    s = sub.add_parser("export")
    s.add_argument("--format", choices=["md", "json"], default="md")
    s.add_argument("--out")
    s.add_argument("--include-serials", action="store_true")
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("import")
    s.add_argument("source")
    s.add_argument("--replace", action="store_true")
    s.set_defaults(func=cmd_import)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.file).expanduser() if args.file else default_path()
    data = load(path)
    if args.func(args, data, path):
        save(path, data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
