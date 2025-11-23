# ----------------------------------------------------------------------------
# OBJECTIU: Filtra incidències per prioritat d'1 a 4, les mostra una a una (paginació),
#           i desa el resultat en un fitxer JSON (sempre sobreescrivint l'anterior).
# ----------------------------------------------------------------------------

# ================================
# === SECCIÓ 1: IMPORTACIONS ESSENCIALS ===
# ================================

import xml.etree.ElementTree as ET  # Per llegir i parsejar XML.
import os  # Per comprovar l'existència del fitxer.
import json  # Per guardar les dades en format JSON.
from colorama import Fore, Style, init  # Per afegir colors a la consola.

# Inicialitza colorama.
init(autoreset=True)

# ================================
# === SECCIÓ 2: CONFIGURACIÓ DE CONSTANTS ===
# ================================

XML_FILE = 'incidencies.xml'  # Fitxer de dades XML.
JSON_FILE = 'incidencies.json'  # Fitxer de dades JSON.
RECORD_TAG = 'Incidencia'  # Etiqueta principal de cada registre.
CAMPO_PRIORIDAD = 'Prioritat_de_lincidncia'  # Etiqueta amb el valor de la prioritat.
FIELD_SEPARATOR = '-'  # Separador visual per als camps.

# ---------------------------------------------
# ================================
# === FUNCIONS D'EMMAGATZEMATGE JSON (MÉS SIMPLE) ===
# ================================

def xml_to_dict(registre):
    # Converteix un element XML d'incidència a un diccionari,
    # preparant-lo per a ser guardat en JSON.
    incidencia_dict = {}
    for camp in registre.iter():
        if camp.text and camp.tag != RECORD_TAG:
            incidencia_dict[camp.tag] = camp.text.strip()
    return incidencia_dict

def emmagatzemar_json(registres_filtrats_xml):
    """
    Guarda el llistat d'incidències en el fitxer JSON_FILE,
    sobreescrivint sempre el contingut anterior.
    """
    # 1. Converteix els registres XML a diccionaris.
    noves_incidencies = [xml_to_dict(registre) for registre in registres_filtrats_xml]

    if not noves_incidencies:
        print(Fore.YELLOW + "\n[JSON] No hi ha incidències per desar." + Style.RESET_ALL)
        return

    # 2. Desament final (mode 'w' sobreescriu).
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(noves_incidencies, f, indent=4, ensure_ascii=False)
        print(Fore.GREEN + f"\n[JSON] Dades desades amb èxit a '{JSON_FILE}' (Fitxer sobreescrit)." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[ERROR JSON] Error al desar el fitxer: {e}" + Style.RESET_ALL)


# ---------------------------------------------

def executar_filtre_prioritat(fitxer_xml):
    # ================================
    # === SECCIÓ 3: COMPROVACIÓ D'ARXIU ===
    # ================================

    if not os.path.exists(fitxer_xml):
        print(Fore.RED + "=" * 60, f"\nERROR: Fitxer '{fitxer_xml}' no trobat.", "\n" + "=" * 60 + Style.RESET_ALL)
        return

    try:
        # Carregar l'XML i obtenir l'element arrel.
        raiz = ET.parse(fitxer_xml).getroot()

        # Mostrar capçalera.
        print(Fore.CYAN + "\n" + "-" * 50)
        print(Fore.MAGENTA + f" {Style.BRIGHT}FILTRE D'INCIDÈNCIES PER PRIORITAT")
        print(" Prioritat: 1 = Baixa, 4 = Urgent ")
        print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

        # ================================
        # === SECCIÓ 4: VALIDACIÓ I OBTENCIÓ DE LA PRIORITAT ===
        # ================================

        prioritat_nombre = None
        # Bucle: Assegura que l'entrada sigui 1, 2, 3 o 4.
        while prioritat_nombre is None:
            prioritat_input = input("Introdueix la prioritat numèrica de l'1 al 4: ").strip()

            if not prioritat_input:
                return print("\nEl programa ha terminat. Adéu!")

            try:
                p_int = int(prioritat_input)
                if 1 <= p_int <= 4:
                    prioritat_nombre = p_int
                else:
                    print(Fore.YELLOW + "\n⚠️ Si us plau, introdueix un nombre entre 1 i 4.\n" + Style.RESET_ALL)
            except ValueError:
                print(Fore.YELLOW + "\n⚠️ Entrada no vàlida. Introdueix un nombre enter.\n" + Style.RESET_ALL)

        valor_cercat_str = str(prioritat_nombre)
        etiqueta_cerca = f"prioritat de nivell {valor_cercat_str}"

        # ================================
        # === SECCIÓ 5: FILTRATGE DE REGISTRES (LIST COMPREHENSION) ===
        # ================================

        registres_trobats = [
            registre
            for registre in raiz.findall(RECORD_TAG)
            # Condició: el camp de prioritat existeix I el seu valor coincideix.
            if registre.find(CAMPO_PRIORIDAD) is not None and
               registre.find(CAMPO_PRIORIDAD).text.strip() == valor_cercat_str
        ]

        comptador = len(registres_trobats)

        # ================================
        # === SECCIÓ 6: RESUM DE RESULTATS ===
        # ================================

        print(Fore.RED + "\n" + "=" * 55)
        if comptador == 0:
            print(f"🚫 No s'han trobat registres amb {etiqueta_cerca}.")
        else:
            print(Fore.LIGHTRED_EX + f"S'han trobat {comptador} incidències amb {etiqueta_cerca}." + Style.RESET_ALL)
        print(Fore.RED + "=" * 55 + Style.RESET_ALL)

        # ================================
        # === SECCIÓ 7: VISUALITZACIÓ PAGINADA (PAS A PAS) ===
        # ================================

        if comptador > 0:
            print("\nIniciant visualització d'incidencies una a una:\n")

            for i, registre in enumerate(registres_trobats):
                # Pausa: Espera la tecla Enter.
                prompt_text = "Prem enter per veure la primera incidència:" if i == 0 else "\nPrem enter per veure la següent incidència:"
                input(Fore.LIGHTGREEN_EX + prompt_text + Style.RESET_ALL)

                # Capçalera de la incidència.
                print(Fore.LIGHTYELLOW_EX + f"\n✅ Incidència {i + 1} de {comptador}:\n" + Style.RESET_ALL)

                # Itera i imprimeix tots els camps amb format.
                for camp in registre.iter():
                    if camp.text and camp.tag != RECORD_TAG:
                        # Alinea el nom del camp a 30 espais.
                        print(f"  {FIELD_SEPARATOR} {camp.tag:<30}: {camp.text.strip()}")

            # Fi de la llista.
            print(Fore.BLUE + "-" * 35 + Style.RESET_ALL)
            print(Fore.LIGHTRED_EX + "\nFi de la llista d'incidències." + Style.RESET_ALL)


        # ================================
        # === SECCIÓ 7.5: EMMAGATZEMATGE EN JSON ===
        # ================================

        if comptador > 0:
            emmagatzemar_json(registres_trobats)

        print("\nPrograma finalitzat!")

    # ================================
    # === SECCIÓ 8: GESTIÓ D'EXCEPCIONS ===
    # ================================

    except ET.ParseError as e:
        print(Fore.RED + f"\nERROR en llegir l'XML: El fitxer està mal format. Detall: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nERROR inesperat: {e}" + Style.RESET_ALL)


# ================================
# === SECCIÓ 9: PUNT D'EXECUCIÓ ===
# ================================

# Crida la funció principal.
if __name__ == "__main__":
    executar_filtre_prioritat(XML_FILE)