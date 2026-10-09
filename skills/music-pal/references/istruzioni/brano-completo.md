# Dal materiale al brano completo: `TRAMA02` → `TRAMA06`


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../../provenance/delugepal/docs/istruzioni/brano-completo.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.


**Chiuso il 2 ottobre 2026.** `[OSS]` Dopo TRAMA06 l'utente risponde
«ok, possiamo chiudere il task compositivo e riempire le caselle».
La chiusura riguarda questo brano originale di IDM cameristica e le conoscenze
che ha messo alla prova, non l'intero repertorio IDM o il contrappunto storico.
Le versioni precedenti restano controesempi documentati, non prove riuscite.
**A cosa serve.** Le prove isolate dicono se un canone, un ground o una
variazione sono corretti. Un brano completo deve farli cooperare dentro una
forma abbastanza lunga da creare memoria, contrasto, culmine e congedo. Questa
istruzione documenta sia l'integrazione sia la sua correzione dopo l'ascolto:
un file formalmente valido può ancora fallire come musica.

Il materiale viene dagli studi già ascoltati di
[forma storica elettronica](forma-storica-elettronica.md): il tema di
`INVERT01`/`VARIAZ01`, il controcanto e il ground. La disposizione, il beat e i
timbri sono decisioni compositive `[DEC]`.

## La forma conservata

lo studio originale ([prova storica](../../provenance/origin-links.md)) costruisce cinque
parti — FILO, OMBRA, CAMPO, GROUND e kit — per **58 battute a 102 BPM**:

| intervallo battute (zero-based, fine esclusa) | sezione | funzione |
|---|---|---|
| [0, 6) | intro | campo lento e frammenti del tema |
| [6, 14) | A | tema, poi risposta della controvoce |
| [14, 22) | A-var | variazione e passaggio fra due timbri |
| [22, 32) | build | crescita di registro e dinamica, senza accumulo di note |
| [32, 44) | sviluppo | preparazione, unico episodio a tre parti, culmine rarefatto |
| [44, 52) | ritorno | tema letterale e due tracce lasciate nella coda |
| [50, 58) | coda | tema aumentato sopra il pedale, strati in sottrazione |

`[CALC]` La coda è **annidata** nel ritorno. Le durate 6/8/8/10/12/8/8
rompono la successione di blocchi uguali; **mappa della forma** non esprime ancora
sezioni sovrapposte, quindi la timeline è scritta direttamente.

## `TRAMA02`: esito negativo d'ascolto

`[OSS]` Il 1 ottobre 2026 l'utente ha respinto `TRAMA02`: batteria priva di
continuità perché variava come una voce contrappuntistica; suoni delle parti
alte banali; contrappunto troppo denso e caotico. Il basso e il suono del kit
erano invece gli elementi salvati dal giudizio.

Questo esito **non conta come copertura percettiva riuscita**. I vecchi
guardiani dimostravano tema, ground, indipendenza ritmica, assenza di parallele
e un arco crescente di attacchi; non dimostravano che tutte quelle proprietà
fossero desiderabili insieme. In particolare il massimo arrivava a 25 colpi di
batteria per battuta e le due voci superiori figuravano contemporaneamente.

## `TRAMA03`: revisione IDM cameristica

`[CALC]` La revisione conserva il tema letterale alle battute 6–10, il ground
di quattro battute nei nove inizi 6, 10, 14, 18, 32, 36, 40, 44 e 48, la coda
aumentata un'ottava sotto e la forma di 58 battute. Cambia invece il modo in cui
il materiale occupa il tempo:

- gli attacchi delle due voci superiori scendono da **367 a 123**;
- non esiste una battuta con entrambe le voci superiori fitte;
- fuori dalle battute 36–40 si incontrano soltanto nelle quattro battute di
  risposta 10–14 e nelle due battute sovrapposte 50–52;
- le battute 31 e 43 sono vuoti reali delle due voci superiori;
- il solo episodio a tre parti dura quattro battute e alterna la voce attiva:
  FILO 3/1/4/1 attacchi, OMBRA 1/3/1/4, GROUND 2/2/2/2;
