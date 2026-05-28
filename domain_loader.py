import re


# Gestiona el conjunto de dominios legítimos.
# Los almacena en un diccionario (hash map) para que la búsqueda sea O(1) amortizado.

class DomainLoader:

    def __init__(self):
        self._dominios = {}

    def cargar_desde_fichero(self, ruta: str) -> int:
        # Lee un fichero .txt con un dominio por línea.
        # Ignora líneas vacías y comentarios que empiezan por #.
        # Complejidad O(d) donde d es el número de dominios en el fichero.
        cargados = 0
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    dominio = linea.strip().lower()
                    if dominio and not dominio.startswith("#"):
                        self._dominios[dominio] = dominio
                        cargados += 1
        except FileNotFoundError:
            print(f"Fichero no encontrado: {ruta}")
        return cargados

    def agregar(self, dominio: str) -> None:
        # Añade un dominio individual. Complejidad O(1) amortizado.
        dominio = dominio.strip().lower()
        if dominio:
            self._dominios[dominio] = dominio

    def agregar_lista(self, dominios: list) -> None:
        # Añade una lista de dominios. Complejidad O(d).
        for d in dominios:
            self.agregar(d)

    def existe(self, dominio: str) -> bool:
        # Comprueba si el dominio está en la lista de legítimos.
        # Complejidad O(1) amortizado — búsqueda en hash map.
        return dominio.strip().lower() in self._dominios

    def obtener_todos(self) -> list:
        # Devuelve todos los dominios cargados como lista. Complejidad O(d).
        return list(self._dominios.keys())

    def total(self) -> int:
        return len(self._dominios)

    @staticmethod
    def extraer_dominio(url: str) -> str:
        # Extrae el dominio limpio de una URL completa.
        # Elimina protocolo, www y cualquier ruta o parámetro.
        # Complejidad O(n) donde n es la longitud de la URL.
        url = url.strip().lower()
        url = re.sub(r"^https?://", "", url)
        url = re.sub(r"^www\.", "", url)
        dominio = re.split(r"[/?#]", url)[0]
        return dominio
