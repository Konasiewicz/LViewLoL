import math
import sys

from lview import *

lview_script_info = {
    "script": "GoSuAwareness",
    "author": "ported by krankkk",
    "description": "GoSuAwareness"
}

drawJungleInfo = True
drawEnemyAARange = True
enemyAARangeColor = Color(64, 192, 192, 192)
drawEnemySpellRanges = True
enemyQRangeColor = Color(64, 0, 250, 154)
enemyWRangeColor = Color(64, 218, 112, 214)
enemyERangeColor = Color(64, 255, 140, 0)
enemyRRangeColor = Color(64, 220, 20, 60)
drawAALeft = True
drawCooldowns = True
trackRecalls = True


def lview_load_cfg(cfg):
    global drawJungleInfo, drawEnemyAARange, enemyAARangeColor, drawEnemySpellRanges, enemyQRangeColor, enemyWRangeColor, enemyERangeColor, enemyRRangeColor
    global drawAALeft, drawCooldowns, trackRecalls
    drawJungleInfo = cfg.get_bool("drawJungleInfo", drawJungleInfo)
    drawEnemyAARange = cfg.get_bool("drawEnemyAARange", drawEnemyAARange)
    drawAALeft = cfg.get_bool("drawAALeft", drawAALeft)
    drawCooldowns = cfg.get_bool("drawCooldowns", drawCooldowns)
    trackRecalls = cfg.get_bool("trackRecalls", trackRecalls)
    drawEnemySpellRanges = cfg.get_bool("drawEnemySpellRanges", drawEnemySpellRanges)
    enemyAARangeColor = strToColor(cfg.get_str("enemyAARangeColor", colorToStr(enemyAARangeColor)))
    enemyQRangeColor = strToColor(cfg.get_str("enemyQRangeColor", colorToStr(enemyQRangeColor)))
    enemyWRangeColor = strToColor(cfg.get_str("enemyWRangeColor", colorToStr(enemyWRangeColor)))
    enemyERangeColor = strToColor(cfg.get_str("enemyERangeColor", colorToStr(enemyERangeColor)))
    enemyRRangeColor = strToColor(cfg.get_str("enemyRRangeColor", colorToStr(enemyRRangeColor)))


def lview_save_cfg(cfg):
    global drawJungleInfo, drawEnemyAARange, enemyAARangeColor, drawEnemySpellRanges, enemyQRangeColor, enemyWRangeColor, enemyERangeColor, enemyRRangeColor
    global drawAALeft, drawCooldowns, trackRecalls
    cfg.set_bool("drawJungleInfo", drawJungleInfo)
    cfg.set_bool("drawEnemyAARange", drawEnemyAARange)
    cfg.set_bool("drawAALeft", drawAALeft)
    cfg.set_bool("drawCooldowns", drawCooldowns)
    cfg.set_bool("trackRecalls", trackRecalls)
    cfg.set_bool("drawEnemySpellRanges", drawEnemySpellRanges)
    cfg.set_str("enemyAARangeColor", colorToStr(enemyAARangeColor))
    cfg.set_str("enemyQRangeColor", colorToStr(enemyQRangeColor))
    cfg.set_str("enemyWRangeColor", colorToStr(enemyWRangeColor))
    cfg.set_str("enemyERangeColor", colorToStr(enemyERangeColor))
    cfg.set_str("enemyRRangeColor", colorToStr(enemyRRangeColor))


def lview_draw_settings(game, ui):
    global drawJungleInfo, drawEnemyAARange, enemyAARangeColor, drawEnemySpellRanges, enemyQRangeColor, enemyWRangeColor, enemyERangeColor, enemyRRangeColor
    global drawAALeft, drawCooldowns, trackRecalls
    drawJungleInfo = ui.checkbox("Draw Jungler Info", drawJungleInfo)
    drawEnemyAARange = ui.checkbox("Draw Enemy AA Range", drawEnemyAARange)
    if drawEnemyAARange and ui.treenode("Change Color of AA Range"):
        enemyAARangeColor = ui.colorpick("AA Range Color", enemyAARangeColor)
        ui.treepop()
    drawEnemySpellRanges = ui.checkbox("Draw Enemy Spell Ranges", drawEnemySpellRanges)
    if drawEnemySpellRanges and ui.treenode("Change Color of Spell Range"):
        enemyQRangeColor = ui.colorpick("Q Range Color", enemyQRangeColor)
        enemyWRangeColor = ui.colorpick("W Range Color", enemyWRangeColor)
        enemyERangeColor = ui.colorpick("E Range Color", enemyERangeColor)
        enemyRRangeColor = ui.colorpick("R Range Color", enemyRRangeColor)
        ui.treepop()
    drawAALeft = ui.checkbox("Draw AA\'s left", drawAALeft)
    drawCooldowns = ui.checkbox("Show Cooldowns", drawCooldowns)
    trackRecalls = ui.checkbox("Track Recalls", trackRecalls)


