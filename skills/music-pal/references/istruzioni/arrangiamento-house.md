# Arrangiare un pezzo HOUSE / TECHNO — build/drop, filtro, sidechain


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/arrangiamento-house.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

⚠️ **PERIMETRO.** Questa istruzione copre **l'essenza** della four-on-the-floor:
non la singola battuta (quella sta in [batteria-house.md](batteria-house.md) e
[basso-house.md](basso-house.md)), ma **l'arco** — come un pezzo dance *progredisce*.
House e techno **sono forma**: una battuta non dice niente di un pezzo, è il
**build/drop** e il **filtro in movimento** a farlo vivere.

> **La cosa da capire:** in un pezzo dance non si aggiungono note per far
> succedere qualcosa. Si **tolgono e si rimettono le parti**, si **apre il
> filtro**, si accende il **pompaggio**. Il movimento è nell'arrangiamento e nel
> suono, non nei colpi.

---

⚠️ **NIENTE CORPUS, come per tutto house/techno** (generi programmati): questo
documento è **`[LIB]`+`[DEC]`**, la convenzione di produzione elettronica. La
**struttura XML del sidechain** è invece `[OSS]` (verificata sui file veri del
Deluge, schema c1.3.0); la **magnitudine** del ducking nel caso storico è stata
tarata e **confermata all'orecchio** (*«va bene»*, 17 settembre 2026).

**Cosa ti serve prima di cominciare:**

- il groove già scritto (cassa, hat, clap, basso, stab) — vedi le due istruzioni
  sorelle;
- un kit **elettronico** (808/909) — il suo kick sarà il **trigger** del sidechain;
- l'idea dell'arco: quante battute, quante sezioni.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione di genere documentata |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | struttura XML osservata sui file veri del Deluge |
| `[da verificare]` | valore che si chiude solo all'orecchio, sul dispositivo |

---

## 1. L'arco — build/drop

`[LIB]`+`[DEC]` Un pezzo dance è un **arco di tensione**: si parte scarni, si
accumula, si esplode (il **drop**), si toglie tutto (il **breakdown**), si
riesplode. Le parti **entrano ed escono**; il filtro **apre e chiude**. Le durate
tipiche sono potenze di due: **8-16-32-64** battute.

L'arco minimo, quello dell'esempio (32 battute):

| sezione | battute | cosa suona | suono |
|---|---|---|---|
| **intro** | 8 | solo **cassa + closed hat** | filtro un po' chiuso |
| **build** | 4 | entrano **basso e stab** | il **cutoff apre** (rampa) |
| **drop** | 8 | **tutto** (clap, open hat, basso, stab) | **sidechain** che pompa |
| **breakdown** | 4 | **via la cassa**, restano stab + basso | stab **filtrato** scuro |
| **drop** | 8 | rientro pieno | filtro aperto, il pompaggio torna |

⚠️ **Il breakdown toglie la cassa**, ed è l'unico posto dove la four-on-the-floor
**si buca** (la regola dice «la cassa non si buca»: qui è l'eccezione che *fa* il
breakdown). Togliere il motore crea il vuoto da cui il drop successivo rientra.

**Come si stende, materialmente.** Si usa `mappa della forma`: una clip per stato (una
batteria d'intro, una piena; uno stab normale, uno che apre, uno filtrato), e la
mappa delle sezioni nel tempo. `forma` fa i conti e piazza le clip sull'arranger;
la **stessa** clip riusata in due sezioni uguali (i due drop) diventa una clip
instanziata due volte. Una clip corta (4 battute) piazzata su una sezione lunga
(8) **si ripete in loop** — è l'arranger a farlo (`collocazione temporale` con `length`
multiplo).

## 2. Il filtro che apre

`[LIB]`+`[DEC]` Lo **sweep del cutoff** è metà del carattere del genere: nel
build il filtro si apre gradualmente (il pezzo «si accende»), e nel drop è
spalancato. Si scrive con:

L’apertura del filtro si decide come arco timbrico della sezione: fissare
punto iniziale, punto finale e durata. L’adapter traduce quell’arco nella
scala effettiva del sintetizzatore, senza assumere unità display universali.

## 3. Il ducking: il livello risponde alla cassa

`[DEC]` Il pompaggio del caso nasce dal rapporto fra un trigger di cassa e
l’attenuazione temporanea di basso o stab. Definisci chi innesca, chi risponde
e in quanto tempo il livello ritorna. L’adapter realizza quel rapporto nel
proprio motore audio; la compressione del bus non è automaticamente equivalente.

Nel drop, la cassa innesca la risposta; nel breakdown, il suo silenzio può
sospenderla. L’arrangiamento governa così parte del movimento di mix senza
dover aggiungere eventi musicali. **La profondità si tara all’orecchio**:
controlla che il basso respiri senza perdere l’identità degli attacchi.
La prova del 17 settembre 2026 fu accettata; il suo valore grezzo resta
un dato dell’adapter storico, non un punto di partenza numerico universale.


## I vincoli

| vincolo | perché |
|---|---|
| **il drop non aggiunge note, rimette parti** | il movimento dance è togliere/rimettere + il filtro, non colpi in più |
| **la cassa si buca SOLO nel breakdown** | è l'eccezione che crea il vuoto; altrove è il motore |
| **il filtro apre nel build, è aperto nel drop** | lo sweep è metà del genere |
| **il sidechain col SIDECHAIN, non col compressore** | distinguere compressione del bus da ducking comandato dalla cassa |
| **il pompaggio è mix, non nota** | si imposta una volta sul suono; l'arrangiamento lo accende togliendo/mettendo la cassa |
| **le sezioni in potenze di due** | 8-16-32-64: la griglia percettiva del dance |

---

## Come si decide UNA sezione

**«Cosa c'è dentro, e cosa sta succedendo al filtro e alla pompa?»**

1. **Le parti**: quali clip suonano (la cassa c'è? il basso? lo stab?).
2. **Il filtro**: è fermo, apre (build), o è chiuso (breakdown)?
3. **La pompa**: c'è la cassa? allora il sidechain pompa da sé. Non c'è? respira.
4. **Il giunto con la sezione dopo**: un breakdown chiama un drop; un build chiama
   il drop. L'arco è fatto di attese e rilasci.

---

## L'esempio lavorato

[materiale della prova originale](../../provenance/delugepal/docs/istruzioni/arrangiamento-house.md): l'arco a 32 battute descritto sopra, sul giro
`Am9 | Dm9 | Fmaj9 | Em9`, kit 808, `Square Saw Bass` scurito, `Pianism I` per lo
stab. Il filtro apre nel build, lo stab del breakdown è filtrato scuro, il
sidechain pompa nei drop. **verifica** vuota, nessuna avvertenza.
⚠️ **Verdetto dell'ascolto (17 settembre 2026): *«va bene»*.**

---

## Cosa manca a questo documento

- il **`[MIS]`**: non esiste (generi programmati), e non è una lacuna da colmare;
- la **techno acid** (LFO sul cutoff, continuo): nominata, non implementata;
- il **lead/topline** e il **vocal chop** (casella 8 della scheda): materiale di
  `py`, fuori da qui.
