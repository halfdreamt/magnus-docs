from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOL_PATH = Path(__file__).resolve().parents[1] / "imtool.py"
SPEC = importlib.util.spec_from_file_location("imtool", TOOL_PATH)
assert SPEC and SPEC.loader
imtool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(imtool)


class DiceTests(unittest.TestCase):
    def test_parse_and_seeded_roll_are_replayable(self) -> None:
        first = imtool.roll_dice("2d10 + 3", seed=451)
        second = imtool.roll_dice("2d10+3", seed=451)
        self.assertEqual(first, second)
        self.assertEqual(first["expression"], "2d10+3")
        self.assertEqual(first["total"], sum(first["rolls"]) + 3)

    def test_percentile_reversal_handles_zero_faces(self) -> None:
        self.assertEqual(imtool.reverse_percentile(1), 10)
        self.assertEqual(imtool.reverse_percentile(10), 1)
        self.assertEqual(imtool.reverse_percentile(100), 100)


class TestResolutionTests(unittest.TestCase):
    def test_advantage_reverses_and_extra_source_adds_ten(self) -> None:
        result = imtool.resolve_test(40, advantage=2, rolled=71)
        self.assertEqual(result["modified_target"], 50)
        self.assertEqual(result["roll"], 17)
        self.assertEqual(result["reversal"], "advantage")
        self.assertTrue(result["success"])
        self.assertEqual(result["sl"], 4)

    def test_advantage_and_disadvantage_cancel_pairwise(self) -> None:
        result = imtool.resolve_test(40, advantage=2, disadvantage=1, rolled=71)
        self.assertEqual(result["modified_target"], 40)
        self.assertEqual(result["roll"], 17)
        self.assertEqual(result["cancelled_sources"], 1)

    def test_disadvantage_reverses_only_when_worse(self) -> None:
        result = imtool.resolve_test(55, disadvantage=1, rolled=16)
        self.assertEqual(result["roll"], 61)
        self.assertFalse(result["success"])

    def test_automatic_ranges_override_target(self) -> None:
        self.assertTrue(imtool.resolve_test(0, rolled=5)["success"])
        self.assertFalse(imtool.resolve_test(100, rolled=96)["success"])

    def test_automatic_ranges_remain_marginal_after_sl_modifiers(self) -> None:
        success = imtool.resolve_test(0, rolled=5, sl_modifier=-5)
        failure = imtool.resolve_test(100, rolled=96, sl_modifier=5)
        self.assertEqual(success["signed_sl"], "+0")
        self.assertEqual(failure["signed_sl"], "0")
        self.assertTrue(success["success"])
        self.assertFalse(failure["success"])

    def test_zero_sl_keeps_success_and_failure_distinct(self) -> None:
        success = imtool.resolve_test(45, rolled=42)
        failure = imtool.resolve_test(40, rolled=42)
        self.assertEqual(success["signed_sl"], "+0")
        self.assertEqual(failure["signed_sl"], "0")
        self.assertTrue(success["success"])
        self.assertFalse(failure["success"])

    def test_sl_modifier_can_change_nonautomatic_outcome(self) -> None:
        result = imtool.resolve_test(35, rolled=41, sl_modifier=2)
        self.assertEqual(result["raw_sl"], -1)
        self.assertEqual(result["sl"], 1)
        self.assertTrue(result["success"])


class EncounterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = imtool.new_encounter("Test encounter", superiority=1)
        imtool.add_actor(
            self.state,
            actor_id="adept",
            name="Adept",
            side="party",
            kind="pc",
            initiative=8,
            max_wounds=12,
            toughness_bonus=3,
            critical_limit=None,
            resolve=None,
            zone="gantry",
            tie_break=0,
        )
        imtool.add_actor(
            self.state,
            actor_id="ganger",
            name="Ganger",
            side="enemy",
            kind="troop",
            initiative=6,
            max_wounds=13,
            toughness_bonus=4,
            critical_limit=None,
            resolve=1,
            zone="floor",
            tie_break=0,
        )

    def test_crossing_maximum_wounds_causes_one_critical(self) -> None:
        actor = imtool.find_actor(self.state, "ganger")
        first = imtool.harm_actor(actor, 11)
        second = imtool.harm_actor(actor, 5)
        self.assertFalse(first["critical_wound"])
        self.assertTrue(second["critical_wound"])
        self.assertEqual(second["excess_damage"], 3)
        self.assertEqual(actor["critical_wounds"], 1)
        self.assertTrue(actor["defeated"])

    def test_critical_hit_and_overflow_still_record_one_critical(self) -> None:
        actor = imtool.find_actor(self.state, "ganger")
        imtool.harm_actor(actor, 20, critical_hit=True)
        self.assertEqual(actor["critical_wounds"], 1)

    def test_pc_dying_uses_untreated_not_total_critical_wounds(self) -> None:
        actor = imtool.find_actor(self.state, "adept")
        imtool.set_critical_wounds(actor, total=4, untreated=3)
        self.assertFalse(actor["dying"])
        imtool.set_critical_wounds(actor, untreated=4)
        self.assertTrue(actor["dying"])

    def test_turn_order_skips_defeated_and_wraps_round(self) -> None:
        first = imtool.advance_turn(self.state)
        self.assertEqual(first["id"], "adept")
        second = imtool.advance_turn(self.state)
        self.assertEqual(second["id"], "ganger")
        wrapped = imtool.advance_turn(self.state)
        self.assertEqual(wrapped["id"], "adept")
        self.assertEqual(self.state["round"], 2)

    def test_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            imtool.save_state(path, self.state)
            loaded = imtool.load_state(path)
        self.assertEqual(loaded, self.state)


class CommandLineFlowTests(unittest.TestCase):
    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL_PATH), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_encounter_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "encounter.json")
            prefix = ("encounter", "--state", state_path)
            self.run_tool(*prefix, "new", "CLI encounter", "--superiority", "1")
            self.run_tool(
                *prefix,
                "add",
                "adept",
                "--name",
                "Adept",
                "--side",
                "party",
                "--kind",
                "pc",
                "--initiative",
                "8",
                "--max-wounds",
                "12",
                "--toughness-bonus",
                "3",
                "--zone",
                "gantry",
            )
            self.run_tool(*prefix, "harm", "adept", "4")
            self.run_tool(*prefix, "condition", "adept", "add", "Bleeding")
            status = self.run_tool(*prefix, "status")

        self.assertIn("CLI encounter — round 1 — Superiority 1", status.stdout)
        self.assertIn("4/12", status.stdout)
        self.assertIn("Bleeding", status.stdout)


if __name__ == "__main__":
    unittest.main()
