#!/usr/bin/env python3
"""horocalc: deterministic calculations for horology questions.

Standard library only. Run `python3 horocalc.py <command> --help` for details.

Commands
  freq          Convert between vph, Hz, beats per second and oscillations.
  rate          Convert observed drift to seconds per day and check tolerances.
  moonphase     Drift of a moonphase display.
  reserve       Power reserve or winding estimates.
  beats         Total beats over a period.
  water         Convert water resistance units and explain the rating.
  magnet        Convert magnetic field units and compare with standards.
  seiko-serial  Decode a Seiko or Grand Seiko caseback serial.
  gold          Convert between karat and millesimal fineness.
  ligne         Convert between lignes and millimeters.
"""

from __future__ import annotations

import argparse
import json
import math
import sys

SYNODIC_MONTH_DAYS = 29.530588853
SECONDS_PER_DAY = 86_400
LIGNE_MM = 2.2558
GAUSS_PER_TESLA = 10_000
MU0 = 4 * math.pi * 1e-7  # vacuum permeability, T*m/A

RATE_STANDARDS = {
    "cosc": (-4.0, 6.0, "COSC chronometer, mean daily rate, uncased movement"),
    "metas": (0.0, 5.0, "METAS Master Chronometer, cased watch"),
    "rolex": (-2.0, 2.0, "Rolex Superlative Chronometer, cased watch"),
    "gs": (-3.0, 5.0, "Grand Seiko Special Standard mechanical, static"),
    "patek": (-3.0, 2.0, "Patek Philippe Seal, movements of 20 mm or more, as commonly stated"),
}

MAGNET_REFERENCES_GAUSS = [
    ("ISO 764 baseline, 4,800 A/m", 4_800 * MU0 * GAUSS_PER_TESLA),
    ("Rolex Milgauss rating", 1_000.0),
    ("Omega Master Chronometer", 15_000.0),
]

SEIKO_MONTHS = {
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "O": 10, "0": 10, "N": 11, "D": 12,
}
MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]


def emit(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2))
        return
    for key, value in result.items():
        if isinstance(value, float):
            value = f"{value:,.4f}".rstrip("0").rstrip(".")
        elif isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
            continue
        print(f"{key}: {value}")


# ---------------------------------------------------------------- freq

def cmd_freq(args: argparse.Namespace) -> dict:
    given = [v for v in (args.vph, args.hz, args.bps) if v is not None]
    if len(given) != 1:
        raise SystemExit("freq: give exactly one of --vph, --hz or --bps")
    if args.vph is not None:
        vph = args.vph
    elif args.hz is not None:
        vph = args.hz * 7_200
    else:
        vph = args.bps * 3_600
    hz = vph / 7_200
    result = {
        "vph": vph,
        "hz": hz,
        "beats_per_second": vph / 3_600,
        "oscillations_per_hour": vph / 2,
        "beats_per_day": vph * 24,
        "beat_interval_ms": 3_600_000 / vph,
    }
    if args.escape_teeth:
        escape_rev_per_hour = (vph / 2) / args.escape_teeth
        result["escape_wheel_teeth"] = args.escape_teeth
        result["escape_wheel_rpm"] = escape_rev_per_hour / 60
        result["fourth_wheel_to_escape_pinion_ratio_for_1rpm_seconds"] = escape_rev_per_hour / 60
    return result


# ---------------------------------------------------------------- rate

