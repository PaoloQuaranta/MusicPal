# Scrivere una linea di basso — HOUSE / TECHNO (in levare)


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/basso-house.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

⚠️ **PERIMETRO.** Questa istruzione copre il basso della **four-on-the-floor**:
una linea che, nell'impostazione di base qui scelta, sta **fuori dalla cassa**,
sui **levare**, e dà il rimbalzo. Questo modello alterna cassa e basso;
non esaurisce le possibilità di house e techno.

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
- il registro **grave** (sub), zona **MIDI 24–36** (do1–do2 nella
  [convenzione MusicPal](../navigation.md#registri-e-nomi-delle-note));
- **la cassa** — nel modello di base il basso ci sta **intorno**. Vedi
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

## Impostazione di base ed eccezioni motivate

`[DEC]` Per un primo esercizio parti dai levare, con poche altezze e registro
grave. Sono vincoli locali per rendere chiaro il botta-e-risposta.

- **Attacchi sul movimento:** un pickup, una sincope o un raddoppio della cassa
  possono segnare un ingresso o una transizione. Scegli dove e perché;
  controlla durata, accento e sovrapposizione sonora con la cassa.
- **Melodia e registro:** una salita o una figura più ricca può distinguere
  una sezione. Conserva il ruolo del grave o assegna esplicitamente quel ruolo
  a un'altra parte; verifica il rapporto con gli stab.
- **Ottava e filtro:** sono opzioni di movimento, non obblighi. Se il movimento
  viene dalle entrate/uscite, dichiaralo; se scegli il filtro, realizzalo e
  controllalo come intervento sul suono.

Valuta all'ascolto se l'eccezione mantiene il rimbalzo o produce il contrasto
voluto. La sola coincidenza di due note non decide l'esito percettivo.

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
