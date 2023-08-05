from .entities.equipment import Gear

class Mace(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Mace",
            description="A heavy mace.",
            damage=5,
            damage_type="physical",
        )

class Sword(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Sword",
            description="A sharp sword.",
            damage=6,
            damage_type="physical",
        )

class Axe(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Axe",
            description="A sharp axe.",
            damage=7,
            damage_type="physical",
        )

class SideKnife(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="offhand",
            name="Side Knife",
            description="A small knife.",
            damage=2,
            damage_type="physical",
        )

class Dagger(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Dagger",
            description="A sharp dagger.",
            damage=4,
            damage_type="physical",
        )

class Staff(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Staff",
            description="A wooden staff.",
            damage=3,
            damage_type="physical",
        )

class Wand(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Wand",
            description="A magical wand.",
            damage=2,
            damage_type="magical",
        )

class ShortBow(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Short Bow",
            description="A short bow.",
            damage=5,
            damage_type="physical",
        )

class Claymore(Gear):
    def __init__(self) -> None:
        super().__init__(
            category="weapon",
            name="Claymore",
            description="A large, two-handed sword.",
            damage=10,
            damage_type="physical",
        )

class Lute(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Lute",
            description = "A guitar-like musical instrument.",
            damage = 2,
            damage_type = "physical"
        )

class TreeTrunk(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Tree Trunk",
            description = "A large tree, torn from the earth and used as a club.",
            damage = 20,
            damage_type = "physical",
        )

class AncientSword(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Ancient Sword",
            description = "A sword that has been passed down through generations.",
            damage = 15,
            damage_type = "physical",
        )

class DemonSlayer(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Demon Slayer",
            description = "Said to have slain the great demon Azazael. Even if it's not true, this sword is still a work of art.",
            damage = 20,
            damage_type = "physical",
        )

class DragonToothSword(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Dragon Tooth Sword",
            description = "A sword forged from the teeth of a dragon.",
            damage = 20,
            damage_type = "physical",
        )

class ExecutionerSAxe(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Executioner's Axe",
            description = "An axe that was used to execute criminals.",
            damage = 20,
            damage_type = "physical",
        )

class ThunderboltHammer(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Thunderbolt Hammer",
            description = "A hammer forged from the lightning of a thunderstorm. Your hair stands on end when you hold it.",
            damage = 20,
            damage_type = "physical",
        )

class CelestialLance(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Celestial Lance",
            description = "A lance forged from the light of the sun, wielded by the sun god's angels.",
            damage = 20,
            damage_type = "physical",
        )

class WandOfTheArchmage(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Wand of the Archmage",
            description = "The wand given to the Archmage upon being raised to the position by the Council of Eight.",
            damage = 20,
            damage_type = "magical",
        )

class StaffOfTheMagi(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Staff of the Magi",
            description = "The staff of the High Magus.",
            damage = 20,
            damage_type = "magical",
        )

class EldritchOrb(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Eldritch Orb",
            description = "You can feel tentacles at the back of your mind when you gaze into the depths of this orb.",
            damage = 20,
            damage_type = "magical",
        )

class ArcaneCrystal(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Arcane Crystal",
            description = "This crystal seems to hum in the presence of magical objects.",
            damage = 20,
            damage_type = "magical",
        )

class ShadowDagger(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Shadow Dagger",
            description = "A plain wooden hilt whose blade is made of shadow.",
            damage = 20,
            damage_type = "physical",
        )

class VenomousRapier(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Venomous Rapier",
            description = "A rapier coated in blood poison, that somehow can never be wiped clean.",
            damage = 20,
            damage_type = "physical",
        )

class AssassinSCrossbow(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Assassin's Crossbow",
            description = "A well oiled crossbow said to be used by the agents of Khazadh when they assassinated the sun god's high priest.",
            damage = 20,
            damage_type = "physical",
        )
        
class HolyAvengerSword(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Holy Avenger Sword",
            description = "The sword used in vengeance against Khazadh, after he killed the sun god's high priest.",
            damage = 20,
            damage_type = "physical",
        )

