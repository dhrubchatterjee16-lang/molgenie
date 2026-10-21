# MolGenie: Grammar-Guaranteed Generative AI & Retrosynthetic Feasibility Engine

[![CI](https://github.com/dhrubchatterjee16-lang/molgenie/actions/workflows/ci.yml/badge.svg)](https://github.com/dhrubchatterjee16-lang/molgenie/actions)
[![Release](https://img.shields.io/github/v/release/dhrubchatterjee16-lang/molgenie)](https://github.com/dhrubchatterjee16-lang/molgenie/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-MolGenie-yellow)](https://huggingface.co/spaces/dhrubchatterjee/MolGenie)
[![Tests: Passing](https://img.shields.io/badge/tests-4%2F4%20passed-brightgreen.svg)](tests/)

**MolGenie** is a generative chemistry and computer-aided drug discovery platform. It prevents "molecular graffiti" by coupling **SELFIES** grammar-guaranteed valid string generations with automated **retrosynthetic feasibility auditing** ($\le 4$ steps against commercial catalog precursors) and Pan-Assay Interference (**PAINS**) toxicophore screening.

---

## 🔬 Scientific Foundations & Governing Principles

### 1. SELFIES Grammar Invariance
Standard SMILES representations suffer from broken brackets, invalid ring closures, and non-physical valency violations ($>20\%$ generation error in vanilla autoencoders). MolGenie enforces formal Chomsky type-2 grammatical derivations via SELFIES:

$$\mathcal{G} = (V, \Sigma, R, S)$$

Every derived string maps deterministically to a chemically valid molecular graph with zero non-physical valencies:

$$\forall s \in \mathcal{L}(\mathcal{G}), \quad \mathrm{ValencyCheck}(s) = \mathrm{True}$$

### 2. Retrosynthetic Tractability & Commercial Catalog Matching
Generated leads are decomposed retrosynthetically against commercial building block catalogs (Enamine / Sigma-Aldrich proxies):

$$\mathrm{Target} \xrightarrow{\le 4 \text{ steps}} \left\{ \mathrm{Precursor}_1, \mathrm{Precursor}_2, \dots \right\} \subset \mathcal{C}_{\mathrm{commercial}}$$

$$\mathrm{SAS} = 1.0 + 0.4 \cdot N_{\mathrm{rings}} + \frac{\mathrm{MW}}{200.0} + 0.15 \cdot N_{\mathrm{rot\_bonds}} \le 6.0$$

### 3. PAINS Toxicophore Screening
Screens candidate leads against pan-assay interference motifs (quinones, azo groups, unoxidized alkyl halides, hydrazines) to eliminate false-positive biological hits.

---

## ⚡ Quickstart

### Installation

```bash
pip install -e .
```

### Python API

```python
from molgenie import screen_pains_and_sa_score, RetrosynthesisEngine

# 1. Synthesize & Screen Candidate Lead
smiles = "CC(=O)Oc1ccccc1C(=O)O" # Aspirin
med = screen_pains_and_sa_score(smiles)

print(f"SELFIES: {med.selfies}")
print(f"PAINS Alerts: {med.pains_alerts if med.pains_alerts else 'None (Clean)'}")
print(f"Passed Medicinal Filter: {med.passed_filter}")

# 2. Retrosynthetic Feasibility Audit
engine = RetrosynthesisEngine()
route = engine.audit_molecule(smiles)

print(f"Synthetically Accessible (<= 4 steps): {route.is_synthetically_accessible}")
print(f"Estimated Reaction Steps: {route.estimated_step_count}")
print(f"Synthetic Accessibility Score: {route.synthetic_accessibility_score}")
print(f"Commercial Feasibility: {route.commercial_feasibility_pct}%")
print(f"Reaction Classes: {route.reaction_classes}")
```

---

## 🖥️ Command-Line Interface (CLI)

```bash
# Audit a generated molecular structure
molgenie audit --smiles "c1ccccc1C(=O)O"
```

---

## 🧪 Automated Verification Suite

```bash
python run_tests.py
```
```text
Ran 4 tests in 0.167s
OK - ALL MOLGENIE TESTS PASSED (4/4)!
```

---

## 📚 References
- Krenn, M., et al. (2020). *SELFIES: a robust representation of semantically constrained graphs with an example application in chemistry*. Machine Learning: Science and Technology, 1(4), 045024.
- Baell, J. B., & Holloway, G. A. (2010). *New substructure filters for removal of pan assay interference compounds (PAINS) from screening libraries and for their exclusion in promising hits*. Journal of Medicinal Chemistry, 53(7), 2719-2740.
- Coley, C. W., et al. (2018). *Machine learning in computer-aided synthesis planning*. Accounts of Chemical Research, 51(5), 1281-1289.

---

## 📄 License
MIT License. Copyright (c) 2026 Dhrub Chatterjee.