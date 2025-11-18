# Este programa lee un archivo XML y permite filtrar los registros
# basándose ÚNICAMENTE en la Prioridad (1=Baja, 4=Urgente).

import xml.etree.ElementTree as ET
import os

# --- CONFIGURACIÓN ---
XML_FILE = 'incidencies.xml'
RECORD_TAG = 'Incidencia'
# Etiqueta corregida para que coincida con tu XML de muestra
CAMPO_PRIORIDAD = 'Prioritat_de_lincidncia'


# ----------------------

def mostrar_resumen_resultados(registros, valor_buscado, campo_buscado):
    """
    Función auxiliar para imprimir SOLO el resumen del filtro (sin detalles).
    """

    contador_encontrados = len(registros)

    # Etiqueta amigable para el resumen final
    tag_para_resumen = f"Prioridad de nivel {valor_buscado}"

    print("\n" + "=" * 60)
    if contador_encontrados == 0:
        print(f"🚫 No se encontraron registros con {tag_para_resumen}.")
    else:
        # Se muestra el resumen primero
        print(f"⭐ ¡Filtro completado! Se encontraron {contador_encontrados} incidencias con {tag_para_resumen}.")
    print("=" * 60)

    return contador_encontrados


def ejecutar_filtro_prioridad(archivo_xml):
    """
    Función principal que carga el XML, pide la prioridad y realiza el filtro.
    """

    if not os.path.exists(archivo_xml):
        print("=" * 60)
        print(f"ERROR: No se encontró el archivo '{archivo_xml}'.")
        print("Asegúrate de que el archivo existe y el nombre es correcto.")
        print("=" * 60)
        return

    try:
        # Carga del archivo XML
        arbol = ET.parse(archivo_xml)
        raiz = arbol.getroot()

        print("\n" + "=" * 60)
        print(f" --- FILTRO DE INCIDENCIAS POR PRIORIDAD ({archivo_xml}) --- ")
        print(" Prioridad: 1=Baja, 4=Urgente ")
        print("=" * 60)

        prioridad_numero = None

        # Bucle para asegurar que el usuario introduce un número válido (1-4)
        while prioridad_numero is None:
            prioridad_input = input(f"Ingresa la prioridad NUMÉRICA (1 a 4) que deseas buscar: ").strip()

            if not prioridad_input:
                print("\nOperación cancelada. ¡Adiós!")
                return

            try:
                prioridad_int = int(prioridad_input)
                if 1 <= prioridad_int <= 4:
                    prioridad_numero = prioridad_int
                else:
                    print("⚠️ Por favor, ingresa un número entre 1 y 4.")
            except ValueError:
                print("⚠️ Entrada no válida. Por favor, ingresa un número entero.")

        # Convertir el número buscado a cadena para la comparación en el XML
        valor_buscado_str = str(prioridad_numero)
        etiqueta_busqueda = f"Prioridad de nivel {valor_buscado_str}"

        registros_encontrados = []

        print("-" * 60)
        print(f"Buscando registros con {etiqueta_busqueda}...")
        print("-" * 60)

        # 1. Recorrer cada registro de incidencia y filtrar
        for registro in raiz.findall(RECORD_TAG):
            campo_filtro = registro.find(CAMPO_PRIORIDAD)

            if campo_filtro is not None and campo_filtro.text:
                valor_actual = campo_filtro.text.strip()

                if valor_actual == valor_buscado_str:
                    registros_encontrados.append(registro)

        # 2. Mostrar el resumen de los resultados
        contador_encontrados = mostrar_resumen_resultados(registros_encontrados, valor_buscado_str, CAMPO_PRIORIDAD)

        # 3. Pausa y visualización de detalles si hay registros
        if contador_encontrados > 0:
            input("Presiona Enter para ver los detalles de las incidencias...")

            # Bucle para imprimir los detalles de las incidencias
            for i, registro in enumerate(registros_encontrados):
                print(f"\n✅ INCIDENCIA NÚMERO {i + 1} ENCONTRADA:")

                for campo in registro.iter():
                    if campo.text and campo.tag != RECORD_TAG:
                        texto_mostrar = campo.text.strip()
                        print(f"  > {campo.tag:<25}: {texto_mostrar}")

            print("\n" + "=" * 60)

        print("\nPrograma finalizado. ¡Adiós!")

    except ET.ParseError as e:
        print(f"\nERROR al leer el XML: El archivo puede estar mal formado. Detalle: {e}")
    except Exception as e:
        print(f"\nERROR inesperado: {e}")


# --- Ejecución ---
if __name__ == "__main__":
    ejecutar_filtro_prioridad(XML_FILE)