- le tre coppie dell'episodio hanno simultaneità 22,2%, 22,2% e 0% e nessuna
  quinta o ottava parallela.

`[CALC]` Cassa e rim mantengono per tutte le battute 6–52 lo stesso scheletro:
cassa a 0 e 216 tick, rim a 96 e 288. Solo i quattro giunti 21, 31, 43 e 51
aggiungono un fill; altrove il charleston cambia soltanto per sottrazione da una
griglia fissa. La coda toglie progressivamente i layer dopo la battuta 52.

I tre suoni non sono più varianti cosmetiche dello stesso synth:

- **FILO**: voce DX7 originale a tre coppie, brillante e articolata, con
  risposta del filtro alla velocity;
- **OMBRA**: ring modulation, passa-banda risonante mosso dall'inviluppo,
  inviluppo breve;
- **CAMPO**: oscillatori continui, wavefold, filtro notch lento, movimento
  casuale nello stereo e `grainFX`.

## Stato della prova

`[CALC]` `TRAMA03` contiene cinque strumenti, termina esattamente a 58
battute e passa i guardiani dedicati, **validazione tecnica** e **avvisi tecnici**.
`[OSS]` Dopo caricamento e ascolto, l'utente conferma soltanto il ritmo della
batteria: il resto migliora poco, alcuni punti sembrano armonicamente incoerenti,
il basso incerto, FILO quasi inudibile anche al massimo. OMBRA aveva troppi
armonici; l'utente l'ha filtrata e risalvata in `TRAMA03`. Anche questa versione
non è copertura percettiva riuscita dell'insieme.

## `TRAMA04`: armonia condivisa e correzione di FILO

lo studio originale ([prova storica](../../provenance/origin-links.md)) parte dalla 03
appena riscaricata, conservando suoni, mix e batteria del salvataggio. La correzione timbrica fatta dall’utente su OMBRA viene conservata; i valori
del sintetizzatore restano documentati nell’adapter storico.

`[CALC]` La 03 aveva cicli diversi per basso e CAMPO. Alla battuta 29,
La–Do♯ della controvoce si sovrapponeva a Mi♭–Si♭ del campo e del basso.
Ridurre il numero di attacchi non corregge quella relazione.

`[DEC]` La 04 rilegge il tema come **Sol dorico** (Sol, La, Si♭, Do, Re, Mi,
Fa): le note originali di FILO restano identiche. Una sola mappa di 58 battute
assegna la fondamentale al basso e le due voci a CAMPO. La prima esposizione
usa fondamentali **Sol–Do–Fa–Sol**; il basso articola la stessa fondamentale
a 0 e 216 tick, insieme alla cassa, senza cambiare altezza nella battuta.
Registro Fa1–Do2. Le due note Mi♭ di OMBRA diventano Mi e i due Do♯ diventano
Do; l'ultimo Do della coda risolve su Si♭ sopra Sol. Il campo resta assente
nell'episodio a tre parti e nei vuoti 31 e 43.

`[CALC]` Il livello percepito di FILO dipendeva anche da un inviluppo esterno
agli operatori FM. La prima correzione rimuove un’attenuazione certa nella catena.
`[OSS]` L’intervento non bastò: il tema restò quasi inudibile. Una relazione
corretta fra note non garantisce che il timbro e il livello la rendano percepibile.

Sette test verificano conservazione del salvataggio, mappa realizzata,
appoggio del basso, inviluppo DX7, silenzi, coda e round-trip locale.
`[OSS]` Dopo ascolto l'utente trova la 04 un po' meglio, ma FILO resta
praticamente inudibile anche col master della voce al massimo.
Nessun timeout, blocco parziale o riapertura.
Suite completa: 2378/2378.
## `TRAMA05`: livelli delle portanti FILO

