from enum import Enum

class Tier(str, Enum):
    common = "COMMON"
    uncommon = "UNCOMMON"
    rare = "RARE"
    epic = "EPIC"
    legendary = "LEGENDARY"
    mythic = "MYTHIC"
    divine = "DIVINE"
    ultimate = "ULTIMATE"
    special = "SPECIAL"
    very_special = "VERY SPECIAL"