def cmd_rate(args: argparse.Namespace) -> dict:
    if args.hours is None and args.days is None:
        raise SystemExit("rate: give --days or --hours")
    days = (args.days or 0) + (args.hours or 0) / 24
    if days <= 0:
        raise SystemExit("rate: period must be positive")
    spd = args.gain / days
    result = {
        "observed_change_s": args.gain,
        "period_days": days,
        "rate_s_per_day": spd,
        "rate_s_per_week": spd * 7,
        "rate_s_per_month_30d": spd * 30,
        "rate_s_per_year": spd * 365.2425,
        "fractional_error_ppm": spd / SECONDS_PER_DAY * 1e6,
    }
    checks = []
    names = list(RATE_STANDARDS) if args.standard == "all" else [args.standard] if args.standard else []
    for name in names:
        lo, hi, label = RATE_STANDARDS[name]
        ok = lo <= spd <= hi
        checks.append(f"{label}: {lo:+g} to {hi:+g} s/d -> {'within' if ok else 'outside'}")
    if args.min is not None and args.max is not None:
        ok = args.min <= spd <= args.max
        checks.append(f"custom {args.min:+g} to {args.max:+g} s/d -> {'within' if ok else 'outside'}")
    if checks:
        result["tolerance_checks"] = checks
        result["note"] = (
            "Official standards test under lab conditions across positions and "
            "temperatures; a wrist rate is only indicative."
        )
    return result


# ---------------------------------------------------------------- moonphase

def cmd_moonphase(args: argparse.Namespace) -> dict:
    if args.period is not None:
        display_period = args.period
        basis = f"display period {display_period} days"
    elif args.teeth is not None:
        moons = args.moons
        display_period = args.teeth / moons
        basis = f"{args.teeth}-tooth disc with {moons} moons, one tooth per day"
    else:
        raise SystemExit("moonphase: give --teeth or --period")
    error_per_lunation = abs(display_period - SYNODIC_MONTH_DAYS)
    if error_per_lunation == 0:
        years_per_day = math.inf
    else:
        lunations_per_day_error = 1 / error_per_lunation
        years_per_day = lunations_per_day_error * SYNODIC_MONTH_DAYS / 365.2425
    return {
        "basis": basis,
        "display_period_days": display_period,
        "true_synodic_month_days": SYNODIC_MONTH_DAYS,
        "error_per_lunation_days": error_per_lunation,
        "direction": "display runs fast" if display_period < SYNODIC_MONTH_DAYS else "display runs slow",
        "years_until_one_day_error": years_per_day,
        "note": (
            "Precision displays use reduction gearing, so pass their claimed "
            "period with --period; the common 135-tooth design is about --period 29.53125."
        ),
    }


# ---------------------------------------------------------------- reserve

def cmd_reserve(args: argparse.Namespace) -> dict:
    result = {}
    if args.barrel_turns is not None and args.hours_per_barrel_turn is not None:
        result["estimated_power_reserve_h"] = args.barrel_turns * args.hours_per_barrel_turn
    if args.reserve_hours is not None and args.crown_turns_full is not None:
        result["crown_turns_per_hour_of_reserve"] = args.crown_turns_full / args.reserve_hours
        if args.hours_needed is not None:
            result["crown_turns_for_requested_hours"] = math.ceil(
                args.crown_turns_full / args.reserve_hours * args.hours_needed
            )
    if args.reserve_hours is not None and args.net_gain_per_hour:
        result["hours_to_full_wind_while_worn"] = args.reserve_hours / args.net_gain_per_hour
    if not result:
        raise SystemExit(
            "reserve: give --barrel-turns and --hours-per-barrel-turn, or "
            "--reserve-hours with --crown-turns-full"
        )
    result["note"] = "Estimates only; real reserve depends on spring condition and wear."
    return result


# ---------------------------------------------------------------- beats

def cmd_beats(args: argparse.Namespace) -> dict:
    hours = args.years * 365.2425 * 24 * args.duty
    beats = args.vph * hours
    return {
        "vph": args.vph,
        "years": args.years,
        "fraction_of_time_running": args.duty,
        "total_beats": beats,
        "total_beats_readable": f"{beats:,.0f}",
        "balance_oscillations": beats / 2,
    }


# ---------------------------------------------------------------- water

WATER_GUIDE = [
    (0, 29, "Below 30 m: treat as splash resistant at most."),
    (30, 49, "30 m, 3 bar: splashes and rain only. Not for swimming."),
    (50, 99, "50 m, 5 bar: light surface swimming at most; many brands advise against it."),
    (100, 199, "100 m, 10 bar: swimming and snorkeling."),
    (200, 10**9, "200 m and up, 20 bar: recreational diving if the watch is a diver, ideally ISO 6425."),
]


