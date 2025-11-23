# Aquest programa permet a l'usuari filtrar incidències específiques d'un fitxer XML basant-se en el seu nivell de prioritat (1 a 4).
# Els resultats es mostren un per un, controlats per la tecla Enter.
# ----------------------------------------------------------------------------

import xml.etree.ElementTree as ET  # Mòdul per parsejar (llegir) fitxers XML.
import os  # Mòdul per interactuar amb el sistema operatiu (usat per verificar fitxers).

# --- CONFIGURACIÓ DE FITXERS I ETIQUETES ---

XML_FILE = 'incidencies.xml'  # Nom del fitxer XML que conté les dades.
RECORD_TAG = 'Incidencia'  # Etiqueta principal que defineix un registre individual (una incidència).
# Etiqueta que conté el valor de prioritat (corregida segons la mostra XML de l'usuari).
CAMPO_PRIORIDAD = 'Prioritat_de_lincidncia'
FIELD_SEPARATOR = '-'  # <--- AQUEST ÉS EL SEPARADOR VISUAL. S'HA MANTINGUT EL GUION ('-').


# ---------------------------------------------

def executar_filtre_prioritat(fitxer_xml):
    """Funció principal que orquestra tot el procés de filtratge:
    carrega l'XML, obté l'entrada de l'usuari, filtra i mostra els resultats."""

    # Comprovació d'existència del fitxer: verifica si el fitxer XML existeix abans d'intentar llegir-lo.
    if not os.path.exists(fitxer_xml):
        # El separador s'ha deixat com a "=" aquí ja que és un missatge d'error del sistema.
        print("=" * 60, f"\nERROR: Fitxer '{fitxer_xml}' no trobat.", "\n" + "=" * 60)
        return  # Finalitza l'execució si el fitxer no hi és.

    try:
        # Carregar l'XML: Parsejar el fitxer i obtenir l'element arrel (l'etiqueta <Incidencies>).
        raiz = ET.parse(fitxer_xml).getroot()

        # Mostrar capçalera del programa amb guions (---). S'utilitza la longitud 50.
        print("\n" + "-" * 50, "\n FILTRE D'INCIDÈNCIES PER PRIORITAT")
        print(" Prioritat: 1 = Baixa, 4 = Urgent ", "\n" + "-" * 50)

        # 1. Obtenció i validació de la prioritat
        prioritat_nombre = None
        # Bucle de validació: es repeteix fins que l'usuari introdueixi un nombre vàlid (1-4).
        while prioritat_nombre is None:
            prioritat_input = input("Introdueix la prioritat numèrica de l'1 al 4: ").strip()

            # Si l'usuari no introdueix res i dona a l'Enter s'acaba el programa.
            if not prioritat_input:
                # Text de sortida millorat (gramaticalment correcte).
                return print("\nEl programa ha terminat. Torna a executar-lo per utilitzar-lo.")

            try:
                # Intenta convertir l'entrada a un nombre enter.
                p_int = int(prioritat_input)

                # Comprova si el nombre està dins del rang vàlid (1 a 4).
                if 1 <= p_int <= 4:
                    prioritat_nombre = p_int  # Valor vàlid trobat, surt del bucle.
                else:
                    # Missatge d'error amb salts de línia
                    print("\n⚠️ Si us plau, introdueix un nombre entre 1 i 4.\n")
            except ValueError:
                # Captura l'error si l'entrada no és un nombre.
                # Missatge d'error amb salts de línia
                print("\n⚠️ Entrada no vàlida. Introdueix un nombre enter.\n")

        # Prepara les variables per a la cerca i la sortida de text.
        valor_cercat_str = str(prioritat_nombre)
        etiqueta_cerca = f"prioritat de nivell {valor_cercat_str}"

        # La línia de "Cercant registres amb..." ha estat eliminada a petició de l'usuari.

        # 2. Filtratge de registres (Ús de List Comprehension per a concisió)
        registres_trobats = [
            registre  # L'element que volem guardar a la llista
            for registre in raiz.findall(RECORD_TAG)  # Itera sobre cada <Incidencia>
            # Condició de filtratge:
            if registre.find(CAMPO_PRIORIDAD) is not None and  # 1. Assegura que l'etiqueta existeixi
               registre.find(CAMPO_PRIORIDAD).text.strip() == valor_cercat_str  # 2. Compara el valor
        ]

        comptador = len(registres_trobats)

        # 3. Mostrar el resum de resultats (usant === per al resum, longitud 60)
        print("\n" + "=" * 55)
        if comptador == 0:
            print(f"🚫 No s'han trobat registres amb {etiqueta_cerca}.")
        else:
            print(f"S'han trobat {comptador} incidències amb {etiqueta_cerca}.")
        print("=" * 55)

        # 4. Visualització de detalls un per un (Paginació controlada per Enter)
        if comptador > 0:
            # Salt de línia afegit
            print("\nIniciant visualització d'incidencies una a una:\n")

            for i, registre in enumerate(registres_trobats):
                # Determina el missatge de pausa. S'ha afegit un salt de línia per a les següents.
                prompt = "Prem enter per veure la primera incidència" if i == 0 else "\nPrem enter per veure la següent incidència"
                # Atura el programa fins que l'usuari premi Enter.
                input(prompt)

                print(f"\n✅ Incidència {i + 1} de {comptador} :\n")

                # Bucle per imprimir cada sub-etiqueta i el seu valor dins de la incidència.
                for camp in registre.iter():
                    # Evita imprimir l'etiqueta principal (<Incidencia>) i assegura que el camp té text.
                    if camp.text and camp.tag != RECORD_TAG:
                        # Imprimeix el camp usant el separador de guió configurat ('-').
                        print(f"  {FIELD_SEPARATOR} {camp.tag:<25}: {camp.text.strip()}")

            # Final de la llista d'incidències: usa guions per a la separació final.
            print("\n" + "-" * 60)
            print("\nFi de la llista d'incidències.")

        print("\nPrograma finalitzat!")

    # Maneig d'errors de lectura de l'XML (si el fitxer està mal format)
    except ET.ParseError as e:
        print(f"\nERROR en llegir l'XML: El fitxer està mal format. Detall: {e}")
    # Maneig de qualsevol altre error inesperat
    except Exception as e:
        print(f"\nERROR inesperat: {e}")

# --- Punt d'Execució de l'Script ---
# Assegura que la funció principal es crida només quan l'script s'executa directament.
if __name__ == "__main__":
    executar_filtre_prioritat(XML_FILE)