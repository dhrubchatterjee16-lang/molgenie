"""
Retrosynthetic Accessibility & Commercial Feasibility Engine
"""

import math
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple, Optional

@dataclass
class RetrosyntheticRouteResult:
    target_smiles: str
    is_synthetically_accessible: bool
    synthetic_accessibility_score: float
    estimated_step_count: int
    matched_precursors: List[str]
    reaction_classes: List[str]
    has_unphysical_motifs: bool
    unphysical_reasons: List[str]
    commercial_feasibility_pct: float

COMMERCIAL_BUILDING_BLOCKS = {
    "c1ccccc1": "Benzene",
    "c1ccccc1O": "Phenol",
    "c1ccccc1N": "Aniline",
    "CC(=O)O": "Acetic Acid",
    "CCO": "Ethanol",
    "CCN": "Ethylamine",
    "c1ccncc1": "Pyridine",
    "c1ccccc1C(=O)O": "Benzoic Acid",
    "c1ccccc1Br": "Bromobenzene",
    "c1ccccc1C=O": "Benzaldehyde",
    "O=C(O)CC(=O)O": "Malonic Acid",
    "OCCO": "Ethylene Glycol",
}

UNPHYSICAL_MOTIFS = [
    (r"OO|O-O", "Peroxide train (high explosion/decomposition hazard)"),
    (r"N#N#N", "Azide cluster / explosive nitrogen content"),
    (r"S-S-S", "Polysulfide train"),
    (r"C=C=C=C", "Cumulene instability"),
    (r"\[Cl\+\]|\[Br\+\]", "Halogen positive charge in unoxidized state"),
    (r"C12C3C1C23", "Prismane / extreme ring strain cage"),
]

class RetrosynthesisEngine:
    """Rule-based retrosynthetic planner and synthetic accessibility scorer."""
    def audit_molecule(self, smiles: str) -> RetrosyntheticRouteResult:
        unphysical_flags = []
        for pattern, reason in UNPHYSICAL_MOTIFS:
            if re.search(pattern, smiles):
                unphysical_flags.append(reason)

        has_unphysical = len(unphysical_flags) > 0

        # Building block matching
        matched_precursors = []
        for bb_smiles, bb_name in COMMERCIAL_BUILDING_BLOCKS.items():
            if bb_smiles in smiles:
                matched_precursors.append(f"{bb_name} ({bb_smiles})")

        # Step count approximation
        complexity = len(smiles) / 10.0 + (smiles.count("=") + smiles.count("#")) * 0.5
        est_steps = max(1, min(8, int(math.ceil(complexity - len(matched_precursors) * 0.4))))

        # SAS score
        sas = 1.5 + (est_steps * 0.8) + (2.5 if has_unphysical else 0.0)
        sas = round(min(10.0, max(1.0, sas)), 2)

        is_accessible = (not has_unphysical) and (est_steps <= 4) and (sas <= 6.0)
        feasibility = max(0.0, min(100.0, (1.0 - (sas - 1.0) / 9.0) * 100.0))

        reactions = []
        if "C(=O)O" in smiles or "CC(=O)" in smiles:
            reactions.append("Amide/Ester Coupling")
        if "c1ccc" in smiles:
            reactions.append("Suzuki-Miyaura / Electrophilic Aromatic Substitution")
        if not reactions:
            reactions.append("Nucleophilic Alkylation")

        return RetrosyntheticRouteResult(
            target_smiles=smiles,
            is_synthetically_accessible=is_accessible,
            synthetic_accessibility_score=sas,
            estimated_step_count=est_steps,
            matched_precursors=matched_precursors,
            reaction_classes=reactions,
            has_unphysical_motifs=has_unphysical,
            unphysical_reasons=unphysical_flags,
            commercial_feasibility_pct=round(feasibility, 1)
        )
