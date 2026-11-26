# Karta źródła: OEIS (On-Line Encyclopedia of Integer Sequences) dla Slayera

Zapisana 26.11.2026 przed klonowaniem repozytorium i przed pierwszym liczeniem (pomiary wstępne z
`dane/matematyka-wspolne/kandydaci_czyste.md`, pozycja E1). Rezerwacja: #357 (część 3 zbioru matematyki i logiki).
Oznaczenia: V = sprawdzone 2026-11-26 w podanym źródle (URL, rewizja, hash, pomiar), I = wywnioskowane.

## 1. Identyfikacja

- V: https://github.com/oeis/oeisdata, rewizja `976b0c73e00453b1c1e6f16d83108cb9bb744c3b`, commit 2026-11-26T08:03:27Z,
  committer „OEIS Robot” (`admin@oeis.org`), wiadomość „oeis data export” (API GitHub). Gałąź domyślna `main`;
  używamy wyłącznie tej rewizji.
- V (README przy rewizji): eksport treści https://oeis.org/ w formacie git; wpis A123456 w `seq/A123/A123456.seq`,
  format wewnętrzny OEIS (https://oeis.org/eishelp1.html); pliki pomocnicze (`files/`, b-files) w Git LFS — nie
  pobieramy ich.

## 2. Prawa

- V: `LICENSE` przy rewizji: „The OEIS content is copyrighted by the OEIS Foundation, Inc. The content is made
  available under the terms of the CC-BY-SA-4.0 license”; dalej pełny tekst CC BY-SA 4.0; odesłanie do
  https://oeis.org/wiki/Legal_Documents. API GitHub rozpoznaje licencję jako `NOASSERTION` (plik ma dopisek przed
  tekstem licencji) — I: to nie zmienia treści licencji.
- V: README: „made available under the terms of the Creative Commons Attribution Share Alike 4.0 license”.
- Licencja per wiersz: `CC-BY-SA-4.0` (jedna dla całej bazy, wydana przez właściciela praw OEIS Foundation). Bez NC/ND.
- Tekst ludzki: wpisy pisane i redagowane przez autorów i edytorów OEIS; dokument składa deterministyczny parser
  (`skrypty/buduj_pule.py`), bez modeli. I: część komentarzy z ostatnich lat mogła powstać z pomocą LLM — OEIS ma
  politykę ograniczającą taki wkład, nie sprawdzaliśmy jej przestrzegania.
- Atrybucja (BY): `url` = `https://oeis.org/A<nr>` per dokument, nazwiska autorów (%A i podpisy komentarzy) zostają.
  SA: eksport musi zostać na CC BY-SA 4.0 (zgodne z repo zgłoszeń przy licencji per wiersz).
- Bramka „można TRENOWAĆ”: **TAK** (licencja otwarta). Bramka „można ZGŁOSIĆ”: **TAK** (licencja per dokument,
  bez NC/ND); opt-out TDM oeis.org (robots.txt, TDMRep) nie sprawdzony — dotyczyłby zbierania strony, nie licencji.

## 3. Zawartość

- V (kandydaci_czyste.md E1): 402 003 plików `.seq`, 597,7 MB, ~308 mln tokenów v6 surowo (1,94 B/tok).
- V (A000045, A123456, A350000 przy rewizji): pola `%I` (wersja), `%S/%T/%U` (wyrazy), `%N` (nazwa), `%C`
  (komentarze), `%D` (bibliografia), `%H` (linki HTML), `%F` (wzory), `%e` (przykłady), `%p/%t/%o` (programy Maple,
  Mathematica, inne), `%Y` (odsyłacze), `%K` (słowa kluczowe), `%O` (offset), `%A` (autor), `%E` (rozszerzenia).
  Podpisy w komentarzach mają postać „ - _Imię Nazwisko_, data”; starsze wpisy mają e-maile osób prywatnych w
  postaci `nazwa(AT)domena.com` (V: A000045, „Sharon Sela (sharonsela(AT)hotmail.com)”).
- Dokument: jedna sekwencja, tekst czytelny bez surowych znaczników `%X` (układ w `preregistracja.json` →
  `dokument.uklad_tekstu`): nazwa, do 60 wyrazów, komentarze, wzory, przykłady, programy z opisem języka, odsyłacze,
  autor bez e-maila. Pominięte: `%H`, `%I`, `%K`, `%O`, `%D`, `%E`, `%V/%W/%X`.
- Decyzja o autorach: `%A` zostaje jako „Author: …” (wymóg atrybucji BY), e-maile usuwane wzorcami z
  preregistracji; `%E` pominięte w całości (głównie „More terms from …”).

## 4. Skala i dostęp

