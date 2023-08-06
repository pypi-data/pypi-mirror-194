from typing import Optional
from pydantic import BaseModel


class InputContainerMetadata(BaseModel):
    """
    example:
    {
        "major_brand": "isom",
        "minor_version": "512",
        "compatible_brands": "isomiso2avc1mp41",
        "comment": "vid:v0200fg10000ccjhgfrc77u70ck4srd0",
        "encoder": "Lavf58.45.100"
    }
    """
    major_brand: Optional[str]
    minor_version: Optional[str]
    compatible_brands: Optional[str]
    comment: Optional[str]
    encoder: Optional[str]

    def __str__(self) -> str:
        return self.json(indent=4)

    def __repr__(self) -> str:
        return self.json(indent=4)
InputContainerMetadata().dict