class DivineMace(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Divine Mace",
            description = "A great studded mace, inscribed with the sun god's glowing runes.",
            damage = 20,
            damage_type = "physical",
        )

class AngelicBow(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Angelic Bow",
            description = "One of the bows wielded by the sun god's angels.",
            damage = 20,
            damage_type = "physical",
        )

class LanceOfLight(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Lance of Light",
            description = "The great lance given to mortals in the time of the great calamity.",
            damage = 20,
            damage_type = "physical",
        )

class StaffOfHealing(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Staff of Healing",
            description = "A staff inscribed with all of the healing incantations of the sun god's divine order.",
            damage = 20,
            damage_type = "physical",
        )

class DivineWand(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Divine Wand",
            description = "The wand that was given to Aamon the Great by the sun god.",
            damage = 20,
            damage_type = "magical",
        )

class SunburstMace(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Sunburst Mace",
            description = "A shining mace that glows with the sun god's holy light.",
            damage = 20,
            damage_type = "physical",
        )

class ResurrectionScepter(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Resurrection Scepter",
            description= "A scepter said to have brought the mad king back from the dead.",
            damage = 20,
            damage_type = "physical",
        )

class SacredTomeOfKnowledge(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Sacred Tome of Knowledge",
            description = "The sacred book of the god of the sun.",
            damage = 20,
            damage_type = "magical",
        )

class TotemStaff(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Totem Staff",
            description = "A shaft of wood covered in carvings of spirit animals.",
            damage = 20,
            damage_type = "magical",
        )

class SpiritAxe(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Spirit Axe",
            description = "An axe that is not quite corporeal, and strikes the very spirit of its victims.",
            damage = 20,
            damage_type = "physical",
        )

class AncestralBow(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Ancestral Bow",
            description = "A bow that was passed down through generations.",
            damage = 20,
            damage_type = "physical",
        )

class DreamcatcherScepter(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "offhand",
            name = "Dreamcatcher Scepter",
            description = "A scepter that was used by the Dreamcatcher.",
            damage = 20,
            damage_type = "magical",
        )

class DemonBaneDagger(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Demon Bane Dagger",
            description = "When the great demon Azazael fell, one of his horns was carved into this dagger.",
            damage = 20,
            damage_type = "physical",
        )
class NecroticStaff(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Necrotic Staff",
            description = "For some reason you can make out the sound of the moaning dead whenever you are near this gnarled wyrmwood branch.",
            damage = 20,
            damage_type = "magical",
        )
class HellfireWhip(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Hellfire Whip",
            description = "A curling leather whip that always feels hot to the touch.",
            damage = 20,
            damage_type = "physical",
        )
class CursedScythe(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Cursed Scythe",
            description = "A wickedly sharp scythe that always seems to find its mark.",
            damage = 20,
            damage_type = "physical",
        )
class ShadowyTomeOfForbiddenKnowledge(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Shadowy Tome of Forbidden Knowledge",
            description = "A tome held closed with chains, not to prevent users from getting in, but to prevent its contents from escaping.",
            damage = 20,
            damage_type = "magical",
        )
class BladeOfChaos(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Blade of Chaos",
            description = "A razor sharp blade whose attacks are unpredictable and deadly.",
            damage = 20,
            damage_type = "physical",
        )
class BattleaxeOfFury(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Battleaxe of Fury",
            description = "A battleaxe that enhances the natural aggression of its user.",
            damage = 20,
            damage_type = "physical",
        )
class WarhammerOfDestruction(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Warhammer of Destruction",
            description = "An especially wicked looking warhammer.",
            damage = 20,
            damage_type = "physical",
        )

class SpearOfTheConqueror(Gear):
    def __init__(self) -> None:
        super().__init__(
            category = "weapon",
            name = "Spear of the Conqueror",
            description = "An ancient spear, the prized possession of Khazadh the Conqueror.",
            damage = 20,
            damage_type = "physical",
        )