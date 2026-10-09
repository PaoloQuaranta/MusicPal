# La struttura: la forma lunga, la mappa delle sezioni


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/struttura.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

Per il riuso di frase, motivo e contrappunto della tradizione classica e barocca
in produzioni elettroniche, vedi
[forma-storica-elettronica.md](forma-storica-elettronica.md).
Per la prima integrazione di mappa, arco, ritorni e coda sovrapposta in una song
di 58 battute, vedi [brano-completo.md](brano-completo.md).

**A cosa serve.** Hai il materiale — un tema, un giro, un groove — e devi
decidere **come si dispone nel tempo**: quante sezioni, in che ordine, quali
tornano e quali contrastano. È lo **scheletro** del pezzo: la stessa idea diventa
un AABA, un blues ripetuto, una testa-soli-testa a seconda della mappa.

È priorità 2 (forma), l'ultima faccia dopo [voicing](voicing.md), [comping](comping.md)
e [contrappunto](contrappunto.md). Quelle tre lavorano **dentro** una o due
battute; la struttura è ciò che **dura più di una battuta** — la forma dell'intero
pezzo. È anche ciò che rende possibile «un pezzo intero» invece di una parte sola.

⚠️ **Questa istruzione copre la MAPPA (lo scheletro): dove cadono le sezioni.** Le
altre due facce della struttura — l'**arco dinamico** (come densità e intensità
salgono e ricadono lungo la forma) e le **transizioni** (turnaround, fill, stacchi)
— sono in «Cosa manca», su domanda.

**Cosa ti serve prima di cominciare:** il materiale di ogni sezione già scritto in
**clip** (gli accordi, la melodia, il basso di ogni sezione), e l'organico.

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | letteratura, con libro e pagina |
| `[MIS]` | misurato su un corpus, con quanti pezzi |
| `[CALC]` | calcolo sulla timeline, verificato da un test |
| `[DEC]` | decisione presa qui, con la ragione |
| `[OSS]` | osservato all'ascolto |

`[CALC]` basta per proprietà definite nella timeline: dove cadono le sezioni,
quali clip ritornano e quali note o accordi chiudono una frase. L'ascolto è
richiesto quando l'affermazione riguarda **l'effetto percepito**: se l'A torna
riconoscibile, se il ponte contrasta, se il beat maschera una cadenza. Dopo una
prima verifica del percorso XML → Deluge, non occorre riascoltare ogni nuova
applicazione della stessa regola; vedi
[forma-storica-elettronica.md](forma-storica-elettronica.md).

---

## Il principio: un pezzo è sezioni disposte nel tempo

`[LIB]` music-composition, `references/form/popular-song-forms.md`: quasi tutte le
forme popolari sono **costruite da un piccolo insieme di tipi di sezione**
(intro, verse, chorus, bridge, outro…) **combinati in un ordine**. Gli stessi tipi
si ricombinano fra generi. La forma **non** è una nota o un accordo: è la
disposizione.

