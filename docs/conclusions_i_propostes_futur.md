# Conclusions i Propostes de Futur — TypoShield

## Conclusions

### Assoliments del projecte

TypoShield és un sistema funcional de detecció de typosquatting que demostra com algoritmes clàssics de similitud de cadenes poden aplicar-se de manera efectiva a problemes reals de ciberseguretat.

**Respecte als requisits tècnics:**

- ✅ **Relació amb la ciberseguretat:** el sistema aborda directament els atacs de typosquatting i phishing per domini.
- ✅ **Estructures de dades:** ús de hash maps (`dict`) per a O(1) en cerca de dominis, llistes ordenades per a top-N resultats i sets per a l'algoritme de Jaccard.
- ✅ **Complexitat i recursivitat:** l'algoritme de Levenshtein utilitza DP. La complexitat dominant és O(D·n·m), analitzada detalladament a l'estudi de complexitat.
- ✅ **POO i polimorfisme:** jerarquia `SimilarityAlgorithm` → `LevenshteinAlgorithm`, `SequenceMatcherAlgorithm`, `JaccardAlgorithm`. `URLAnalyzer` usa polimorfisme per acceptar qualsevol implementació.
- ✅ **Gitflow:** treball col·laboratiu amb branques per funcionalitat i commits descriptius.

**Limitacions identificades:**

- La base de dominis legítims és estàtica (fitxer `domains.txt`); en un entorn real hauria de sincronitzar-se amb serveis com Tranco o Majestic Million.
- El sistema no analitza el contingut de la pàgina ni verifica el certificat SSL, cosa que reduiria els falsos negatius.
- Dominis internacionalitzats (IDN/punycode) requereixen preprocessament addicional.

---

## Propostes de futur

### P1 — Integració com a extensió de navegador

La interfície actual és de línia de comandes. Una extensió de Chrome/Firefox podria interceptar les navegacions i avisar l'usuari en temps real. L'arquitectura modular de TypoShield facilita aquesta integració: `URLAnalyzer` es podria exposar com a API REST.

### P2 — Detecció d'IDN homoglyphs

Dominis com `раурɑl.com` (amb caràcters ciríl·lics) no es detecten correctament per comparació de caràcters. Caldria normalitzar a punnycode i afegir un mapa de substitucions visuals (0 ↔ o, 1 ↔ l, @ ↔ a, etc.).

### P3 — Base de dades dinàmica

Substituir el fitxer estàtic per una integració amb **Tranco** (llista de dominis populars actualitzada setmanalment) o la **Cisco Umbrella Top 1M**, carregant-los en memòria amb el mateix hash map existent.

### P4 — Anàlisi de reputació en temps real

Consultar APIs com **VirusTotal**, **URLhaus** o **AbuseIPDB** per enriquir la classificació de risc amb informació de reputació externa.

### P5 — Model de scoring multi-factor

Combinar la similitud textual amb altres senyals:
- Antiguitat del domini (WHOIS)
- Presència de HTTPS i validesa del certificat
- Longitud inusual del domini
- Presència de caràcters especials o números

Un model de puntuació ponderada reduiria els falsos positius i negatiu.

### P6 — Optimitzacions algorítmiques

- Implementar l'optimització d'espai O(min(n,m)) per a Levenshtein.
- Afegir poda primerenca per aturar el càlcul quan la distància supera un llindar.
- Indexació per longitud de domini per reduir el D efectiu (veure estudi de complexitat, M3).

---

## Valoració global

El projecte ha permès aplicar de manera pràctica conceptes clau del curs: disseny d'algoritmes, anàlisi de complexitat, programació orientada a objectes i treball col·laboratiu amb Git. El problema del typosquatting és rellevant i en creixement, i TypoShield constitueix una base sòlida i extensible per abordar-lo.
