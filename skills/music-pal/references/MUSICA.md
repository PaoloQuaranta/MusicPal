# Conoscenza musicale — cosa funziona sul materiale di questo utente


> Conoscenza musicale estratta da DelugePal, commit `cbf99ff305be`.
> [Documento originale e contesto delle prove](../provenance/delugepal/docs/MUSICA.md).
> API e trasferimenti appartengono agli adapter; le osservazioni storiche non certificano altre macchine.

Questo documento raccoglie il metodo, il mestiere e le lezioni compositive
verificate nel progetto originale. È utilizzabile insieme alle istruzioni
di questa skill senza installare altre skill o collegare un dispositivo.
Le sue osservazioni hanno il perimetro dichiarato accanto a ciascuna prova.

Il perimetro è largo — jazz, poi classica, barocca e antica, poi i
contemporanei: elettronica, IDM, techno, hip hop, trip hop, dub, DnB, jungle —
e un documento a forma di un genere solo non lo regge. Quindi qui stanno tre
cose e nient'altro: **lo schema** con cui si descrive un repertorio qualunque,
**il comune** che vale per tutti, e **l'indice** delle schede. Un repertorio
compilato è una scheda in [`repertori/`](repertori), una per file.

**Come si legge: lo schema più una scheda sola, mai tutte.** Le schede non
si leggono in fila e non si leggono per intero — si guarda lo schema per sapere
in quale casella cade la domanda, e poi quella casella nel repertorio su cui si
sta lavorando. Si caricano 1–3 file pertinenti alla domanda, partendo dalla navigazione della skill.

Stessa disciplina del resto del progetto: si scrive ciò che è stato
verificato, e si segna `[IPO]` ciò che è supposto.

I marcatori, e cosa vuol dire ciascuno:

| marcatore | vuol dire |
|---|---|
| `[MIS]` | misurato su un corpus di musica, col numero e con quanti casi |
| `[WEB]` | preso da ricerca web, con la fonte |
| `[OSS]` | osservato nei file del corpus, coi numeri |
| `[MAN]` | affermato dalla documentazione |
| `[IPO]` | ipotesi non verificata |

**Il marcatore sta accanto all'affermazione che qualifica**, mai raccolto
in una lista a parte: un elenco di «cose misurate» separato dalle cose misurate
invecchia male, e dopo un mese non si sa più quale numero fosse quale.

E una regola contro la duplicazione, la stessa che vale nel codice: **un
numero vive in una casella sola.** Due repertori che si toccano si toccano con
un **rimando**, non con una copia — altrimenti fra un mese ci sono due valori
diversi in due file e nessuno sa quale è stato misurato. E *come* si è
misurato non sta qui affatto: sta in [`FINDINGS.md`: contesto storico](../provenance/delugepal/docs/FINDINGS.md) e in
[`ARCHITETTURA.md`: contesto storico](../provenance/delugepal/docs/ARCHITETTURA.md). Lì c'è come si è misurato, qui come si
usa.

---

## Lo schema: dieci caselle musicali

Le caselle sono formulate come **domande**, non come campi. Il test usato
per sceglierle: **devono sopravvivere sia a Josquin sia alla jungle.** Uno
schema ricavato dai due repertori che il progetto ha già in mano avrebbe
caselle come «griglia a 16 passi» o «velocity groove», e nella musica antica
sarebbero vuote non per mancanza di ricerca ma perché la domanda non si pone.

Il guadagno vero non è l'ordine, è la **collisione**. A documento
organizzato per genere l'*inégalité* barocca e lo swing del jazz non si
sfiorano mai, mentre sono la stessa domanda — dove cade il levare dentro il
movimento — fatta a due repertori. Nello schema cadono tutt'e due nella
**casella 4**, e lì uno dei due ha già la risposta misurata.

Le dieci caselle musicali, sempre tutte e sempre in quest'ordine. Nelle schede sono titoli
di livello 2, con esattamente questo testo. Gli ID originali 1–9 e 11 sono conservati;
la casella 10 descriveva il Deluge e ora appartiene al suo adapter.

### 1. Cos'è, e cosa non è

I confini, e l'errore tipico di chi lo confonde con un vicino.
**Compilarla** vuol dire saper dire cosa il repertorio *non* è, e con che cosa
lo si scambia. **Vuota** vuol dire che se ne hanno le etichette e non il
mestiere — ed è la lezione più cara del progetto: una ricerca sola su un genere
basta a scrivere qualcosa di formalmente corretto e musicalmente morto.

### 2. Metro e griglia

Quale unità, quanti passi, quanto è rigida la griglia. **Compilarla**
vuol dire poter scrivere un pattern senza chiedersi su che cosa lo si conta.
**Vuota** vuol dire che non si sa in quale unità porre le domande dalla 4 in
poi.

### 3. Tempo

Il range vero, e cosa cambia ai bordi. **Compilarla** vuol dire un
intervallo con dentro il centro del repertorio, non un valore solo. **Vuota**
vuol dire che il tempo si sceglierà per abitudine, e l'abitudine è quella del
repertorio precedente.

### 4. Feel

Dove cadono le note rispetto alla griglia: swing, *inégalité*,
laid-back, rubato — oppure «dritto, ed è una scelta». È la casella dove i
repertori collidono, e l'unica del progetto che abbia numeri `[MIS]`.
**Vuota** vuol dire che si suonerà quantizzato.

### 5. Ruoli e spartizione

