# PAM Generador de Documentos - API Web

Esta API permite generar documentos de manera automatizada a través de HTTP requests.

## Instalación y Ejecución

### Opción 1: Ejecutar con Python
```bash
cd "c:\Fuentes\PAM"
.\.venv\Scripts\activate
python api.py
```

### Opción 2: Ejecutar el ejecutable
```bash
cd "c:\Fuentes\PAM\dist"
.\PAM_API.exe
```

La API se ejecutará en `http://localhost:8000`

## Endpoints

### GET /
Verifica que la API está corriendo.

**Respuesta:**
```json
{
  "message": "PAM Generador de Documentos API",
  "status": "running"
}
```

### POST /generate/animal/{animal_name}
Genera un documento para el animal especificado.

**Parámetros:**
- `animal_name`: Nombre del animal (string)

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/generate/animal/Lola
```

**Respuesta exitosa:**
```json
{
  "status": "success",
  "document_path": "C:\\Fuentes\\PAM\\dist\\Documentos Generados\\Lola_202603192140.docx"
}
```

### POST /generate/row/{row_number}
Genera un documento para la fila especificada en la hoja de cálculo.

**Parámetros:**
- `row_number`: Número de fila (integer)

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/generate/row/5
```

**Respuesta exitosa:**
```json
{
  "status": "success",
  "document_path": "C:\\Fuentes\\PAM\\dist\\Documentos Generados\\Fila_5_202603192140.docx"
}
```

## Errores

- **400 Bad Request**: Animal no encontrado o fila inválida
- **500 Internal Server Error**: Error interno (problemas de conexión, permisos, etc.)

## Documentación Interactiva

Cuando la API esté corriendo, puedes acceder a la documentación automática en:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Notas

- Los documentos generados se guardan en la carpeta `Documentos Generados`
- Requiere conexión a internet y acceso a Google Sheets
- Las credenciales de Google deben estar configuradas en `conf/service_account.json`