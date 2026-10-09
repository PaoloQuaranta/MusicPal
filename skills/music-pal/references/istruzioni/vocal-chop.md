# Il VOCAL CHOP — affettare una voce e suonarla a ritmo


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/vocal-chop.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

⚠️ **PERIMETRO.** Il vocal chop è un campione vocale **tagliato in fette** (una per
riga di un kit) e **innescato a ritmo**: il «yeah» stutterato di house/garage, il
frammento vocale del trip-hop. È **audio**, non note — riempie la casella 8 di
house/trip-hop, che era rimasta aperta perché è materiale di campioni. ⚠️ Lo
**stesso meccanismo** (affettare un campione in un kit) sblocca il **break tagliato**
di jungle/DnB.

> **La cosa da capire:** non si compone una melodia, si **ricompone un suono a
> pezzi**. Prendi una voce, la tagli, e riordini/ripeti le fette a tempo. Il
> materiale è il campione; la musica è il ritmo del taglio.

---

⚠️ **NIENTE CORPUS** (è una tecnica, non un repertorio): `[LIB]`+`[DEC]`. La
**struttura della fetta** è `[OSS]` (lo Slicer nativo del Deluge e i file veri:
`FINDINGS.md` §«Campioni e tick»).

**Cosa ti serve prima di cominciare:**

- un **campione** vocale sulla SD (`SAMPLES/...`) e la sua lunghezza in **frame**
  (**wav frames**, col wav a portata — SD nel lettore, o `dsysex
  get`);
- **quante fette** (default 16, come lo Slicer; per una parola sola anche 8);
- il contesto (un beat house, un groove trip-hop).

---

## Il grado di prova

| | |
|---|---|
| `[LIB]` | convenzione documentata |
| `[OSS]` | struttura osservata (lo Slicer / i file veri) |
| `[DEC]` | decisione presa qui (il taglio, il pattern) |

---

## 1. Come si taglia

Seleziona intervalli del campione sorgente e assegna ciascun frammento a un
evento innescabile. `[DEC]` Il taglio in N parti uguali è deterministico;
tagliare sui transienti o sulle sillabe può invece seguire il contenuto.
La prima realizzazione storica copre fette uguali, non un rilevatore di sillabe.

## 2. Un innesco, un frammento

`[OSS]` Nel caso storico ogni innesco riproduceva la fetta completa, delimitata
dal suo intervallo sorgente. Il limite della fetta e la modalità di riproduzione
sono due decisioni distinte. Per un altro sampler verifica quale intervallo
viene effettivamente riprodotto e quando termina.

Se si sente la parola intera, controlla prima il pattern: fette contigue
suonate nell’ordine originale ricostruiscono la parola. Non attribuire
automaticamente il risultato alla modalità del sampler.

## 3. Come si compone il chop

`[DEC]` La musica è il **ritmo del taglio**. Le mosse:

- ⚠️ **NON metterle in fila (1-2-3-…-8) contigue**: ricostruiscono la parola e si
  risente l'«mmyeah» intero, non un chop — è l'errore che è costato tre ascolti;
- **buchi**: lascia silenzio fra i frammenti (non un colpo per sedicesimo) — è il
  silenzio a rendere «staccati» i pezzi;
- **stuttera**: ripeti una fetta (`8 8 8`), il glitch ritmico;
- **ri-ordina**: salta fra fette non contigue (`8 · 5 · 1 · 6`), il pattern che non è
  più la parola;
- **innesca a tempo**: sui movimenti, sui levare, in sincope — è una parte ritmica.

Si scrive come una batteria: **scrittura degli eventi**.

## 4. Il legame col break (jungle/DnB)

Il taglio in fette è **lo stesso gesto** su un **break** di batteria: tagli un amen/funky
drummer in fette e le riordini. Il vocal chop e il break-chop sono la stessa tecnica
su materiale diverso. (Il break vero è un altro pezzo/genere; qui c'è il meccanismo.)

---

## I vincoli

| vincolo | perché |
|---|---|
| **ogni innesco deve riprodurre il frammento scelto** | controllare intervallo sorgente, riproduzione e ordine degli eventi |
| **il campione deve essere disponibile al sampler** | risolvere la sorgente prima di valutare il pattern |
| **il chop è ritmo, non melodia** | si riordinano/ripetono le fette a tempo, non si suonano altezze |
| **le fette uguali sono un punto di partenza** | se cadono male sulle sillabe, cambia N o prepara i tagli in un'applicazione audio dedicata |
| **niente riflesso** | il pattern del chop si compone PER il pezzo, all'orecchio |

---

## L'esempio lavorato

[materiale della prova originale](../../provenance/delugepal/docs/istruzioni/vocal-chop.md): l'«mmyeah» (`SAMPLES/RECORD/REC00027.WAV`, 142725 frame)
in **8 fette**, innescate su un beat **house** four-on-the-floor (808) + basso in
levare. Il chop è **spezzettato** (buchi, stutter, salti), non la parola in fila.
⚠️ **Verdetto dell'ascolto (19 settembre 2026): *«ora sento le fette»* — funziona.**
Il pattern e N restano `[DEC]`, da rifinire (quali fette valorizzare si sente).

---

## Cosa manca a questo documento

- il **pitch/stretch** delle fette e gli **effetti** sul vocal: sound design;
- il **break** vero (jungle/DnB): il meccanismo c'è (`kit.affetta`), il genere no.
