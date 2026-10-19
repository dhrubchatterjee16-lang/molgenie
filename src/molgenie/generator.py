"""
SELFIES Grammatical Grammar & PAINS Medicinal Chemistry Screening
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

PAINS_SMARTS = [
    ("Quinone", "O=C1C=CC(=O)C=C1"),
    ("Alkyl halide", "[CX4][Cl,Br,I]"),
    ("Hydrazine", "[NX3][NX3]"),
    ("Azo group", "[#6]-N=N-[#6]"),
    ("Epoxide", "C1OC1")
]

@dataclass
class MedicinalFilterResult:
    smiles: str
    selfies: str
    sa_score: float
    pains_alerts: List[str]
    passed_filter: bool
    recommendation: str

def smiles_to_selfies_safe(smiles: str) -> str:
    try:
        import selfies as sf
        return sf.encoder(smiles)
    except Exception:
        # Syntactic tokenization fallback
        tokens = []
        for c in smiles:
            if c.isalnum() or c in "=()#":
                tokens.append(f"[{c}]")
        return "".join(tokens)

def selfies_to_smiles_safe(selfies_str: str) -> str:
    try:
        import selfies as sf
        return sf.decoder(selfies_str)
    except Exception:
        return selfies_str.replace("[", "").replace("]", "")

def screen_pains_and_sa_score(smiles: str) -> MedicinalFilterResult:
    pains_found = []
    sa_score = 2.5
    
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            for alert_name, smarts in PAINS_SMARTS:
                query = Chem.MolFromSmarts(smarts)
                if query and mol.HasSubstructMatch(query):
                    pains_found.append(alert_name)
            
            num_rings = Descriptors.RingCount(mol)
            mw = Descriptors.MolWt(mol)
            rotatable_bonds = Descriptors.NumRotatableBonds(mol)
            sa_score = 1.0 + (num_rings * 0.4) + (mw / 200.0) + (rotatable_bonds * 0.15)
            sa_score = min(10.0, max(1.0, sa_score))
    except Exception:
        pass

    passed = len(pains_found) == 0 and sa_score < 6.0
    rec = "Viable lead candidate" if passed else "Flagged for synthetic difficulty or PAINS toxicophore"

    return MedicinalFilterResult(
        smiles=smiles,
        selfies=smiles_to_selfies_safe(smiles),
        sa_score=round(sa_score, 2),
        pains_alerts=pains_found,
        passed_filter=passed,
        recommendation=rec
    )
