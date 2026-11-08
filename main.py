"""Check VPN split-tunnel routes against a corporate policy.

Usage: python3 main.py routes.csv --corporate 10.0.0.0/8,172.16.0.0/12
CSV columns: route,destination,via (tunnel/direct).
A route whose destination falls inside a corporate network must go
via the tunnel; anything else may go direct. VIOLATION otherwise OK.
"""
import argparse, csv, ipaddress, sys

def check(rows, corporate):
    nets = [ipaddress.ip_network(c.strip()) for c in corporate]
    out = []
    for row in rows:
        dest = ipaddress.ip_network(row["destination"].strip())
        corporate_dest = any(dest.subnet_of(n) or dest.overlaps(n) for n in nets)
        via = row["via"].strip().lower()
        verdict = "VIOLATION" if corporate_dest and via != "tunnel" else "OK"
        out.append((row["route"], row["destination"], via, verdict))
    return sorted(out, key=lambda r: r[3] == "OK")

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--corporate", required=True, help="comma-separated CIDRs")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        result = check(list(csv.DictReader(f)), args.corporate.split(","))
    for route, dest, via, verdict in result:
        print(f"{route} {dest} via {via}: {verdict}")
    print(f"{sum(1 for *_, v in result if v == 'VIOLATION')} violation(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