Chi occupa cosa, e soprattutto **cosa lascia libero**. Il [basso continuo](istruzioni/basso-continuo.md)
più le voci, il comping più il walking, le sei parti del reggae: è la stessa
domanda fatta a repertori diversi. **Vuota** vuol dire parti che si
sovrappongono senza che nessuno l'abbia deciso.

### 6. Dinamica

Accenti, fantasmi, dinamica terrazzata — o «non è questo il parametro»,
che è a sua volta una risposta. **Compilarla** vuol dire numeri, non aggettivi.
**Vuota** vuol dire colpi tutti uguali, e un risultato che marcia invece di
respirare.

### 7. Armonia

Vocabolario, ritmo armonico, condotta delle parti. Una casella 7 che tace su
come si muovono le voci sta tacendo sul pezzo che manca. ⚠️ **Il buco c'è
stato fino al 29 agosto 2026**, ed è chiuso: **realizzazione armonica** copriva il solo
**vocabolario** — sigle e voicing — e ora usa **condotta delle parti**, che posa
ogni accordo dove muove meno voci. Restano fuori il **ritmo armonico** e le
**sostituzioni**.

### 8. Melodia e ornamentazione

Materiale, sviluppo, e cosa si improvvisa invece di scriverlo.
**Vuota** vuol dire note giuste e nessun discorso: la differenza fra una scala
percorsa e una frase.

### 9. Forma e densità

La scala lunga, l'arco. Questa casella esiste perché tutto il resto di una
scheda descrive **una battuta**:

> Un pezzo ne dura centoventi.

La prova di [basso ostinato](istruzioni/basso-ostinato.md) mostra un caso di
identità nel basso e trasformazione della superficie lungo cinque ritorni.
Il [brano completo `TRAMA02` → `TRAMA06`](istruzioni/brano-completo.md)
integra tema, ground, sviluppo a tre parti e coda sovrapposta in 58 battute.
`[OSS]` `TRAMA02` ha fallito l'ascolto per batteria discontinua, suoni alti
banali e contrappunto caotico; non conta come copertura percettiva riuscita.
`TRAMA03` conserva forma e materiale, ma dimezza abbondantemente le voci alte,
stabilizza il groove e separa FM, ring modulation e campo granulare. `[OSS]`
L'ascolto conferma solo la batteria: armonia e basso restano incerti, FILO è
quasi inudibile e OMBRA viene corretta dall'utente. `TRAMA04` parte da quel
salvataggio, coordina basso e campo in Sol dorico e apre l'inviluppo esterno
DX7. `[OSS]` L'utente trova la 04 un po' meglio, ma FILO resta quasi inudibile.
`TRAMA05` alza le portanti DX7; `TRAMA06` aumenta ancora il livello interno
e riduce la sensibilita alla velocity delle portanti. `[OSS]` Il 2 ottobre
2026 l'utente accetta la 06 e chiude il task compositivo. Il percorso copre
ora un brano cameristico completo all'ascolto; nella scheda IDM si compilano
armonia, melodia e forma per il perimetro provato, senza estenderlo a tutti i sottogeneri.

**Vuota** vuol dire un arrangiamento che accende tutte le parti all'inizio e
le lascia accese.

### 11. Trappole del generatore

Cosa sbaglia un programma **per costruzione** in questo repertorio. Sta
per repertorio e non in un registro unico, perché «cosa sbaglia un generatore
*qui*» non si trasferisce: le trappole del dub, raccolte in una lista comune,
sembrerebbero lezioni generali e non lo sono.

### Lo stato di una casella, e perché una casella vuota è informazione

La prima riga non vuota di una casella dichiara il suo stato, così si legge
senza contare niente:

| la casella comincia con | vuol dire |
|---|---|
| `**Vuota.**`, o `**Vuota, …**` | non c'è ancora niente |
| `**Parziale.**` | c'è qualcosa, e la casella dice cosa manca |
| qualunque altra cosa | è piena |

**Una casella vuota è informazione, non uno spazio bianco.** «Jazz /
6. Dinamica: vuota» è un compito, e una casella vuota o parziale **dichiara
cosa servirebbe per completarla** — quale lettore, quale corpus, quale misura.
Così l'agenda del progetto si legge dallo schema invece che da una lista tenuta
a parte, e i lettori che verranno atterrano da soli nella casella che
riempiono.

⚠️ **Ma l'agenda dice cosa manca, non in che ordine riempirlo**, e dal 30 agosto
2026 l'ordine lo decide il pezzo che si sta scrivendo: vedi «Le caselle si
riempiono SU DOMANDA» nel comune. Riempirle a tappeto costa mesi e produce
righe che nessuno mette alla prova — è già successo due volte, e le due caselle
scritte in anticipo dicevano il falso.

Per lo stesso motivo le dieci caselle musicali ci sono **sempre tutte**, anche quando sono
vuote: è quello che permette di sapere dove guardare senza leggere, e di vedere
cosa manca senza che qualcuno debba accorgersene.

---

## Il comune

Quello che vale per **ogni** repertorio. Sta qui e non nelle schede per la
stessa ragione per cui un numero vive in una casella sola: scritto una volta,
si corregge una volta.

Due parti: **metodo**, come si lavora e a chi si crede; **il mestiere**,
la musica che non dipende dal repertorio. La realizzazione sta negli adapter. Dove un pezzo di comune alimenta una casella precisa, la casella è
nominata.

### Metodo

#### Il corpus dà RELAZIONI, non superfici — 30 agosto 2026

