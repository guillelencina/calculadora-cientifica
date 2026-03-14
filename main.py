from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI(
    title="Calculadora Científica API",
    description="API para realizar cálculos científicos y físicos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos ---

class OperacionBasica(BaseModel):
    a: float
    b: float
    operacion: str  # suma, resta, multiplicacion, division

class FuncionMatematica(BaseModel):
    valor: float
    funcion: str  # sqrt, log, log10, sin, cos, tan, exp, factorial

class EnergiaKinetica(BaseModel):
    masa: float       # kg
    velocidad: float  # m/s

class CaidaLibre(BaseModel):
    altura: float     # metros
    g: float = 9.81   # m/s² (aceleración gravitacional)

class OhmLey(BaseModel):
    voltaje: float = None
    corriente: float = None
    resistencia: float = None

# --- Endpoints básicos ---

@app.get("/")
def root():
    return {"mensaje": "Calculadora Científica API activa 🔬", "version": "1.0.0"}

@app.post("/calcular/basico")
def calcular_basico(datos: OperacionBasica):
    operaciones = {
        "suma": datos.a + datos.b,
        "resta": datos.a - datos.b,
        "multiplicacion": datos.a * datos.b,
        "division": datos.a / datos.b if datos.b != 0 else None
    }
    if datos.operacion not in operaciones:
        raise HTTPException(status_code=400, detail="Operación no válida")
    resultado = operaciones[datos.operacion]
    if resultado is None:
        raise HTTPException(status_code=400, detail="División por cero no permitida")
    return {"operacion": datos.operacion, "a": datos.a, "b": datos.b, "resultado": resultado}

@app.post("/calcular/funcion")
def calcular_funcion(datos: FuncionMatematica):
    try:
        funciones = {
            "sqrt": math.sqrt(datos.valor),
            "log": math.log(datos.valor),
            "log10": math.log10(datos.valor),
            "sin": math.sin(math.radians(datos.valor)),
            "cos": math.cos(math.radians(datos.valor)),
            "tan": math.tan(math.radians(datos.valor)),
            "exp": math.exp(datos.valor),
            "factorial": float(math.factorial(int(datos.valor))) if datos.valor >= 0 else None,
        }
        if datos.funcion not in funciones:
            raise HTTPException(status_code=400, detail="Función no válida")
        resultado = funciones[datos.funcion]
        if resultado is None:
            raise HTTPException(status_code=400, detail="Valor no válido para esta función")
        return {"funcion": datos.funcion, "valor": datos.valor, "resultado": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error matemático: {str(e)}")

# --- Endpoints de física ---

@app.post("/fisica/energia-kinetica")
def energia_kinetica(datos: EnergiaKinetica):
    """Calcula la energía cinética: Ec = ½ × m × v²"""
    ec = 0.5 * datos.masa * datos.velocidad ** 2
    return {
        "formula": "Ec = ½ × m × v²",
        "masa_kg": datos.masa,
        "velocidad_ms": datos.velocidad,
        "energia_joules": ec
    }

@app.post("/fisica/caida-libre")
def caida_libre(datos: CaidaLibre):
    """Calcula tiempo de caída y velocidad final: t = √(2h/g), v = g×t"""
    tiempo = math.sqrt(2 * datos.altura / datos.g)
    velocidad_final = datos.g * tiempo
    return {
        "formula": "t = √(2h/g) | v = g×t",
        "altura_m": datos.altura,
        "gravedad_ms2": datos.g,
        "tiempo_caida_s": round(tiempo, 4),
        "velocidad_final_ms": round(velocidad_final, 4)
    }

@app.post("/fisica/ley-ohm")
def ley_ohm(datos: OhmLey):
    """Calcula el valor faltante usando la Ley de Ohm: V = I × R"""
    valores = {"voltaje": datos.voltaje, "corriente": datos.corriente, "resistencia": datos.resistencia}
    nulos = [k for k, v in valores.items() if v is None]
    if len(nulos) != 1:
        raise HTTPException(status_code=400, detail="Debes dejar exactamente UN campo en None para calcular")
    
    if nulos[0] == "voltaje":
        resultado = datos.corriente * datos.resistencia
        return {"calculado": "voltaje", "valor": resultado, "unidad": "V", "formula": "V = I × R"}
    elif nulos[0] == "corriente":
        if datos.resistencia == 0:
            raise HTTPException(status_code=400, detail="La resistencia no puede ser 0")
        resultado = datos.voltaje / datos.resistencia
        return {"calculado": "corriente", "valor": resultado, "unidad": "A", "formula": "I = V / R"}
    else:
        if datos.corriente == 0:
            raise HTTPException(status_code=400, detail="La corriente no puede ser 0")
        resultado = datos.voltaje / datos.corriente
        return {"calculado": "resistencia", "valor": resultado, "unidad": "Ω", "formula": "R = V / I"}
