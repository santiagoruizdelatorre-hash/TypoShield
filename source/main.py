import sys
import os

from algorithms import get_algorithm, ALGORITMOS_DISPONIBLES
from domain_loader import DomainLoader
from analyzer import URLAnalyzer, RiskClassifier, ResultadoAnalisis


# Clase orquestadora. Inicializa todos los componentes del sistema
# y expone los métodos principales para analizar URLs.

class TypoShield:

    FICHERO_DOMINIOS = os.path.join(os.path.dirname(__file__), "domains.txt")

    def __init__(self, algoritmo_nombre: str = "levenshtein"):
        self.loader = DomainLoader()
        self.clasificador = RiskClassifier()
        self.algoritmo = get_algorithm(algoritmo_nombre)
        self.analyzer = URLAnalyzer(self.loader, self.algoritmo, self.clasificador)
        self._cargar_dominios()

    def _cargar_dominios(self):
        n = self.loader.cargar_desde_fichero(self.FICHERO_DOMINIOS)
        if n == 0:
            # Si no se encuentra el fichero cargamos un conjunto básico
            self.loader.agregar_lista([
                "google.com", "facebook.com", "twitter.com", "instagram.com",
                "amazon.com", "microsoft.com", "apple.com", "netflix.com",
                "paypal.com", "linkedin.com", "github.com", "youtube.com",
                "wikipedia.org", "reddit.com", "whatsapp.com", "tiktok.com",
            ])

    def cambiar_algoritmo(self, nombre: str):
        self.algoritmo = get_algorithm(nombre)
        self.analyzer = URLAnalyzer(self.loader, self.algoritmo, self.clasificador)
        print(f"  Algoritmo cambiado a: {self.algoritmo.name()}")

    def analizar_url(self, url: str) -> ResultadoAnalisis:
        return self.analyzer.analizar(url)

    def analizar_lista(self, urls: list) -> list:
        return self.analyzer.analizar_lista(urls)


def imprimir_resultado(r: ResultadoAnalisis, clasificador: RiskClassifier):
    etiqueta = clasificador.etiqueta_color(r.riesgo)
    print(f"\n{'─' * 55}")
    print(f"  URL analizada    : {r.url_original}")
    print(f"  Dominio extraído : {r.dominio_extraido}")
    print(f"  Algoritmo        : {r.algoritmo_usado}")
    print(f"  Resultado        : {etiqueta}")

    if r.es_legitimo:
        print("  Dominio reconocido como legítimo.")
    else:
        print(f"  Mejor coincidencia: {r.mejor_coincidencia} ({r.mejor_score:.2%})")
        print("\n  Top 5 similares:")
        for dominio, score in r.similitudes[:5]:
            barra = "█" * int(score * 20)
            print(f"    {dominio:<25} {score:.2%}  {barra}")
    print(f"{'─' * 55}")


def menu():
    shield = TypoShield()
    print("\n" + "=" * 55)
    print("   TypoShield — Detector de URLs engañosas")
    print("=" * 55)
    print(f"   Dominios cargados : {shield.loader.total()}")
    print(f"   Algoritmo activo  : {shield.algoritmo.name()}")
    print("=" * 55)

    opciones = {
        "1": "Analizar una URL",
        "2": "Analizar varias URLs",
        "3": "Cambiar algoritmo",
        "4": "Cargar dominios desde fichero",
        "5": "Salir",
    }

    while True:
        print()
        for k, v in opciones.items():
            print(f"  [{k}] {v}")
        opcion = input("\n  Opción: ").strip()

        if opcion == "1":
            url = input("  URL: ").strip()
            if url:
                imprimir_resultado(shield.analizar_url(url), shield.clasificador)

        elif opcion == "2":
            print("  Introduce las URLs (línea vacía para terminar):")
            urls = []
            while True:
                u = input("  > ").strip()
                if not u:
                    break
                urls.append(u)
            for r in shield.analizar_lista(urls):
                imprimir_resultado(r, shield.clasificador)

        elif opcion == "3":
            print(f"  Disponibles: {', '.join(ALGORITMOS_DISPONIBLES.keys())}")
            nombre = input("  Nombre: ").strip()
            try:
                shield.cambiar_algoritmo(nombre)
            except ValueError as e:
                print(f"  Error: {e}")

        elif opcion == "4":
            ruta = input("  Ruta al fichero: ").strip()
            n = shield.loader.cargar_desde_fichero(ruta)
            print(f"  {n} dominios cargados. Total: {shield.loader.total()}")

        elif opcion == "5":
            print("\n  Hasta pronto.\n")
            sys.exit(0)

        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    menu()
