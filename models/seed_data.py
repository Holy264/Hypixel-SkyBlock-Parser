"""
Иерархия категорий Hypixel SkyBlock Bazaar.
Узлы — словари (категории), листья — списки предметов.
Глубина: main → sub → [sub-sub] → items.
"""

BAZAAR_CATEGORIES: dict = {
    # ═══════════════════════════════════════════════════════════════
    # FARMING
    # ═══════════════════════════════════════════════════════════════
    "Farming": {
        "Wheat & Seeds": [
            "Wheat", "Enchanted Bread", "Enchanted Wheat",
            "Enchanted Hay Bale", "Seeds", "Enchanted Seeds", "Box of Seeds",
        ],
        "Carrot": [
            "Carrot", "Enchanted Carrot", "Enchanted Carrot on a Stick",
            "Enchanted Golden Carrot",
        ],
        "Potato": [
            "Potato", "Poisonous Potato", "Enchanted Potato",
            "Enchanted Poisonous Potato", "Enchanted Baked Potato",
        ],
        "Pumpkin": ["Pumpkin", "Enchanted Pumpkin", "Polished Pumpkin"],
        "Melon Slice": [
            "Melon Slice", "Enchanted Melon Slice", "Enchanted Glistering Melon Slice",
            "Melon", "Enchanted Melon",
        ],
        "Mushrooms": [
            "Red Mushroom", "Enchanted Red Mushroom",
            "Red Mushroom Block", "Enchanted Red Mushroom Block",
            "Brown Mushroom", "Enchanted Brown Mushroom",
            "Brown Mushroom Block", "Enchanted Brown Mushroom Block",
        ],
        "Cocoa Beans": ["Cocoa Beans", "Enchanted Cocoa Beans", "Enchanted Cookie"],
        "Cactus": ["Cactus", "Enchanted Cactus Green", "Enchanted Cactus"],
        "Sugar Cane": [
            "Sugar Cane", "Enchanted Sugar", "Enchanted Paper", "Enchanted Sugar Cane",
        ],
        "Leather & Beef": [
            "Leather", "Enchanted Leather", "Raw Beef", "Enchanted Raw Beef",
        ],
        "Pork": [
            "Raw Porkchop", "Enchanted Raw Porkchop", "Enchanted Cooked Porkchop",
        ],
        "Chicken & Feather": [
            "Raw Chicken", "Enchanted Raw Chicken", "Enchanted Cake",
            "Feather", "Enchanted Feather",
            "Egg", "Enchanted Egg", "Super Enchanted Egg", "Omega Enchanted Egg",
        ],
        "Raw Mutton": [
            "Raw Mutton", "Enchanted Raw Mutton", "Enchanted Cooked Mutton",
            "White Wool", "Enchanted Wool",
        ],

        "Rabbit": [
            "Raw Rabbit", "Enchanted Raw Rabbit", "Enchanted Cooked Rabbit",
            "Rabbit's Foot", "Rabbit Hide",
            "Enchanted Rabbit Foot", "Enchanted Rabbit Hide",
            
            "Faction Rabbit Walker", "Faction Rabbit Tundra", "Faction Rabbit Shortcut",
            "Faction Rabbit Anchor", "Faction Rabbit Peon", "Faction Rabbit Haybale",
            "Faction Rabbit Icefur", "Faction Rabbit Traffic", "Faction Rabbit Daisy",
            "Faction Rabbit Chasm", "Faction Rabbit Sunset", "Faction Rabbit Twigy",
            "Faction Rabbit Valley", "Faction Rabbit Horizon", "Faction Rabbit Skyrise",
            "Faction Rabbit Lavender",
            ],
        "Nether Warts": [
            "Nether Wart", "Enchanted Nether Wart", "Mutant Nether Wart",
        ],
        "Garden": [
            "Compost", "Compost Bundle", "Cropie", "Squash", "Fermento",
            "Condensed Fermento", "Dung", "Tasty Cheese", "Plant Matter",
            "Honey Jar", "Wriggling Larva", "Fine Flour",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MINING
    # ═══════════════════════════════════════════════════════════════
    "Mining": {
        "Cobblestone": ["Cobblestone", "Enchanted Cobblestone"],
        "Coal": [
            "Coal", "Enchanted Coal", "Enchanted Charcoal", "Enchanted Coal Block",
        ],
        "Iron": ["Iron Ingot", "Enchanted Iron Ingot", "Enchanted Iron Block"],
        "Gold": ["Gold Ingot", "Enchanted Gold Ingot", "Enchanted Gold Block"],
        "Diamond": [
            "Diamond", "Enchanted Diamond", "Enchanted Diamond Block", "Refined Diamond",
        ],
        "Lapis": [
            "Lapis Lazuli", "Enchanted Lapis Lazuli", "Enchanted Lapis Lazuli Block",
        ],
        "Emerald": ["Emerald", "Enchanted Emerald", "Enchanted Emerald Block"],
        "Redstone Dust": [
            "Redstone Dust", "Enchanted Redstone Dust", "Enchanted Redstone Block",
        ],
        "Obsidian": ["Obsidian", "Enchanted Obsidian"],
        "End Stone": ["End Stone", "Enchanted End Stone"],
        "Flint & Gravel": ["Flint", "Enchanted Flint", "Gravel"],
        "Sand": ["Sand", "Enchanted Sand"],
        "Ice": [
            "Ice", "Packed Ice", "Enchanted Ice",
            "Enchanted Packed Ice", "Glacial Fragment",
        ],
        "Snow": ["Snowball", "Snow Block", "Enchanted Snow Block"],
        "Hard Stone": [
            "Hard Stone", "Enchanted Hard Stone", "Concentrated Stone",
        ],

        # ─── Gemstones: три уровня вложенности ───
        "Gemstones": {
            "Jade Gemstone": [
                "Rough Jade Gemstone", "Flawed Jade Gemstone", "Fine Jade Gemstone",
                "Flawless Jade Gemstone", "Perfect Jade Gemstone",
            ],
            "Amber Gemstone": [
                "Rough Amber Gemstone", "Flawed Amber Gemstone", "Fine Amber Gemstone",
                "Flawless Amber Gemstone", "Perfect Amber Gemstone",
            ],
            "Topaz Gemstone": [
                "Rough Topaz Gemstone", "Flawed Topaz Gemstone", "Fine Topaz Gemstone",
                "Flawless Topaz Gemstone", "Perfect Topaz Gemstone",
            ],
            "Sapphire Gemstone": [
                "Rough Sapphire Gemstone", "Flawed Sapphire Gemstone", "Fine Sapphire Gemstone",
                "Flawless Sapphire Gemstone", "Perfect Sapphire Gemstone",
            ],
            "Amethyst Gemstone": [
                "Rough Amethyst Gemstone", "Flawed Amethyst Gemstone", "Fine Amethyst Gemstone",
                "Flawless Amethyst Gemstone", "Perfect Amethyst Gemstone",
            ],
            "Jasper Gemstone": [
                "Rough Jasper Gemstone", "Flawed Jasper Gemstone", "Fine Jasper Gemstone",
                "Flawless Jasper Gemstone", "Perfect Jasper Gemstone",
            ],
            "Ruby Gemstone": [
                "Rough Ruby Gemstone", "Flawed Ruby Gemstone", "Fine Ruby Gemstone",
                "Flawless Ruby Gemstone", "Perfect Ruby Gemstone",
            ],
            "Opal Gemstone": [
                "Rough Opal Gemstone", "Flawed Opal Gemstone", "Fine Opal Gemstone",
                "Flawless Opal Gemstone", "Perfect Opal Gemstone",
            ],
            "Onyx Gemstone": [
                "Rough Onyx Gemstone", "Flawed Onyx Gemstone", "Fine Onyx Gemstone",
                "Flawless Onyx Gemstone", "Perfect Onyx Gemstone",
            ],
            "Aquamarine Gemstone": [
                "Rough Aquamarine Gemstone", "Flawed Aquamarine Gemstone",
                "Fine Aquamarine Gemstone", "Flawless Aquamarine Gemstone",
                "Perfect Aquamarine Gemstone",
            ],
            "Citrine Gemstone": [
                "Rough Citrine Gemstone", "Flawed Citrine Gemstone",
                "Fine Citrine Gemstone", "Flawless Citrine Gemstone",
                "Perfect Citrine Gemstone",
            ],
            "Peridot Gemstone": [
                "Rough Peridot Gemstone", "Flawed Peridot Gemstone",
                "Fine Peridot Gemstone", "Flawless Peridot Gemstone",
                "Perfect Peridot Gemstone",
            ],
        },

        "Goblin Eggs": [
            "Goblin Egg", "Red Goblin Egg", "Blue Goblin Egg",
            "Yellow Goblin Egg", "Green Goblin Egg",
        ],
        "Dwarven Mines": [
            "Mithril", "Enchanted Mithril", "Refined Mithril", "Starfall",
            "Titanium", "Enchanted Titanium", "Refined Titanium",
            "Treasurite", "Sorrow",
        ],
        "Forge": [
            "Plasma", "Glacite Jewel", "Fuel Canister", "Bejeweled Handle",
            "Gemstone Mixture", "Mithril Plate", "Drill Motor", "Golden Plate",
        ],
        "Crystal Hollows": [
            "Precursor Apparatus", "Electron Transmitter", "FTX 3070",
            "Robotron Reflector", "Superlite Motor", "Control Switch",
            "Synthetic Heart", "Jungle Key", "Jungle Heart", "Divan Fragment",
            "Corleonite", "Sludge Juice", "Yoggie", "Ascension Rope",
            "Wishing Compass", "Bob-omb",
        ],
        "Crimson Isle": {
            "Glowstone": [
                "Glowstone Dust", "Enchanted Glowstone Dust",
                "Enchanted Glowstone", "Enchanted Redstone Lamp",
            ],
            "Netherrack": ["Netherrack", "Enchanted Netherrack"],
            "Nether Quartz": [
                "Nether Quartz", "Enchanted Nether Quartz", "Enchanted Quartz Block",
            ],
            "Red Sand": ["Red Sand", "Enchanted Red Sand", "Enchanted Red Sand Cube"],
            "Sulphur": ["Sulphur", "Enchanted Sulphur", "Enchanted Sulphur Cube"],
            "Mycelium": ["Mycelium", "Enchanted Mycelium", "Enchanted Mycelium Cube"],
        },
        "Glacite Tunnels": [
            "Umber", "Enchanted Umber", "Refined Umber", "Umber Plate", "Umber Key",
            "Tungsten", "Enchanted Tungsten", "Refined Tungsten",
            "Tungsten Plate", "Tungsten Key",
            "Glacite", "Enchanted Glacite", "Glacite Amalgamation",
            "Perfect Plate", "Skeleton Key", "Suspicious Scrap",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # COMBAT
    # ═══════════════════════════════════════════════════════════════
    "Combat": {
        "Rotten Flesh": ["Rotten Flesh", "Enchanted Rotten Flesh"],
        "Bone": [
            "Bone", "Enchanted Bone", "Enchanted Bone Block", "Enchanted Bone Meal",
        ],
        "Arachnids": [
            "String", "Enchanted String",
            "Spider Eye", "Enchanted Spider Eye", "Enchanted Fermented Spider Eye",
            "Soul String", "Arachne's Calling", "Arachne Fragment", "Arachne's Fang",
        ],
        "Gunpowder": ["Gunpowder", "Enchanted Gunpowder", "Enchanted Firework Rocket"],
        "Ender Pearl": [
            "Ender Pearl", "Enchanted Ender Pearl", "Enchanted Eye of Ender",
            "Absolute Ender Pearl", "Tessellated Ender Pearl",
        ],
        "Ghast Tear": ["Ghast Tear", "Enchanted Ghast Tear", "Silver Fang"],
        "Slimes": [
            "Slimeball", "Enchanted Slimeball", "Enchanted Slime Block", "Poison Sample",
        ],
        "Magma Cream": [
            "Magma Cream", "Enchanted Magma Cream", "Whipped Magma Cream",
        ],
        "Blaze Rod": ["Blaze Rod", "Enchanted Blaze Powder", "Enchanted Blaze Rod"],
        "The End": ["Summoning Eye", "Crystal Fragment"],
        "Dragon Fragments": [
            "Protector Dragon Fragment", "Old Dragon Fragment",
            "Unstable Dragon Fragment", "Strong Dragon Fragment",
            "Young Dragon Fragment", "Wise Dragon Fragment",
            "Superior Dragon Fragment", "Holy Dragon Fragment",
        ],
        "Draconic Sacrifice": ["Ritual Residue", "Mite Gel"],
        "Crimson Isle": {
            "Mob Drops": [
                "Blaze Ashes", "Mutated Blaze Ashes", "Millennia-Old Blaze Ashes",
                "Spectre Dust", "Wither Soul", "Bezos", "Magmag",
                "Digested Mushrooms", "Burning Eye", "Magma Chunk",
                "Gazing Pearl", "Flames", "Kada Lead", "Match-Sticks",
                "Tentacle Meat", "Corrupted Fragment",
            ],
            "Mini Bosses": [
                "Hallowed Skull", "Spell Powder", "Leather Cloth",
                "Lumino Fiber", "Compact Ooze", "Rekindled Ember Fragment",
            ],
            "Special": [
                "Nether Star", "Heavy Pearl", "Kuudra Teeth", "X", "Y", "Z",
            ],
        },
        "Slayers": {
            "Revenant Horror": [
                "Revenant Flesh", "Revenant Viscera", "Golden Powder",
                "Undead Catalyst", "Revenant Catalyst",
            ],
            "Tarantula Broodfather": [
                "Tarantula Web", "Tarantula Silk", "Spider Catalyst",
                "Tarantula Catalyst", "Fly Swatter", "Toxic Arrow Poison",
            ],
            "Sven Packmaster": [
                "Wolf Tooth", "Golden Tooth", "Weak Wolf Catalyst",
            ],
            "Voidgloom Seraph": [
                "Null Sphere", "Null Ovoid", "Null Atom", "Raw Soulflow",
                "Soulflow", "Braided Griffin Feather", "Twilight Arrow Poison",
                "Null Blade", "Null Edge",
            ],
            "Inferno Demonlord": [
                "Derelict Ashe", "Amalgamated Crimsonite", "Molten Powder",
                "Blaze Rod Distillate", "Gabagool Distillate",
                "Glowstone Distillate", "Magma Cream Distillate",
                "Nether Wart Distillate", "Bundle of Magma Arrows",
                "Kelvin Inverter", "Subzero Inverter",
            ],
        },
        "Catacombs": {
            "Special Fragments": [
                "Jolly Pink Rock", "L.A.S.R.'s Eye", "Bigfoot's Lasso",
                "Diamante's Handle",
            ],
            "Mob Drops": [
                "Mimic Fragment", "Fel Pearl", "Ancient Rose", "Healing Tissue",
            ],
            "Secret Drops": [
                "Dungeon Chest Key", "Superboom TNT", "Trap", "Spirit Leap",
                "Inflatable Jerry", "Decoy", "Architect's First Draft",
            ],
            "Catacombs Misc.": [
                "Kismet Feather", "Wither Catalyst", "Spirit Wing", "Spirit Bone",
            ],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # WOODS & FISHES
    # ═══════════════════════════════════════════════════════════════
    "Woods & Fishes": {
        "Wood": {
            "Oak": ["Oak Log", "Enchanted Oak Log"],
            "Spruce": ["Spruce Log", "Enchanted Spruce Log"],
            "Birch": ["Birch Log", "Enchanted Birch Log"],
            "Dark Oak": ["Dark Oak Log", "Enchanted Dark Oak Log"],
            "Acacia": ["Acacia Log", "Enchanted Acacia Log"],
            "Jungle": ["Jungle Log", "Enchanted Jungle Log"],
            "Fig": ["Fig Log", "Enchanted Fig Log", "Figstone"],
            "Mangrove": ["Mangrove Log", "Enchanted Mangrove Log", "Mangcore"],
        },
        "Fish": {
            "Raw Cod": ["Raw Cod", "Enchanted Raw Cod", "Enchanted Cooked Cod"],
            "Salmon": ["Raw Salmon", "Enchanted Raw Salmon", "Enchanted Cooked Salmon"],
            "Tropical Fish": ["Tropical Fish", "Enchanted Tropical Fish"],
            "Pufferfish": ["Pufferfish", "Enchanted Pufferfish"],
        },
        "Flowers": [
            "Poppy", "Enchanted Poppy", "Dandelion", "Enchanted Dandelion",
        ],
        "Prismarine": [
            "Prismarine Shard", "Enchanted Prismarine Shard",
            "Prismarine Crystals", "Enchanted Prismarine Crystals",
        ],
        "Clay Ball": ["Clay Ball", "Enchanted Clay Ball", "Enchanted Clay Block"],
        "Sponge": ["Sponge", "Enchanted Sponge", "Enchanted Wet Sponge"],
        "Lily Pad": ["Lily Pad", "Enchanted Lily Pad"],
        "Ink Sac": ["Ink Sac", "Enchanted Ink Sac"],
        "Baits": [
            "Carrot Bait", "Minnow Bait", "Fish Bait", "Light Bait", "Dark Bait",
            "Spooky Bait", "Spiked Bait", "Blessed Bait", "Ice Bait", "Frozen Bait",
            "Whale Bait", "Shark Bait", "Corrupted Bait", "Hot Bait",
            "Glowy Chum Bait", "Worm Bait", "Golden Bait", "Treasure Bait",
            "Hotspot Bait", "Wooden Bait",
        ],
        "Mob Drops": [
            "Worm Membrane", "Hunk of Ice", "Hunk of Blue Ice",
            "Emperor's Skull", "Bobbin' Scriptures", "Magma Core",
            "Half-Eaten Mushroom", "Singed Powder", "Fried Feather",
            "Scorched Crab Stick", "Brimstone Handle", "Broken Radar", "Blue Ring",
        ],
        "Magmafish": [
            "Magmafish", "Silver Magmafish", "Gold Magmafish", "Diamond Magmafish",
        ],
        "Lava Fishing": [
            "Lava Shell", "Lump of Magma", "Moogma Pelt", "Cup of Blood",
            "Pyroclastic Scale", "Flaming Heart", "Orb of Energy",
            "Horn of Taurus", "Thunder Fragment", "Magma Lord Fragment",
        ],
        "Water Orbs": [
            "Water Orb", "Lava Water Orb", "Spooky Water Orb",
            "Shark Water Orb", "Winter Water Orb", "Bayou Water Orb",
            "Hotspot Water Orb",
        ],
        "Chum Fishing": [
            "Chum", "Glowing Mushroom", "Empty Chum Bucket", "Full Chum Bucket",
        ],
        "Backwater Bayou": [
            "Rusty Coin", "Busted Belt Buckle", "Old Leather Boot", "Torn Cloth",
            "Bronze Bowl", "Alligator Skin", "Titanoboa Shed", "Can of Worms",
        ],
        "Moonglade Marsh": [
            "Vinesap", "Enchanted Vinesap",
            "Tender Wood", "Enchanted Tender Wood",
            "Sea Lumies", "Enchanted Sea Lumies",
            "Flexbone", "Lushlilac", "Lushlilac Bonbon",
            "Exalted Lushlilac Bonbon", "Prime Lushlilac Bonbon",
            "Candycomb", "Oceandy", "Wet Water", "Gill Membrane",
            "Sturdy Bone", "Starlyn Prize", "Deep Root",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # ODDITIES
    # ═══════════════════════════════════════════════════════════════
    "Oddities": {
        "Booster Cookie": ["Booster Cookie"],

        "Modifiers": {
            "Item Upgrades": [
                "Recombobulator 3000", "Wood Singularity", "Silex",
                "Transmission Tuner", "Divan's Powder Coating", "Golden Bounty",
                "Mana Disintegrator", "A Beginner's Guide to Pesthunting",
                "Gold Bottle Cap", "Troubled Bubble", "Severed Pincer",
                "Octopus Tendril", "Chain of the End Times", "Ensnared Snail",
            ],
            "Wither Scrolls": ["Implosion", "Wither Shield", "Shadow Warp"],
            "Master Stars": [
                "First Master Star", "Second Master Star", "Third Master Star",
                "Fourth Master Star", "Fifth Master Star",
            ],
            "Book Modifiers": [
                "Hot Potato Book", "Fuming Potato Book", "Book of Stats",
                "The Art of War", "Farming for Dummies", "The Art of Peace",
                "Jalapeno Book", "Bookworm's Favorite Book",
                "Polarvoid Book", "Wet Book",
            ],
            "Boosters": [
                "Foraging Booster", "Fighting Booster",
                "Foraging Fortune Booster", "Foraging Wisdom Booster",
                "Sweep Booster",
            ],
        },

        "Enchantments": {
            "Normal Enchantments": [
                "Enchanted Book (Absorb I)", "Enchanted Book (Angler VI)",
                "Enchanted Book (Bane of Arthropods VI)",
                "Enchanted Book (Big Brain III-V)", "Enchanted Book (Blast Protection VI-VII)",
                "Enchanted Book (Blessing VI)", "Enchanted Book (Caster VI)",
                "Enchanted Book (Cayenne IV-V)", "Enchanted Book (Champion I)",
                "Enchanted Book (Chance IV-V)", "Enchanted Book (Charm I-V)",
                "Enchanted Book (Cleave VI)", "Enchanted Book (Compact I)",
                "Enchanted Book (Corruption I-V)", "Enchanted Book (Counter-Strike III-V)",
                "Enchanted Book (Critical VI-VII)", "Enchanted Book (Cubism VI)",
                "Enchanted Book (Cultivating I)", "Enchanted Book (Dedication I-IV)",
                "Enchanted Book (Delicate V)", "Enchanted Book (Divine Gift I-III)",
                "Enchanted Book (Gravity I-V)", "Enchanted Book (Drain IV-V)",
                "Enchanted Book (Ender Slayer VI-VII)", "Enchanted Book (Execute VI)",
                "Enchanted Book (Experience IV-V)", "Enchanted Book (Expertise I)",
                "Enchanted Book (Feather Falling VI-X)",
                "Enchanted Book (Ferocious Mana I-X)",
                "Enchanted Book (Fire Aspect III)",
                "Enchanted Book (Fire Protection VI-VII)",
                "Enchanted Book (First Strike V)",
                "Enchanted Book (Forest Pledge III-V)",
                "Enchanted Book (Fortune IV)", "Enchanted Book (Frail VI)",
                "Enchanted Book (Giant Killer VI-VII)",
                "Enchanted Book (Green Thumb I-V)",
                "Enchanted Book (Growth VI-VII)",
                "Enchanted Book (Hardened Mana I-X)",
                "Enchanted Book (Harvesting VI)", "Enchanted Book (Hecatomb I-X)",
                "Enchanted Book (Ice Cold I-V)",
                "Enchanted Book (Infinite Quiver VI-X)",
                "Enchanted Book (Lapidary I-V)", "Enchanted Book (Lethality VI)",
                "Enchanted Book (Life Steal IV-V)", "Enchanted Book (Looting IV-V)",
                "Enchanted Book (Luck VI-VII)", "Enchanted Book (Luck of the Sea VI)",
                "Enchanted Book (Lure VI)", "Enchanted Book (Magnet VI)",
                "Enchanted Book (Mana Steal I-III)",
                "Enchanted Book (Mana Vampire I-X)",
                "Enchanted Book (Overload I-V)",
                "Enchanted Book (Paleontologist I-V)",
                "Enchanted Book (Pesterminator I-V)",
                "Enchanted Book (Piscary VI)", "Enchanted Book (Power VI-VII)",
                "Enchanted Book (Prismatic I-V)",
                "Enchanted Book (Projectile Protection VI-VII)",
                "Enchanted Book (Prosecute VI)", "Enchanted Book (Prosperity I-V)",
                "Enchanted Book (Protection VI-VII)",
                "Enchanted Book (Quantum III-V)",
                "Enchanted Book (Quick Bite I-V)",
                "Enchanted Book (Reflection I-V)",
                "Enchanted Book (Rejuvenate I-V)",
                "Enchanted Book (Replenish I)",
                "Enchanted Book (Respiration IV)",
                "Enchanted Book (Respite I-V)",
                "Enchanted Book (Scavenger IV-V)",
                "Enchanted Book (Scuba III-V)",
                "Enchanted Book (Sharpness VI-VII)",
                "Enchanted Book (Small Brain III-V)",
                "Enchanted Book (Smarty Pants I-V)",
                "Enchanted Book (Smite VI-VII)",
                "Enchanted Book (Smoldering I-V)", "Enchanted Book (Snipe IV)",
                "Enchanted Book (Spiked Hook VI)", "Enchanted Book (Stealth I)",
                "Enchanted Book (Strong Mana I-X)",
                "Enchanted Book (Sugar Rush I-III)",
                "Enchanted Book (Sunder I-VI)", "Enchanted Book (Tabasco II-III)",
                "Enchanted Book (Thunderbolt VI-VII)",
                "Enchanted Book (Thunderlord VI-VII)",
                "Enchanted Book (Tidal I-III)",
                "Enchanted Book (Titan Killer VI-VII)",
                "Enchanted Book (Toxophilite I)",
                "Enchanted Book (Transylvanian IV-V)",
                "Enchanted Book (Triple-Strike V)",
                "Enchanted Book (True Protection I)",
                "Enchanted Book (Turbo-Cacti I-V)",
                "Enchanted Book (Turbo-Cane I-V)",
                "Enchanted Book (Turbo-Carrot I-V)",
                "Enchanted Book (Turbo-Cocoa I-V)",
                "Enchanted Book (Turbo-Melon I-V)",
                "Enchanted Book (Turbo-Mushrooms I-V)",
                "Enchanted Book (Turbo-Potato I-V)",
                "Enchanted Book (Turbo-Pumpkin I-V)",
                "Enchanted Book (Turbo-Warts I-V)",
                "Enchanted Book (Turbo-Wheat I-V)",
                "Enchanted Book (Vampirism VI)", "Enchanted Book (Venomous VI)",
                "Enchanted Book (Vicious III-V)",
                "Enchanted Book (Woodsplitter I-V)",
            ],
            "Ultimate Enchantments": [
                "Enchanted Book (Bank I-V)",
                "Enchanted Book (Bobbin' Time III-V)",
                "Enchanted Book (Chimera I-V)",
                "Enchanted Book (Combo I-V)",
                "Enchanted Book (Duplex I-V)",
                "Enchanted Book (Fatal Tempo I-V)",
                "Enchanted Book (First Impression I-V)",
                "Enchanted Book (Flash I-V)",
                "Enchanted Book (Flowstate I-III)",
                "Enchanted Book (Habanero Tactics IV-V)",
                "Enchanted Book (Inferno I-V)",
                "Enchanted Book (Last Stand I-V)",
                "Enchanted Book (Legion I-V)",
                "Enchanted Book (Missile I-V)",
                "Enchanted Book (No Pain No Gain I-V)",
                "Enchanted Book (One For All I)",
                "Enchanted Book (Refrigerate I-V)",
                "Enchanted Book (Rend I-V)",
                "Enchanted Book (Soul Eater I-V)",
                "Enchanted Book (Swarm I-V)",
                "Enchanted Book (The One IV-V)",
                "Enchanted Book (Ultimate Jerry I-V)",
                "Enchanted Book (Ultimate Wise I-V)",
                "Enchanted Book (Wisdom I-V)",
            ],
        },

        "EXP Bottles": [
            "Experience Bottle", "Grand Experience Bottle",
            "Titanic Experience Bottle", "Colossal Experience Bottle",
        ],

        "Shards": [
            "Abyssal Lanternfish Shard", "Aero Shard", "Alligator Shard",
            "Ananke Shard", "Apex Dragon Shard", "Arachne Shard", "Azure Shard",
            "Bal Shard", "Bambloom Shard", "Bambuleaf Shard",
            "Barbarian Duke X Shard", "Basilisk Shard", "Beaconmite Shard",
            "Bezal Shard", "Birries Shard", "Bitbug Shard", "Blizzard Shard",
            "Bogged Shard", "Bolt Shard", "Boreal Owl Shard", "Bramble Shard",
            "Bruiser Shard", "Bullfrog Shard", "Burningsoul Shard", "Caiman Shard",
            "Carrot King Shard", "Cascade Shard", "Cavernshade Shard",
            "Chameleon Shard", "Chill Shard", "Cinderbat Shard", "Cod Shard",
            "Condor Shard", "Coralot Shard", "Crocodile Shard", "Cropeetle Shard",
            "Crow Shard", "Cryo Shard", "Cuboa Shard", "Daemon Shard", "Dodo Shard",
            "Draconic Shard", "Dragonfly Shard", "Dreadwing Shard", "Drowned Shard",
            "Eel Shard", "End Stone Protector Shard", "Ent Shard", "Etherdrake Shard",
            "Falcon Shard", "Fenlord Shard", "Firefly Shard", "Fire Eel Shard",
            "Flaming Spider Shard", "Flare Shard", "Flash Shard", "Fungloom Shard",
            "Galaxy Fish Shard", "Gecko Shard", "Ghost Shard", "Glacite Walker Shard",
            "Golden Ghoul Shard", "Goldfin Shard", "Grove Shard", "Harpy Shard",
            "Hellwisp Shard", "Heron Shard", "Hideonbox Shard", "Hideoncave Shard",
            "Hideondra Shard", "Hideongeon Shard", "Hideongift Shard",
            "Hideonleaf Shard", "Hideonring Shard", "Hideonsack Shard",
            "Iguana Shard", "Inferno Koi Shard", "Invisibug Shard", "Jormung Shard",
            "Joydive Shard", "Kada Knight Shard", "King Cobra Shard", "Kiwi Shard",
            "Komodo Dragon Shard", "Kraken Shard", "Ladybug Shard",
            "Lapis Creeper Shard", "Lapis Skeleton Shard", "Lapis Zombie Shard",
            "Lava Flame Shard", "Leatherback Shard", "Leviathan Shard",
            "Lizard King Shard", "Lord Jawbus Shard", "Lumisquid Shard",
            "Lunar Moth Shard", "Magma Slug Shard", "Matcho Shard", "Megalith Shard",
            "Mimic Shard", "Miner Zombie Shard", "Mist Shard", "Mochibear Shard",
            "Moltenfish Shard", "Molthorn Shard", "Moray Eel Shard", "Mossybit Shard",
            "Mudworm Shard", "Naga Shard", "Newt Shard", "Night Squid Shard",
            "Obsidian Defender Shard", "Pandarai Shard", "Pest Shard",
            "Phanflare Shard", "Phanpyre Shard", "Piranha Shard",
            "Power Dragon Shard", "Praying Mantis Shard", "Prince Shard",
            "Python Shard", "Quake Shard", "Quartzfang Shard", "Rain Slime Shard",
            "Rana Shard", "Revenant Shard", "Salamander Shard", "Salmon Shard",
            "Scarf Shard", "Seagull Shard", "Sea Emperor Shard", "Sea Serpent Shard",
            "Seer Shard", "Shellwise Shard", "Shinyfish Shard", "Silentdepth Shard",
            "Skeletor Shard", "Snowfin Shard", "Soul of the Alpha Shard",
            "Sparrow Shard", "Spike Shard", "Stalagmight Shard", "Starborn Shard",
            "Star Sentry Shard", "Stridersurfer Shard", "Sun Fish Shard",
            "Sycophant Shard", "Sylvan Shard", "Tadgang Shard", "Tank Zombie Shard",
            "Taurus Shard", "Tempest Shard", "Tenebris Shard", "Termite Shard",
            "Terra Shard", "Thorn Shard", "Thyst Shard", "Tiamat Shard",
            "Tide Shard", "Toad Shard", "Tortoise Shard", "Toucan Shard",
            "Troglobyte Shard", "Verdant Shard", "Viper Shard",
            "Voracious Spider Shard", "Wartybug Shard", "Water Hydra Shard",
            "Wither Shard", "Wither Spectre Shard", "Wyvern Shard", "XYZ Shard",
            "Yog Shard", "Zealot Shard", "Zombie Soldier Shard",
        ],

        "Reforge Stones": [
            "Hardened Wood", "Overflowing Trash Can", "Salt Cube", "Warped Stone",
            "Blazen Sphere", "Blaze Wax", "Burrowing Spores", "Calcified Heart",
            "Candy Corn", "Diamond Atom", "Diamonite", "Dragon Claw", "Dragon Scale",
            "Dwarven Treasure", "End Stone Geode", "Entropy Suppressor",
            "Flowering Bouquet", "Full-Jaw Fanging Kit", "Jaderald", "Jerry Stone",
            "Lapis Crystal", "Large Walnut", "Mangrove Gem", "Meteor Chunk",
            "Midas Jewel", "Molten Cube", "Moonglade Jewel", "Necromancer's Brooch",
            "Black Diamond", "Optical Lens", "Overgrown Grass", "Pitchin' Koi",
            "Premium Flesh", "Presumed Gallon of Red Paint", "Pure Mithril",
            "Rare Diamond", "Red Nose", "Red Scarf", "Dwarven Geode",
            "Rusty Anchor", "Kaleidoscopic Mineral", "Searing Stone", "Shiny Prism",
            "SkyMart Brochure", "Spirit Stone", "Squeaky Toy", "Suspicious Vial",
            "Terry's Snowglobe", "Titanium Tesseract", "Amber Material",
            "Beady Eyes", "Blessed Fruit", "Bulky Stone", "Clipped Wings",
            "Deep Sea Orb", "Dragon Horn", "Frozen Bauble", "Giant Tooth",
            "Gleaming Crystal", "Golden Ball", "Kuudra Mandible", "Lucky Dice",
            "Petrified Starfall", "Pocket Iceberg", "Precursor Gear",
            "Andesite Whetstone", "Sadan's Brooch", "Wither Blood",
            "Frigid Husk", "Scorched Topaz",
        ],

        "Power Stones": [
            "Displaced Leech", "Luxurious Spool", "Rock Candy", "Acacia Birdhouse",
            "Beating Heart", "Dark Orb", "Ender Monocle", "End Stone Shulker",
            "Furball", "Mandraa", "Obsidian Tablet", "Horns of Torment",
            "Magma Urchin", "Precious Pearl", "Bubba Blister",
            "Fang-tastic Chocolate Chip", "Eccentric Painting", "Glacite Chunk",
            "Hazmat Enderman", "Vitamin Death", "Scorched Books", "Stock of Stonks",
        ],

        "Pet Upgrades": {
            "Pet Candies": [
                "Simple Carrot Candy", "Great Carrot Candy", "Superb Carrot Candy",
                "Ultimate Carrot Candy", "Chyme", "Pet Cake", "Lucky Clover Core",
                "Exp Share Core", "Tier Boost Core", "Radioactive Vial",
                "Enderman Cortex Rewriter", "Jerry 3D Glasses", "Vampire Fang",
                "Mixed Mite Gel", "Pure Mithril Gem", "Black Woolen Yarn",
                "Magic Top Hat", "Guardian Lucky Block", "Chocolate Syringe",
                "Scuttler Shell",
            ],
            "Inferno Minion": [
                "Crude Gabagool", "Very Crude Gabagool", "Fuel Gabagool",
                "Heavy Gabagool", "Hypergolic Gabagool", "Inferno Vertex",
                "Inferno Apex", "Reaper Pepper", "Chili Pepper",
                "Stuffed Chili Pepper", "Inferno Fuel Block",
                "Hypergolic Ionized Ceramics", "Sulphuric Coal",
                "Re-heated Gummy Polar Bear", "Capsaicin Eyedrops",
            ],
            "Minion Upgrades": {
                "Minion Storage": [
                    "Small Storage", "Medium Storage", "Large Storage",
                    "X-Large Storage", "XX-Large Storage",
                ],
                "Compactors": [
                    "Compactor", "Dwarven Super Compactor", "Super Compactor 3000",
                    "Diamond Spreading", "Minion Expander", "Potato Spreading",
                    "Auto Smelter", "Soulflow Engine", "Lesser Soulflow Engine",
                    "Budget Hopper", "Enchanted Hopper", "Corrupt Soil",
                    "Mithril Infusion", "Berberis Fuel Injector", "Flycatcher",
                    "Sleepy Hollow", "Free Will",
                    "Fishing Minion XII Upgrade Stone",
                    "Clay Minion XII Upgrade Stone",
                    "Revenant Minion XII Upgrade Stone",
                    "Tarantula Minion XII Upgrade Stone",
                ],
                "Fuels": [
                    "Enchanted Lava Bucket", "Magma Bucket", "Plasma Bucket",
                    "Hamster Wheel", "Foul Flesh", "Power Crystal", "Catalyst",
                    "Hyper Catalyst", "Solar Panel", "Oil Barrel",
                    "Scorched Power Crystal", "Volta",
                ],
            },
        },

        "Essence": [
            "Wither Essence", "Spider Essence", "Undead Essence",
            "Dragon Essence", "Gold Essence", "Diamond Essence",
            "Ice Essence", "Crimson Essence", "Forest Essence",
        ],

        "Events": {
            "Spooky": [
                "Green Candy", "Purple Candy", "Dark Candy", "Ectoplasm",
                "Pumpkin Guts", "Spooky Fragment", "Werewolf Skin",
                "Soul Fragment", "Bat Firework", "Blast o' Lantern",
                "Horseman's Candle", "Expired Pumpkin",
            ],
            "Winter": [
                "White Gift", "Green Gift", "Red Gift", "Party Gift",
                "Refined Bottle of Jyrre", "Volcanic Rock",
            ],
            "Minerals": [
                "Refined Mineral", "Glossy Gemstone", "Jacob's Ticket",
                "Agatha's Coupon",
            ],
            "Mythological": [
                "Griffin Feather", "Daedalus Stick",
                "Ancient Claw", "Enchanted Ancient Claw",
            ],
            "Fishing Festival": [
                "Nurse Shark Tooth", "Blue Shark Tooth", "Tiger Shark Tooth",
                "Great White Shark Tooth", "Shark Fin",
                "Enchanted Shark Fin", "Great White Tooth Meal",
            ],
            "Jerry Boxes": [
                "Green Jerry Box", "Blue Jerry Box",
                "Purple Jerry Box", "Golden Jerry Box",
            ],
            "Diaz": [
                "Avaricious Chalice", "Freshly-Minted Coins",
                "Blood-Stained Coins", "Blood-Soaked Coins",
            ],
            "Hoppity's Hunt": [
                "Supreme Chocolate Bar", "Refined Dark Cacao Truffle",
            ],
            "Year of the Seal": [
                "Bouncy Beach Ball", "Giant Bouncy Beach Ball",
            ],
        },

        "Consumables": [
            "Magical Mushroom Soup", "Mystical Mushroom Soup",
            "Metaphysical Serum",
            "Dwarven O's Ore Oats", "Dwarven O's Block Bran",
            "Dwarven O's Gemstone Grahams", "Dwarven O's Metallic Minis",
            "Spotlite", "Moby-Duck: Collector's Edition",
            "Vial of Venom", "Festering Maggot",
        ],

        "Cross-Dimensional": [
            "Lush Berberis", "Enchanted Lush Berberis", "Agarimoo Tongue",
            "Exportable Carrots", "Hemovibe", "Hemoglass", "Hemobomb",
            "Highlite", "Extremely Real Shuriken",
        ],

        "Upgrade Fragments": [
            "Bonzo Fragment", "Dark Queen's Soul", "Golden Fragment",
            "Livid Fragment", "Scarf Fragment", "Thorn Fragment",
            "Winter Fragment",
        ],
    },
    
    "Unknown": {
        "Uncategorized": [],
    },
}