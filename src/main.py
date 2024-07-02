from deobf import Deobf

if __name__ == '__main__':
    Deobf("AchievementTemplateTb").save_deobfuscated(makeID="AchievementID")
    Deobf("AvatarBaseTemplateTb").save_deobfuscated(makeID="ID")
    Deobf("EquipmentSuitTemplateTb").save_deobfuscated(makeID="ID")
    Deobf("ItemTemplateTb").save_deobfuscated(makeID="ID")
    Deobf("WeaponTemplateTb").save_deobfuscated(makeID="ItemID")
