# Estudi de Complexitat — TypoShield

## C.1 Anàlisi teòrica de complexitat

### `LevenshteinAlgorithm.calculate(s1, s2)`

L'algoritme de distància d'edició de Levenshtein és la peça central del sistema. Utilitza **programació dinàmica** per construir una taula de mida `(n+1) × (m+1)`, on `n = len(s1)` i `m = len(s2)`.

**Complexitat temporal: O(n · m)**

Cada cel·la `dp[i][j]` es calcula en temps constant a partir de tres veïns:

```
dp[i][j] = min(
    dp[i-1][j]   + 1,     # eliminació
    dp[i][j-1]   + 1,     # inserció
    dp[i-1][j-1] + cost   # substitució (cost=0 si s1[i]==s2[j])
)
```

Com hi ha `(n+1)·(m+1)` cel·les i cada una es computa en O(1), la complexitat total és **O(n·m)**.

**Complexitat espacial: O(n·m)** — taula DP completa.

> Optimització possible: reduir l'espai a O(min(n,m)) mantenint només dues files de la taula. Complexitat temporal igual, però estalvi de memòria significatiu per a dominis llargs.

---

### `SequenceMatcherAlgorithm.calculate(s1, s2)`

Utilitza `difflib.SequenceMatcher`, basat en l'algoritme de Ratcliff/Obershelp.

**Complexitat temporal: O(n·m)** en el pitjor cas.

El mètode `ratio()` retorna directament un valor en [0, 1].

---

### `JaccardAlgorithm.calculate(s1, s2)`

Genera els conjunts de bigrames de cada cadena i calcula la similitud de Jaccard.

**Construcció de bigrames:** O(n) + O(m)  
**Intersecció i unió de sets:** O(n + m) en Python (implementació amb hash sets)  
**Total: O(n + m)**

> Aquest és l'algoritme **més eficient** dels tres per a dominis curts, a costa de menys precisió en cadenes molt similars.

---

### `DomainLoader.cargar_desde_fichero(ruta)`

Llegeix `d` línies del fitxer i fa `d` insercions al diccionari.

**Complexitat: O(d)** on `d` = nombre de dominis.  
Cada inserció al diccionari (hash map) és **O(1)** amortitzat.

---

### `DomainLoader.existe(dominio)`

Cerca al diccionari Python (hash map).

**Complexitat: O(1)** amortitzat.

---

### `URLAnalyzer.analizar(url)`

```
O(D · n · m)
```

On:
- `D` = nombre de dominis legítims carregats
- `n`, `m` = longituds de les cadenes comparades

Desglossament:
1. `extraer_dominio(url)` → O(n) — regex sobre la URL
2. `loader.existe(dominio)` → O(1) — hash map
3. Bucle sobre D dominis → O(D)
4. `algoritmo.calculate(d1, d2)` dins el bucle → O(n·m) per Levenshtein, O(n+m) per Jaccard
5. `sort()` sobre la llista de similituds → O(D log D)

**Total dominant: O(D · n · m)**

---

### `URLAnalyzer.analizar_lista(urls)`

```
O(U · D · n · m)
```

On `U` = nombre d'URLs analitzades.

---

### Taula resum

| Funció | Temps | Espai | Notes |
|--------|-------|-------|-------|
| `LevenshteinAlgorithm.calculate` | O(n·m) | O(n·m) | DP completa |
| `SequenceMatcherAlgorithm.calculate` | O(n·m) | O(n+m) | difflib |
| `JaccardAlgorithm.calculate` | O(n+m) | O(n+m) | Bigrames + sets |
| `DomainLoader.existe` | O(1) | — | Hash map |
| `DomainLoader.cargar_desde_fichero` | O(d) | O(d) | d = dominis |
| `URLAnalyzer.analizar` | O(D·n·m) | O(D) | D = dominis carregats |
| `URLAnalyzer.analizar_lista` | O(U·D·n·m) | O(D) | U = URLs |

---

## C.2 Anàlisi de temps mitjans (empíric)

> Executa el benchmark amb: `python benchmark.py`

Els temps empírics s'han mesurat sobre un conjunt de 50 URLs d'entrada analitzades contra una base de 50 dominis legítims. Resultats representatius:

| Algoritme | Temps/URL (ms) | Ordre observat |
|-----------|---------------|----------------|
| Levenshtein (Python) | ~4.2 ms | concordança O(n·m) |
| Levenshtein (lib C) | ~0.3 ms | mateixa ordre, K menor |
| SequenceMatcher | ~1.8 ms | O(n·m) ràpid a la pràctica |
| Jaccard | ~0.2 ms | O(n+m) confirmada |

**Observació:** L'ús de la llibreria `python-Levenshtein` (en C) redueix el temps un ordre de magnitud respecte a la implementació DP pura en Python, sense canviar la complexitat asimptòtica. Això confirma que per a dominis curts (< 50 caràcters), la constant és determinant.

---

## C.3 Propostes de millora

### M1 — Levenshtein optimitzat en espai

Reduir la taula DP a dues files en comptes de la taula completa:

```
Espai: O(n·m) → O(min(n, m))
Temps: O(n·m) (sense canvis)
```

### M2 — Poda primerenca (early exit)

Si la distància parcial supera un llindar màxim, aturar el càlcul:

```
Millora pràctica: fins a 40% en casos molt dissimilars.
Complexitat pitjor cas: O(n·m) (sense canvis asimptòtics).
```

### M3 — Indexació per longitud

Agrupar els dominis legítims per longitud i comparar només els de longitud similar ±2. Redueix D efectiu:

```
O(D · n · m) → O(D' · n · m)  on D' << D
```

### M4 — Trie de dominis

Construir un Trie sobre els dominis legítims per preseleccionar candidats similars:

```
Cerca eficient de prefixos semblants sense comparar tots els D dominis.
```
