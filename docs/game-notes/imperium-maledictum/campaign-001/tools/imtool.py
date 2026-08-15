#!/usr/bin/env python3
"""Small, dependency-free utilities for Imperium Maledictum play.

This tool intentionally stops short of automating attacks or Critical Wound
tables. It rolls transparent, replayable dice and records encounter facts; the
GM still adjudicates the fiction and any rules interactions.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence


SCHEMA = "imtool.encounter"
SCHEMA_VERSION = 1
DEFAULT_STATE = Path(__file__).resolve().parent.parent / "runtime" / "encounter.json"

DIFFICULTIES = {
    "very-easy": 60,
    "easy": 40,
    "routine": 20,
    "challenging": 0,
    "difficult": -10,
    "hard": -20,
    "very-hard": -30,
}

DICE_PATTERN = re.compile(r"^(?P<count>\d*)[dD](?P<sides>\d+)(?P<modifier>[+-]\d+)?$")
ACTOR_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class UserError(Exception):
    """An expected command-line or state-file error."""


def explicit_seed(seed: int | None) -> int:
    """Return an explicit seed so every random result can be replayed."""

    return seed if seed is not None else secrets.randbits(64)


def parse_dice(expression: str) -> tuple[int, int, int]:
    compact = expression.replace(" ", "")
    match = DICE_PATTERN.fullmatch(compact)
    if not match:
        raise UserError("dice must look like d100, 2d10, or 3d6+2")

    count = int(match.group("count") or "1")
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or "0")
    if not 1 <= count <= 100:
        raise UserError("dice count must be between 1 and 100")
    if not 2 <= sides <= 10_000:
        raise UserError("die size must be between d2 and d10000")
    if abs(modifier) > 1_000_000:
        raise UserError("dice modifier is unreasonably large")
    return count, sides, modifier


def normalized_dice(count: int, sides: int, modifier: int) -> str:
    suffix = f"{modifier:+d}" if modifier else ""
    return f"{count}d{sides}{suffix}"


def roll_dice(expression: str, seed: int | None = None) -> dict[str, Any]:
    count, sides, modifier = parse_dice(expression)
    used_seed = explicit_seed(seed)
    generator = random.Random(used_seed)
    rolls = [generator.randint(1, sides) for _ in range(count)]
    return {
        "expression": normalized_dice(count, sides, modifier),
        "rolls": rolls,
        "modifier": modifier,
        "total": sum(rolls) + modifier,
        "seed": used_seed,
    }


def percentile_digits(value: int) -> str:
    if not 1 <= value <= 100:
        raise UserError("a percentile roll must be between 1 and 100")
    return "00" if value == 100 else f"{value:02d}"


def reverse_percentile(value: int) -> int:
    reversed_digits = percentile_digits(value)[::-1]
    return 100 if reversed_digits == "00" else int(reversed_digits)


def roll_tens_digit(value: int) -> int:
    return 0 if value == 100 else value // 10


def target_tens_digit(value: int) -> int:
    # int() truncates toward zero, which keeps negative modified targets legible.
    return int(value / 10)


def parse_difficulty(value: str) -> int:
    key = value.strip().lower().replace("_", "-").replace(" ", "-")
    if key in DIFFICULTIES:
        return DIFFICULTIES[key]
    try:
        number = int(value)
    except ValueError as exc:
        names = ", ".join(DIFFICULTIES)
        raise argparse.ArgumentTypeError(
            f"difficulty must be a modifier or one of: {names}"
        ) from exc
    if not -100 <= number <= 100:
        raise argparse.ArgumentTypeError("difficulty modifier must be -100 to +100")
    return number


def resolve_test(
    target: int,
    *,
    difficulty: int = 0,
    advantage: int = 0,
    disadvantage: int = 0,
    sl_modifier: int = 0,
    rolled: int | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    if not 0 <= target <= 100:
        raise UserError("target must be between 0 and 100")
    if advantage < 0 or disadvantage < 0:
        raise UserError("Advantage and Disadvantage counts cannot be negative")
    if rolled is not None and not 1 <= rolled <= 100:
        raise UserError("a supplied percentile roll must be between 1 and 100")

    cancelled = min(advantage, disadvantage)
    remaining_advantage = advantage - cancelled
    remaining_disadvantage = disadvantage - cancelled
    stack_modifier = 0
    if remaining_advantage:
        stack_modifier = (remaining_advantage - 1) * 10
    elif remaining_disadvantage:
        stack_modifier = -(remaining_disadvantage - 1) * 10

    used_seed: int | None = None
    if rolled is None:
        die = roll_dice("d100", seed)
        original_roll = die["rolls"][0]
        used_seed = die["seed"]
    else:
        original_roll = rolled

    reversed_roll = reverse_percentile(original_roll)
    used_roll = original_roll
    reversal = "none"
    if remaining_advantage and reversed_roll < original_roll:
        used_roll = reversed_roll
        reversal = "advantage"
    elif remaining_disadvantage and reversed_roll > original_roll:
        used_roll = reversed_roll
        reversal = "disadvantage"

    modified_target = target + difficulty + stack_modifier
    natural_success = used_roll <= modified_target
    automatic: str | None = None
    if used_roll <= 5:
        base_success = True
        automatic = "success"
    elif used_roll >= 96:
        base_success = False
        automatic = "failure"
    else:
        base_success = natural_success

    raw_sl = target_tens_digit(modified_target) - roll_tens_digit(used_roll)
    # Automatic outcomes cannot be reversed by a numerical SL modifier. Give
    # them the appropriate zero sign if the raw arithmetic points the other way.
    if automatic == "success" and raw_sl < 0:
        raw_sl = 0
    elif automatic == "failure" and raw_sl > 0:
        raw_sl = 0

    final_sl = raw_sl + sl_modifier
    if automatic is not None:
        # The core rules always treat 01-05 and 96-00 as marginal (+0/-0),
        # even when another effect would adjust SL.
        final_sl = 0
        success = base_success
    elif final_sl > 0:
        success = True
    elif final_sl < 0:
        success = False
    else:
        success = base_success

    signed_sl = f"+{final_sl}" if final_sl > 0 or (final_sl == 0 and success) else str(final_sl)
    is_double = percentile_digits(used_roll)[0] == percentile_digits(used_roll)[1]
    return {
        "base_target": target,
        "difficulty_modifier": difficulty,
        "stack_modifier": stack_modifier,
        "modified_target": modified_target,
        "original_roll": original_roll,
        "reversed_roll": reversed_roll,
        "roll": used_roll,
        "reversal": reversal,
        "advantage": remaining_advantage,
        "disadvantage": remaining_disadvantage,
        "cancelled_sources": cancelled,
        "raw_sl": raw_sl,
        "sl_modifier": sl_modifier,
        "sl": final_sl,
        "signed_sl": signed_sl,
        "success": success,
        "automatic": automatic,
        "double": is_double,
        "critical_candidate": is_double and success,
        "fumble_candidate": is_double and not success,
        "automatic_fumble": used_roll == 99,
        "seed": used_seed,
    }


def new_encounter(name: str, superiority: int = 0) -> dict[str, Any]:
    if not name.strip():
        raise UserError("encounter name cannot be empty")
    if superiority < 0:
        raise UserError("Superiority cannot be negative")
    return {
        "schema": SCHEMA,
        "version": SCHEMA_VERSION,
        "name": name.strip(),
        "round": 1,
        "current_actor_id": None,
        "superiority": superiority,
        "actors": [],
    }


def validate_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise UserError("encounter state must be a JSON object")
    if state.get("schema") != SCHEMA or state.get("version") != SCHEMA_VERSION:
        raise UserError("unsupported encounter-state schema or version")
    if not isinstance(state.get("actors"), list):
        raise UserError("encounter state has no valid actor list")
    return state


def load_state(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return validate_state(json.load(handle))
    except FileNotFoundError as exc:
        raise UserError(f"no encounter state at {path}; run 'encounter new' first") from exc
    except json.JSONDecodeError as exc:
        raise UserError(f"encounter state at {path} is not valid JSON: {exc}") from exc


def save_state(path: Path, state: dict[str, Any]) -> None:
    validate_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            temporary_name = handle.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def find_actor(state: dict[str, Any], actor_id: str) -> dict[str, Any]:
    for actor in state["actors"]:
        if actor.get("id") == actor_id:
            return actor
    raise UserError(f"unknown actor id: {actor_id}")


def initiative_order(state: dict[str, Any], *, include_defeated: bool = False) -> list[dict[str, Any]]:
    actors = state["actors"]
    if not include_defeated:
        actors = [actor for actor in actors if not actor["defeated"]]
    return sorted(
        actors,
        key=lambda actor: (-actor["initiative"], -actor["tie_break"], actor["id"]),
    )


def update_actor_flags(actor: dict[str, Any]) -> None:
    actor["dying"] = (
        actor["kind"] == "pc"
        and actor["untreated_critical_wounds"] > actor["toughness_bonus"]
    )
    limit = actor["critical_limit"]
    if actor["kind"] != "pc" and limit is not None and actor["critical_wounds"] > limit:
        actor["defeated"] = True


def add_actor(
    state: dict[str, Any],
    *,
    actor_id: str,
    name: str,
    side: str,
    kind: str,
    initiative: int,
    max_wounds: int,
    toughness_bonus: int,
    critical_limit: int | None,
    resolve: int | None,
    zone: str,
    tie_break: int,
) -> dict[str, Any]:
    if not ACTOR_ID_PATTERN.fullmatch(actor_id):
        raise UserError("actor id must use lowercase letters, numbers, hyphens, or underscores")
    if any(actor.get("id") == actor_id for actor in state["actors"]):
        raise UserError(f"actor id already exists: {actor_id}")
    if not name.strip():
        raise UserError("actor name cannot be empty")
    if max_wounds <= 0:
        raise UserError("Maximum Wounds must be positive")
    if toughness_bonus < 0:
        raise UserError("Toughness Bonus cannot be negative")
    if critical_limit is not None and critical_limit < 0:
        raise UserError("Critical Wound limit cannot be negative")
    if resolve is not None and resolve < 0:
        raise UserError("Resolve cannot be negative")

    if kind == "pc":
        critical_limit = None
    elif critical_limit is None:
        critical_limit = {"troop": 0, "elite": 1, "npc": 0}.get(kind)
        if critical_limit is None:
            raise UserError("leaders require their stat block's --critical-limit")

    actor = {
        "id": actor_id,
        "name": name.strip(),
        "side": side,
        "kind": kind,
        "initiative": initiative,
        "tie_break": tie_break,
        "wounds": 0,
        "max_wounds": max_wounds,
        "critical_wounds": 0,
        "untreated_critical_wounds": 0,
        "critical_limit": critical_limit,
        "toughness_bonus": toughness_bonus,
        "resolve": resolve,
        "zone": zone.strip() or "unspecified",
        "conditions": [],
        "defeated": False,
        "dying": False,
    }
    state["actors"].append(actor)
    return actor


def harm_actor(actor: dict[str, Any], amount: int, *, critical_hit: bool = False) -> dict[str, Any]:
    if amount < 0:
        raise UserError("harm amount cannot be negative")
    old_wounds = actor["wounds"]
    excess_damage = max(0, old_wounds + amount - actor["max_wounds"])
    actor["wounds"] = min(actor["max_wounds"], old_wounds + amount)
    critical = bool(critical_hit or excess_damage > 0)
    if critical:
        actor["critical_wounds"] += 1
        # Whether a table result requires treatment is not known yet. The GM
        # records that separately with `encounter critical` after rolling it.
    update_actor_flags(actor)
    return {
        "old_wounds": old_wounds,
        "new_wounds": actor["wounds"],
        "excess_damage": excess_damage,
        "critical_wound": critical,
        "critical_hit": critical_hit,
    }


def heal_actor(actor: dict[str, Any], amount: int) -> tuple[int, int]:
    if amount < 0:
        raise UserError("healing amount cannot be negative")
    old_wounds = actor["wounds"]
    actor["wounds"] = max(0, old_wounds - amount)
    return old_wounds, actor["wounds"]


def set_critical_wounds(
    actor: dict[str, Any],
    *,
    total: int | None = None,
    untreated: int | None = None,
) -> None:
    if total is None and untreated is None:
        raise UserError("provide --total, --untreated, or both")
    new_total = actor["critical_wounds"] if total is None else total
    new_untreated = actor["untreated_critical_wounds"] if untreated is None else untreated
    if new_total < 0 or new_untreated < 0:
        raise UserError("Critical Wound counts cannot be negative")
    if new_untreated > new_total:
        raise UserError("untreated Critical Wounds cannot exceed total Critical Wounds")
    actor["critical_wounds"] = new_total
    actor["untreated_critical_wounds"] = new_untreated
    update_actor_flags(actor)


def advance_turn(state: dict[str, Any]) -> dict[str, Any]:
    order = initiative_order(state)
    if not order:
        raise UserError("no undefeated actors remain in the encounter")
    ids = [actor["id"] for actor in order]
    current = state.get("current_actor_id")
    if current not in ids:
        next_index = 0
    else:
        next_index = ids.index(current) + 1
        if next_index >= len(ids):
            next_index = 0
            state["round"] += 1
    state["current_actor_id"] = ids[next_index]
    return order[next_index]


def actor_status(actor: dict[str, Any], superiority: int) -> str:
    labels: list[str] = []
    if actor["defeated"]:
        labels.append("DEFEATED")
    if actor["dying"]:
        labels.append("DYING")
    if actor["wounds"] >= actor["max_wounds"] and not actor["defeated"]:
        labels.append("MAX WOUNDS")
    if (
        actor["side"] == "enemy"
        and actor["resolve"] is not None
        and superiority >= actor["resolve"]
        and not actor["defeated"]
    ):
        labels.append("DESPERATE")
    labels.extend(actor["conditions"])
    return ", ".join(labels) if labels else "—"


def render_status(state: dict[str, Any]) -> str:
    lines = [
        f"{state['name']} — round {state['round']} — Superiority {state['superiority']}",
        "",
        "  ID               INIT  SIDE     ZONE              WOUNDS   CRIT   RES  STATUS",
        "  ---------------- ----  -------  ----------------  -------  -----  ---  ------",
    ]
    current = state.get("current_actor_id")
    for actor in initiative_order(state, include_defeated=True):
        marker = ">" if actor["id"] == current else " "
        critical = str(actor["critical_wounds"])
        if actor["untreated_critical_wounds"]:
            critical += f"({actor['untreated_critical_wounds']}u)"
        resolve = "—" if actor["resolve"] is None else str(actor["resolve"])
        lines.append(
            f"{marker} {actor['id'][:16]:16} {actor['initiative']:>4}  "
            f"{actor['side'][:7]:7}  {actor['zone'][:16]:16}  "
            f"{actor['wounds']:>3}/{actor['max_wounds']:<3}  {critical:>5}  "
            f"{resolve:>3}  {actor_status(actor, state['superiority'])}"
        )
    if not state["actors"]:
        lines.append("  (no actors)")
    return "\n".join(lines)


def emit(data: Any, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(data)


def cmd_roll(args: argparse.Namespace) -> None:
    result = roll_dice(args.expression, args.seed)
    if args.json:
        emit(result, as_json=True)
        return
    modifier = f" {result['modifier']:+d}" if result["modifier"] else ""
    print(
        f"{result['expression']}: {result['rolls']}{modifier} = {result['total']} "
        f"(seed {result['seed']})"
    )


def cmd_test(args: argparse.Namespace) -> None:
    result = resolve_test(
        args.target,
        difficulty=args.difficulty,
        advantage=args.advantage,
        disadvantage=args.disadvantage,
        sl_modifier=args.sl_modifier,
        rolled=args.roll,
        seed=args.seed,
    )
    if args.json:
        emit(result, as_json=True)
        return
    changed = ""
    if result["roll"] != result["original_roll"]:
        changed = f" -> {percentile_digits(result['roll'])} ({result['reversal']})"
    tags: list[str] = []
    if result["automatic"]:
        tags.append(f"automatic {result['automatic']}")
    if result["critical_candidate"]:
        tags.append("double/possible Critical")
    if result["fumble_candidate"]:
        tags.append("double/Fumble candidate")
    if result["automatic_fumble"]:
        tags.append("99 Fumble")
    suffix = f"; {', '.join(tags)}" if tags else ""
    seed = f"; seed {result['seed']}" if result["seed"] is not None else ""
    print(
        f"Target {result['modified_target']}; rolled "
        f"{percentile_digits(result['original_roll'])}{changed}: "
        f"{'SUCCESS' if result['success'] else 'FAILURE'} "
        f"({result['signed_sl']} SL{suffix}{seed})"
    )


def encounter_path(args: argparse.Namespace) -> Path:
    return Path(args.state).expanduser().resolve()


def cmd_encounter(args: argparse.Namespace) -> None:
    path = encounter_path(args)
    command = args.encounter_command
    if command == "new":
        if path.exists() and not args.force:
            raise UserError(f"state already exists at {path}; use --force to replace it")
        state = new_encounter(args.name, args.superiority)
        save_state(path, state)
        print(f"Created encounter '{state['name']}' at {path}")
        return

    state = load_state(path)
    if command == "status":
        emit(state if args.json else render_status(state), as_json=args.json)
        return
    if command == "add":
        actor = add_actor(
            state,
            actor_id=args.actor_id,
            name=args.name,
            side=args.side,
            kind=args.kind,
            initiative=args.initiative,
            max_wounds=args.max_wounds,
            toughness_bonus=args.toughness_bonus,
            critical_limit=args.critical_limit,
            resolve=args.resolve,
            zone=args.zone,
            tie_break=args.tie_break,
        )
        save_state(path, state)
        print(f"Added {actor['name']} ({actor['id']})")
        return

    actor = find_actor(state, args.actor_id) if hasattr(args, "actor_id") else None
    if command == "harm":
        result = harm_actor(actor, args.amount, critical_hit=args.critical_hit)
        save_state(path, state)
        message = f"{actor['name']}: {result['old_wounds']} -> {result['new_wounds']} Wounds"
        if result["critical_wound"]:
            message += "; +1 Critical Wound"
            if result["excess_damage"]:
                message += f" ({result['excess_damage']} excess Damage for Severity)"
            message += "; record treatment after resolving the Critical Wound table"
        print(message)
    elif command == "heal":
        old, new = heal_actor(actor, args.amount)
        save_state(path, state)
        print(f"{actor['name']}: {old} -> {new} Wounds")
    elif command == "critical":
        set_critical_wounds(actor, total=args.total, untreated=args.untreated)
        save_state(path, state)
        print(
            f"{actor['name']}: {actor['critical_wounds']} Critical Wounds, "
            f"{actor['untreated_critical_wounds']} untreated"
        )
    elif command == "condition":
        condition = args.condition.strip()
        if not condition:
            raise UserError("condition cannot be empty")
        if args.operation == "add" and condition not in actor["conditions"]:
            actor["conditions"].append(condition)
            actor["conditions"].sort(key=str.casefold)
        elif args.operation == "remove":
            try:
                actor["conditions"].remove(condition)
            except ValueError as exc:
                raise UserError(f"{actor['name']} does not have condition: {condition}") from exc
        save_state(path, state)
        print(f"{actor['name']} conditions: {', '.join(actor['conditions']) or 'none'}")
    elif command == "move":
        actor["zone"] = args.zone.strip() or "unspecified"
        save_state(path, state)
        print(f"{actor['name']} moved to {actor['zone']}")
    elif command in {"defeat", "restore"}:
        actor["defeated"] = command == "defeat"
        if command == "restore":
            update_actor_flags(actor)
        if state.get("current_actor_id") == actor["id"] and actor["defeated"]:
            state["current_actor_id"] = None
        save_state(path, state)
        print(f"{actor['name']}: {'defeated' if actor['defeated'] else 'active'}")
    elif command == "superiority":
        old = state["superiority"]
        state["superiority"] = max(0, old + args.delta)
        save_state(path, state)
        print(f"Superiority: {old} -> {state['superiority']}")
    elif command == "next":
        next_actor = advance_turn(state)
        save_state(path, state)
        print(f"Round {state['round']}: {next_actor['name']} acts")
    else:  # pragma: no cover - argparse prevents this
        raise UserError(f"unsupported encounter command: {command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Imperium Maledictum dice and encounter helper",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    roll_parser = subparsers.add_parser("roll", help="roll an ordinary dice expression")
    roll_parser.add_argument("expression", help="for example d100, 2d10, or 1d10+3")
    roll_parser.add_argument("--seed", type=int, help="replayable random seed")
    roll_parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    roll_parser.set_defaults(handler=cmd_roll)

    test_parser = subparsers.add_parser("test", help="resolve an Imperium Maledictum d100 Test")
    test_parser.add_argument("target", type=int, help="unmodified Skill or Characteristic target")
    test_parser.add_argument(
        "--difficulty",
        type=parse_difficulty,
        default=0,
        help="named difficulty or modifier; default: challenging",
    )
    test_parser.add_argument("--advantage", type=int, default=0, help="number of Advantage sources")
    test_parser.add_argument(
        "--disadvantage", type=int, default=0, help="number of Disadvantage sources"
    )
    test_parser.add_argument(
        "--sl-modifier",
        type=int,
        default=0,
        help="SL adjustment such as Influence or spent Superiority",
    )
    test_parser.add_argument("--roll", type=int, help="use a supplied roll instead of rolling")
    test_parser.add_argument("--seed", type=int, help="replayable random seed")
    test_parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    test_parser.set_defaults(handler=cmd_test)

    encounter_parser = subparsers.add_parser("encounter", help="manage persistent encounter state")
    encounter_parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE),
        help=f"state JSON path (default: {DEFAULT_STATE})",
    )
    encounter_subparsers = encounter_parser.add_subparsers(
        dest="encounter_command", required=True
    )

    new_parser = encounter_subparsers.add_parser("new", help="create a fresh encounter")
    new_parser.add_argument("name")
    new_parser.add_argument("--superiority", type=int, default=0)
    new_parser.add_argument("--force", action="store_true", help="replace an existing state file")

    status_parser = encounter_subparsers.add_parser("status", help="show the encounter dashboard")
    status_parser.add_argument("--json", action="store_true", help="emit the complete state JSON")

    add_parser = encounter_subparsers.add_parser("add", help="add a combatant")
    add_parser.add_argument("actor_id")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--side", choices=("party", "enemy", "neutral"), required=True)
    add_parser.add_argument(
        "--kind", choices=("pc", "troop", "elite", "leader", "npc"), required=True
    )
    add_parser.add_argument("--initiative", type=int, required=True)
    add_parser.add_argument("--tie-break", type=int, default=0)
    add_parser.add_argument("--max-wounds", type=int, required=True)
    add_parser.add_argument("--toughness-bonus", type=int, default=0)
    add_parser.add_argument(
        "--critical-limit",
        type=int,
        help="Critical Wounds printed in an NPC stat block; required for leaders",
    )
    add_parser.add_argument("--resolve", type=int)
    add_parser.add_argument("--zone", default="unspecified")

    harm_parser = encounter_subparsers.add_parser("harm", help="record Wounds after Armour")
    harm_parser.add_argument("actor_id")
    harm_parser.add_argument("amount", type=int)
    harm_parser.add_argument("--critical-hit", action="store_true")

    heal_parser = encounter_subparsers.add_parser("heal", help="heal ordinary Wounds")
    heal_parser.add_argument("actor_id")
    heal_parser.add_argument("amount", type=int)

    critical_parser = encounter_subparsers.add_parser(
        "critical", help="set total and/or untreated Critical Wound counts"
    )
    critical_parser.add_argument("actor_id")
    critical_parser.add_argument("--total", type=int)
    critical_parser.add_argument("--untreated", type=int)

    condition_parser = encounter_subparsers.add_parser("condition", help="add or remove a Condition")
    condition_parser.add_argument("actor_id")
    condition_parser.add_argument("operation", choices=("add", "remove"))
    condition_parser.add_argument("condition")

    move_parser = encounter_subparsers.add_parser("move", help="move a combatant to a named Zone")
    move_parser.add_argument("actor_id")
    move_parser.add_argument("zone")

    defeat_parser = encounter_subparsers.add_parser("defeat", help="mark a combatant defeated")
    defeat_parser.add_argument("actor_id")
    restore_parser = encounter_subparsers.add_parser("restore", help="return a combatant to play")
    restore_parser.add_argument("actor_id")

    superiority_parser = encounter_subparsers.add_parser(
        "superiority", help="adjust group Superiority by a signed amount"
    )
    superiority_parser.add_argument("delta", type=int)

    encounter_subparsers.add_parser("next", help="advance to the next undefeated combatant")
    encounter_parser.set_defaults(handler=cmd_encounter)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.handler(args)
    except UserError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