**È la regola che dice cosa si può prendere da un corpus, ed è stata data
dall'utente il 30 agosto 2026 dopo aver ascoltato tre pezzi:**

> «Credo sia importante sottolineare che noi vogliamo un tool per AI per
> creare musica **ORIGINALE**, non repliche dei pattern studiati. Vogliamo
> usare quel database per produrre qualcosa di **nuovo ma coerente con il
> contesto**.»

⚠️ **Non è un desiderio, è un criterio di accettazione, e va applicato PRIMA
di prendere una misura.** Una misura si può usare per generare se descrive una
**relazione** — fra una nota e la sua funzione, fra una frase e la sua fine,
fra una sezione e quella dopo. Non si può usare se descrive una **superficie**:
quali passi ha colpito quel batterista, con che frequenza quel solista ha
suonato quel grado.

Le relazioni generalizzano, e ogni cosa che ne esce è nuova. Le superfici sono
**di chi le ha suonate**, e riprodurle è una copia con del rumore sopra.

##### L'inventario, fatto il giorno in cui la regola è arrivata

Vale come esempio di come si applica, e perché non è ovvia: metà del lavoro
del jazz stava dalla parte giusta e metà no, senza che nessuno se ne fosse
accorto.

| dalla parte **giusta** — relazioni | |
|---|---|
| una frase atterra su fondamentale, quinta o settima minore | è una regola: ogni linea che ne esce è diversa |
| un motivo è di almeno cinque note e ricorre | regola |
| l'arco di densità sulla forma | una **forma**, non un pattern |
| una corsa dura una battuta e le corse si addensano | regole |
| la condotta delle parti per minimo movimento | **calcolata**, non copiata da nessuno |
| le griglie armoniche (blues, rhythm changes) | modelli condivisi, non composizioni |

| dalla parte **sbagliata** — superfici | |
|---|---|
| il pattern di batteria campionato dalle frequenze di **una** esecuzione | riproduce le abitudini di quel batterista |
| le altezze dell'assolo campionate da un istogramma di gradi | dà note con la statistica giusta, non una linea con un'intenzione |

⚠️ **E un caso grigio, che non va risolto per decreto: il groove template.**
Velocity e microtiming presi da un'esecuzione nominata sono un trasferimento
di *feel*, quello che qualunque DAW fa con un groove template — ma restano la
copia della tempistica di un esecutore. Sta qui perché l'ascolto lo ha
approvato tre volte, e perché la sua alternativa (inventare un microtiming)
sarebbe peggio. **Chi lo usa lo sappia; chi lo togliesse non sbaglierebbe.**

##### La prova da fare prima di prendere una misura

**Due generazioni con la stessa misura devono poter essere diverse.** Se la
misura fissa *cosa* si suona, è una superficie; se fissa *come si sta* — dove
si atterra, quanto si cresce, cosa risponde a cosa — è una relazione.

##### Il difetto che ha fatto arrivare la regola

Il 30 agosto 2026 la batteria dei tre pezzi jazz è stata resa varia
campionando le frequenze di tre esecuzioni diverse. Ha risolto il sintomo — i
tre pezzi non suonavano più uguali — **col metodo sbagliato**, e l'utente ha
sentito subito il difetto nuovo:

> «La batteria in questi pezzi suona discontinua rispetto a basso e piano che
> sono praticamente costanti. Le interruzioni, accenti e struttura delle parti
> di batteria sono strettamente correlati alla sezione ritmica, e non le puoi
> applicare acriticamente.»

Misurato: deviazione standard dei colpi per battuta, **batteria 1,48-1,65**,
comping 0,54-0,61, **basso 0,00**. La batteria varia contro uno sfondo fermo.

⚠️ **E la correlazione che servirebbe non è misurabile da nessun corpus in
casa:** il Groove MIDI è batteria sola, `wjazzd.db` è la linea solista sola.
**Nessuno dei due ha l'insieme suonare insieme.** È il muro della casella 5.

#### Le caselle si riempiono SU DOMANDA — 30 agosto 2026

**Lo schema ha dieci caselle musicali e il perimetro ha quattro repertori: quarantaquattro
caselle.** Riempirle a tappeto è un lavoro di mesi, e il 30 agosto 2026 l'utente
ha proposto di non farlo:

> «Visto che il repertorio è mastodontico, non credo sia possibile pensare a un
> riempimento completo di tutte le caselle… io punterei a usare questo primo
> passaggio sul blues per creare un metodo di riempimento delle caselle, da
> applicare **in itinere ogni volta che il task compositivo lo richiede**.»

**Ha ragione, e non è un'opinione: sta nei tempi dei commit.**

| | come è stata riempita | quanto è costata |
|---|---|---|
| **casella 6** del jazz, dinamica | *a tappeto*, senza che nessun pezzo la chiedesse | **undici giorni** (18-29 agosto, due rami) |
| **caselle 8, 7 e 11** del jazz | *su domanda*, ognuna aperta da un difetto sentito | **circa otto ore in tutto**, 29-30 agosto |

Venti volte, per casella. E la casella 6 è quella che ha prodotto il rabbit
hole di `HANDOFF.md` §6-quindecies.

##### Il ciclo

1. **Genera con quello che c'è**, dichiarando ogni ripiego. Una casella vuota
   non ferma un pezzo: dice solo con che grado di prova esce quel che ne
   dipende.
