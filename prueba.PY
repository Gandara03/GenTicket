import requests
from requests.auth import HTTPBasicAuth
import csv
import html
import re
import os

API_USER = "Alexis"
API_PASS = "7XnRG0YsFFPRDaMLp2sn4ugX"
BASE_URL = "https://bidcom.sd.cloud.invgate.net/api/v1"
CREATOR_ID_DESEADO = 507

def limpiar_texto_html(texto):
    if not texto:
        return ""
    texto = html.unescape(texto)              # Decodifica entidades HTML
    texto = re.sub(r'<[^>]+>', '', texto)     # Elimina etiquetas HTML
    texto = re.sub(r'\s+', ' ', texto).strip()  # Espacios extra
    return texto

def obtener_ticket_por_id(ticket_id):
    url = f"{BASE_URL}/incident?id={ticket_id}&date_format=iso8601"
    response = requests.get(url, auth=HTTPBasicAuth(API_USER, API_PASS))
    
    if response.status_code != 200:
        print(f"[{ticket_id}] Error HTTP {response.status_code}")
        return None

    try:
        return response.json()
    except Exception as e:
        print(f"[{ticket_id}] Error al parsear JSON: {e}")
        print("Respuesta cruda:", response.text)
        return None


def generar_txt(tickets, bloque):
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_txt = os.path.join(carpeta, f"tickets_{bloque}.txt")
    os.makedirs(carpeta, exist_ok=True)
    with open(ruta_txt, "w", encoding="utf-8-sig") as f:
        for i, ticket in enumerate(tickets, 1):
            titulo = limpiar_texto_html(ticket.get('title', ''))
            descripcion = limpiar_texto_html(ticket.get('description', ''))
            creador_id = ticket.get('creator_id', '')
            creador_nombre = "Alexis Gandara" if creador_id == 507 else creador_id
            f.write(f"--- Ticket #{i} ---\n")
            f.write(f"Título: {titulo}\n")
            f.write(f"Descripción: {descripcion}\n")
            f.write(f"Creador: {creador_nombre}\n")
            f.write(f"Asignado a ID: {ticket.get('assigned_id', '')}\n")
            f.write("\n")


def generar_csv(tickets, bloque):
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(carpeta, f"tickets_{bloque}.csv")
    os.makedirs(carpeta, exist_ok=True)
    with open(ruta_csv, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Título", "Descripción", "Creador", "Asignado ID"])
        for ticket in tickets:
            titulo = limpiar_texto_html(ticket.get('title', ''))
            descripcion = limpiar_texto_html(ticket.get('description', ''))
            creador_id = ticket.get('creator_id', '')
            creador_nombre = "Alexis Gandara" if creador_id == 507 else creador_id
            writer.writerow([
                titulo,
                descripcion,
                creador_nombre,
                ticket.get('assigned_id', '')
            ])


if __name__ == "__main__":
    try:
        print("Obteniendo tickets desde InvGate por ID...")
        inicio = 12000
        fin = 15711
        bloque_actual = 1
        for bloque_inicio in range(inicio, fin, 1000):
            bloque_fin = min(bloque_inicio + 1000, fin)
            tickets_filtrados = []
            for ticket_id in range(bloque_inicio, bloque_fin):
                ticket = obtener_ticket_por_id(ticket_id)
                if ticket and ticket.get("creator_id") == CREATOR_ID_DESEADO:
                    tickets_filtrados.append(ticket)
                    print(f"[{ticket_id}] Agregado: {limpiar_texto_html(ticket.get('title', ''))}")
            print(f"\nTotal tickets del creador {CREATOR_ID_DESEADO} en el bloque {bloque_actual}: {len(tickets_filtrados)}")
            if tickets_filtrados:
                generar_txt(tickets_filtrados, bloque_actual)
                generar_csv(tickets_filtrados, bloque_actual)
                print(f"Archivos tickets_{bloque_actual}.txt y tickets_{bloque_actual}.csv generados correctamente.")
            else:
                print(f"No se encontraron tickets del creador indicado en el bloque {bloque_actual}.")
            bloque_actual += 1
        input("Presiona Enter para finalizar...")
    except Exception as e:
        print("Ocurrió un error:", e)
        input("Presiona Enter para salir...")
