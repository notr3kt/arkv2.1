# Migration Notes: ARK v2.1 → S1NGULARITY

## Overview
All branding and persona references have been reworked from **ARK / ARK Intelligence** to **S1NGULARITY**. The underlying capabilities and module structures remain intact.

## Renamed Assets
- `ark-master-instructions-v2.md` → `s1ngularity-master-instructions-v2.md`
- `TOON Files/ark-master-instructions-v3.md` → `TOON Files/s1ngularity-master-instructions-v3.md`
- `ark-core-system.json` → `s1ngularity-core-system.json`
- `ark-master-v3.toon` (root) → `s1ngularity-master-v3.toon`
- `TOON Files/ark-master-v3.toon` → `TOON Files/s1ngularity-master-v3.toon`

> Note: Functional module filenames (`ark-*.json`, `.toon`) are preserved for backward compatibility with existing loaders; only master/core assets were renamed to reflect the new brand.

## Persona / Greeting Changes
- System identity now greets users as **“Hi! I’m S1NGULARITY…”** across master instructions and TOON assets.

## Breaking Changes
- References to master/core instruction filenames must point to the new `s1ngularity-*` names.
- Any tooling or loaders that hardcode the previous filenames should be updated accordingly.

## Upgrade Guide
1. Update any scripts, pipelines, or loaders to reference the new master/core filenames listed above.
2. Continue loading the existing operational modules (`ark-*.json` and `.toon`) as before; no schema changes were introduced.
3. Verify system prompts or UI copy display **S1NGULARITY** in place of **ARK Intelligence**.
4. If custom email templates or contact addresses referenced the old brand, align them with **S1NGULARITY** naming conventions.
