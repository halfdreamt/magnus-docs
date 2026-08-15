# Campaign utility kit

`imtool.py` is a small Python 3 command-line helper with no third-party
dependencies. It provides transparent dice, Imperium Maledictum Test math, and
a persistent encounter dashboard. It records mechanical facts without trying
to replace GM adjudication.

Run these examples from the `campaign-001` directory:

```sh
python3 tools/imtool.py roll 2d10+20
python3 tools/imtool.py test 47 --difficulty difficult --advantage 1
python3 tools/imtool.py test 47 --roll 71 --advantage 2 --sl-modifier 1
```

Every generated roll prints its seed. Pass the same seed again to reproduce
the result exactly. `--roll` is useful when physical dice were rolled. Add
`--json` to `roll` or `test` when another tool needs structured output.

The Test helper handles named Difficulty, automatic 01–05 success and 96–00
failure, SL, digit reversal, cancellation and stacking of Advantage and
Disadvantage, and after-roll SL modifiers such as Influence or spent
Superiority. A double is only labelled a *candidate*: whether it is a Critical
or Fumble depends on the kind of Test and, for an Opposed Test, the other
participant's result.

For an Opposed Test, the printed success or failure describes only that
participant's own roll. Resolve the opposition by comparing both final SL
results; a failed roll can still win against a worse one.

## Encounter dashboard

The default live state is `runtime/encounter.json`, which is intentionally
ignored by Git. Create a fresh encounter and add combatants using the numbers
on their sheets or stat blocks:

```sh
python3 tools/imtool.py encounter new "Tutorial encounter" --superiority 1
python3 tools/imtool.py encounter add adept \
  --name "Adept Vey" --side party --kind pc --initiative 8 \
  --max-wounds 12 --toughness-bonus 3 --zone gantry
python3 tools/imtool.py encounter add ganger-1 \
  --name "Vylathi Ganger" --side enemy --kind troop --initiative 7 \
  --max-wounds 13 --toughness-bonus 4 --resolve 1 --zone floor
python3 tools/imtool.py encounter status
python3 tools/imtool.py encounter next
```

Record only Wounds that remain **after Armour and other reductions**. The
tracker caps Wounds at Maximum Wounds and records one Critical Wound when a hit
crosses that threshold or `--critical-hit` is supplied. If both happen in the
same attack, they are one Critical Wound with excess Damage added to its
Severity Roll, not two separate wounds.

```sh
python3 tools/imtool.py encounter harm ganger-1 8
python3 tools/imtool.py encounter harm ganger-1 7 --critical-hit
python3 tools/imtool.py encounter critical adept --total 1 --untreated 1
python3 tools/imtool.py encounter condition adept add Bleeding
python3 tools/imtool.py encounter heal adept 4
python3 tools/imtool.py encounter move adept "reactor floor"
python3 tools/imtool.py encounter superiority +1
python3 tools/imtool.py encounter status
```

Troops default to 0 and Elites to 1 allowed Critical Wound, matching the usual
stat-block categories. Leaders require `--critical-limit` because their printed
values vary. PCs are instead flagged `DYING` when their untreated Critical
Wounds exceed Toughness Bonus. The tool never rolls injury tables, decides
whether a Critical Wound requires treatment, applies Armour, or declares a PC
dead; those remain visible GM decisions.

The dashboard labels an enemy `DESPERATE` when Superiority equals or exceeds
its Resolve, following the dedicated Resolve subsection on core page 198. That
label is a prompt for the GM, not an automatic surrender.

Use `--state some/file.json` immediately after `encounter` to keep a separate
state file. `encounter new` refuses to replace an existing file unless
`--force` is explicit.

## Tests

```sh
python3 -m unittest discover -s tools/tests -v
```
