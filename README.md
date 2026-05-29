# TypoShield
### Detector inteligente de URLs engañosas

TypoShield analiza la similitud textual entre dominios para detectar ataques de typosquatting y phishing. Dado un dominio sospechoso, lo compara contra una base de dominios legítimos usando algoritmos de similitud de cadenas y clasifica el nivel de riesgo en ALTO / MEDIO / BAJO / SEGURO.

---

## Integrantes del grupo

Alex Albalat  
Santiago Ruiz de la Torre  
Dara Cárdenas

---

## Contexto y problemática

El typosquatting consiste en registrar dominios muy similares a sitios legítimos (p. ej. `g00gle.com` en lugar de `google.com`). Los atacantes aprovechan errores tipográficos o sustituciones visuales para dirigir a usuarios a páginas fraudulentas con el objetivo de robar credenciales, distribuir malware o ejecutar campañas de phishing.

Las soluciones actuales (Google Safe Browsing, antivirus) dependen de listas negras estáticas y no detectan dominios maliciosos recién registrados. TypoShield aborda este problema con análisis de similitud textual en tiempo real: no necesita una base de datos de URLs maliciosas porque su lógica es inversa — si un dominio desconocido se parece mucho a uno legítimo pero no es exactamente ese, se considera sospechoso.

Los dominios legítimos de referencia provienen de la lista [Tranco](https://tranco-list.eu), un ranking semanal de dominios populares diseñado específicamente para investigación en ciberseguridad. El fichero `domains.txt` incluido en el repositorio contiene una selección representativa de esta lista.

---

## Funcionalidades principales

1. Carga de dominios legítimos desde fichero `.txt` (formato Tranco) o por código.
2. Análisis de URL individual: extrae el dominio y lo compara contra la base.
3. Análisis de lista de URLs en lote.
4. Cálculo de similitud mediante tres algoritmos seleccionables.
5. Clasificación de riesgo en niveles ALTO / MEDIO / BAJO / SEGURO con umbrales configurables.
6. Cambio de algoritmo en tiempo de ejecución.
7. Interfaz web local en `http://localhost:5000` y modo terminal con colores.

---

## Uso de POO y polimorfismo

### Clases principales

**`SimilarityAlgorithm`** (`algorithms.py`)  
Clase abstracta base. Define la interfaz `calculate(s1, s2): float` que todas las implementaciones deben respetar. Es el núcleo del polimorfismo del sistema.

**`LevenshteinAlgorithm`** (`algorithms.py`)  
Implementa `calculate` usando distancia de edición con programación dinámica. Complejidad O(n·m), donde n y m son las longitudes de los dos dominios comparados.

**`SequenceMatcherAlgorithm`** (`algorithms.py`)  
Implementa `calculate` usando el algoritmo de Ratcliff/Obershelp de la librería `difflib`. Complejidad O(n·m).

**`JaccardAlgorithm`** (`algorithms.py`)  
Implementa `calculate` usando similitud de Jaccard sobre bigramas de caracteres. Complejidad O(n+m).

**`DomainLoader`** (`domain_loader.py`)  
Gestiona la base de dominios legítimos almacenándolos en un diccionario (hash map). La búsqueda y el acceso son O(1) amortizado.

**`RiskClassifier`** (`analyzer.py`)  
Clasifica el nivel de riesgo a partir del score de similitud más alto. La clasificación es O(1).

**`URLAnalyzer`** (`analyzer.py`)  
Orquesta el análisis completo. Recibe cualquier objeto de tipo `SimilarityAlgorithm` — aquí es donde se aplica el polimorfismo. Complejidad O(D·n·m), donde D es el número de dominios legítimos cargados.

**`TypoShield`** (`main.py`)  
Punto de entrada y orquestador general del sistema.

### Polimorfismo

`URLAnalyzer` recibe un objeto de tipo `SimilarityAlgorithm` sin conocer la subclase concreta. Cambiar el algoritmo en tiempo de ejecución no requiere modificar `URLAnalyzer`:

```python
# Mismo URLAnalyzer, distintos algoritmos — polimorfismo
analyzer = URLAnalyzer(loader, LevenshteinAlgorithm())
analyzer = URLAnalyzer(loader, JaccardAlgorithm())
analyzer = URLAnalyzer(loader, SequenceMatcherAlgorithm())
```

---

## Instrucciones de ejecución y dependencias

### Requisitos

- Python 3.10 o superior
- Flask para la interfaz web:

```bash
pip install flask
```

Dependencia opcional que mejora el rendimiento de Levenshtein (implementación en C):

```bash
pip install python-Levenshtein
```

Sin esta librería el proyecto funciona igualmente usando la implementación DP propia incluida en `algorithms.py`.

### Ejecución — interfaz web

```bash
cd source
python app.py
```

Abrir `http://localhost:5000` en el navegador. La aplicación corre en local, no requiere conexión a internet ni instalación en el navegador.

### Ejecución — terminal

```bash
cd source
python main.py
```

### Estructura del repositorio

```
TypoShield/
├── README.md
├── .gitignore
├── /docs
│   ├── uml.png
│   ├── flux_carga_dominios.png
│   ├── flux_analisis_url.png
│   ├── flux_comparacion_multiple.png
│   ├── estudi_complexitat.pdf
│   └── conclusions_i_propostes_futur.pdf
├── /source
│   ├── main.py
│   ├── app.py
│   ├── algorithms.py
│   ├── domain_loader.py
│   ├── analyzer.py
│   ├── benchmark.py
│   └── domains.txt
└── /build
    └── (vacío — proyecto Python, no requiere compilación)
```

---

## Video demostrativo

PRESENTACIÓN: https://youtu.be/yqIcd0J0POE

DEMOSTRACIÓN y USO: https://youtu.be/mf9FJlrizKE

---

## Uso de herramientas externas o IA

Este proyecto ha sido desarrollado manualmente por los miembros del grupo. Se ha utilizado Claude para asistir en la estructuración inicial del código, generación de plantillas y resolución de dudas puntuales. Todo el código funcional ha sido revisado, comprendido y adaptado por los integrantes del grupo. Las líneas generadas con asistencia de IA están marcadas con el comentario `# AI-assisted` en el código fuente.

---

## Licencia

Proyecto académico — ENTI Barcelona, Grado en Ciberseguridad.
