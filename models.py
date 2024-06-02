from pydantic import BaseModel, Field
from typing import Optional, List
from typing_extensions import Literal

# Create pydantic model of a Pokemon with name, type 1, type 2
class Pokemon(BaseModel):
    name: str
    type1: Literal[
        "Normal", "Fire", "Fighting", "Water", "Flying", "Grass", "Poison",
        "Electric", "Ground", "Psychic", "Rock", "Ice", "Bug", "Dragon", "Ghost",
        "Dark", "Steel", "Fairy"
    ]
    type2: Optional[Literal[
        "Normal", "Fire", "Fighting", "Water", "Flying", "Grass", "Poison",
        "Electric", "Ground", "Psychic", "Rock", "Ice", "Bug", "Dragon", "Ghost",
        "Dark", "Steel", "Fairy"
    ]] = None
    optimal_set_1: Optional[str] = Field(
        None,
        description="Optimal attack set (fast move and charge move) in Pokemon Go for this Pokemon",
    )
    optimal_set_2: Optional[str] = Field(
        None,
        description="Optimal attack set (fast move and charge move) in Pokemon Go for this Pokemon",
    )
    description: Optional[str] = None

class Tier(BaseModel):
    tier: str
    pokemon_list: List[Pokemon]

class TierList(BaseModel):
    tier_list: List[Tier]