2. **Fai ascoltare.**
3. ⚠️ **Il difetto nomina la casella.** «Poco pirotecnico» → la 8. «Alcune note
   sembrano fuori tonalità» → i gradi. «Le frasi finiscono su note che non hanno
   senso» → gli atterraggi. Non si sceglie la casella da un'agenda: la sceglie
   l'orecchio.

   ⚠️ **E la domanda ha due forme, non una** — aggiunto il 30 agosto 2026,
   aprendo la casella 9. Oltre al **difetto sentito** in un pezzo che c'è,
   c'è il **limite di capacità**: un pezzo che si vuole scrivere e non si può.
   La 9 è stata aperta così — «Pal sa scrivere solo un blues perché la forma è
   cablata» — e non da un ascolto. Vale come domanda a tutti gli effetti,
   purché sia **un pezzo vero che si vuole**, non «prima o poi servirà»: è
   quest'ultimo che riporta al lavoro a tappeto.
4. **Misura solo quello**, col bersaglio fissato **prima** dei numeri.
5. **Rimettilo nel generatore, UNA COSA ALLA VOLTA.**
6. **Riascolta.** Se peggiora si torna indietro — è successo, `JAZZ04`.
7. **Scrivi la correzione con la data**, nella casella che le compete.

⚠️ **Il passo che fa la velocità è il 3.** Non si misura mai ciò di cui nessuno
si è lamentato. È esattamente ciò che la casella 6 ha fatto per undici giorni, e
gli ultimi quattro *dentro una casella già chiusa*.

##### E una casella scritta senza domanda invecchia SBAGLIATA

Non è solo lentezza. È il difetto che si è visto **due volte nello stesso
giorno**, il 29-30 agosto, e una terza volta il 1 settembre — la più cara delle
tre, perché quella riga aveva **cambiato il piano di lavoro**:

| casella | diceva | com'era |
|---|---|---|
| **jazz 7**, armonia | «la chiuderebbe `assets/jazz-voicings.md`… manca implementarla, non trovarla» | quella fonte **non specifica affatto** l'alternanza A/B: nomi ambigui per sua stessa ammissione, esempio che non usa nessuna delle due forme, e una regola che fallisce sul proprio esempio |
| **jazz 9**, forma | «la chiuderebbe MusicXML o le lead sheet: il lettore va scritto, non procurato» | la colonna `form` di `wjazzd.db` la porta su **tutti e 361** gli assoli swing |
| **jazz 5**, ruoli | «nessun corpus in casa ha l'insieme che suona insieme… non è questione di quanti dati: è che il dato non c'è» | il dato c'era, a un download di distanza e con licenza MIT (Jazz Trio Database, 1294 trii). ⚠️ E il MusicXML che quella riga chiedeva **non l'avrebbe chiusa comunque**: nel più grande corpus libero oltre il 90% degli spartiti ha meno di cinque parti |

Tutte e due **mandavano a cercare fuori qualcosa che era già in casa**, e
nessuna delle due era stata messa alla prova perché nessun pezzo gliel'aveva
chiesto. Una riga così costa più di una casella vuota: una casella vuota dice
«non lo so», questa dice «va' di là» e sbaglia direzione.

##### I due limiti, che sono veri e vanno tenuti

⚠️ **1. Su domanda si misura stretto, e stretto vale stretto.** Gli atterraggi
della casella 8 sono misurati su blues `A12` a feel `SWING`: che valgano su un
AABA o su una ballad **non è noto**. La disciplina dei gradi — `[MIS]` contro
`[OSS]`, e «quante esecuzioni, quanti esecutori» — va estesa al **contesto** e
non solo alla numerosità. Una misura porta con sé il perimetro in cui è stata
presa, e chi la riusa fuori da lì lo sta assumendo, non sapendo.

⚠️ **2. Alcune caselle hanno prerequisiti che non si scoprono a metà pezzo.**
Quelle vanno **viste arrivare**: il metodo su domanda copre tutto ciò che è
**già raggiungibile**, e quel che richiede infrastruttura nuova va tenuto in
una lista corta e dichiarata, perché nessun ascolto la può produrre al volo.

⚠️ **Ma l'unico esempio che questa regola aveva è crollato il 1 settembre
2026, e la regola resta senza.** Diceva: «la casella 5 vuole un lettore
MusicXML: non è una cosa che si trova mancante alle cinque e si risolve alle
sei». La casella 5 è stata chiusa in un pomeriggio, con **200 righe di
stdlib** su un corpus che era a un download di distanza — e il lettore
MusicXML non c'entrava. La regola non è per questo sbagliata; è **senza
prova**, e chi la invoca per rimandare un lavoro deve portare l'esempio che
qui manca. Il costo di crederle senza verificare è misurato: il lavoro giusto
era raggiungibile da due giorni e nessuno aveva guardato.

##### Cosa NON segue da qui

- **non che le misure non servano.** La misura ha localizzato in un colpo un
  difetto invisibile a orecchio nudo — il grado 11 al triplo della sua quota,
  e *solo* sulle due battute delle corse;
- **non che una casella vada chiusa in fretta.** Va **aperta** solo su domanda;
  una volta aperta si misura con la cura di sempre, e si dichiara cosa resta
  fuori;
- **non che l'agenda sparisca.** L'indice resta la vista di cosa c'è. Cambia chi
  decide l'ordine: non la matrice, ma il pezzo che si sta scrivendo.

#### Il corpus non è autoritativo — detto dall'utente, 16 agosto 2026

