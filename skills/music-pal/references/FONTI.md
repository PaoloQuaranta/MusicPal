# Fonti musicali e attribuzioni


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../provenance/delugepal/docs/FONTI.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

## Corpora musicali, e le loro licenze

⚠️ **Questi non sono fonti nel caso storico Deluge: sono il materiale da cui la conoscenza
musicale è misurata**, e a differenza di tutto il resto di questo documento
**portano obblighi di licenza.** Le fonti tecniche qui sopra si citano per
onestà; queste si citano perché è richiesto.

Nessuno dei tre corpora è versionato — stanno in `to-read/`, fuori dal repo, e
non vengono ridistribuiti. Ma i **numeri** che ne escono stanno in
`docs/MUSICA.md` e nelle schede di `docs/repertori/`, che sono pubblicati: è
quello a far scattare l'attribuzione, non il file.

⚠️ **Le licenze sono diverse, e non è un dettaglio.** Due chiedono
l'attribuzione, una ha anche una clausola di reciprocità — vedi in fondo.

### Groove MIDI Dataset — CC BY 4.0

1150 esecuzioni di batteria di dieci batteristi, etichettate per stile, BPM,
metro e `beat`/`fill`. Da qui vengono la **scala di velocity** e i **groove
template** della casella 6 del jazz, e il feel del primo pezzo jazz.

- **Licenza:** Creative Commons Attribution 4.0 International (CC BY 4.0),
  <https://creativecommons.org/licenses/by/4.0/>. Letta dal file `LICENSE`
  **dentro il dataset**, non dal web.
- **Citazione richiesta**, dalla pagina del dataset:

      Jon Gillick, Adam Roberts, Jesse Engel, Douglas Eck, and David Bamman.
      «Learning to Groove with Inverse Sequence Transformations.»
      International Conference on Machine Learning (ICML), 2019.

- <https://magenta.tensorflow.org/datasets/groove>

La CC BY chiede **l'attribuzione e nient'altro**: si può usare per qualunque
scopo, anche commerciale, purché si dica da dove viene.

### Jazz Trio Database (JTD) — MIT

1294 esecuzioni di trio jazz del 1947–2015 — **34 pianisti, 98 bassisti,
106 batteristi** — con gli onset di **piano, basso e batteria allineati agli
stessi beat**, la posizione metrica, e il MIDI del solo piano. Da qui vengono
i numeri della **casella 5 del jazz**, «ruoli e spartizione».

⚠️ **È l'unico corpus in casa che ha l'insieme che suona insieme.** Il Groove
MIDI è batteria sola, WJazzD è la linea solista sola: nessuno dei due può dire
come i tre si rispondono, e per questo l'handoff dava quella misura per
impossibile fino al 1 settembre 2026.

- **Licenza:** MIT — `The MIT License (MIT) Copyright (c) 2023, Huw Cheston`.
  ⚠️ Presa dal **repository**, non da dentro l'archivio: a differenza del
  Groove MIDI, lo zip delle annotazioni **non porta un file di licenza**. La
  MIT chiede che la nota di copyright e la nota di permesso accompagnino
  «copie o porzioni sostanziali» del materiale: qui non se ne ridistribuisce
  nessuna, e la citazione resta comunque dovuta.
- **Citazione richiesta:**

      Huw Cheston, Joshua L. Schlichting, Ian Cross, Peter M. C. Harrison.
      «Jazz Trio Database: Automated Annotation of Jazz Piano Trio Recordings
      Processed Using Audio Source Separation.» Transactions of the
      International Society for Music Information Retrieval, 2024.

- <https://github.com/HuwCheston/Jazz-Trio-Database>

⚠️ **Cosa NON porta, e va saputo prima di citarlo.** Gli onset di basso e
batteria **non hanno altezze**, e quelli di batteria **non dicono quale pezzo
del kit** ha suonato: un'affermazione del tipo «il rullante fa X» non è
ricavabile da questa fonte. E le annotazioni sono **automatiche** — F-measure
dichiarata 0,94 sugli onset — con **34 brani su 1294** validati a mano.
L'audio, che va richiesto agli autori, **non serve e non è stato chiesto**.

### Weimar Jazz Database (WJazzD) — ODbL 1.0

456 assoli jazz trascritti a mano, con gli accordi e i battiti allineati alla
linea. Da qui vengono lo **swing misurato** della casella 4 e il **giro
armonico** del primo pezzo jazz.

- **Licenza:** Open Database License (ODbL) 1.0 per il database,
  <https://opendatacommons.org/licenses/odbl/1.0/>; i contenuti individuali
  sotto Database Contents License (DbCL) 1.0,
  <https://opendatacommons.org/licenses/dbcl/1.0/>.
- **Autore:** The Jazzomat Research Project (c) 2012-2017
- **Versione:** 2.1, `status` FINAL, creata il 2018-01-07
- <https://jazzomat.hfm-weimar.de/>

  ⚠️ **Licenza, autore e versione vengono dal database stesso**, tabella
  `db_info`, non da una pagina web:

      sqlite3 to-read/MIDI/wjazzd.db "select * from db_info"

  Per un database è la fonte più autoritativa che esista, ed è a portata di
  query. Vale la pena saperlo perché la licenza dell'ODbL **non l'avrei
  indovinata**: a occhio sembrava un caso da Creative Commons come l'altro.

- **Citazione richiesta**, dalla pagina del progetto:

      Pfleiderer, Martin; Frieler, Klaus; Abeßer, Jakob; Zaddach,
      Wolf-Georg; Burkhart, Benjamin (a cura di) (2017): Inside the
      Jazzomat — New Perspectives for Jazz Research. Schott Campus.

  ⚠️ La pagina, letta il 29 agosto 2026, ha reso il terzo nome come
  «Abessert». È quasi certamente un artefatto della **ß**, e il nome corretto
  è **Abeßer**. Scritto corretto e segnalato qui, invece che copiato com'era o
  corretto in silenzio: in un'attribuzione di licenza il nome di una persona è
  precisamente la cosa che non si tira a indovinare. Chi può, lo verifichi
  sulla pubblicazione.

### La clausola che l'ODbL ha e la CC BY no

⚠️ **L'ODbL è share-alike sui database derivati**: chi *distribuisce* un
database derivato da WJazzD deve distribuirlo sotto la stessa licenza. La CC BY
del Groove MIDI non chiede niente del genere.

Cosa questo progetto pubblica oggi, in fatto: **misure aggregate** — mediane,
conteggi, distribuzioni, e un giro armonico di dodici battute — dentro documenti
in prosa, non porzioni del database né un database. Il `.db` non è versionato e
non viene ridistribuito.

⚠️ **Questo è il quadro dei fatti, non un parere legale, e non è una cosa che
decide un agente.** Se il progetto un giorno pubblicasse estratti riga per riga,
o un file derivato interrogabile, la domanda andrebbe posta a chi di dovere
prima, non dopo.

---
