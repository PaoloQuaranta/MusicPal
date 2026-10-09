# Scrivere una linea di basso — HOUSE / TECHNO (in levare)


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/basso-house.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

⚠️ **PERIMETRO.** Questa istruzione copre il basso della **four-on-the-floor**:
una linea che sta **fuori dalla cassa**, sui **levare**, e dà il rimbalzo. ⚠️ È
**l'opposto dell'hip hop**, dove il basso stava *con* la cassa: qui la cassa
occupa i movimenti, e il basso occupa i buchi in mezzo.

| | house | techno |
|---|---|---|
| ritmo | in **levare**, saltellante, spesso a **ottave** | **rotolante** (sedicesimi), ipnotico, acid |
| suono | sub caldo o saw plucky | saw filtrato, acid (LFO sul cutoff) |
| altezza | segue le fondamentali del giro | spesso **una nota sola**, o due |

---

⚠️ **NIENTE CORPUS**, come per techno/house in generale (generi programmati): è
`[LIB]`+`[DEC]`, la convenzione di genere.

**Cosa ti serve prima di cominciare:**

- il giro (spesso breve e ripetuto, o un vamp di un accordo solo);
- il registro **grave** (sub), zona do1-do2 (24-36);
- **la cassa** — il basso ci sta **intorno**, non sopra. Vedi
  [batteria-house.md](batteria-house.md).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione di genere documentata |
| `[DEC]` | decisione presa qui, con la ragione |

---

## Il cuore — il basso in levare, «fuori dalla cassa»

`[LIB]`+`[DEC]` La cassa four-on-the-floor prende **tutti i movimenti**. Perché il
groove pompi, il basso lascia il movimento alla cassa e suona sui **levare** — la
"&" di ogni movimento (passi 2, 6, 10, 14 sulla griglia a 16). È il **contrario
dell'aggancio** dell'hip hop: lì basso e cassa erano lo stesso colpo, qui si
**alternano**. Questo botta-e-risposta cassa↓ / basso↑ è la pompa della house.

```
cassa:   x...x...x...x...    i movimenti
basso:   ..o...o...o...o.    i levare (la "&")
```

---

## L'altezza — la fondamentale, e l'ottava

`[LIB]`+`[DEC]` La house classica fa **saltare il basso all'ottava**: fondamentale
grave sul levare, e l'ottava sopra sul levare dopo — il rimbalzo «boing». Le
mosse:

- la **fondamentale** del giro, sul levare, grave;
- il **salto d'ottava** (grave↔sopra): la firma del rimbalzo house;
- nella **techno**, spesso **una nota sola** che rotola sui sedicesimi (l'acid),
  col carattere che viene dal **filtro** (LFO sul cutoff), non dalle altezze.

⚠️ **Rado in note diverse, fitto in ritmo.** L'altezza cambia poco (segue il
giro, o sta ferma); è il **ritmo in levare** a fare il basso, non la melodia.

---

## Sub tenuto o plucky corto

`[DEC]` Come nell'hip hop, la durata dice il suono:

- **house plucky**: note corte, staccate, che rimbalzano (il basso «organ» /
  saw);
- **sub/techno rotolante**: note più tenute o legate sui sedicesimi, con il
  filtro che le muove.

---

## Cosa NON fare

- **non mettere il basso sul movimento con la cassa.** Nella house sta sui
  **levare**: sul movimento raddoppia la cassa e il groove smette di pompare
  (l'opposto dell'hip hop);
- **non fare una linea melodica ricca.** L'altezza cambia poco; è il **ritmo in
  levare** il basso;
- **non salire di registro.** Grave, sub: in mezzo sparisce sotto gli stab;
- **non dimenticare l'ottava** (house) o **il filtro** (techno/acid): sono loro a
  dare vita a una linea che, in altezza, è quasi ferma.

---

## Cosa manca a questa istruzione

- il **`[MIS]`**: non esiste (generi programmati);
- il **filtro in movimento** (l'acid): LFO→cutoff via `collegamento di modulazione`, o
  l'automazione del cutoff — è una scelta di **suono/movimento**, non di note, e
  l'esempio non lo usa ancora. È metà del carattere della techno;
- il **sidechain** (il basso che «respira» sotto la cassa): è una scelta di mix,
  non rappresentabile come nota;
- il rapporto col **build/drop** dell'arrangiamento (il basso entra al drop).

### Eventi musicali espliciti della prova

Le tuple del codice originale vengono conservate come dati, senza
chiamate al dispositivo. Posizione e durate numeriche sono i tick della
**griglia storica del costruttore**, non beat e non unità universali.
Le figure scritte come frazioni sono durate musicali. Prima di riutilizzare
una posizione, dichiarare PPQ in quarti e metro del materiale originario.

| posizione storica | altezza (MIDI o nome) | durata | velocity, se esplicita |
|---|---|---|---|
| 48 | 33 | 40 | 100 |
| 144 | 45 | 40 | 92 |
| 240 | 33 | 40 | 100 |
| 336 | 45 | 40 | 92 |
