from talon import actions, app, Module, Context

def on_region_1():
    print('Region 1 activated')

def on_region_2():
    print('Region 2 activated')

def register_dwell_toolbar():
    print('Registering Dwell Toolbar')
    keys = [
	    actions.user.hud_create_virtual_key(
            action=on_region_1,
            text='Region 1',
            colour='FF0000',
            text_colour='FFFFFF',
            # x=0, # automatic if not specified
            # y=0,
            # width=300,
            # height=300,
        ),
        actions.user.hud_create_virtual_key(
            action=on_region_2,
            text='Region 2',
            colour='00FF00',
            text_colour='FFFFFF',
            # x=0, # automatic if not specified
            # y=300,
            # width=300,
            # height=300,
        )
	]
    actions.user.hud_register_dwell_toolbar('dwell_actions', keys)

# app.register('ready', register_dwell_toolbar)