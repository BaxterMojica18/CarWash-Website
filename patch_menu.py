with open('/app/frontend/js/menu.js', 'r', encoding='utf-8') as f:
    menu = f.read()

# 1. Add Tickets tab after admin tabs block
old = "            { name: 'Settings', href: 'settings.html', icon: 'settings' }\n        ];\n    }\n\n\n    // 1. Add Role-specific Tabs"
new = "            { name: 'Settings', href: 'settings.html', icon: 'settings' }\n        ];\n    }\n\n    // Owner/superadmin only: Tickets tab\n    const isOwner = roles.includes('superadmin') || roles.includes('owner');\n    if (!isClient && isOwner) {\n        tabsToRender = [...tabsToRender, { name: 'Tickets', href: 'tickets.html', icon: 'tickets' }];\n    }\n\n\n    // 1. Add Role-specific Tabs"
if old in menu:
    menu = menu.replace(old, new)
    print('Tickets tab: OK')
else:
    print('Tickets tab: NOT FOUND, trying alt...')
    # Try without double newline
    old2 = "            { name: 'Settings', href: 'settings.html', icon: 'settings' }\n        ];\n    }\n\n    // 1. Add Role-specific Tabs"
    new2 = "            { name: 'Settings', href: 'settings.html', icon: 'settings' }\n        ];\n    }\n\n    // Owner/superadmin only: Tickets tab\n    const isOwner = roles.includes('superadmin') || roles.includes('owner');\n    if (!isClient && isOwner) {\n        tabsToRender = [...tabsToRender, { name: 'Tickets', href: 'tickets.html', icon: 'tickets' }];\n    }\n\n    // 1. Add Role-specific Tabs"
    if old2 in menu:
        menu = menu.replace(old2, new2)
        print('Tickets tab alt: OK')
    else:
        print('Tickets tab: STILL NOT FOUND')

# 2. Add tickets icon to icons dict
old3 = "        'audit-logs':"
new3 = "        'tickets': '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\"/></svg>',\n        'audit-logs':"
if old3 in menu:
    menu = menu.replace(old3, new3, 1)
    print('Icon: OK')
else:
    print('Icon: NOT FOUND')

# 3. Add tickets key in normalizeSidebarIcons
old4 = "        else if (lowerText.includes('audit')) key = 'audit-logs';"
new4 = "        else if (lowerText.includes('audit')) key = 'audit-logs';\n        else if (lowerText.includes('ticket')) key = 'tickets';"
if old4 in menu:
    menu = menu.replace(old4, new4)
    print('Key: OK')
else:
    print('Key: NOT FOUND')

with open('/app/frontend/js/menu.js', 'w', encoding='utf-8') as f:
    f.write(menu)

print('Done. tickets.html in menu:', 'tickets.html' in menu)