def lview_update(game, ui):
    self = game.player
    for champion in game.champs:
        if champion.is_enemy_to(self):
            if isValidTarget(self, champion, 3000):
                if drawEnemyAARange:
                    game.draw_circle_world(champion.pos, champion.atk_range + champion.gameplay_radius, 100, 2, enemyAARangeColor)
                if drawEnemySpellRanges:
                    game.draw_circle_world(champion.pos, champion.Q.cast_range, 100, 2, enemyQRangeColor)
                    game.draw_circle_world(champion.pos, champion.W.cast_range, 100, 2, enemyWRangeColor)
                    game.draw_circle_world(champion.pos, champion.E.cast_range, 100, 2, enemyERangeColor)
                    game.draw_circle_world(champion.pos, champion.R.cast_range, 100, 2, enemyRRangeColor)
                if drawAALeft:
                    AALeft = champion.health / CalcPhysicalDamage(self, champion, self.base_atk + self.bonus_atk)
                    game.draw_text(game.hp_bar_pos(champion).add(Vec2(80, 10)), str(math.ceil(AALeft)), Color.WHITE)
            if drawCooldowns and isValidTarget(self, champion):
                p = game.hp_bar_pos(champion)
                p.x -= 70
                if game.is_point_on_screen(p):
                    p.x += 25
                    draw_spell(game, champion.Q, p, 24)
                    p.x += 25
                    draw_spell(game, champion.W, p, 24)
                    p.x += 25
                    draw_spell(game, champion.E, p, 24)
                    p.x += 25
                    draw_spell(game, champion.R, p, 24)
                    p.x += 37
                    p.y -= 32
                    draw_spell(game, champion.D, p, 15, False, True)
                    p.y += 16
                    draw_spell(game, champion.F, p, 15, False, True)
            if drawJungleInfo:
                # this will break on multiple smites
                smite = champion.get_summoner_spell(SummonerSpellType.Smite)
                if smite is not None:
                    if not champion.is_alive:
                        game.draw_text(game.hp_bar_pos(self).add(Vec2(300, -20)), "Jungler: Dead", Color.WHITE)
                    else:
                        if not isValidTarget(self, champion):
                            game.draw_text(game.hp_bar_pos(self).add(Vec2(300, -20)), "Jungler: Invisible", Color.GRAY)
                        else:
                            if getDistance(self.pos, champion.pos) > 3000:
                                game.draw_text(game.hp_bar_pos(self).add(Vec2(300, -20)), "Jungler: Visible", Color.WHITE)
                            else:
                                game.draw_text(game.hp_bar_pos(self).add(Vec2(300, -20)), "Jungler: Near", Color.DARK_RED)
            if trackRecalls:
                for buff in champion.buffs:
                    if str(buff.name) == "recall" and buff.end_time > game.time:
                        game.draw_text(game.hp_bar_pos(self).add(Vec2(-20, 300)), champion.name + "started Recalling at " + str(math.ceil(champion.health)) + "HP",
                                       Color.DARK_RED)


def draw_spell(game, spell, pos, size, show_lvl=True, show_cd=True):
    cooldown = spell.get_current_cooldown(game.time)
    color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY

    game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)
    if show_cd and cooldown > 0.0:
        game.draw_text(pos.add(Vec2(4, 5)), str(int(cooldown)), Color.WHITE)
    if show_lvl:
        for i in range(spell.level):
            offset = i * 4
            game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.YELLOW)


def get_color_for_cooldown(cooldown):
    if cooldown > 0.0:
        return Color.DARK_RED
    else:
        return Color(1, 1, 1, 1)


def colorToStr(color):
    r = color.r
    g = color.g
    b = color.b
    a = color.a
    return str(r) + ":" + str(g) + ":" + str(b) + ":" + str(a)


def strToColor(str):
    split = str.split(":")
    return Color(float(split[0]), float(split[1]), float(split[2]), float(split[3]))


def isValidTarget(source, target, range=sys.maxsize):
    return target and target.is_visible and target.is_alive and getDistance(source.pos, target.pos) < range


def getDistance(pos1, pos2):
    return math.sqrt(getDistanceSqr(pos1, pos2))


def getDistanceSqr(pos1, pos2):
    dx = pos1.x - pos2.x
    dz = (pos1.z or pos1.y) - (pos2.z or pos2.y)
    return dx * dx + dz * dz


def CalcPhysicalDamage(source, target, damage):  # todo
    ArmorPenPercent = 1  # source.armorPenPercent
    ArmorPenFlat = 0  # source.armorPen * (0.6 + (0.4 * (target.lvl / 18)))
    BonusArmorPen = 0  # source.bonusArmorPenPercent
    if source.has_tags(UnitTag.Unit_Minion):
        ArmorPenPercent = 1
        ArmorPenFlat = 0
        BonusArmorPen = 1
    elif source.has_tags(UnitTag.Unit_Structure_Turret):
        ArmorPenFlat = 0
        BonusArmorPen = 1
        if source.name.find('3') != -1 or source.name.find('4') != -1:
            ArmorPenPercent = 0.25
        else:
            ArmorPenPercent = 0.7
    if target.has_tags(UnitTag.Unit_Minion):
        damage = damage * 1.25
        if target.name.find('MinionSiege') != -1:
            damage = damage * 0.7
            return damage
    armor = target.armour
    bonusArmor = 0  # target.bonusArmor
    value = 100 / (100 + (armor * ArmorPenPercent) - (bonusArmor * (1 - BonusArmorPen)) - ArmorPenFlat)
    if armor < 0:
        value = 2 - 100 / (100 - armor)
    elif (armor * ArmorPenPercent) - (bonusArmor * (1 - BonusArmorPen)) - ArmorPenFlat < 0:
        value = 1
    return max(0, math.floor(value * damage))