- Klon: `git clone --filter=blob:none --sparse` z `sparse-checkout set seq`, checkout rewizji, bez LFS
  (`GIT_LFS_SKIP_SMUDGE=1`), w `dane/oeis/robocze/oeisdata`.
- I (E1): ~0,22 mld v6 po odcięciu `%H/%I/%K/%O/%U`; po filtrze budowy i dedupie z FineMath mniej. Pomiar w
  `wyniki/budowa.json` i `wyniki/probka_pliki.json`.

## 5. Ryzyka

- PII: e-maile autorów (maskowane przy budowie, detektory pii/pii_zaciemniony/pii_at_bez_nawiasow jako kontrola).
  Ciągi liczb mogą dawać fałszywe trafienia detektora telefonu/IP (np. „192.168.1.1” jako wyrazy) — I, mierzone w
  przebiegu.
- Nakładanie: V (E1): `oeis.org` 2 966/266 351 w próbce FineMath-4+, 578/196 757 w InfiWebMath; url
  `https://oeis.org/A<nr>` jest zgodny ze stroną, więc dedup_finemath4/dedup_infiwebmath4 po url usuwa te sekwencje.
- Testy: OEIS bywa cytowany w zadaniach (MATH, MMLU); ewal_13gram ściśle.
- Jakość: dużo liczb i szablonowych wpisów („Numbers k such that …”); dedup_wewnatrz MinHash usunie część; wpisy
  bez komentarzy i wzorów odcina filtr budowy.

## 6. Nowość

- I: wysoka dla Slayera w czystej postaci (w FineMath są tylko strony HTML OEIS z nawigacją); brak dowodu wpływu
  na wyniki modelu (kandydaci_czyste.md, „Nie sprawdzone”).

## Nie sprawdzone

- Opt-out TDM oeis.org; polityka OEIS wobec wkładu generowanego przez LLM i jej przestrzeganie.
- Czy wszystkie wpisy (także zaimportowane z dawnych książek Sloane’a) są objęte licencją bez wyjątków poza
  ogólnym zapisem LICENSE.

## 7. Wynik budowy puli (26.11.2026, po preregistracji)

Komendy (venv `dane/matematyka-wspolne/robocze/venv`): `skrypty/buduj_pule.py buduj` (kod 0, 178 s, log
`robocze/logi/buduj.log`), `skrypty/buduj_pule.py sprawdz` (kod 0: „OK: 311925 wierszy, 191127613 tokenów v6, 63
grup”), `skrypty/buduj_pule.py probka` (120 pozycji do recenzji filtra budowy w `robocze/probka_filtra_budowy.jsonl`).
Liczby: `wyniki/budowa.json`, `wyniki/probka_pliki.json`.

- V: klon przy `976b0c73…`, 402 003 plików `.seq`, 597 687 151 B, 0 błędów UTF-8.
- V: zachowane 311 925 dokumentów, **191 127 613 tokenów v6** (mediana 533, p99 1 910, max 24 682 na dokument);
  licencja per wiersz `CC-BY-SA-4.0` w 311 925/311 925.
- V: odrzucone filtrem budowy 90 078 dokumentów (22,4%), 28 879 398 tokenów v6 (13,1%): `bez_tresci` 84 860 dok. /
  28,0 mln tok., `krotka` 3 130 / 0,60 mln, `martwa` 2 088 / 0,27 mln, `brak_n` 0. I: `bez_tresci` zabiera też wpisy z
  samymi programami lub przykładami (np. A126033) — reguła z zadania, przyjęta bez zmiany.
- V: e-maile usunięte przy budowie: 13 744 dopasowań `nazwa(AT)domena`, 12 `nazwa@domena`, 18 `nazwa at domena`;
  po maskowaniu 0/0/0 w puli. I: 18 trafień `at domena` to głównie fałszywe („the link at www.opertech.com”, „a post
  at mymathforum.com”) — fraza usuwana, zdanie lekko okaleczone; koszt pomijalny.
- V (pomiar informacyjny detektora DCLM-EN, bez decyzji): IPv4 w 129 dokumentach, telefon w 7 (I: głównie ciągi
  liczb i wersje, nie dane osób); w trybie `maskuj_email_usun_telefon_ip` te dokumenty odpadną w agregacji.
- Znaczniki `_Imię_` zostają w wierszach programów (`%p/%t/%o`, komentarze kodu), zgodnie z preregistracją (zamiana
  tylko w `%A/%C/%F/%e/%Y/%N`).

### Przykłady przed/po