def cmd_water(args: argparse.Namespace) -> dict:
    given = [v for v in (args.m, args.bar, args.atm, args.psi) if v is not None]
    if len(given) != 1:
        raise SystemExit("water: give exactly one of --m, --bar, --atm or --psi")
    # Watch industry convention: 1 bar of overpressure is about 10 m.
    if args.m is not None:
        bar = args.m / 10
    elif args.bar is not None:
        bar = args.bar
    elif args.atm is not None:
        bar = args.atm * 1.01325
    else:
        bar = args.psi / 14.5038
    meters = bar * 10
    guide = next(text for lo, hi, text in WATER_GUIDE if lo <= meters <= hi)
    result = {
        "meters_rating": meters,
        "bar": bar,
        "atm": bar / 1.01325,
        "psi": bar * 14.5038,
        "practical_meaning": guide,
        "caveat": (
            "Ratings come from a static pressure test, not a safe dive depth. "
            "Gaskets age, so test regularly."
        ),
    }
    if meters >= 100:
        result["iso_6425_test_pressure_bar"] = bar * 1.25
        result["iso_6425_note"] = "ISO 6425 divers are tested at 125 percent of rated pressure."
    return result


# ---------------------------------------------------------------- magnet

def cmd_magnet(args: argparse.Namespace) -> dict:
    given = [v for v in (args.gauss, args.tesla, args.am) if v is not None]
    if len(given) != 1:
        raise SystemExit("magnet: give exactly one of --gauss, --tesla or --am")
    if args.gauss is not None:
        gauss = args.gauss
    elif args.tesla is not None:
        gauss = args.tesla * GAUSS_PER_TESLA
    else:
        gauss = args.am * MU0 * GAUSS_PER_TESLA
    tesla = gauss / GAUSS_PER_TESLA
    am = tesla / MU0
    comparisons = [
        f"{label} ({ref:,.0f} gauss): {'exceeds' if gauss > ref else 'within'}"
        for label, ref in MAGNET_REFERENCES_GAUSS
    ]
    return {
        "gauss": gauss,
        "millitesla": tesla * 1_000,
        "tesla": tesla,
        "a_per_m": am,
        "compared_with": comparisons,
        "note": "Conversion assumes a field in air, where B = mu0 * H.",
    }


# ---------------------------------------------------------------- seiko

def cmd_seiko(args: argparse.Namespace) -> dict:
    serial = args.serial.strip().upper().replace(" ", "")
    if len(serial) < 2:
        raise SystemExit("seiko-serial: serial too short")
    year_digit, month_char = serial[0], serial[1]
    if not year_digit.isdigit():
        raise SystemExit("seiko-serial: the first character should be a digit, the year's last digit")
    month = SEIKO_MONTHS.get(month_char)
    result = {
        "serial": serial,
        "year_last_digit": int(year_digit),
        "month": MONTH_NAMES[month] if month else f"unrecognized month code '{month_char}'",
        "production_number": serial[2:] or "none",
    }
    start, end = args.from_year, args.to_year
    candidates = [
        y for y in range(start, end + 1) if y % 10 == int(year_digit)
    ]
    result["candidate_years"] = [str(y) for y in candidates] or ["none in range"]
    result["note"] = (
        "Pick the decade using the caliber's production period, case design and dial. "
        "Pass --from-year and --to-year to narrow candidates."
    )
    return result


# ---------------------------------------------------------------- gold

def cmd_gold(args: argparse.Namespace) -> dict:
    if (args.karat is None) == (args.fineness is None):
        raise SystemExit("gold: give exactly one of --karat or --fineness")
    if args.karat is not None:
        fineness = args.karat / 24 * 1_000
    else:
        fineness = args.fineness
    karat = fineness / 1_000 * 24
    result = {
        "karat": karat,
        "fineness_per_mille": fineness,
        "percent_gold": fineness / 10,
        "common_hallmarks": "375 = 9k, 585 = 14k, 750 = 18k, 916 = 22k, 999 = 24k",
    }
    if args.grams is not None:
        result["case_weight_g"] = args.grams
        result["pure_gold_content_g"] = args.grams * fineness / 1_000
        result["pure_gold_content_troy_oz"] = args.grams * fineness / 1_000 / 31.1034768
    return result


