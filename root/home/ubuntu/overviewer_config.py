def signFilter(poi):
    text = None

    icons = ["signpost", "anvil", "anvil_red", "base_plain_red.svg", "base_plain.svg", "factory", "factory_red", "hoe", "hoe_red", "home_2x", "home", "location_2x", "location", "mine", "mine_red", "ship", "ship_red", "tower", "tower_red", "town", "town_red"]

    if poi['id'] == 'Sign' or poi['id'] == 'minecraft:sign':
        if (poi['Text1'] == 'Welcome to' or poi['Text1'] == 'Base:') and poi['Text2']:
            poi['icon'] = "markers/marker_home.png"
            text = poi['Text2']
        elif poi['Text3'] == 'icon:' and poi['Text4'] in icons:
            icon = poi['Text4']
            text = "\n".join([poi['Text1'], poi['Text2']])
            if icon != "signpost":
                icon = "markers/marker_%s" % (icon)

            icon = "%s.png" % (icon)
            poi['icon'] = icon

    return text

worlds["Cantina"] = "/srv/minecraft/world"

renders["overworld_daytime"] = {
    "world": "Cantina",
    "title": "Overworld Daytime",
    "dimension": "overworld",
    "rendermode": "smooth_lighting",
    "markers": [{"name": "Marked Locations", "filterFunction": signFilter, "checked": True}],
}

renders["nether"] = {
    "world": "Cantina",
    "title": "Nether",
    "dimension": "nether",
    "rendermode": "nether_smooth_lighting",
    "markers": [{"name": "Marked Locations", "filterFunction": signFilter, "checked": True}],
}

outputdir = "/srv/http/overviewer"