**A017686** (zachowany; e-mail w podpisie komentarza usunięty). Przed (`seq/A017/A017686.seq`, skrót):
```
%N A017686 Denominator of sum of -11th powers of divisors of n.
%C A017686 Sum_{d|n} 1/d^k is equal to sigma_k(n)/n^k. [...] - Ahmed Fares (ahmedfares(AT)my-deja.com), Apr 05 2001
%H A017686 Harvey P. Dale, <a href="/A017686/b017686.txt">Table of n, a(n) for n = 1..1000</a>
%t A017686 Denominator[DivisorSigma[-11,Range[20]]] (* _Harvey P. Dale_, Dec 18 2012 *)
%o A017686 (PARI) vector(20, n, denominator(sigma(n, 11)/n^11)) \\ _G. C. Greubel_, Nov 06 2018
%Y A017686 Cf. A017685.
%K A017686 nonn,frac
%A A017686 _N. J. A. Sloane_
```
Po:
```
A017686: Denominator of sum of -11th powers of divisors of n.

Terms: 1, 2048, 177147, 4194304, 48828125, 30233088, 1977326743, [...] 34271896307633

Comments:
Sum_{d|n} 1/d^k is equal to sigma_k(n)/n^k. [...] - Ahmed Fares, Apr 05 2001

Programs:
(Mathematica)
Denominator[DivisorSigma[-11,Range[20]]] (* _Harvey P. Dale_, Dec 18 2012 *)
(PARI) vector(20, n, denominator(sigma(n, 11)/n^11)) \\ _G. C. Greubel_, Nov 06 2018
[...]
Cross-references:
Cf. A017685.

Author: N. J. A. Sloane
```

**A100030** (zachowany; Maple/Mathematica/PARI z opisem języka, `%E` pominięte). Przed:
```
%N A100030 Bisection of A008472.
%C A100030 The sum of the distinct primes dividing 2n. - _Emeric Deutsch_, Mar 11 2005
%e A100030 a(6)=5 because 12 = 2^2*3 and 2+3 = 5.
%p A100030 with(numtheory): a:=proc(n) local b: [...] # _Emeric Deutsch_, Mar 11 2005
%t A100030 a[n_] := Total[FactorInteger[2*n][[;;, 1]]]; Array[a, 81] (* _Amiram Eldar_, Oct 31 2026 *)
%o A100030 (PARI) a(n) = vecsum(factor(2*n)[, 1]); \\ _Amiram Eldar_, Oct 31 2026
%Y A100030 Cf. A008472, A100029.
%K A100030 nonn,easy
%A A100030 _N. J. A. Sloane_, Nov 20 2004
%E A100030 More terms from _Emeric Deutsch_, Mar 11 2005
```
Po:
```
A100030: Bisection of A008472.

Terms: 2, 2, 5, 2, 7, 5, 9, 2, 5, 7, 13, [...] 61, 10, ...

Comments:
The sum of the distinct primes dividing 2n. - Emeric Deutsch, Mar 11 2005

Examples:
a(6)=5 because 12 = 2^2*3 and 2+3 = 5.

Programs:
(Maple)
with(numtheory): a:=proc(n) local b: [...] # _Emeric Deutsch_, Mar 11 2005
(Mathematica)
a[n_] := Total[FactorInteger[2*n][[;;, 1]]]; Array[a, 81] (* _Amiram Eldar_, Oct 31 2026 *)
(PARI) a(n) = vecsum(factor(2*n)[, 1]); \\ _Amiram Eldar_, Oct 31 2026

Cross-references:
Cf. A008472, A100029.

Author: N. J. A. Sloane, Nov 20 2004
```

**A005625** (odrzucony: `bez_tresci`, brak `%C` i `%F`). Przed:
```
%N A005625 Spiral sieve using Fibonacci numbers.
%D A005625 N. J. A. Sloane and Simon Plouffe, The Encyclopedia of Integer Sequences, Academic Press, 1995 [...]
%H A005625 H. W. Gould, <a href="https://www.fq.math.ca/Scanned/12-4/gould.pdf">Some sequences [...]</a>, [...]
%A A005625 _N. J. A. Sloane_
%E A005625 More terms from Chris Deugau (deugaucj(AT)uvic.ca), Dec 24 2005
```
Po (w `robocze/odrzucone.parquet`, poza pulą):
```
A005625: Spiral sieve using Fibonacci numbers.

Terms: 1, 2, 4, 7, 9, 17, 25, 46, 51, 83, [...] 14934506

Author: N. J. A. Sloane
```

## Nie sprawdzone (po budowie)

- Recenzja próbki filtra budowy (40 na powód) i ręczna próbka po agregacji — nie zrobione.
- Detektory potoku (przebieg, agreguj: ewal_13gram, dedupy wobec FineMath-4+, InfiWebMath-4+, 1.07, 8x3b, 1.08) —
  nie uruchomione; uzysk po dedupie nieznany. Tryb `pii.tryb = maskuj_email_usun_telefon_ip` wymaga implementacji
  w `agreguj_mat.py` (integrator).