⚠️ **La regola che conta più di tutte le mappe: ripetizione contro sviluppo**
(`[LIB]` stesso file). Una sezione che torna dà **riconoscibilità**; ma una forma
che ripete **identica** è statica — *«l'ultima ripetizione deve pesare di più»*
(final chorus elevation: si modula, si addensa, si aggiunge una voce). La mappa dà
lo scheletro; lo **sviluppo** (la variazione dell'ultimo giro) è la carne, ed è la
faccia successiva.

---

## Il vocabolario

### Le sezioni

`[LIB]` popular-song-forms.md: i mattoni, con cosa fanno —

| sezione | cosa fa | battute tipiche |
|---|---|---|
| **intro** | stabilisce tono, tempo, groove | 4-8 (o 1-2, moderno) |
| **A** / verse | il corpo, la casa | 8 (o 16) |
| **B** / bridge / ponte | il **contrasto**, spesso modula, poi riporta a casa | 8 |
| chorus | il gancio, il ritornello | 8-16 |
| **out** / outro | scarica la tensione, chiude | 4-8 |

### Le mappe canoniche

`[LIB]` popular-song-forms.md, e `[MIS]` casella 9 di
[`docs/repertori/jazz.md`](../repertori/jazz.md) (349 assoli swing con forma
scomponibile, da `wjazzd.db`) —

| mappa | cos'è | dato |
|---|---|---|
| **`A A B A`** | l'**AABA** di 32 battute, la forma più comune del jazz | `[MIS]` **103** assoli |
| **blues** (`A` × N) | il blues di **12 battute**, ripetuto | `[MIS]` **81** assoli; template `Blues` |
| **rhythm changes** | un AABA con l'armonia di *I Got Rhythm* | `[MIS]` **19**; template `I Got Rhythm` |
| **testa / soli / testa** | la testa una volta, poi i soli sul giro, poi la testa | `[LIB]` la prassi del jazz |
| **verse-chorus** | il default del pop | `[LIB]` |
| **intro-build-drop-breakdown** | la forma dell'EDM | `[LIB]` |

⚠️ **Niente filologia** (perimetro, 11 settembre 2026): la mappa è un colore
disponibile, non un obbligo. Si attinge al bagaglio (l'AABA, il blues, il
testa-soli-testa) per una composizione dell'utente, non si replica un genere.

### Le lunghezze

`[LIB]` popular-song-forms.md: default **8 battute** per sezione (o 16); il blues
fa eccezione a **12**. Corto dà urgenza, lungo dà spazio. ⚠️ Una sezione fuori
misura si sente: un chorus di 24 battute è ingombrante, uno di 4 non fa in tempo
a posarsi.

---

## Esempio lavorato: un AABA

`[OSS]` **Ascoltato il 14 settembre 2026**, caricato nel caso storico Deluge (`STRUTTURA01`).
Un AABA vero, la forma più comune del jazz, steso con `mappa della forma`. Due strumenti —
Rhodes per gli accordi, tromba per la melodia — e due materiali: **A** è la casa
(`Cmaj7 Am7 Dm7 G7`, tema medio), **B** il ponte (`Fmaj7 Bb7 Cmaj7 G7`, parte sul
**IV**, tema acuto, chiude sul **V** e riporta a casa). Mappa `A A B A`, sezioni da
4 battute. La timeline realizza la forma. In
lo studio originale ([prova storica](../../provenance/origin-links.md)).

**Verdetto: «suona giusto, approvato».** ⚠️ Si sente la **forma** — l'A che
**torna** riconoscibile, il ponte che **contrasta** e riporta a casa: lo scheletro
regge. È passata al primo colpo, come le altre facce della forma.

## Esempio integrato: una forma narrativa non uniforme

`[CALC]` [`TRAMA02` → `TRAMA06`](brano-completo.md) dispone intro 6, A 8,
variazione 8, build 10, sviluppo 12, ritorno 8 e coda 8 battute. La coda
comincia due battute prima della fine del ritorno. Tema e ground tornano
letteralmente nella prima stesura; nella revisione il basso segue invece
una mappa armonica comune al campo. `[OSS]` La prima orchestrazione ha fallito l'ascolto: la densità
misurata come culmine era invece caos percepito. `TRAMA03` conserva la mappa ma
sposta il culmine su registro, dinamica e timbro, con un solo quartetto di
battute realmente a tre parti. È un esempio composto direttamente sulla
timeline; non estende l'API sequenziale di **mappa della forma**.
`[OSS]` Dopo le correzioni di armonia, basso e livello DX7, l'utente accetta
`TRAMA06` e chiude il task il 2 ottobre 2026: l'esempio integrato e ora
verificato anche all'ascolto, non solo nei dati.

---

## Cosa NON fare

- **non far comporre la forma al codice:** `mappa della forma` stende una mappa che decidi
  tu, non ne inventa una;
- **non ripetere una sezione identica all'infinito senza sviluppo:** una forma che
  non cresce è statica — l'ultima ripetizione deve pesare di più (`place_unique`);
- **non far contrastare il ponte troppo:** un ponte che cambia tutto si scolla — dà
  sollievo restando lo stesso pezzo (popular-song-forms.md);
- **non sbagliare le lunghezze:** 8 battute a sezione è la norma, 12 il blues;
  fuori misura si sente;
- **non aspettarsi che si suoni dalla session view:** è una forma d'arranger —
  `open_in_arranger`, poi play.

---

## Cosa manca a questa istruzione

- ~~l'**arco dinamico**~~ **[fatto](arco-dinamico.md)**: come densità e intensità
  salgono al ponte e ricadono sull'ultimo A (`[MIS]` casella 9). La seconda faccia
  della struttura;
- ~~le **transizioni**~~ **[fatte](transizioni.md)** (i giunti armonico-melodici):
  turnaround, pickup, break, con la clip bianca `variazione`. Resta fuori il
  **fill di batteria**. La terza faccia della struttura;
- ~~un esempio di forma **non uniforme e annidata**~~ **[fatto a livello di
  composizione e ascolto](brano-completo.md)**: `TRAMA06` sovrappone la coda al ritorno.
  Resta da estendere **mappa della forma**: `battute_per` copre lunghezze diverse ma non
  esprime ancora le sovrapposizioni.
