# Este programa lee y muestra la información de un archivo XML
# Se necesitan conocimientos MÍNIMOS de Python.

import xml.etree.ElementTree as ET

# --- CONFIGURACIÓN ---
XML_FILE = 'incidencies.xml'  # ¡ARCHIVO XML ACTUALIZADO!
RECORD_TAG = 'Incidencia'
# ----------------------

def mostrar_datos_xml_supersimples(archivo_xml):
    # 1. Cargar el archivo XML
    arbol = ET.parse(archivo_xml)
    raiz = arbol.getroot()

    print("--- INICIO DE DATOS XML ---")

    contador = 0

    # 2. Recorrer cada registro de incidencia
    for registro in raiz.findall(RECORD_TAG):
        contador += 1

        print(f"\nREGISTRO {contador}:")

        # 3. Recorrer todos los campos dentro de este registro
        for campo in registro.iter():
            # Mostramos el nombre de la etiqueta (campo.tag) y su valor (campo.text)
            if campo.text and campo.tag != RECORD_TAG:
                print(f"  - {campo.tag}: {campo.text.strip()}")

    print("\n--- FIN DE DATOS XML ---")

# --- Ejecución ---
if __name__ == "__main__":
    mostrar_datos_xml_supersimples(XML_FILE)