`[DEC]` Su indicazione dell'utente, solo output level delle portanti DX7
1/3/5 aumentato di 17: **82→99, 74→91, 66→83**. Modulatori 2/4/6
invariati a 67/61/55. Algoritmo 5, rapporti, inviluppi, velocity, filtri,
volume della voce e song, note, batteria e OMBRA restano identici alla 04
appena riscaricata ([materiale della prova originale](../../provenance/delugepal/docs/istruzioni/brano-completo.md)).

`[CALC]` **SY.update_dx7_patch** modifica una voce esistente senza il reset
effettuato da **SY.set_dx7**. Il confronto dell'intera song riletta conferma
soltanto il livello interno delle portanti FILO. Gli altri suoni e il
materiale musicale restano quelli già corretti.

Su richiesta dell'utente, dalla 05 appena riscaricata: portanti 1/3/5
tutte a **99**, sensibilita alla velocity **5/4/3→2/2/2**. Il primo output
level era gia al massimo. La sensibilita alla velocity agisce sul livello
degli operatori, come descritto nel
[modello DX7 del motore](https://github.com/google/music-synthesizer-for-android/blob/master/wiki/Dx7Envelope.wiki);
qui e ridotta solo sulle portanti. Questo intervento cambia anche il bilanciamento
delle tre coppie rispetto alla 05, non i loro rapporti o modulatori.
Tutti gli altri dati della song sono identici alla fonte fresca
[materiale della prova originale](../../provenance/delugepal/docs/istruzioni/brano-completo.md), verificato ripristinando il solo payload
originale e confrontando l'intero documento.
Verifica/avvertenze vuote.
`[OSS]` La 06 e stata accettata e il task compositivo chiuso dall'utente.
Riscaricata per archivio locale in [materiale della prova originale](../../provenance/delugepal/docs/istruzioni/brano-completo.md): stesso hash
del file inviato e rigenerato.
I file song restano privati in `out/`, secondo
la politica del repository; codice, test e documentazione sono versionati.
## Caselle compilate dal brano

Nella [scheda IDM](../repertori/idm.md), le caselle **7, 8 e 9** passano da
parziali a compilate per i due territori dichiarati:

| casella | conoscenza utilizzabile |
|---|---|
| 5 · ruoli | tema/risposta/campo/basso/beat separati; una sola voce superiore fitta alla volta |
| 6 · dinamica | continuita del beat; culmine con registro e timbro; livello DX7 distinto dal master |
| 7 · armonia | Sol dorico; una mappa comune per fondamentali e campo; risoluzione della coda |
| 8 · melodia | tema, risposta, variazione, ritorno letterale e aumentazione |
| 9 · forma | arco lungo non uniforme; coda sovrapposta; due vuoti e culmine rarefatto |
| 10 · Deluge | conservazione dei suoni risalvati; revisione DX7 senza reset; rilettura verificata |
| 11 · trappole | non trasferire il contrappunto alla batteria; evitare cicli armonici incoerenti e preset troppo deboli |

Le caselle 5/6/10/11 erano gia compilate e ricevono nuove evidenze, non un
nuovo stato. La casella 1 resta parziale per i sottogeneri non ancora provati.

## Cosa insegna alla copertura

- una proprietà formalmente corretta può diventare un difetto quando viene
  applicata simultaneamente a troppe parti;
- la batteria può segnare la forma conservando lo scheletro e variando per
  sottrazione o con pochi fill nominati;
- in una tessitura contrappuntistica elettronica il culmine non richiede il
  massimo numero di attacchi: registro, dinamica e timbro possono portarlo;
- la copertura percettiva cresce soltanto dopo l'ascolto; `TRAMA02` e `TRAMA03`
  registrano fallimenti utili, `TRAMA04` migliora un po' e `TRAMA06` chiude il caso;
- basso, campo e tema devono condividere una direzione armonica: tre linee
  valide prese separatamente non garantiscono un insieme coerente;
- un guardiano della libreria può essere neutralizzato dal generatore:
  l'inviluppo DX7 va verificato anche nel file finale.
