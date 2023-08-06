moon_ping = ['MoonminingExtractionFinished']
moon_ping_admin = ['MoonminingAutomaticFracture', 'MoonminingExtractionStarted', 'MoonminingLaserFired']
"""
def process_ping(_id, _title, _content, _fields, _timestamp, _catagory, _col, _img, _url, _footer):
    custom_data = {'color': _col, 
                    'title': _title, 
                    'description': _content, 
                    'timestamp': _timestamp.replace(tzinfo=None).isoformat(),
                    'fields': _fields}
    if _img:
        custom_data['image'] = {'url': _img}
    if _footer:
        custom_data['footer'] = _footer

    return custom_data

if notification.notification_type == "MoonminingLaserFired":
    title = "Moon Laser Fired"
    notification_data = yaml.load(notification.notification_text)

    # firedBy: 824787891
    # firedByLink: <a href="showinfo:1380//824787891">PoseDamen</a>
    # moonID: 40291428
    # oreVolumeByType:
    #   45493: 1983681.4476127427
    #   46679: 2845769.539271295
    #   46681: 2046606.19987059
    #   46688: 2115548.2348155645
    # solarSystemID: 30004612
    # structureID: 1029754054149
    # structureLink: <a href="showinfo:35835//1029754054149">NY6-FH - ISF Two</a>
    # structureName: NY6-FH - ISF Two
    # structureTypeID: 35835

    system_name = MapSolarSystem.objects.get(
        solarSystemID=notification_data['solarSystemID']).solarSystemName
    system_name = '[%s](http://evemaps.dotlan.net/system/%s)' % \
                (system_name,
                system_name.replace(' ', '_'))
    structure_type = TypeName.objects.get(type_id=notification_data['structureTypeID']).name
    structure_name = notification_data['structureName']
    if len(structure_name)<1:
        structure_name = "Unknown"

    body = "Fired By [{0}](https://zkillboard.com/search/{1}/)".format(strip_tags(notification_data['firedByLink']), strip_tags(notification_data['firedByLink']).replace(" ", "%20"))

    timestamp = notification.timestamp
    corp_id = notification.character.character.corporation_id
    corp_ticker = notification.character.character.corporation_ticker
    footer = {"icon_url": "https://imageserver.eveonline.com/Corporation/%s_64.png" % (str(corp_id)),
                "text": "%s (%s)" % (notification.character.character.corporation_name, corp_ticker)}

    fields = [{'name': 'Structure', 'value': structure_name, 'inline': True},
                {'name': 'System', 'value': system_name, 'inline': True},
                {'name': 'Type', 'value': structure_type, 'inline': True},
                ]

    ping = process_ping(notification.notification_id,
                        title,
                        body,
                        fields,
                        timestamp,
                        "moon",
                        16756480,
                        False,
                        False,
                        footer)

    if ping:
        for hook in moon_hooks_admin:
            if hook.corporation is None:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            elif hook.corporation.corporation_id == notification.character.character.corporation_id:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            else:
                pass  # ignore

elif notification.notification_type == "MoonminingExtractionStarted":
    title = "Moon Extraction Started"
    notification_data = yaml.load(notification.notification_text)

    # autoTime: 132071260201940545
    # moonID: 40291428
    # oreVolumeByType:
    #   45493: 2742775.374017656
    #   46679: 3934758.0841854215
    #   46681: 2829779.495126257
    #   46688: 2925103.528079887
    # readyTime: 132071130601940545
    # solarSystemID: 30004612
    # startedBy: 824787891
    # startedByLink: <a href="showinfo:1380//824787891">PoseDamen</a>
    # structureID: 1029754054149
    # structureLink: <a href="showinfo:35835//1029754054149">NY6-FH - ISF Two</a>
    # structureName: NY6-FH - ISF Two
    # structureTypeID: 35835

    system_name = MapSolarSystem.objects.get(
        solarSystemID=notification_data['solarSystemID']).solarSystemName
    system_name = '[%s](http://evemaps.dotlan.net/system/%s)' % \
            (system_name,
            system_name.replace(' ', '_'))

    structure_type = TypeName.objects.get(type_id=notification_data['structureTypeID']).name
    structure_name = notification_data['structureName']
    if len(structure_name)<1:
        structure_name = "Unknown"

    body = "Started By [{0}](https://zkillboard.com/search/{1}/)".format(strip_tags(notification_data['startedByLink']), strip_tags(notification_data['startedByLink']).replace(" ", "%20"))
    timestamp = notification.timestamp
    corp_id = notification.character.character.corporation_id
    corp_ticker = notification.character.character.corporation_ticker
    footer = {"icon_url": "https://imageserver.eveonline.com/Corporation/%s_64.png" % (str(corp_id)),
                "text": "%s (%s)" % (notification.character.character.corporation_name, corp_ticker)}

    ready_time = filetime_to_dt(notification_data['readyTime'])

    fields = [{'name': 'Structure', 'value': structure_name, 'inline': True},
                {'name': 'System', 'value': system_name, 'inline': True},
                {'name': 'Type', 'value': structure_type, 'inline': True},
                {'name': 'Date Ready', 'value': ready_time.strftime("%Y-%m-%d %H:%M"), 'inline': False}
    ]

    ping = process_ping(notification.notification_id,
                        title,
                        body,
                        fields,
                        timestamp,
                        "moon",
                        6881024,
                        False,
                        False,
                        footer)

    if ping:
        for hook in moon_hooks_admin:
            if hook.corporation is None:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            elif hook.corporation.corporation_id == notification.character.character.corporation_id:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            else:
                pass  # ignore

elif notification.notification_type == "MoonminingAutomaticFracture":
    title = "Moon Auto-Fractured!"
    notification_data = yaml.load(notification.notification_text)

    # moonID: 40291417
    # oreVolumeByType:
    #   45492: 1524501.871099406
    #   46677: 2656351.8252801565
    #   46678: 1902385.1244004236
    #   46681: 2110988.956997792
    # solarSystemID: 30004612
    # structureID: 1030287515076
    # structureLink: <a href="showinfo:35835//1030287515076">NY6-FH - ISF-5</a>
    # structureName: NY6-FH - ISF-5
    # structureTypeID: 35835

    system_name = MapSolarSystem.objects.get(
        solarSystemID=notification_data['solarSystemID']).solarSystemName
    system_name = '[%s](http://evemaps.dotlan.net/system/%s)' % \
            (system_name,
            system_name.replace(' ', '_'))

    structure_type = TypeName.objects.get(type_id=notification_data['structureTypeID']).name
    structure_name = notification_data['structureName']
    if len(structure_name)<1:
        structure_name = "Unknown"

    body = "Ready To Mine!"
    timestamp = notification.timestamp
    corp_id = notification.character.character.corporation_id
    corp_ticker = notification.character.character.corporation_ticker
    footer = {"icon_url": "https://imageserver.eveonline.com/Corporation/%s_64.png" % (str(corp_id)),
                "text": "%s (%s)" % (notification.character.character.corporation_name, corp_ticker)}
    
    fields = [{'name': 'Structure', 'value': structure_name, 'inline': True},
                {'name': 'System', 'value': system_name, 'inline': True},
                {'name': 'Type', 'value': structure_type, 'inline': True},

    ]

    ping = process_ping(notification.notification_id,
                        title,
                        body,
                        fields,
                        timestamp,
                        "moon",
                        65533,
                        False,
                        False,
                        footer)

    if ping:
        for hook in moon_hooks_admin:
            if hook.corporation is None:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            elif hook.corporation.corporation_id == notification.character.character.corporation_id:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            else:
                pass  # ignore

elif notification.notification_type in moon_ping:
moon_hooks = discord_hooks.filter(moon_ping=True)

if notification.notification_type == "MoonminingExtractionFinished":
    title = "Moon Extraction Complete"
    notification_data = yaml.load(notification.notification_text)

    # autoTime: 132052212600000000
    # moonID: 40291390
    # oreVolumeByType:
    #   45490: 1588072.4935986102
    #   46677: 2029652.6969759
    #   46679: 3063178.818627033
    #   46682: 2839990.2933705184
    # solarSystemID: 30004612
    # structureID: 1029754067191
    # structureLink: <a href="showinfo:35835//1029754067191">NY6-FH - ISF Three</a>
    # structureName: NY6-FH - ISF Three
    # structureTypeID: 35835

    system_name = MapSolarSystem.objects.get(
        solarSystemID=notification_data['solarSystemID']).solarSystemName
    system_name = '[%s](http://evemaps.dotlan.net/system/%s)' % \
            (system_name,
            system_name.replace(' ', '_'))
    
    structure_type = TypeName.objects.get(type_id=notification_data['structureTypeID']).name
    structure_name = notification_data['structureName']
    if len(structure_name)<1:
        structure_name = "Unknown"

    body = "Ready to Fracture!"
    timestamp = notification.timestamp
    corp_id = notification.character.character.corporation_id
    corp_ticker = notification.character.character.corporation_ticker
    footer = {"icon_url": "https://imageserver.eveonline.com/Corporation/%s_64.png" % (str(corp_id)),
                "text": "%s (%s)" % (notification.character.character.corporation_name, corp_ticker)}

    auto_time = filetime_to_dt(notification_data['autoTime'])
    ores = {}       
    totalm3 = 0
    for t,q in notification_data['oreVolumeByType'].items():
        ores[t] = TypeName.objects.get(type_id=t).name
        totalm3 += q
    ore_string = []
    for t,q in notification_data['oreVolumeByType'].items():
        ore_string.append(
            "**{}**: {:2.1f}%".format(
                ores[t],
                q/totalm3*100
            )
        )
    fields = [{'name': 'Structure', 'value': structure_name, 'inline': True},
                {'name': 'System', 'value': system_name, 'inline': True},
                {'name': 'Type', 'value': structure_type, 'inline': True},
                {'name': 'Auto Fire', 'value': auto_time.strftime("%Y-%m-%d %H:%M"), 'inline': False},
                {'name': 'Ore', 'value': "\n".join(ore_string)},
    ]

    ping = process_ping(notification.notification_id,
                        title,
                        body,
                        fields,
                        timestamp,
                        "moon",
                        6881024,
                        False,
                        False,
                        footer)

    if ping:
        for hook in moon_hooks:
            if hook.corporation is None:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            elif hook.corporation.corporation_id == notification.character.character.corporation_id:
                embed_lists[hook.discord_webhook]['embeds'].append(ping)
            else:
                pass  # ignore
"""