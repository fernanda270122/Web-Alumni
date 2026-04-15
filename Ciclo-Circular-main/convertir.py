with open('backup_datos_j.json', 'rb') as f:
    content = f.read()
with open('backup_datos_j_utf8.json', 'w', encoding='utf-8') as f:
    f.write(content.decode('latin-1'))
print("Listo")