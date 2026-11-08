# vpn-split-tunnel-checker

Verify VPN split-tunnel routes: any destination inside a corporate network must travel via the tunnel — violations are listed first.

## How to run

```sh
python3 main.py routes.csv --corporate 10.0.0.0/8,172.16.0.0/12
```

## Example output

```
R-2 10.5.0.0/16 via direct: VIOLATION
R-1 8.8.8.8/32 via direct: OK
1 violation(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
