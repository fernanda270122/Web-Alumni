with open('backup_datos_j_utf8.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar donde empieza el JSON real
start = content.find('[')
content = content[start:]

with open('backup_datos_j_clean.json', 'w', encoding='utf-8') as f:
    f.write(content)
print("Listo")