> «Molte feature non esistono solo perché io non le ho usate nelle mie song,
> ma non è detto per questo che non esistano.»

Vale come regola di metodo generale ed è **già costata una volta**: le
tabelle dei patch cable stavano per essere costruite come cancello sul
corpus, cioè "coppia mai vista, coppia rifiutata". Sarebbe stato sbagliato e
avrebbe reso impossibile metà del sound design.

Dove il corpus resta utile è come *informazione*: **collegamento di modulazione**
riferisce quante volte quella coppia compare, così chi legge sa se è terreno
battuto — ma non blocca niente.

#### Il ciclo di revisione ha un protocollo

Il ciclo di questo progetto — *«l'utente ascolta e dice cosa cambiare»* — è
esattamente ciò per cui esiste
`creative-workflows/revision-and-feedback-loops.md`. La sua regola centrale:

> Ogni richiesta di modifica contiene tre strati: **Keep** (cosa è piaciuto),
> **Change** (cosa no), **Direction** (l'asse su cui muoversi). «Preserve the
> liked material and change the smallest musical variable that could solve the
> problem.»

**applica_verbo** fa già una cosa del genere per i **suoni**, e riferisce cosa
ha mosso. Per la **composizione** non esiste l'equivalente, e si vede nella
storia: `DUBPAL02` è stato corretto dichiarando cosa si cambiava (risonanza,
volume, feedback, riverbero) e **mai cosa si teneva**. Con la regola 1 —
riscaricare dal dispositivo — il danno è stato evitato per un pelo, e per un
motivo indipendente.

Da adottare nel rapporto di ogni revisione, prima di toccare il file:

```
Tengo:    …
Cambio:   …
Direzione: …
Resta regolabile: …
```

*(ogni volta che una proposta viene corretta, la lezione va nella casella che
le compete — la 11 della scheda se è una trappola di quel repertorio, il comune
se vale per tutti — con la data)*

#### Un ascolto non è una misura di percezione — 24 agosto 2026

Tutto questo progetto poggia su un'idea giusta: **l'utente ascolta, e la sua
correzione vale più di qualunque ragionamento.** Il 24 agosto 2026 quello
strumento è stato usato per la prima volta per rispondere a una domanda
**quantitativa** — di quanti millisecondi debba spostarsi una nota perché si
senta — ed è l'ascoltatore stesso ad aver messo il limite:

*«Considera che variazioni di pochi ms sono difficili da percepire
consapevolmente da un umano, soprattutto con un orecchio poco allenato come il
mio. […] A questo livello di dettaglio tutte le mie valutazioni sono
imprecise.»*

Non è modestia, è la descrizione corretta dello strumento. Tre regole ne
discendono, e valgono per ogni repertorio:

1. **quel che un ascoltatore riferisce è `[OSS]` su quell'ascoltatore in quella
   sessione.** È fortissimo per *«funziona / non funziona»*, *«c'è / non c'è»*,
   *«è sbagliato»* — che è ciò per cui il ciclo di revisione esiste. È debole per
   *«quanto»*, e una risposta sola non diventa una soglia per il fatto di essere
   stata data con sicurezza;
2. **prima di concludere «non si sente», si amplifica.** La stessa differenza a
   un tempo molto più lento è un'altra cosa: un «non si sente» è **datato alle
   condizioni in cui si è ascoltato**, non è una proprietà del materiale. Un
   ascolto che vuole sapere se uno scarto è percepibile ha **due manopole** —
   l'isolamento della voce e il tempo — e girarne una sola dà una risposta che
   sembra definitiva e non lo è;
3. **e per misurare davvero una soglia servono ripetizioni, ordine casuale e
   ascolto alla cieca.** È psicoacustica, non una sessione in più al Deluge: se
   il numero serve, si cambia esperimento; se non serve, si scrive che non c'è.

⚠️ **E le domande vanno fatte aperte.** Le tre del 24 agosto erano binarie e
contenevano le parole della risposta — «volume o dove cadono?», «prima o
insieme?». Quella volta ha retto perché l'ascoltatore non ha detto sempre di sì,
e anzi è tornato a smentirsi da solo; ma è stata fortuna di formulazione, non
una buona formulazione.

Sta qui, nel metodo, e non nella casella 11 di una scheda, perché non riguarda
un repertorio: riguarda **quanto peso dare all'orecchio come strumento di
misura**, e l'orecchio è lo stesso quando ascolta dub o jazz.

### Il mestiere

#### Velocity groove

*Alimenta la casella 6, «Dinamica».*

> Richiesta dell'utente, 16 agosto 2026: «conoscere drum pattern tipici di un
> genere è molto utile, e magari anche velocity grooves». Ha ragione, ed è
> quello che manca a `DUBPAL01`: i pattern erano quasi giusti e **piatti**.

**La velocity non è un dettaglio di rifinitura: è metà del groove.** Colpi
tutti uguali appiattiscono il polso, e il risultato "marcia" invece di
respirare — vale per qualunque genere.

La scala corrente della programmazione di batteria, su 127: [WEB]

| livello | velocity | quando |
|---|---|---|
| massimo | 110-127 | il colpo che definisce la battuta |
| forte | 100-110 | accenti |
| normale | 90-100 | il corpo del pattern |
| sottovoce | 70-90 | riempimento |
| **fantasma** | **< 70** (rullante: 35-50) | tessuto, non evento |

⚠️ **Questa scala è `[WEB]`, e vale finché un repertorio non ha misure sue.**
È il ripiego onesto: dove nessuno ha aperto un corpus, questi sono i numeri che
ci sono, e valgono per qualunque genere. Ma dove un corpus è stato aperto la
scala misurata **vince su questa**, e un repertorio ce l'ha già: la **casella 6
di [`repertori/jazz.md`](repertori/jazz.md)** porta mediana, quartili ed
escursione per strumento della batteria jazz, con accanto quante esecuzioni e
quanti batteristi sostengono ogni riga. Là i numeri, qui il ripiego — e sono
**diversi**, in qualche riga di parecchio: chi scrive jazz usa quelli, non
questi. **Non si ricopiano qui**, per la regola in cima a questa pagina.

E di quanto varia un accento rispetto al colpo normale, per strumento: [WEB]

| | escursione |
|---|---|
| cassa | ~30 |
| rullante | ~20 |
| piatti e charleston | ~15 |

Regole pratiche che ne discendono:

- **rullante**: colpi principali 100-115, **fantasmi a 35-50** fra un accento
  e l'altro (sulla "e" o sulla "a" del movimento).
- **charleston**: variare fra **60-95**, con l'accento occasionale a 100. Su
  una fila di charleston: accento sui movimenti a 85-90, quelli in mezzo a
  65-75.

Nella libreria i livelli sono tre, e si scrivono nel pattern:

```
x  colpo (90)      X  accento (110)      o  fantasma (42)      .  silenzio
```

**pattern ritmico** per spostarli. Il
terzo livello **non c'era** fino al 16 agosto 2026: è stato aggiunto proprio
per questa lacuna, perché con due soli livelli un fantasma è impossibile.

#### Ma swing e laid-back non sono la stessa cosa — correzione del 17 agosto 2026

*Alimenta la casella 4, «Feel».*

La versione precedente di questa pagina diceva che nel caso storico Deluge il laid-back
«non si fa spostando le note: c'è lo swing di song». **Sono due cose diverse,
e la seconda non copre la prima.**

- lo **swing** cambia il *rapporto* fra i due ottavi di ogni movimento. Nel
  caso storico Deluge era un'impostazione **della song**, comune alle tracce;
  in altri esecutori può essere applicato a clip o parti indipendenti;
- il **laid-back** è una parte intera che arriva costantemente *dopo* la
  griglia, indipendentemente dalle altre. `music-composition`
  (`rhythm-groove/groove-and-feel.md`) lo chiama pocket **a strati**: cassa sul
  tempo, rullante appena dietro, charleston appena avanti — e dice che è così
  che funzionano quasi tutti i groove di soul e reggae. Lo swing globale del caso storico, che
  muove tutti insieme, non lo poteva produrre da solo.

**Dichiarare tempo e risoluzione prima di trasformare uno scarto.** Nel caso
storico la griglia era 96 tick per quarto: a 70 BPM un tick vale circa 8,9 ms.
È un esempio di conversione, non una risoluzione universale o una soglia
percettiva. Il rapporto generale è `ms = 60000 × scarto_in_quarti / BPM`.

**Il loop conserva tutti gli eventi.** Ritardare una parte in un loop richiede
di decidere lo spostamento rispetto al ciclo: un evento oltre il confine non
va perso o ignorato. Il vecchio adapter traslava senza ricondurre al ciclo;
quel limite descrive la prova storica, non una ragione musicale per rinunciare
al laid-back. Conta il rapporto fra gli strati, e il risultato si ascolta.

`[IPO]` Che quel particolare ritardo fosse sentito come pocket e non errore
non era stato ascoltato. Il calcolo di posizioni non dimostra il carattere del groove.

⚠️ Il **24 agosto 2026** una parte di questo `[IPO]` è stata messa alla prova
per la prima volta — qui sotto — e non su un basso ma su una batteria. Quel che
si è sentito è la **separazione fra due voci**; che uno strato spostato *suoni*
come pocket invece che come errore resta non ascoltato.

##### Le due domande sono diverse, e la soglia dipende dal tempo — 24 agosto 2026

⚠️ **Uno scarto scritto è in tick; la finestra dell'udibile è in
millisecondi.** Un tick è una frazione del movimento sulla risoluzione dichiarata — `60000/(BPM × PPQ_quarti)` ms —
quindi **la stessa scrittura vale millisecondi diversi secondo il tempo a cui la
si suona**, e la sua udibilità con essa. Chi posa un groove template senza
guardare il BPM sta decidendo, senza saperlo, quanto grande sarà il proprio
lavoro in millisecondi: lo stesso residuo che a tempo lento si sente, a tempo
veloce ne vale pochi e può non arrivare a nessuno. **I residui si dicono in
tick**, e i millisecondi si scrivono accanto **con il tempo che li produce**,
mai da soli.

⚠️ **E le domande sono due, non una.** La finestra 20–40 ms citata come ipotesi nel
[documento storico](../provenance/delugepal/docs/MUSICA.md) riguardava
**uno spostamento contro la griglia** — una parte che arriva prima o dopo il
tempo, cioè una grandezza **assoluta**. Quanto due voci che suonano *insieme*
debbano separarsi per essere sentite separate è **un'altra domanda**: sono due
compiti percettivi diversi, la sensibilità dell'uno non si trasporta all'altro,
e quell’ipotesi riguardava soltanto il primo: non è una soglia universale misurata.

Il primo ascolto di questo progetto su note scritte fuori griglia — **un
ascoltatore, un giro di due battute, metronomo acceso**, 24 agosto 2026 `[OSS]`
— ha stabilito **due cose**, ed è utile scriverle piccole: che le due domande
qui sopra vanno **poste separate**, e che **uno scarto scritto si sente, quando
è abbastanza grande** — lo stesso spostamento di 3 tick, non distinto al tempo a
cui era scritto, è stato sentito rallentando il tempo di quasi sette volte.

⚠️ **Quei 3 tick sono la coppia del 24 agosto 2026**, costruita **prima** che la
finestra di grazia fosse tolta da **profilo da colpi** (commit `18f26e5`). È
il numero **di ciò che è stato ascoltato**, e come tale resta: rifacendo la
stessa catena col codice di oggi la riga esce a **−4 tick** e altre otto
posizioni su trentuno cambiano. I due file di quella coppia sono un **esemplare
unico** e non vanno rigenerati — rieseguire lo script che li ha scritti li
sovrascriverebbe, e con essi il materiale sia degli ascolti sia la [realizzazione tecnica originale](../provenance/delugepal/docs/MUSICA.md).
La casella 6 di [`repertori/jazz.md`](repertori/jazz.md) porta l'avvertenza per
esteso.

⚠️ **Quanto grande debba essere, invece, NON è stato stabilito, e non è un
dettaglio mancante: è tutto il resto.** Da quegli ascolti non esce nessuna
soglia — il perché sta nel metodo, «Un ascolto non è una misura di percezione» —
e la finestra storica 20–40 ms **resta un’ipotesi non verificata**: non è stata
confermata e non è stata contraddetta.

I numeri, i tempi, la coppia di file e tutte le cautele stanno nella **casella 6
di [`repertori/jazz.md`](repertori/jazz.md)**, che è dove sono stati osservati:
qui la distinzione, là il caso.

#### L'arco di densità

*Alimenta la casella 9, «Forma e densità».*

`music-composition` (`orchestration/arrangement-density.md`) misura ogni
sezione su una scala di **densità 1-9**, e la regola che ne ricava è secca:

> «Density should always be moving, even if subtly. **Static density across a
> long section feels "stuck"**.»

E dà i tempi di tolleranza dell'ascoltatore: **30 secondi** a densità massima
sono comodi, **60** cominciano a pesare, **90 e oltre** e l'ascoltatore si
stacca. Un pezzo dub a 70 BPM fa una battuta ogni 3,4 secondi: novanta secondi
sono **26 battute**. Un arrangiamento che tiene tutte le parti accese per 32
battute è già oltre, e nessun controllo del progetto se ne accorge.

I tre errori catalogati che un generatore commette per costruzione, perché
scrive tutte le parti e poi le lascia accese:

| errore | cosa succede |
|---|---|
| **too much, too soon** | l'intro è già alla densità del ritornello, e da lì non si sale più |
| **static density** | nessun contrasto: «listeners track music partly through density variation» |
| **no silence** | mai un respiro. E il dub *è* il genere del respiro |
**Qui è dove il dub e la scala di densità coincidono.** «Si compone
togliendo» era già scritto in questa pagina, ma come attitudine.
**La tecnica c'era già da
tre giorni; mancava la decisione da prendere.**
L'arco concreto — quale numero per quale sezione — è di repertorio, e sta
nella casella 9 della scheda.

#### Variare è scelto, non randomizzato

*Alimenta le caselle 6 e 9.*

> «A 1-bar repeating loop sounds robotic. A 2- or 4-bar loop with subtle
> variations — an extra ghost note here, a missed hat there — feels alive.»

Cioè: la variazione non è un evento di confine, è un **tessuto**. Nel
vocabolario che questa pagina già usa, i **fantasmi** (`o`, 42 su 127) sono lo
strumento giusto perché costano poco: spostarne uno, toglierne uno, aggiungerne
uno cambia la battuta senza cambiare il pattern.

E il contrappeso, che vale quanto la regola, perché la correzione istintiva a
«suona piatto» è randomizzare tutto:

> «**Do not overhumanize by randomizing everything. Groove has intentional
> consistency.**»

Le variazioni sono **scelte e poche**, non rumore aggiunto ovunque. Un
generatore che randomizza le velocity ottiene un pattern che non è più piatto
e non è ancora un groove.

#### Cassa e basso sono una coppia, e va dichiarata

*Alimenta la casella 5, «Ruoli e spartizione».*

`instrument-idiom/bass.md` è netto: «**Do not ignore the kick drum.** Bass
rhythm without kick context is incomplete», e dà quattro rapporti possibili —
unisono con la cassa, basso che riempie i buchi della cassa, basso lungo sotto
cassa fitta, cassa sui movimenti e basso sincopato.

Quale dei quattro rapporti valga è di repertorio, e sta nella casella 5 della
scheda. Comune è che il rapporto vada **dichiarato**, e non lasciato al caso:
**Scritta, diventa una cosa da tenere o da cambiare di proposito**; non
scritta, è una cosa che si rompe senza accorgersene appena si tocca una delle
due righe.

#### La playability è una decisione, non una regola

*Alimenta la casella 5, «Ruoli e spartizione».*

`instrument-idiom/drums-percussion.md` ha un controllo che sembra fatto apposta
per questo progetto: «MIDI can create patterns that no drummer would choose» —
quattro arti, tempo di spostarsi fra charleston, tom e piatto, fantasmi
realizzabili a quel tempo.

Vale, ma **non sempre, e la differenza va decisa ogni volta**:

| | la playability vincola? |
|---|---|
| roots one drop, kit suonato | **sì** — il genere nasce da una batteria vera, e un pattern impossibile suona finto |
| dub da banco del mixer, kit sintetizzato | **no** — `DUBPAL01` ha un kit costruito dal synth vuoto, nessun campione, nessun batterista implicito |

Il difetto è dichiararlo per caso invece che scegliere. Un kit sintetizzato che
suona un pattern a sei arti è una decisione; lo stesso pattern su un kit roots
è un errore.

#### Sound design: registro, risonanza, livello e movimento cooperano

Le cautele erano nella sezione macchina originale; qui sta il significato
musicale, senza importare soglie del display Deluge.

`[OSS]` Nella sirena `DUBPAL01`, una risonanza che sembrava moderata nel
parametro risultava aggressiva all’orecchio. **Non esiste una soglia universale
di risonanza:** registro, spettro dell’oscillatore e banda del picco cambiano
il livello percepito. Il delay e il riverbero possono ripetere e accumulare
quella banda; i parametri vanno giudicati insieme.

La correzione dell’utente fu un compenso: conservare il carattere risonante
abbassando il livello della patch e gli accumulatori. `[OSS]` `DUBPAL02` applicò
quella scelta. I numeri del sintetizzatore sono nella
[prova originale](../provenance/delugepal/docs/MUSICA.md), non ricette portabili.

Un filtro portato all’estremo può rendere la sorgente quasi inudibile invece
che semplicemente scura o sottile. Controllare anche se il filtro e la
modulazione sono effettivamente attivi: un valore nominale non descrive da solo
il suono. Distinguere il silenzio voluto dalla perdita involontaria di una parte.

**Base e profondità dell’LFO si scelgono insieme.** Un cutoff modulato oscilla
intorno alla propria base: l’escursione completa deve essere compatibile con
il suono voluto. Se una parte sparisce per metà del ciclo, può essere
un’estremità della modulazione, non una nota mancante. La saturazione e i limiti
della scala effettiva restano materia dell’adapter e dell’ascolto.

**Eco e feedback sono un gesto lungo la forma.** L’accumulo che crea un culmine
va anche fatto decadere, se la coda deve terminare. Un valore isolato non
spiega la dinamica di quella coda.

#### Groove template: separare le trasformazioni

Un profilo porta dinamica e residuo temporale da **una esecuzione nominata**.
Il rapporto di swing e il residuo sono trasformazioni distinte: se si applica
uno swing comune, rimuovere lo stesso swing dal profilo prima di posarlo evita
di applicarlo due volte. L’istruzione [groove-template](istruzioni/groove-template.md)
descrive scelta, limiti, collisioni e adattamento della dinamica.

Quantizzare dopo il profilo riscrive le sue posizioni. Anche una trasformazione
casuale successiva può sostituire il tocco scelto; controllare ordine e scopo
di ogni passaggio, anziché sommare “umanizzazioni” senza sapere cosa conservano.
L’effetto specifico del comando humanize Deluge rimaneva `[IPO]` nel caso
storico: non è una conclusione verificata su quel comando.

## L'indice dei repertori

Una matrice repertorio × casella, che dice **senza aprire niente cosa manca
a quale repertorio**. Ogni riga viene dalla prima riga non vuota di ogni
casella della scheda corrispondente: la scheda è la fonte, questa matrice ne
è la vista.

| repertorio | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| [reggae / dub](repertori/reggae-dub.md) | ◐ | ● | ● | ◐ | ● | ● | ◐ | ○ | ◐ | ● |
| [jazz](repertori/jazz.md) | ◐ | ○ | ◐ | ● | ● | ● | ● | ● | ● | ◐ |
| classica · barocca · antica | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| [hip hop](repertori/hiphop.md) | ◐ | ● | ● | ● | ● | ● | ● | ○ | ○ | ● |
| [house / techno](repertori/house.md) | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| [trip hop](repertori/trip-hop.md) | ◐ | ● | ● | ● | ● | ● | ● | ◐ | ◐ | ● |
| [DnB / jungle](repertori/dnb-jungle.md) | ◐ | ● | ● | ● | ● | ● | ● | ○ | ◐ | ● |
| [elettronica / IDM](repertori/idm.md) | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● |

`●` compilata · `◐` parziale, e la scheda dice di cosa · `○` vuota.

Il **grado di prova** non sta qui: `[MIS]`, `[WEB]`, `[OSS]`, `[IPO]`, `[MAN]`
stanno dentro la scheda, accanto all'affermazione che qualificano. La matrice
dice solo dove c'è qualcosa.

Gli altri repertori del perimetro — classica, barocca e antica — non hanno un
file, e non è una
dimenticanza: un file che dicesse soltanto «vuota» dieci volte è rumore da
aprire, mentre una riga d'indice è la stessa informazione a costo zero. La riga
aggregata qui sopra, senza link, è quella informazione: dieci caselle musicali vuote per
il gruppo storico. ⚠️ **Hip hop, house/techno, trip hop e
DnB/jungle hanno invece una scheda** (il boom-bap e la four-on-the-floor dal 17
settembre 2026, il trip-hop e DnB/jungle dal 18-19): sono le prime righe del
**perimetro 3** con un file, e per questo stanno staccate, col link. DnB/jungle e
poi elettronica/IDM sono stati **scorporati** dalla vecchia riga aggregata:
ognuno ha ora la propria scheda.
