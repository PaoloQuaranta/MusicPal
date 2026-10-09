# Il fill: la transizione nella batteria


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/fill.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

**A cosa serve.** Un **fill** è la battuta in cui la batteria smette di tenere il
tempo e **annuncia** la sezione nuova — il buco prima del ritornello, sul
turnaround, all'ingresso del ponte. È la faccia ritmica delle
[transizioni](transizioni.md): il segnale che «sta per cambiare qualcosa».

È priorità 3 (ritmo), e chiude quello che le facce della forma avevano lasciato
aperto: le [transizioni](transizioni.md) hanno fatto i giunti armonico-melodici
(turnaround, pickup), il fill è il giunto **nella batteria**. Poggia su
[batteria-jazz.md](batteria-jazz.md) (il vocabolario del groove).

**Cosa ti serve prima di cominciare:** una parte di batteria (il groove), e la
forma — dove sono i giunti.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quanti pezzi e quanti esecutori |
| `[CALC]` | calcolo sulla firma, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

⚠️ **Ritmo, quindi l'ascolto pieno** (metodo per area). Ma il fill è **molto
misurato**: `[MIS]`/`[CALC]` per la firma (dove, quanto, cosa cambia), e l'ascolto
per il feel — se il fill «annuncia» senza strappare.

---

## Il principio: dove lo dice la forma, cosa lo dice il corpus

⚠️ **La casella 9 di [jazz.md](../repertori/jazz.md) lo dice netto: «dove va un
fill non lo dice il corpus».** Il dataset consegna i fill come file staccati da
ogni pezzo — quanto spesso ne vada uno (ogni quattro battute, sul turnaround) non
è ricavabile da lì. **Ma ora la forma c'è** (priorità 2): il fill va al **giunto**
— l'ultima battuta di una sezione, dove il turnaround riporta o il pickup consegna.
È la convergenza: il **dove** viene dalla forma, il **cosa** dal corpus.

---

## La firma del fill, misurata

`[MIS]` casella 9 (**51 fill jazz**). ⚠️ **La cautela prima del numero: sono due
batteristi** (`drummer1` 44, `drummer7` 7). I numeri sono `[MIS]` ma descrivono
**quei due**; generalizzarli al jazz è un passo che il corpus non paga.

**Dura una battuta.** Mediana **0,93 battute** `[MIS]`: non una figura di due o
quattro, il buco di **una** battuta.

**Non è un fuoco d'artificio.** **15,7 colpi** contro i 12,9 del beat `[MIS]`: **un
quinto più fitto, non il doppio**. Chi raddoppia i colpi è già fuori dal corpus.

⚠️ **La firma NON è la densità: è che il ride si ferma e arrivano i tom.** La
quota di colpi per strumento `[MIS]`:

| strumento | nel beat | nel fill |
|---|---|---|
| **ride** | 20,4% | **3,3%** |
| **tom** (basso + medio) | 9,9% | **29,0%** |
| rullante | 30,8% | 40,3% |
| cassa | 16,1% | 8,1% |

Il ride passa da un colpo su cinque a uno su trenta, i tom **triplicano**. È
questo il fill, non la densità.

**E non alza la voce.** `[MIS]` rullante, cassa e tom nei fill stanno **sotto** la
loro mediana nei beat: un fill non è un crescendo, è un **cambio di strumento** a
volume uguale o minore.

---

## Esempio lavorato: le battute «(fill)» del blues

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato come `FILL01`.
`batteria_scritta.py` ([prova storica](../../provenance/origin-links.md)) lasciava le battute **12 e
24** (i turnaround) marcate «(fill)» e vuote, perché il fill era «una decisione
arbitraria». lo studio originale ([prova storica](../../provenance/origin-links.md)) scrive un fill con la
firma misurata — il segnatempo si ferma dopo il primo movimento, i tom scendono
verso il downbeat della sezione dopo, un filo più fitto e non più forte — e passa
`controlla_fill` senza problemi (`controllo documentato nella provenienza`). **costruisci** lo monta al
giunto di un AABA di 8 battute con la clip bianca.

**Verdetto: «suona giusto, approvato».** Il fill **annuncia** la sezione nuova — il
segnatempo tace, i tom scendono al giunto. ⚠️ **Su un kit di ripiego** (il TR-808
di `DRUMS1_4`, l'unico coi tom: elettronico, **senza ride** — il segnatempo è il
charleston): si è sentita la **struttura** del fill, non il timbro jazz. Un kit
acustico coi tom (non ancora in casa) resta il modo di sentirlo nel suo suono.

---

## Cosa NON fare

- **non fare del fill un fuoco d'artificio:** ~1,2× il beat, non il doppio — la
  firma è il cambio di strumento, non la densità (`[MIS]`);
- **non alzare la voce nel fill:** non è un crescendo, è un cambio di strumento a
  volume uguale o minore (`[MIS]`);
- **non tenere il ride nel fill:** il ride si ferma, i tom arrivano — è la firma;
- **non mettere il fill dove capita:** va al **giunto**, e il giunto lo dice la
  [forma](struttura.md), non il corpus;
- **non toccare la battuta di groove per fare il fill:** si posa con la clip bianca
  ([`variazione`](transizioni.md)), come ogni transizione.

---

## Cosa manca a questa istruzione

- **quanto spesso** va un fill (ogni 4 battute, ogni 8, solo sul turnaround): il
  corpus non lo dice, e la forma lo decide caso per caso — non c'è un numero;
- il **mezzo fill** (due movimenti invece di una battuta) e il **pickup di
  batteria** su un solo movimento;
- i fill **non-jazz** (il tom roll dell'EDM, il crash-and-stop): un'altra firma,
  su domanda;
- **le spazzole** e i feel diversi dallo swing (batteria-jazz.md li ha già in
  «cosa manca»).

### Materiale musicale degli esempi originali

Questi sono i materiali espliciti delle prove, riscritti come notazione
dichiarativa. Le operazioni del sequencer sono nell’adapter storico.

| contesto della prova | materiale |
|---|---|
| Come si scrive, materialmente | `x...x.x.x...x.x.` |
| Come si scrive, materialmente | `.......x....x...` |
| Come si scrive, materialmente | `....x.......x...` |
| Come si scrive, materialmente | `x.......x.......` |
| Come si scrive, materialmente | `x...............` |
| Come si scrive, materialmente | `x.x...x.x.......` |
| Come si scrive, materialmente | `....x.x.....x...` |
| Come si scrive, materialmente | `........x.x.x.x.` |

Per le griglie simboliche, `.` è silenzio, `x` colpo, `X` accento e
`o` fantasma; le durate e il metro si leggono nel contesto della prova.
