import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(r, d, v):
    return {"route": r, "destination": d, "via": v}

class TestSplitTunnel(unittest.TestCase):
    def test_corporate_via_direct_is_violation(self):
        self.assertEqual(check([row("R1", "10.5.0.0/16", "direct")], ["10.0.0.0/8"])[0][3], "VIOLATION")
    def test_corporate_via_tunnel_ok(self):
        self.assertEqual(check([row("R1", "10.5.0.0/16", "tunnel")], ["10.0.0.0/8"])[0][3], "OK")
    def test_public_via_direct_ok(self):
        self.assertEqual(check([row("R1", "8.8.8.8/32", "direct")], ["10.0.0.0/8"])[0][3], "OK")
    def test_violations_first(self):
        r = check([row("A", "8.8.8.8/32", "direct"), row("B", "10.5.0.0/16", "direct")], ["10.0.0.0/8"])
        self.assertEqual(r[0][0], "B")
