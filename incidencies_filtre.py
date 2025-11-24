# ----------------------------------------------------------------------------
# OBJECTIU: Filtra incidències per prioritat d'1 a 4 i les mostra una a una
# ----------------------------------------------------------------------------

# === SECCIÓ 1: IMPORTACIONS ESSENCIALS ===

import xml.etree.ElementTree as ET  # Per llegir i parsejar XML.
import os  # Per comprovar l'existència del fitxer.
from colorama import Fore, Style, init  # Per afegir colors a la consola.

# Inicialitza colorama.
init(autoreset=True)

# === SECCIÓ 2: CONFIGURACIÓ DE CONSTANTS ===

XML_FILE = 'incidencies.xml'  # Fitxer de dades.
RECORD_TAG = 'Incidencia'  # Etiqueta principal de cada registre.
CAMPO_PRIORIDAD = 'Prioritat_de_lincidncia'  # Etiqueta amb el valor de la prioritat.
FIELD_SEPARATOR = '-'  # Separador visual per als camps.

# ---------------------------------------------

def executar_filtre_prioritat(fitxer_xml):

    # === SECCIÓ 3: COMPROVACIÓ D'ARXIU ===

    if not os.path.exists(fitxer_xml):
        # Error si l'XML no es troba.
        print("=" * 60, f"\nERROR: Fitxer '{fitxer_xml}' no trobat.", "\n" + "=" * 60)
        return

    try:
        # Carregar l'XML i obtenir l'element arrel.
        raiz = ET.parse(fitxer_xml).getroot()

        # Mostrar capçalera.
        print(Fore.CYAN + "\n" + "-" * 50)
        print(Fore.MAGENTA + f" {Style.BRIGHT}FILTRE D'INCIDÈNCIES PER PRIORITAT")
        print(" Prioritat: 1 = Baixa, 4 = Urgent ")
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

        # === SECCIÓ 4: VALIDACIÓ I OBTENCIÓ DE LA PRIORITAT ===

        prioritat_nombre = None
        # Bucle: Assegura que l'entrada sigui 1, 2, 3 o 4.
        while prioritat_nombre is None:
            prioritat_input = input("\n Introdueix la prioritat numèrica de l'1 al 4:\n").strip()

            if not prioritat_input:
                return print("\n El programa ha terminat. Torna a executar-lo per utilitzar-lo.")

            try:
                p_int = int(prioritat_input)
                if 1 <= p_int <= 4:
                    prioritat_nombre = p_int
                else:
                    print("\n⚠️ Si us plau, introdueix un nombre entre 1 i 4.\n")
            except ValueError:
                print("\n⚠️ Entrada no vàlida. Introdueix un nombre enter.\n")

        valor_cercat_str = str(prioritat_nombre)
        etiqueta_cerca = f"prioritat de nivell {valor_cercat_str}"

        # === SECCIÓ 5: FILTRATGE DE REGISTRES (LIST COMPREHENSION) ===

        registres_trobats = [
            registre
            for registre in raiz.findall(RECORD_TAG)
            # Condició: el camp de prioritat existeix I el seu valor coincideix.
            if registre.find(CAMPO_PRIORIDAD) is not None and
               registre.find(CAMPO_PRIORIDAD).text.strip() == valor_cercat_str
        ]

        comptador = len(registres_trobats)

        # === SECCIÓ 6: RESUM DE RESULTATS ===

        print(Fore.RED + "\n" + "=" * 55)
        if comptador == 0:
            print(f" 🚫 No s'han trobat registres amb {etiqueta_cerca}.")
        else:
            print(Fore.LIGHTRED_EX + f" S'han trobat {comptador} incidències amb {etiqueta_cerca}.")
        print(Fore.RED + "=" * 55 + Style.RESET_ALL)

        # === SECCIÓ 7: VISUALITZACIÓ PAGINADA ===

        if comptador > 0:
            print("\n Iniciant visualització d'incidencies una a una:\n")

            for i, registre in enumerate(registres_trobats):
                # Pausa: Espera la tecla Enter.
                prompt_text = " Prem enter per veure la primera incidència\n" if i == 0 else "\n Prem enter per veure la següent incidència\n"
                input(Fore.LIGHTGREEN_EX + prompt_text + Style.RESET_ALL)

                # Capçalera de la incidència (amb color GROC CLAR).
                print(f"\n{Fore.LIGHTYELLOW_EX} ✅ Incidència {i + 1} de {comptador} :{Style.RESET_ALL}\n")

                # Itera i imprimeix tots els camps amb format.
                for camp in registre.iter():
                    if camp.text and camp.tag != RECORD_TAG:
                        # Alinea el nom del camp a 30 espais.
                        print(f"  {FIELD_SEPARATOR} {camp.tag:<30}: {camp.text.strip()}")

            # Fi de la llista.
            print(Fore.LIGHTRED_EX + "\n" + "-" * 60)
            print("\n Fi de la llista d'incidències." + Style.RESET_ALL)

        print("\n Programa finalitzat!")

    # === SECCIÓ 8: GESTIÓ D'EXCEPCIONS ===

    except ET.ParseError as e:
        print(f"\n ERROR en llegir l'XML: El fitxer està mal format. Detall: {e}")
    except Exception as e:
        print(f"\n ERROR inesperat: {e}")

# === SECCIÓ 9: PUNT D'EXECUCIÓ ===

# Crida la funció principal.
if __name__ == "__main__":
    executar_filtre_prioritat(XML_FILE)