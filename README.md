# 🔬 Calculadora Científica — FastAPI + HTML/JS

Proyecto fullstack que combina una **API REST en Python (FastAPI)** con un **frontend en HTML/CSS/JS puro**.

## 📁 Estructura

```
calculadora-cientifica/
├── main.py           # API backend (FastAPI)
├── index.html        # Frontend (HTML/CSS/JS)
├── requirements.txt  # Dependencias Python
└── README.md
```

## 🚀 Cómo correrlo

### 1. Instalá las dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciá la API
```bash
uvicorn main:app --reload
```
La API queda disponible en: `http://localhost:8000`

### 3. Abrí el frontend
Abrí `index.html` en tu navegador. Asegurate que la URL de la API en la app sea `http://localhost:8000`.

---

## 📡 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado de la API |
| POST | `/calcular/basico` | Suma, resta, multiplicación, división |
| POST | `/calcular/funcion` | sqrt, log, sin, cos, tan, etc. |
| POST | `/fisica/energia-kinetica` | Ec = ½mv² |
| POST | `/fisica/caida-libre` | t = √(2h/g) |
| POST | `/fisica/ley-ohm` | V = I × R |

### Documentación interactiva (Swagger)
Con la API corriendo, entrá a: `http://localhost:8000/docs`

---

## 🛠 Tecnologías

- **Backend**: Python, FastAPI, Pydantic, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **Sin frameworks de frontend** — vanilla puro

## 👤 Autor
Guille — Física / Data Science / Medical Physics
