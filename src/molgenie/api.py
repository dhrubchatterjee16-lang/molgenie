"""
FastAPI Microservice for MolGenie
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

try:
    from fastapi import FastAPI, HTTPException
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from .generator import screen_pains_and_sa_score, smiles_to_selfies_safe
from .retrosynthesis import RetrosynthesisEngine

if HAS_FASTAPI:
    app = FastAPI(
        title="MolGenie API",
        description="Grammar-Guaranteed Molecular Generation & Retrosynthetic Feasibility Service",
        version="1.0.0"
    )

    class AuditRequest(BaseModel):
        smiles: str = Field(..., description="SMILES chemical representation")

    @app.get("/")
    def root():
        return {
            "service": "MolGenie",
            "version": "1.0.0",
            "status": "operational"
        }

    @app.post("/mol/audit")
    def api_audit(req: AuditRequest):
        med = screen_pains_and_sa_score(req.smiles)
        retro = RetrosynthesisEngine().audit_molecule(req.smiles)
        return {
            "smiles": req.smiles,
            "selfies": med.selfies,
            "synthetically_accessible": retro.is_synthetically_accessible,
            "step_count": retro.estimated_step_count,
            "sa_score": retro.synthetic_accessibility_score,
            "commercial_feasibility_pct": retro.commercial_feasibility_pct,
            "pains_alerts": med.pains_alerts,
            "reaction_classes": retro.reaction_classes,
            "matched_precursors": retro.matched_precursors,
            "recommendation": med.recommendation
        }
else:
    app = None
