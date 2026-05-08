content = open('/app/app/main.py', 'rb').read().decode('utf-8')

old1 = '    audit_logs,\r\n\r\n    notifications,\r\n)'
new1 = '    audit_logs,\r\n\r\n    notifications,\r\n    support_tickets,\r\n)'
content = content.replace(old1, new1)

old2 = 'app.include_router(\r\n    notifications.router, prefix="/api/notifications", tags=["Notifications"]\r\n)'
new2 = 'app.include_router(\r\n    notifications.router, prefix="/api/notifications", tags=["Notifications"]\r\n)\r\napp.include_router(support_tickets.router, prefix="/api/support-tickets", tags=["Support Tickets"])'
content = content.replace(old2, new2)

open('/app/app/main.py', 'wb').write(content.encode('utf-8'))
print('Done:', 'support_tickets' in content)
