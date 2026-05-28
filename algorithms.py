from abc import ABC, abstractmethod
import difflib


# Clase base abstracta. Cualquier algoritmo de similitud debe heredar de esta
# clase e implementar el método calculate(). Aquí es donde está el polimorfismo.

class SimilarityAlgorithm(ABC):

    @abstractmethod
    def calculate(self, s1: str, s2: str) -> float:
        # Devuelve un valor entre 0.0 (nada similares) y 1.0 (idénticos)
        pass

    def name(self) -> str:
        return self.__class__.__name__


# Algoritmo 1: distancia de Levenshtein con programación dinámica.
# Complejidad temporal O(n·m), donde n y m son las longitudes de s1 y s2.
# Complejidad espacial O(n·m) por la tabla DP.

class LevenshteinAlgorithm(SimilarityAlgorithm):

    def calculate(self, s1: str, s2: str) -> float:
        dist = self._levenshtein_dp(s1, s2)
        max_len = max(len(s1), len(s2), 1)
        return 1.0 - dist / max_len

    def _levenshtein_dp(self, s1: str, s2: str) -> int:
        n, m = len(s1), len(s2)

        # Creamos la tabla DP de (n+1) x (m+1)
        dp = [[0] * (m + 1) for _ in range(n + 1)]

        # Casos base: transformar un prefijo vacío cuesta i inserciones o eliminaciones
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j

        # Rellenamos la tabla comparando carácter a carácter
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                coste = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,         # eliminación
                    dp[i][j - 1] + 1,          # inserción
                    dp[i - 1][j - 1] + coste   # sustitución
                )

        return dp[n][m]

    def name(self) -> str:
        return "Levenshtein"


# Algoritmo 2: SequenceMatcher de la librería difflib.
# Basado en el algoritmo de Ratcliff/Obershelp. Complejidad O(n·m).

class SequenceMatcherAlgorithm(SimilarityAlgorithm):

    def calculate(self, s1: str, s2: str) -> float:
        matcher = difflib.SequenceMatcher(None, s1, s2)
        return matcher.ratio()

    def name(self) -> str:
        return "SequenceMatcher"


# Algoritmo 3: similitud de Jaccard sobre bigramas de caracteres.
# Complejidad O(n+m) donde n y m son las longitudes de s1 y s2.

class JaccardAlgorithm(SimilarityAlgorithm):

    def __init__(self, n: int = 2):
        self.n = n

    def _ngrams(self, s: str) -> set:
        # Generamos todos los n-gramas de la cadena como un conjunto
        return {s[i:i + self.n] for i in range(len(s) - self.n + 1)}

    def calculate(self, s1: str, s2: str) -> float:
        set1 = self._ngrams(s1)
        set2 = self._ngrams(s2)

        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0

        # Jaccard = tamaño de la intersección / tamaño de la unión
        interseccion = set1 & set2
        union = set1 | set2
        return len(interseccion) / len(union)

    def name(self) -> str:
        return "Jaccard"


# Diccionario con los algoritmos disponibles para acceder a ellos por nombre.
# El acceso es O(1) al ser un hash map.

ALGORITMOS_DISPONIBLES = {
    "levenshtein":     LevenshteinAlgorithm(),
    "sequencematcher": SequenceMatcherAlgorithm(),
    "jaccard":         JaccardAlgorithm(),
}


def get_algorithm(nombre: str) -> SimilarityAlgorithm:
    nombre = nombre.lower().strip()
    if nombre not in ALGORITMOS_DISPONIBLES:
        raise ValueError(f"Algoritmo '{nombre}' no disponible. Opciones: {list(ALGORITMOS_DISPONIBLES.keys())}")
    return ALGORITMOS_DISPONIBLES[nombre]
