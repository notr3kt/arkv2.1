# Migration Notes: ARK v2.1 → S1NGULARITY

## Overview
All branding, filenames, and identifiers have been reworked from **ARK / ARK Intelligence** to **S1NGULARITY**. The underlying capabilities remain the same; this pass focuses on renaming and clarity.

## Renamed Assets
### Master and Core
- `ark-master-instructions-v2.md` → `s1ngularity-master-instructions-v2.md`
- `TOON Files/ark-master-instructions-v3.md` → `TOON Files/s1ngularity-master-instructions-v3.md`
- `ark-core-system.json` → `s1ngularity-core-system.json`
- `ark-master-v3.toon` → `s1ngularity-master-v3.toon`
- `TOON Files/ark-master-v3.toon` → `TOON Files/s1ngularity-master-v3.toon`

### Operational Modules (root)
- `ark-advanced-ai-engine.json` → `s1ngularity-advanced-ai-engine.json`
- `ark-advanced-matching.json` → `s1ngularity-advanced-matching.json`
- `ark-analytics-insights.json` → `s1ngularity-analytics-insights.json`
- `ark-bias-detection-compliance.json` → `s1ngularity-bias-detection-compliance.json`
- `ark-boolean-engine-v1.json` → `s1ngularity-boolean-engine-v1.json`
- `ark-communications.json` → `s1ngularity-communications.json`
- `ark-context-awareness.json` → `s1ngularity-context-awareness.json`
- `ark-fallback-resilience.json` → `s1ngularity-fallback-resilience.json`
- `ark-governance-resilience.json` → `s1ngularity-governance-resilience.json`
- `ark-integrations-ecosystem.json` → `s1ngularity-integrations-ecosystem.json`
- `ark-jd-intelligence.json` → `s1ngularity-jd-intelligence.json`
- `ark-output-templates.json` → `s1ngularity-output-templates.json`
- `ark-persona-cultural-fit.json` → `s1ngularity-persona-cultural-fit.json`
- `ark-reasoning-intelligence.json` → `s1ngularity-reasoning-intelligence.json`
- `ark-resume-analysis.json` → `s1ngularity-resume-analysis.json`
- `ark-security-feedback.json` → `s1ngularity-security-feedback.json`
- `ark-web-search-integration.json` → `s1ngularity-web-search-integration.json`
- `ark_intelligence_v2_condensed.txt` → `s1ngularity_intelligence_v2_condensed.txt`

### TOON and Workflow Assets
- `TOON Files/ark-analytics-compliance.toon` → `TOON Files/s1ngularity-analytics-compliance.toon`
- `TOON Files/ark-boolean-engine.toon` → `TOON Files/s1ngularity-boolean-engine.toon`
- `TOON Files/ark-context-resilience.toon` → `TOON Files/s1ngularity-context-resilience.toon`
- `TOON Files/ark-core-foundation.toon` → `TOON Files/s1ngularity-core-foundation.toon`
- `TOON Files/ark-enhancements-guide.toon` → `TOON Files/s1ngularity-enhancements-guide.toon`
- `TOON Files/ark-integrations-search.toon` → `TOON Files/s1ngularity-integrations-search.toon`
- `TOON Files/ark-intelligence-engines.toon` → `TOON Files/s1ngularity-intelligence-engines.toon`
- `TOON Files/ark-matching-suite.toon` → `TOON Files/s1ngularity-matching-suite.toon`
- `TOON Files/ark-n8n-multiagent-workflow.json` → `TOON Files/s1ngularity-n8n-multiagent-workflow.json`
- `TOON Files/ark-operational-standards.toon` → `TOON Files/s1ngularity-operational-standards.toon`
- `TOON Files/ark-security-feedback.toon` → `TOON Files/s1ngularity-security-feedback.toon`

## Breaking Changes
- All module filenames now use the `s1ngularity-` prefix. Update loaders, manifests, or references accordingly.
- Config keys and internal identifiers that previously used `ark_` have been updated to `s1ngularity_`.
- Greetings and personas introduce the assistant as **S1NGULARITY**.

## Upgrade Guide
1. Update any scripts, pipelines, or loaders to reference the new filenames listed above.
2. If you cached module names or configuration keys, replace `ark-` / `ark_` with `s1ngularity-` / `s1ngularity_`.
3. Verify system prompts or UI copy display **S1NGULARITY** in place of **ARK Intelligence**.
4. Validate automated workflows (e.g., n8n) point to the renamed TOON files and that version identifiers or tags reflect the new brand.
