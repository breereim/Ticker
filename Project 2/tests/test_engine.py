import unittest

from engine import CURRENT, estimates, evaluate, run_case, stress_table, turnover


class MeridianTests(unittest.TestCase):
    def test_turnover_and_reserve(self):
        means, vols, corr = estimates()
        row = evaluate((0.25, 0, 0.30, 0.45), means, vols, corr)
        self.assertAlmostEqual(turnover(row["weights"], CURRENT), 0.25)
        self.assertAlmostEqual(row["reserve"], 0.25)
        self.assertEqual(row["failures"], [])

    def test_baseline_failures_and_portfolio(self):
        case = run_case()
        self.assertTrue(any("Turnover" in s for s in case["equal"]["failures"]))
        self.assertFalse(case["equal"]["objective"])
        self.assertTrue(any("Turnover" in s for s in case["inverse_vol"]["failures"]))
        self.assertTrue(any("Reserve" in s for s in case["benchmark"]["failures"]))
        self.assertEqual(case["portfolio"]["failures"], [])
        self.assertTrue(case["portfolio"]["objective"])

    def test_constraint_conflict(self):
        self.assertIsNone(run_case(reserve_min=0.30)["portfolio"])

    def test_window_changes_weights(self):
        self.assertNotEqual(run_case()["portfolio"]["weights"],
                            run_case(last_36=True)["portfolio"]["weights"])

    def test_stress_has_all_dimensions(self):
        rows = stress_table()
        self.assertEqual(len(rows), 6)
        self.assertFalse(rows[4]["feasible"])


if __name__ == "__main__":
    unittest.main()
