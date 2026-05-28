import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from algorithms import LevenshteinAlgorithm, SequenceMatcherAlgorithm, JaccardAlgorithm
from domain_loader import DomainLoader
from analyzer import URLAnalyzer, RiskClassifier


URLS_TEST = [
    "https://g00gle.com/login",
    "https://paypa1.com/account",
    "https://amaz0n.com/order",
    "https://faceb00k.com/login",
    "https://micros0ft.com/office",
    "https://gogle.com",
    "https://paypal.com",
    "https://randomdomainxyz.com",
    "https://twiter.com",
    "https://linkedln.com",
]

DOMINIS_TEST = [
    "google.com", "facebook.com", "twitter.com", "instagram.com",
    "amazon.com", "microsoft.com", "apple.com", "netflix.com",
    "paypal.com", "linkedin.com", "github.com", "youtube.com",
    "wikipedia.org", "reddit.com", "whatsapp.com", "tiktok.com",
    "bing.com", "yahoo.com", "duckduckgo.com", "stripe.com",
    "visa.com", "mastercard.com", "ebay.com", "adobe.com",
    "dropbox.com", "slack.com", "zoom.us", "shopify.com",
    "wordpress.com", "cloudflare.com", "gitlab.com",
    "stackoverflow.com", "medium.com", "bbc.com", "nytimes.com",
    "spotify.com", "twitch.tv", "discord.com", "pinterest.com",
    "outlook.com", "gmail.com", "protonmail.com", "icloud.com",
    "salesforce.com", "oracle.com", "ibm.com", "intel.com",
    "nvidia.com", "amd.com", "samsung.com",
]

ALGORITMOS = {
    "Levenshtein":     LevenshteinAlgorithm(),
    "SequenceMatcher": SequenceMatcherAlgorithm(),
    "Jaccard":         JaccardAlgorithm(),
}

REPETICIONES = 20


def benchmark():
    loader = DomainLoader()
    loader.agregar_lista(DOMINIS_TEST)
    clasificador = RiskClassifier()

    print(f"\n{'=' * 60}")
    print(f"  Benchmark TypoShield")
    print(f"  {len(URLS_TEST)} URLs x {len(DOMINIS_TEST)} dominios x {REPETICIONES} repeticiones")
    print(f"{'=' * 60}")
    print(f"  {'Algoritmo':<22} {'Tiempo total':>14} {'Tiempo/URL':>14}")
    print(f"  {'─' * 22} {'─' * 14} {'─' * 14}")

    resultados = {}

    for nombre, alg in ALGORITMOS.items():
        analizador = URLAnalyzer(loader, alg, clasificador)

        inicio = time.perf_counter()
        for _ in range(REPETICIONES):
            for url in URLS_TEST:
                analizador.analizar(url)
        fin = time.perf_counter()

        total = fin - inicio
        por_url = (total / (REPETICIONES * len(URLS_TEST))) * 1000

        resultados[nombre] = por_url
        print(f"  {nombre:<22} {total:>12.4f} s   {por_url:>12.3f} ms")

    print(f"{'=' * 60}")
    mas_rapido = min(resultados, key=resultados.get)
    print(f"\n  Algoritmo más rápido: {mas_rapido} ({resultados[mas_rapido]:.3f} ms/URL)\n")


if __name__ == "__main__":
    benchmark()