# ---------------------------------------------------------------- ligne

def cmd_ligne(args: argparse.Namespace) -> dict:
    if (args.lignes is None) == (args.mm is None):
        raise SystemExit("ligne: give exactly one of --lignes or --mm")
    if args.lignes is not None:
        return {"lignes": args.lignes, "mm": args.lignes * LIGNE_MM}
    return {"mm": args.mm, "lignes": args.mm / LIGNE_MM}


# ---------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="horocalc", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="print JSON output")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("freq", help="frequency conversions")
    s.add_argument("--vph", type=float)
    s.add_argument("--hz", type=float)
    s.add_argument("--bps", type=float, help="beats per second")
    s.add_argument("--escape-teeth", type=int, help="escape wheel teeth, usually 15")
    s.set_defaults(func=cmd_freq)

    s = sub.add_parser("rate", help="drift to seconds per day")
    s.add_argument("--gain", type=float, required=True,
                   help="seconds gained over the period; negative for a loss")
    s.add_argument("--days", type=float)
    s.add_argument("--hours", type=float)
    s.add_argument("--standard", choices=list(RATE_STANDARDS) + ["all"])
    s.add_argument("--min", type=float, help="custom lower tolerance, s/d")
    s.add_argument("--max", type=float, help="custom upper tolerance, s/d")
    s.set_defaults(func=cmd_rate)

    s = sub.add_parser("moonphase", help="moonphase drift")
    s.add_argument("--teeth", type=int, help="teeth on the moon disc, e.g. 59 or 135")
    s.add_argument("--moons", type=int, default=2, help="moons painted on the disc")
    s.add_argument("--period", type=float, help="displayed lunation period in days")
    s.set_defaults(func=cmd_moonphase)

    s = sub.add_parser("reserve", help="power reserve estimates")
    s.add_argument("--barrel-turns", type=float)
    s.add_argument("--hours-per-barrel-turn", type=float)
    s.add_argument("--reserve-hours", type=float)
    s.add_argument("--crown-turns-full", type=float, help="crown turns from empty to full")
    s.add_argument("--hours-needed", type=float)
    s.add_argument("--net-gain-per-hour", type=float,
                   help="hours of reserve gained per hour worn, net of consumption")
    s.set_defaults(func=cmd_reserve)

    s = sub.add_parser("beats", help="beats over a period")
    s.add_argument("--vph", type=float, required=True)
    s.add_argument("--years", type=float, required=True)
    s.add_argument("--duty", type=float, default=1.0, help="fraction of time running, 0 to 1")
    s.set_defaults(func=cmd_beats)

    s = sub.add_parser("water", help="water resistance units")
    s.add_argument("--m", type=float)
    s.add_argument("--bar", type=float)
    s.add_argument("--atm", type=float)
    s.add_argument("--psi", type=float)
    s.set_defaults(func=cmd_water)

    s = sub.add_parser("magnet", help="magnetic field units")
    s.add_argument("--gauss", type=float)
    s.add_argument("--tesla", type=float)
    s.add_argument("--am", type=float, help="amperes per meter")
    s.set_defaults(func=cmd_magnet)

    s = sub.add_parser("seiko-serial", help="decode a Seiko serial")
    s.add_argument("serial")
    s.add_argument("--from-year", type=int, default=1960)
    s.add_argument("--to-year", type=int, default=2029)
    s.set_defaults(func=cmd_seiko)

    s = sub.add_parser("gold", help="karat and fineness")
    s.add_argument("--karat", type=float)
    s.add_argument("--fineness", type=float, help="parts per thousand, e.g. 750")
    s.add_argument("--grams", type=float, help="weight of gold component")
    s.set_defaults(func=cmd_gold)

    s = sub.add_parser("ligne", help="lignes and millimeters")
    s.add_argument("--lignes", type=float)
    s.add_argument("--mm", type=float)
    s.set_defaults(func=cmd_ligne)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.func(args)
    emit(result, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
