from dataclasses import dataclass
from algorithms import SimilarityAlgorithm
from domain_loader import DomainLoader


# Contenedor con el resultado de analizar una URL.

@dataclass
class ResultadoAnalisis:
    url_original: str
    dominio_extraido: str
    es_legitimo: bool
    riesgo: str
    similitudes: list
    algoritmo_usado: str
    mejor_coincidencia: str = ""
    mejor_score: float = 0.0


# Clasifica el nivel de riesgo según el score de similitud más alto.
# Si el score supera el umbral_alto el dominio es muy parecido a uno legítimo → ALTO.
# Si supera umbral_medio → MEDIO. Si no → BAJO. Si es exactamente legítimo → SEGURO.

class RiskClassifier:

    def __init__(self, umbral_alto: float = 0.85, umbral_medio: float = 0.65):
        self.umbral_alto = umbral_alto
        self.umbral_medio = umbral_medio

    def clasificar(self, score: float, es_legitimo: bool) -> str:
        # Complejidad O(1)
        if es_legitimo:
            return "SEGURO"
        if score >= self.umbral_alto:
            return "ALTO"
        if score >= self.umbral_medio:
            return "MEDIO"
        return "BAJO"

    def etiqueta_color(self, riesgo: str) -> str:
        # Devuelve la etiqueta con código de color ANSI para la terminal
        colores = {
            "SEGURO": "\033[92m",
            "BAJO":   "\033[94m",
            "MEDIO":  "\033[93m",
            "ALTO":   "\033[91m",
        }
        reset = "\033[0m"
        color = colores.get(riesgo, "")
        return f"{color}[{riesgo}]{reset}"


# Clase principal de análisis.
# Recibe cualquier objeto de tipo SimilarityAlgorithm gracias al polimorfismo,
# lo que permite cambiar el algoritmo sin modificar esta clase.
#
# Complejidad de analizar(): O(D·n·m)
#   D = número de dominios legítimos cargados
#   n, m = longitudes de los dominios comparados

class URLAnalyzer:

    def __init__(self, loader: DomainLoader, algoritmo: SimilarityAlgorithm, clasificador: RiskClassifier = None):
        self.loader = loader
        self.algoritmo = algoritmo  # polimorfismo: puede ser Levenshtein, Jaccard o SequenceMatcher
        self.clasificador = clasificador if clasificador else RiskClassifier()

    def analizar(self, url: str) -> ResultadoAnalisis:
        # Extrae el dominio de la URL y lo compara contra todos los legítimos.
        # Complejidad O(D·n·m)
        dominio = DomainLoader.extraer_dominio(url)
        es_legitimo = self.loader.existe(dominio)  # O(1) amortizado

        similitudes = []

        # Comparamos contra cada dominio legítimo — O(D) iteraciones, cada una O(n·m)
        for dom_legitimo in self.loader.obtener_todos():
            score = self.algoritmo.calculate(dominio, dom_legitimo)
            similitudes.append((dom_legitimo, score))

        # Ordenamos por score de mayor a menor — O(D log D)
        similitudes.sort(key=lambda x: x[1], reverse=True)

        mejor_coincidencia, mejor_score = similitudes[0] if similitudes else ("", 0.0)
        riesgo = self.clasificador.clasificar(mejor_score, es_legitimo)

        return ResultadoAnalisis(
            url_original=url,
            dominio_extraido=dominio,
            es_legitimo=es_legitimo,
            riesgo=riesgo,
            similitudes=similitudes,
            algoritmo_usado=self.algoritmo.name(),
            mejor_coincidencia=mejor_coincidencia,
            mejor_score=mejor_score,
        )

    def analizar_lista(self, urls: list) -> list:
        # Analiza una lista de URLs. Complejidad O(U·D·n·m) donde U es el número de URLs.
        return [self.analizar(url) for url in urls]
