# Generador de Tickets - Gemini (Web)

Aplicación Flask para generar tickets a partir de chats, usando Gemini y una base de ejemplos en Excel.

## Requisitos
- Python 3.8+
- Flask
- openpyxl
- google-generativeai
- gunicorn

## Instalación local

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=tu_api_key_aqui
python app.py
```

Accede a http://localhost:5000

## Despliegue en Render
- Sube el código a GitHub.
- Crea un nuevo Web Service en Render y conecta tu repo.
- Añade la variable de entorno `GEMINI_API_KEY` en la configuración de Render.
- Render detectará el Procfile y ejecutará la app automáticamente.

## Notas
- El archivo de ejemplos Excel debe estar en la raíz del proyecto.
- Los tickets generados se guardan en la carpeta `tickets_guardados`. 