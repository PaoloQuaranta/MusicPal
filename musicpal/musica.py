"""Portable pitch, rhythm, harmony and musical interaction primitives."""
from __future__ import annotations

import re

#: I gradi della scala cromatica dal do, per nome.
NOMI_IT = {'do': 0, 're': 2, 'mi': 4, 'fa': 5, 'sol': 7, 'la': 9, 'si': 11}
NOMI_EN = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}

#: Come si scrive un'altezza in uscita, preferendo i diesis.
CROMATICA_IT = ('do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#',
                'la', 'la#', 'si')
CROMATICA_EN = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

#: do4 = 60, la convenzione MIDI standard.
OTTAVA_DEL_DO_CENTRALE = 4

# Il '#' e' inequivocabile (non e' mai una lettera di nota) e lo cattura la
# regex. La 'b' del bemolle invece e' anche una lettera di nota inglese, e
# in italiano e' l'ultima lettera di 'sol' e 'si': va sciolta a mano, vedi
# `_grado_e_bemolle`.
_ALTEZZA = re.compile(r'^([a-z]+)(#)?(-?\d+)$')


def _grado_e_bemolle(lettere: str) -> tuple[int | None, bool]:
    """Riconosce la base italiana o inglese dentro `lettere`.

    Si prova prima il nome per intero (compresi quelli di piu' lettere come
    'sol' o 'si'): se combacia, non c'e' bemolle. Solo se non combacia, e se
    finisce per 'b', si riprova togliendo quella 'b' finale e trattandola
    come bemolle attaccato alla nota. Cosi' 'sib' e' si bemolle (non 'si' +
    lettera a caso) e 'bb' e' b (inglese) bemolle, mentre 'b' da sola resta
    la nota inglese si, naturale — non c'e' ambiguita' perche' nessun nome
    completo (ne' italiano ne' inglese) finisce gia' per 'b'.
    """
    if lettere in NOMI_IT:
        return NOMI_IT[lettere], False
    if lettere in NOMI_EN:
        return NOMI_EN[lettere], False
    if len(lettere) > 1 and lettere[-1] == 'b':
        base = lettere[:-1]
        if base in NOMI_IT:
            return NOMI_IT[base], True
        if base in NOMI_EN:
            return NOMI_EN[base], True
    return None, False


def altezza(nome: str) -> int:
    """Il numero MIDI di un nome di altezza: `do4`, `C4`, `fa#3`, `mib5`.

    Accetta nomi italiani e inglesi, maiuscole o minuscole indifferentemente.
    do4 = C4 = 60, la convenzione MIDI standard (do centrale).
    """
    if not isinstance(nome, str):
        raise ValueError(f'altezza() vuole un nome (stringa) come "do4", '
                         f'non {type(nome).__name__} ({nome!r})')
    testo = nome.strip().lower()
    m = _ALTEZZA.match(testo)
    if not m:
        raise ValueError(f'{nome!r} non e un nome di altezza (es. do4, fa#3)')
    lettere, diesis, ottava = m.group(1), m.group(2), int(m.group(3))

    grado, bemolle = _grado_e_bemolle(lettere)
    if grado is None:
        raise ValueError(f'{nome!r}: {lettere!r} non e una nota')

    if diesis:
        grado += 1
    elif bemolle:
        grado -= 1

    midi = (ottava + 1) * 12 + grado
    if not 0 <= midi <= 127:
        raise ValueError(f'{nome!r} da {midi}, fuori dall estensione MIDI 0-127')
    return midi


def nome_altezza(midi: int, italiano: bool = True) -> str:
    """Il nome di un numero MIDI, coi diesis: 60 -> 'do4'."""
    if not 0 <= midi <= 127:
        raise ValueError(f'{midi} fuori dall estensione MIDI 0-127')
    tabella = CROMATICA_IT if italiano else CROMATICA_EN
    return f'{tabella[midi % 12]}{midi // 12 - 1}'


# ------------------------------------------------------------------ ritmi

from .notes import Note
from .timebase import DEFAULT_PPQ

#: Griglia di default (inputTickMagnitude=2): 16 passi in 384 tick.
#: Per altre risoluzioni le primitive accettano tick_per_battuta.
TICK_PER_PASSO = DEFAULT_PPQ // 4
TICK_PER_BATTUTA = DEFAULT_PPQ * 4

#: Un movimento (quarto) e' 4 sedicesimi: e' il taglio minimo ammesso per
#: un pattern, non la battuta intera. [BUG capitolato] la versione proposta
#: nel capitolato esigeva un multiplo di 16 (una battuta intera), ma il test
#: passa un pattern di 8 caratteri ('X...x...', mezza battuta) aspettandosi
#: che venga accettato: verificato che 4 (un movimento) e' il taglio giusto.
PASSI_PER_MOVIMENTO = 4

#: I caratteri di un pattern a passi.
PAUSA = '.'
COLPO = 'x'
ACCENTO = 'X'
#: Il colpo FANTASMA: quello che non si sente come evento ma come tessuto.
#: [LACUNA trovata usando la libreria, 16 agosto 2026] Fino a qui i livelli
#: erano due, `x` e `X`, e con due livelli un pattern resta piatto: i colpi
#: fantasma sono meta' del mestiere di chi programma una batteria, e senza
#: di loro il groove "marcia" invece di respirare.
FANTASMA = 'o'

#: Velocity di default per i tre livelli. I numeri non sono inventati: la
#: pratica corrente di programmazione li colloca cosi' su 127 --
#: 110-127 massimo, 100-110 forte, 90-100 normale, 80-90 sottovoce,
#: sotto 70 fantasma (35-50 per un rullante fantasma).
VEL_COLPO = 90
VEL_ACCENTO = 110
VEL_FANTASMA = 42


def passi(pattern: str, *, velocity: int = VEL_COLPO,
          accento: int = VEL_ACCENTO, fantasma: int = VEL_FANTASMA,
          lunghezza: int | None = None, da: int = 0,
          tick_per_battuta: int = TICK_PER_BATTUTA) -> list[Note]:
    """Le note di un pattern percussivo: `'x...x...x...x...'`.

    Un carattere per sedicesimo, come le colonne della griglia del Deluge:
    `x` colpo, `X` colpo accentato, **`o` colpo fantasma**, `.` silenzio. La
    lunghezza dev'essere un multiplo di 4, cioe' un numero intero di
    movimenti (non serve una battuta intera: mezza battuta o un solo
    movimento sono pattern validi).

    I tre livelli servono a una cosa sola, ed e' la ragione per cui il
    fantasma e' stato aggiunto: **con due soli livelli il groove marcia.**
    Un charleston fatto di colpi tutti uguali appiattisce il polso, e un
    rullante senza fantasma fra un accento e l'altro non ha tessuto. Vedi
    `docs/MUSICA.md`, «Velocity groove».

    `lunghezza`, se data, e' GIA' in tick grezzi -- la DURATA della nota,
    non il passo fra una e l'altra. [NOME CORRETTO] si chiamava `durata`
    fino alla revisione finale, e il nome era ingannevole: in `melodia()` e
    `accordi()` (qui sotto) `durata` e' tutt'altra cosa, il PASSO fra le
    note, e passa SEMPRE da `durata_in_tick()` (accetta '1/8' come una
    stringa). Chiamare `passi(pattern, durata='1/8')` non sollevava nulla e
    creava una `Note` con `length` uguale alla stringa `'1/8'`, che esplode
    molto piu' tardi con un `AttributeError` lontano dalla causa. Rinominato
    apposta perche' un nome diverso obbliga a controllare cosa si vuole
    dire, invece di trascinare l'abitudine presa con `melodia()`.
    """
    if not isinstance(pattern, str):
        raise ValueError(f'passi() vuole una stringa di passi (es. '
                         f'"x...x..."), non {type(pattern).__name__} '
                         f'({pattern!r})')
    if lunghezza is not None and not isinstance(lunghezza, int):
        raise ValueError(
            f'lunghezza deve essere un intero in tick grezzi, non '
            f'{type(lunghezza).__name__} ({lunghezza!r}) -- per una durata '
            f'come "1/8" usare durata_in_tick() prima di passarla qui')
    testo = pattern.replace(' ', '')
    if not testo or len(testo) % PASSI_PER_MOVIMENTO:
        raise ValueError(
            f'un pattern ha una lunghezza multipla di {PASSI_PER_MOVIMENTO} '
            f'passi (un movimento), questo ne ha {len(testo)}')
    ammessi = {PAUSA, COLPO, ACCENTO, FANTASMA}
    estranei = sorted(set(testo) - ammessi)
    if estranei:
        raise ValueError(f'caratteri non ammessi {estranei}, '
                         f'usare {sorted(ammessi)}')
    livello = {COLPO: velocity, ACCENTO: accento, FANTASMA: fantasma}
    if (isinstance(tick_per_battuta, bool)
            or not isinstance(tick_per_battuta, int)
            or tick_per_battuta <= 0 or tick_per_battuta % 16):
        raise ValueError('tick_per_battuta deve essere un multiplo positivo di 16')
    tick_per_passo = tick_per_battuta // 16
    lung = tick_per_passo if lunghezza is None else lunghezza
    out = []
    for i, c in enumerate(testo):
        if c == PAUSA:
            continue
        out.append(Note(pos=da + i * tick_per_passo, length=lung,
                        velocity=livello[c]))
    return out


def applica_groove(note: list[Note], profilo, dove: str, *,
                   profile_ppq: float = DEFAULT_PPQ,
                   tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[str, object]:
    """Posa velocity e residuo misurati su un pattern uscito da `passi()`.

    `profile_ppq` is the PPQ of the profile residuals. Dataset `profilo()`
    returns 96 PPQ; `profilo_da_colpi(colpi, ppq)` returns the supplied PPQ,
    which must be passed here as `profile_ppq`. `tick_per_battuta` declares
    the target reference grid, always four quarter notes (4 * target PPQ),
    regardless of meter. Meter belongs in the interchange pattern. Residuals are rescaled
    to that grid before rounding to ticks; defaults preserve 96 PPQ behavior.

    ⚠️ MUTA `note` IN POSTO E NON RITORNA NOTE. E' l'eccezione del modulo:
    `passi()`, `melodia()`, `accordi()` e `armonia()` COSTRUISCONO e
    RITORNANO `Note` nuove, questa invece scrive dentro le `Note` che le
    vengono passate -- il ritorno e' solo il rapporto (vedi sotto), non le
    note aggiornate. Chi chiama tiene il riferimento alla stessa lista
    passata in ingresso; e' quella, mutata, il risultato musicale.

    Il pattern resta la stringa leggibile che e'; il feel arriva da
    un'esecuzione vera. `dove` e' il nome GM dello strumento nel profilo.

    ⚠️ LO SWING NON E' QUI. Il profilo porta il solo RESIDUO -- di quanto
    ogni strumento arriva prima o dopo il resto del kit -- perche' lo swing lo fa
    `song.set_swing()`, che e' di song e vale anche per basso e comping. Un
    template che portasse anche lo swing lo farebbe applicare due volte.

    ⚠️ NON INVENTA. Se il pattern chiede un colpo su un passo dove quel
    batterista non ha mai suonato, la nota resta com'e' e il passo finisce
    in `senza_appoggio`. Riempire i buchi da se' sarebbe inventare con la
    benedizione della funzione scritta per impedirlo.

    Ritorna un rapporto (regola 4: un'operazione silenziosa non e'
    correggibile): `strumento`, `da` (l'id del profilo), `toccate`,
    `senza_appoggio` (i passi senza misura) e `collisioni` -- le posizioni
    dove due note sono finite sullo stesso tick, cosa possibile dal 26
    agosto 2026 perche' lo scarto puo' arrivare a un passo intero.
    """
    # Profilo retains its original seven-field tuple contract. Its residual
    # timebase is explicit at application rather than hidden in a new field.
    import math
    if (isinstance(profile_ppq, bool) or not isinstance(profile_ppq, (int, float))
            or not math.isfinite(profile_ppq) or profile_ppq <= 0):
        raise ValueError('profile_ppq must be positive and finite')
    if (isinstance(tick_per_battuta, bool) or not isinstance(tick_per_battuta, int)
            or tick_per_battuta <= 0 or tick_per_battuta % 16):
        raise ValueError('tick_per_battuta must be a positive multiple of 16')
    tick_per_passo = tick_per_battuta // 16
    fattore = (tick_per_battuta / 4) / profile_ppq
    if dove not in profilo.passi:
        raise ValueError(
            f'lo strumento {dove!r} non e\' nel profilo {profilo.id!r}: '
            f'ci sono {sorted(profilo.passi)}')
    per_passo = {p.passo: p for p in profilo.passi[dove]}

    toccate = 0
    senza = []
    for n in note:
        passo = (n.pos // tick_per_passo) % 16
        misura = per_passo.get(passo)
        if misura is None:
            if passo not in senza:
                senza.append(passo)
            continue
        # `Note` e' una dataclass MUTABILE: si scrivono i campi.
        # `max(0, ...)` perche' un residuo negativo sul primo passo manderebbe
        # la nota prima dell'inizio della clip, che il Deluge non sa leggere.
        n.velocity = misura.velocity
        n.pos = max(0, n.pos + int(round(misura.scarto * fattore)))
        toccate += 1

    # ⚠️ DAL 26 AGOSTO 2026 due note possono finire sullo stesso tick: uno
    # scarto puo' arrivare a un passo intero, quindi il passo 3 in ritardo e
    # il 4 in anticipo si incontrano. Il Deluge lo accetta e non e' un
    # errore, ma va riferito -- e' la regola 4, un'operazione silenziosa non
    # e' correggibile.
    quante: dict[int, int] = {}
    for n in note:
        quante[n.pos] = quante.get(n.pos, 0) + 1
    collisioni = sorted(p for p, q in quante.items() if q > 1)

    return {'strumento': dove, 'da': profilo.id, 'toccate': toccate,
            'senza_appoggio': sorted(senza), 'collisioni': collisioni}


def rimappa_dinamica(voci: list[list[Note]], pavimento: int,
                     soffitto: int | None = None) -> dict[str, object]:
    """Rimappa la velocity di note gia' scritte in `[pavimento, soffitto]`,
    PRESERVANDO ordine e proporzioni -- una mappa lineare.

    ⚠️ MUTA le `Note` in posto, come `applica_groove()`.

    A cosa serve: un groove template porta la dinamica di un batterista vero,
    coi fantasmi intorno a velocity 24. Su un kit che non da' voce alle velocity
    basse -- un kit elettronico campionato -- quei colpi SPARISCONO all'udito,
    e la parte suona come se avesse note in meno. Rimappare alza il FONDO fino a
    dove il kit lo voce, senza appiattire.

    ⚠️ NON e' ritoccare la misura: e' adattarla allo STRUMENTO. La forma resta
    quella del batterista (fantasma < comp < accento), cambia solo il range in
    cui cade -- una mappa lineare conserva l'ordine e le proporzioni delle
    differenze. Resta una DECISIONE, non una misura, e per questo va dichiarata:
    il rapporto di ritorno (regola 4) dice da quale range a quale.

    ⚠️ Si rimappa l'INTERO insieme di voci in una volta -- `voci` e' l'elenco
    delle liste di note del kit -- perche' la dinamica che conta e' quella DI
    KIT: il fantasma del rullante e' piano RISPETTO al ride e al piede. Prendere
    min e max su una voce sola gonfierebbe i fantasmi del rullante fino al
    fortissimo dentro la loro riga, distruggendo proprio il rapporto che si
    voleva tenere.

    `soffitto` di default e' il massimo misurato: si alza il pavimento e si
    lascia il forte dov'e'.
    """
    tutte = [n for lst in voci for n in lst]
    if not tutte:
        return {'toccate': 0, 'da': None, 'a': None}
    vmin = min(n.velocity for n in tutte)
    vmax = max(n.velocity for n in tutte)
    if soffitto is None:
        soffitto = vmax
    if not (1 <= pavimento <= 127) or not (1 <= soffitto <= 127) \
            or pavimento > soffitto:
        raise ValueError(
            f'range [{pavimento}, {soffitto}] non valido: '
            f'1..127 e pavimento <= soffitto')
    for n in tutte:
        if vmax == vmin:
            n.velocity = pavimento
        else:
            n.velocity = round(pavimento + (n.velocity - vmin)
                               * (soffitto - pavimento) / (vmax - vmin))
    return {'toccate': len(tutte), 'da': (vmin, vmax), 'a': (pavimento, soffitto)}


def applica_microtiming(note: list[Note], scarti_tick: list[int]) -> dict[str, object]:
    """Posa una sequenza di scarti su una parte scritta, in ORDINE di tempo.

    ⚠️ MUTA `note` in posto. A cosa serve: dare a una linea -- tipico il basso
    walking -- il MICROTIMING che non ha. Un basso quantizzato esatto
    (dispersione zero) non puo' andare incontro a una batteria che il
    microtiming ce l'ha (il groove template): resta un metronomo sotto una
    parte che respira, ed e' il difetto che blocca l'aggancio (casella 5 di
    docs/repertori/jazz.md, docs/istruzioni/aggancio.md).

    `scarti_tick` e' la sequenza di deviazioni, in tick, di UN esecutore vero --
    da `jtd.microtiming()`, convertita al tempo del pezzo. Si posa in ordine di
    tempo: la nota piu' presto prende il primo scarto, e cosi' via, CICLANDO se
    le note sono piu' della sequenza. Positivo = dopo la griglia; `max(0, ...)`
    perche' una nota non va prima di zero.

    ⚠️ NON e' lo swing (di song) ne' il groove template (della batteria, per
    passo): e' il float di UNA linea, nota per nota, da un'esecuzione nominata.
    Ritorna un rapporto (regola 4): `toccate` e lo `scarto` minimo e massimo
    posati.
    """
    if not scarti_tick:
        raise ValueError('la sequenza di scarti e\' vuota')
    ordinate = sorted(note, key=lambda n: n.pos)
    posati = []
    for i, n in enumerate(ordinate):
        s = scarti_tick[i % len(scarti_tick)]
        n.pos = max(0, n.pos + s)
        posati.append(s)
    return {'toccate': len(ordinate),
            'scarto_min': min(posati) if posati else 0,
            'scarto_max': max(posati) if posati else 0}


def durata_in_tick(spec: str | int, *,
                   tick_per_battuta: int = TICK_PER_BATTUTA) -> int:
    """`'1/8'` -> 48 tick al default. Un intero e' gia' in tick grezzi.

    Per una song usare tick_per_battuta=song.ticks_per_bar(doc.root).
    """
    if (isinstance(tick_per_battuta, bool)
            or not isinstance(tick_per_battuta, int)
            or tick_per_battuta <= 0):
        raise ValueError('tick_per_battuta deve essere un intero positivo')
    if isinstance(spec, int):
        if spec <= 0:
            raise ValueError(f'{spec} tick: la durata deve essere positiva')
        return spec
    testo = str(spec).strip()
    if '/' not in testo:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)')
    num, den = testo.split('/', 1)
    try:
        n, d = int(num), int(den)
    except ValueError:
        raise ValueError(f'{spec!r} non e una durata (es. 1/8, 1/4)') from None
    if d <= 0 or n <= 0:
        raise ValueError(f'{spec!r}: numeratore e denominatore positivi')
    tick = tick_per_battuta * n // d
    if tick <= 0:
        raise ValueError(f'{spec!r} da {tick} tick')
    return tick


#: Vocabolario delle articolazioni: quanta parte del passo occupa la nota,
#: in proporzione (non un numero fisso di tick). E' una proporzione e non
#: un valore assoluto perche' un tick fisso non scala col tempo: pochi tick
#: sono impercettibili a un passo lento e sproporzionati a uno veloce, una
#: frazione del passo invece resta lo stesso "sapore" a qualunque tempo.
#: 'legato' = 1.0: la nota dura quanto il passo, cioe' tocca la successiva.
ARTICOLAZIONI = {
    'staccato': 0.5,
    'normale': 0.85,
    'legato': 1.0,
}


def melodia(spec: str, *, durata: str | int = '1/8', da: int = 0,
            velocity: int = 80, articolazione: str = 'normale',
            stacco: int | None = None,
            tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[int, list[Note]]:
    """Da `'re2 fa#2 la2 re3'` alle note, raggruppate per altezza.

    Il Deluge tiene le note in righe, una per altezza, quindi il risultato e'
    un dizionario altezza -> note e non una lista piatta: due `re2` nella
    stessa frase finiscono nella STESSA riga, non in due.

    Un punto e' una pausa: occupa il suo posto e non produce nota.
    `articolazione` e' il vocabolario espressivo (vedi `ARTICOLAZIONI`): un
    basso vuole 'staccato', un pad 'legato'. `stacco`, se dato, e' uno
    scavalco esplicito in tick e vince sull'articolazione, per chi vuole il
    controllo fine.
    """
    if not isinstance(spec, str):
        raise ValueError(f'melodia() vuole una stringa di altezze (es. '
                         f'"do4 re4"), non {type(spec).__name__} ({spec!r})')
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    passo = durata_in_tick(durata, tick_per_battuta=tick_per_battuta)
    if stacco is not None:
        lung = max(1, passo - stacco)
    else:
        lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))
    out: dict[int, list[Note]] = {}
    for i, gettone in enumerate(spec.split()):
        if gettone == PAUSA:
            continue
        y = altezza(gettone)
        out.setdefault(y, []).append(
            Note(pos=da + i * passo, length=lung, velocity=velocity))
    return out


def linea(eventi, *, velocity: int = 80, articolazione: str = 'normale',
          stacco: int | None = None,
          tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[int, list[Note]]:
    """Da `[(tick, altezza, durata), ...]` alle note, raggruppate per altezza.

    Il caso GENERALE di cui `melodia()` e' la scorciatoia a passo fisso: li'
    una durata sola vale per tutta la stringa e le note stanno su una griglia
    regolare, qui ognuna porta la sua posizione e la sua durata.

    [LACUNA capitolato] Serve da quando il walking ha smesso di fare quattro
    note per battuta (6 settembre 2026): una linea che TIENE una nota per due
    movimenti e ne infila una in piu' su una croma non e' esprimibile a passo
    fisso. `melodia()` resta com'e' -- e' la forma comoda per una frase, e
    nessun chiamante si tocca.

    `altezza` e' un numero di nota MIDI oppure un nome (`'do4'`, `'fa#2'`):
    lo stesso vocabolario di `melodia()`. `durata` e' in tick oppure una
    figura (`'1/8'`), ed e' lo SPAZIO che la nota occupa: quanto suona lo
    decide `articolazione`, come li'. Gli eventi non devono essere in ordine.
    """
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    out: dict[int, list[Note]] = {}
    for tick, alt, durata in eventi:
        if not isinstance(tick, int) or tick < 0:
            raise ValueError(f'tick {tick!r}: la posizione e un intero non '
                             f'negativo, in tick')
        passo = durata_in_tick(durata, tick_per_battuta=tick_per_battuta)
        if stacco is not None:
            lung = max(1, passo - stacco)
        else:
            lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))
        y = alt if isinstance(alt, int) else altezza(alt)
        out.setdefault(y, []).append(
            Note(pos=tick, length=lung, velocity=velocity))
    for note in out.values():
        note.sort(key=lambda n: n.pos)
    return out


#: Il separatore fra un accordo e il successivo, dentro `accordi()`.
SEPARATORE_ACCORDI = '|'


def accordi(spec: str, *, durata: str | int = '1/4', da: int = 0,
           velocity: int = 80, articolazione: str = 'normale',
           stacco: int | None = None,
           tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[int, list[Note]]:
    """Da `'re3 fa3 la3 | sib3 re4 fa4'` a una PROGRESSIONE di accordi.

    [LACUNA capitolato] `melodia()` mette una nota per passo, in sequenza:
    e' giusto per una linea, ma un accordo vuole le sue note ALLA STESSA
    posizione, e un accompagnamento e' quasi sempre una PROGRESSIONE, non
    un accordo isolato -- da qui il separatore `|`, cosi' un'intera
    progressione si scrive in una riga sola.

    Ogni gruppo separato da `|` e' un accordo: le altezze al suo interno,
    separate da spazi come in `melodia()`, condividono tutte la stessa
    posizione. Un gruppo che e' un solo punto (`'.'`) e' una pausa: occupa
    il suo passo e non produce nessuna nota, esattamente come in
    `melodia()`.

    Il resto e' identico a `melodia()`, di proposito -- stesso vocabolario,
    stessa firma dove ha senso: `durata` e' il passo fra un accordo e il
    successivo, `articolazione` (vedi `ARTICOLAZIONI`) e `stacco` governano
    quanto dura ogni nota dentro il suo passo, e il ritorno raggruppa per
    altezza (`y -> note`) perche' e' cosi' che il Deluge tiene le righe di
    una clip: due accordi che condividono un'altezza mettono le loro note
    nella STESSA riga, non in due.
    """
    if not isinstance(spec, str):
        raise ValueError(f'accordi() vuole una stringa di accordi (es. '
                         f'"do3 mi3 sol3"), non {type(spec).__name__} '
                         f'({spec!r})')
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(
            f'articolazione {articolazione!r} sconosciuta, usare '
            f'{sorted(ARTICOLAZIONI)}')
    if not spec.strip():
        raise ValueError('accordi(): la sequenza e vuota')
    passo = durata_in_tick(durata, tick_per_battuta=tick_per_battuta)
    if stacco is not None:
        lung = max(1, passo - stacco)
    else:
        lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))

    out: dict[int, list[Note]] = {}
    for i, gruppo in enumerate(spec.split(SEPARATORE_ACCORDI)):
        gettoni = gruppo.split()
        if not gettoni or gettoni == [PAUSA]:
            continue
        pos = da + i * passo
        for gettone in gettoni:
            if gettone == PAUSA:
                continue
            y = altezza(gettone)
            out.setdefault(y, []).append(
                Note(pos=pos, length=lung, velocity=velocity))
    return out


def dinamica(note: dict[int, list[Note]], fattore: float, *,
             minimo: int = 1) -> dict[int, list[Note]]:
    """Scala le velocity di una parte -- il livello dinamico.

    E' la leva delle DINAMICHE dell'arco (docs/istruzioni/arco-dinamico.md): la
    stessa frase si posa piu' piano (`fattore` < 1) o piu' forte (> 1) a seconda
    di dove sta nell'arco del pezzo -- rada e piano sull'A d'apertura, piena e
    forte sul ponte, che ricade sull'ultimo A.

    Ritorna una struttura NUOVA (non muta l'originale), cosi' la stessa frase si
    puo' posare a piu' livelli -- l'A che torna piu' piano di com'era. `fattore`
    moltiplica la velocity di ogni nota, e il risultato e' stretto fra `minimo`
    e 127: una velocity non esce mai dai binari MIDI.
    """
    from dataclasses import replace                          # noqa: PLC0415
    if fattore < 0:
        raise ValueError(f'dinamica(): fattore negativo ({fattore})')
    fuori: dict[int, list[Note]] = {}
    for y, ns in note.items():
        fuori[y] = [replace(n, velocity=max(minimo,
                                            min(127, round(n.velocity * fattore))))
                    for n in ns]
    return fuori


# ------------------------------------------------------------- lo swing
#
# Dove cade il LEVARE dentro il movimento, in frazione: 0,5 e' dritto,
# 0,667 e' la terzina. Il rapporto fra le due meta' del movimento e' la BUR
# (beat-upbeat ratio) della letteratura: 1 dritto, 2 terzina.
#
# Sta QUI e non in un lettore di corpus perche' la usano in due -- `wjazz`
# sulla Weimar e `groove` sul Groove MIDI -- e un numero, o una formula,
# vive in un posto solo.


def in_bur(levare: float) -> float:
    """Da posizione del levare a BUR. 0,5 -> 1 (dritto), 0,667 -> 2."""
    if not 0 < levare < 1:
        raise ValueError(f'il levare sta fra 0 e 1, non {levare}')
    return levare / (1 - levare)


def da_bur(bur: float) -> float:
    """L'inverso: da BUR a posizione del levare. 2 -> 0,667."""
    if bur <= 0:
        raise ValueError(f'la BUR e\' positiva, non {bur}')
    return bur / (1 + bur)


# -------------------------------------------------- sigle di accordo e voicing
#
# PERCHE' ESISTE
# --------------
# `accordi()` vuole le altezze GIA' SCELTE: 'do3 mi3 sol3'. Per il reggae non
# si notava, perche' li' l'armonia sono due accordi e il mestiere sta nel
# ritmo. Per il jazz e' il contrario -- il SIMBOLO e' l'oggetto centrale, e
# scegliere le note e' una decisione con un nome (shell, senza fondamentale,
# drop 2). Senza un posto dove metterla, quella decisione la prenderei a mano
# ogni volta, diversa ogni volta, e non resterebbe scritta da nessuna parte.
#
# DA DOVE VENGONO I NUMERI
# ------------------------
# Dalla skill `music-composition`, non da me:
#   - le sigle e le ambiguita' da `assets/chord-symbol-ambiguity-and-parsing.md`
#   - i voicing da `assets/jazz-voicings.md`
# I test portano i valori attesi di quei documenti (drop 2 di domaj7, i
# voicing senza fondamentale di re-7 e domaj7), non quelli che produce questo
# codice: e' la stessa disciplina della coppia controllata.
#
# COSA NON FA, E VA DETTO
# -----------------------
# ⚠️ Fino al 29 agosto 2026 qui c'era scritto che la condotta delle parti non
# c'era, e che il documento «mostra come nel ii-V-I le voci si ALTERNANO fra
# due forme (A e B)». La prima meta' e' stata risolta -- `voci_condotte()` --
# e la seconda era SBAGLIATA: quel documento non specifica l'alternanza A/B in
# modo implementabile, e le tre ragioni stanno nella docstring di
# `voci_condotte()`.
#
# Non fa la SOSTITUZIONE DI TENSIONE: la tredicesima al posto della quinta che
# il G7 dell'esempio usa. E' una scelta di colore, non di condotta, e la fonte
# la mostra una volta senza dire quando si applica.

from typing import NamedTuple                              # noqa: E402

#: Le sigle, come mappa GRADO -> semitoni sopra la fondamentale.
#:
#: Non una lista piatta di intervalli: serve sapere QUALE grado e' quale, se
#: no shell (3 e 7) e senza-fondamentale (3-5-7-9) diventano indovinelli.
#: Il caso che lo dimostra: `6` e `dim7` hanno tutti e due un intervallo di 9
#: semitoni, ma in uno e' la sesta e nell'altro la settima diminuita.
SIGLE: dict[str, dict[int, int]] = {
    '':         {1: 0, 3: 4, 5: 7},
    'm':        {1: 0, 3: 3, 5: 7},
    '-':        {1: 0, 3: 3, 5: 7},
    'min':      {1: 0, 3: 3, 5: 7},
    'dim':      {1: 0, 3: 3, 5: 6},
    'aug':      {1: 0, 3: 4, 5: 8},
    'sus':      {1: 0, 4: 5, 5: 7},
    'sus4':     {1: 0, 4: 5, 5: 7},
    'sus2':     {1: 0, 2: 2, 5: 7},
    '5':        {1: 0, 5: 7},
    '6':        {1: 0, 3: 4, 5: 7, 6: 9},
    'm6':       {1: 0, 3: 3, 5: 7, 6: 9},
    '-6':       {1: 0, 3: 3, 5: 7, 6: 9},
    '69':       {1: 0, 3: 4, 5: 7, 6: 9, 9: 14},
    '7':        {1: 0, 3: 4, 5: 7, 7: 10},
    'maj7':     {1: 0, 3: 4, 5: 7, 7: 11},
    'ma7':      {1: 0, 3: 4, 5: 7, 7: 11},
    'm7':       {1: 0, 3: 3, 5: 7, 7: 10},
    '-7':       {1: 0, 3: 3, 5: 7, 7: 10},
    'min7':     {1: 0, 3: 3, 5: 7, 7: 10},
    'm7b5':     {1: 0, 3: 3, 5: 6, 7: 10},
    'm7-5':     {1: 0, 3: 3, 5: 6, 7: 10},
    'dim7':     {1: 0, 3: 3, 5: 6, 7: 9},
    'mmaj7':    {1: 0, 3: 3, 5: 7, 7: 11},
    '-maj7':    {1: 0, 3: 3, 5: 7, 7: 11},
    'add9':     {1: 0, 3: 4, 5: 7, 9: 14},
    '9':        {1: 0, 3: 4, 5: 7, 7: 10, 9: 14},
    'maj9':     {1: 0, 3: 4, 5: 7, 7: 11, 9: 14},
    'm9':       {1: 0, 3: 3, 5: 7, 7: 10, 9: 14},
    '-9':       {1: 0, 3: 3, 5: 7, 7: 10, 9: 14},
    '13':       {1: 0, 3: 4, 5: 7, 7: 10, 9: 14, 13: 21},
    'maj7#11':  {1: 0, 3: 4, 5: 7, 7: 11, 11: 18},
    '7b9':      {1: 0, 3: 4, 5: 7, 7: 10, 9: 13},
    '7#9':      {1: 0, 3: 4, 5: 7, 7: 10, 9: 15},
    '7b5':      {1: 0, 3: 4, 5: 6, 7: 10},
    '7#5':      {1: 0, 3: 4, 5: 8, 7: 10},
    '7#11':     {1: 0, 3: 4, 5: 7, 7: 10, 11: 18},
    '7b13':     {1: 0, 3: 4, 5: 7, 7: 10, 13: 20},
    '7sus':     {1: 0, 4: 5, 5: 7, 7: 10},
    '7sus4':    {1: 0, 4: 5, 5: 7, 7: 10},
    #: Il documento dice che un 'alt' usa un SOTTOINSIEME delle alterazioni,
    #: "usually 2-3", non tutte insieme. Questo e' il sottoinsieme che lui
    #: stesso scrive come esempio (3, b7, b9, b13).
    '7alt':     {1: 0, 3: 4, 7: 10, 9: 13, 13: 20},
}

#: Le sigle ambigue: si legge in un modo, e si DICE quale e cosa si e'
#: scartato. Il difetto da evitare non e' scegliere -- e' scegliere in
#: silenzio, che e' la famiglia di errori piu' costosa di questo progetto.
AMBIGUE: dict[str, tuple[str, str]] = {
    '2':   ('sus2', "letta come sus2 (uso di chart pop e chitarristici); "
                    "l'altra lettura era add9, che TIENE la terza"),
    'maj': ('',     "letta come triade maggiore; in certe notazioni informali "
                    "'maj' sta per maj7"),
    'alt': ('7alt', "letta come 7alt: la sigla presuppone la settima di "
                    "dominante, che pero' non e' scritta"),
    '+':   ('aug',  "letta come triade aumentata; in certe tabelle il '+' e' "
                    "invece la quinta alzata di un accordo di settima"),
    '7+5': ('7#5',  "'+5' letto come quinta alzata"),
    '7-5': ('7b5',  "'-5' letto come quinta abbassata, uso dei chart vecchi"),
}

#: I voicing, e cosa vuole ciascuno. Da `assets/jazz-voicings.md`.
VOICING = {
    'chiuso': 'tutte le note dell accordo, dalla fondamentale in su',
    'shell': 'solo terza e settima: le due note che portano l identita',
    'senza-fondamentale': '3-5-7-9, il basso suona la fondamentale altrove',
    'drop2': 'posizione chiusa con la seconda voce dall alto giu di un ottava',
    'quartale': 'tre quarte giuste e una terza: il suono del comping modale',
}

#: Lo stack di quarte, in semitoni dalla fondamentale. Dalla fonte --
#: `assets/jazz-voicings.md`, «Quartal voicings»: «Stack of 4ths. The "So
#: What" voicing (modal jazz): D - G - C - F - A -- five notes stacked in
#: 4ths». Su un minore settima danno fondamentale, 11, b7, b3 e 5.
QUARTE = (0, 5, 10, 15, 19)

#: Le lettere di nota, dalle piu' lunghe alle piu' corte: l'alternanza di una
#: regex prende il PRIMO ramo che combacia, non il piu' lungo, quindi
#: l'ordine qui e' semantico e non estetico ('sol' prima di 's', 'fa' prima
#: di 'f'). Le inglesi stanno in coda perche' 'la' deve vincere su 'a'.
_BASI = ('sol', 'do', 're', 'mi', 'fa', 'la', 'si')
_RADICE = re.compile(r'^(' + '|'.join(_BASI) + r'|[a-g])([#b])?', re.I)

#: Da simboli tipografici a ascii. `o7`/`o` non ci sono di proposito: 'o' e'
#: una lettera comunissima e confonderla con il pallino del diminuito
#: farebbe leggere sigle a caso.
_SIMBOLI = (('♭', 'b'), ('♯', '#'), ('Δ9', 'maj9'),
            ('Δ', 'maj7'), ('ø7', 'm7b5'), ('ø', 'm7b5'),
            ('°', 'dim'), ('–', '-'), ('—', '-'))


class Sigla(NamedTuple):
    """Un simbolo di accordo, sciolto ma non ancora messo in un registro."""

    testo: str
    #: La classe di altezza della fondamentale, 0-11 (do = 0).
    fondamentale: int
    #: Grado -> semitoni sopra la fondamentale. La chiave e' il grado, cosi'
    #: 'la terza' e 'la settima' restano interrogabili per nome.
    gradi: dict[int, int]
    #: La classe di altezza del basso di uno slash, o None.
    basso: int | None
    #: Come e' stata sciolta un'ambiguita', o None se non ce n'erano.
    letto_come: str | None

    @property
    def intervalli(self) -> tuple[int, ...]:
        """I semitoni sopra la fondamentale, in ordine."""
        return tuple(sorted(self.gradi.values()))


def _classe(testo: str) -> int | None:
    """La classe di altezza di un nome di nota SENZA ottava, o None."""
    m = _RADICE.fullmatch(testo.strip())
    if not m:
        return None
    lettere, alterazione = m.group(1).lower(), m.group(2)
    grado, bemolle = _grado_e_bemolle(lettere)
    if grado is None:
        return None
    if alterazione == '#':
        grado += 1
    elif alterazione == 'b' or bemolle:
        grado -= 1
    return grado % 12


def _normalizza_coda(coda: str) -> str:
    """La coda di una sigla in forma canonica, minuscola.

    La maiuscola va guardata PRIMA di abbassare tutto: in 'CM7' la M grande
    e' maggiore e in 'Cm7' la m piccola e' minore, cioe' due accordi diversi
    che differiscono per il solo caso di una lettera. Abbassare e basta
    trasformerebbe silenziosamente un maj7 in un m7 -- lo stesso genere di
    difetto muto che 'Ab' -> A# aveva gia' prodotto in `set_scale`.
    """
    testo = coda.replace('(', '').replace(')', '').replace(' ', '')
    for prima, dopo in (('Maj', 'maj'), ('MAJ', 'maj'), ('Min', 'min'),
                        ('MIN', 'min')):
        testo = testo.replace(prima, dopo)
    if testo.startswith('M') and (len(testo) == 1 or testo[1].isdigit()):
        testo = 'maj' + testo[1:]
    return testo.lower()


def sigla(testo: str) -> Sigla:
    """Da `'Cmaj7'`, `'re-7'`, `'F#7b9'`, `'C/E'` a una `Sigla`.

    La fondamentale passa dallo STESSO vocabolario di `altezza()` -- italiano
    e inglese, diesis e bemolli -- perche' un secondo parser di altezze e'
    una seconda occasione di sbagliare, e in questo progetto quell'errore e'
    gia' stato pagato una volta.

    Una sigla che non e' in tabella viene RIFIUTATA e l'errore dice cosa
    esiste. Tirare a indovinare su un simbolo sconosciuto vorrebbe dire
    scrivere note che nessuno ha chiesto.
    """
    if not isinstance(testo, str):
        raise ValueError(f'sigla() vuole una stringa come "Cmaj7", non '
                         f'{type(testo).__name__} ({testo!r})')
    grezzo = testo.strip()
    if not grezzo:
        raise ValueError('sigla(): la sigla e vuota')
    for prima, dopo in _SIMBOLI:
        grezzo = grezzo.replace(prima, dopo)

    # Lo slash: e' un basso solo se cio' che segue e' davvero una nota, se no
    # e' parte della sigla -- '6/9' non ha nessun basso di nome '9'.
    basso = None
    if '/' in grezzo:
        capo, _, coda_slash = grezzo.rpartition('/')
        classe_basso = _classe(coda_slash)
        if classe_basso is not None:
            basso, grezzo = classe_basso, capo
    #: Uno slash che resta NON e' un basso: e' interno alla sigla, come in
    #: '6/9'. Vanno tolti tutti e due i casi, e in quest'ordine: 'C6/9/E' ha
    #: sia il basso sia lo slash interno, e trattarne uno solo lasciava la
    #: sigla illeggibile. [difetto trovato provando a mano, 17 agosto 2026]
    grezzo = grezzo.replace('/', '')

    m = _RADICE.match(grezzo)
    if not m:
        raise ValueError(f'{testo!r}: non riconosco la fondamentale '
                         f'(es. C, do, Bb, sib, F#, fa#)')
    fondamentale = _classe(m.group(0))
    if fondamentale is None:
        raise ValueError(f'{testo!r}: {m.group(0)!r} non e una nota')

    coda = _normalizza_coda(grezzo[m.end():])
    letto_come = None
    if coda in AMBIGUE:
        canonica, spiegazione = AMBIGUE[coda]
        letto_come = f'{testo}: {spiegazione}'
        coda = canonica
    if coda not in SIGLE:
        raise ValueError(
            f'{testo!r}: sigla {coda!r} sconosciuta. Quelle riconosciute '
            f'sono {sorted(k for k in SIGLE if k)} (piu maj7, m7, 7 e la '
            f'triade a coda vuota). Aggiungerne una vuol dire aggiungerla a '
            f'SIGLE con i suoi gradi, non indovinarla qui')
    return Sigla(testo=testo, fondamentale=fondamentale,
                 gradi=dict(SIGLE[coda]), basso=basso, letto_come=letto_come)


def _pretende(s: Sigla, gradi: tuple[int, ...], voicing: str) -> None:
    """Un voicing che nomina un grado non puo' girare senza quel grado."""
    nomi = {3: 'terza', 5: 'quinta', 7: 'settima'}
    mancanti = [g for g in gradi if g not in s.gradi]
    if mancanti:
        quali = ', '.join(nomi.get(g, str(g)) for g in mancanti)
        raise ValueError(
            f"voicing {voicing!r} su {s.testo!r}: manca {quali}. "
            f"{VOICING[voicing]}, e un accordo che non ce l ha non puo' "
            f"averne uno -- costruirlo lo stesso vorrebbe dire inventare "
            f"una nota che la sigla non dichiara")


def voci(simbolo, *, voicing: str = 'chiuso',
         registro: str = 'do3') -> list[int]:
    """Le altezze MIDI di un accordo, in un registro, con un voicing.

    `registro` e' l'ancora in basso: la fondamentale va sulla prima altezza
    della sua classe che sta a `registro` o sopra. Cosi' `do4` mette un
    domaj7 su 60 e un re-7 su 62, che e' come si legge una griglia.

    Il basso di uno slash va SOTTO tutto il resto, all'ottava piu' vicina.
    """
    s = simbolo if isinstance(simbolo, Sigla) else sigla(simbolo)
    if voicing not in VOICING:
        raise ValueError(f'voicing {voicing!r} sconosciuto, usare '
                         f'{sorted(VOICING)}')
    ancora = altezza(registro)
    radice = ancora + (s.fondamentale - ancora) % 12

    if voicing == 'chiuso':
        note = [radice + i for i in s.intervalli]
    elif voicing == 'shell':
        _pretende(s, (3, 7), voicing)
        note = [radice + s.gradi[3], radice + s.gradi[7]]
    elif voicing == 'senza-fondamentale':
        _pretende(s, (3, 7), voicing)
        # La nona si AGGIUNGE se la sigla non ce l'ha: e' il punto del
        # voicing di Bill Evans, non un'aggiunta arbitraria -- il documento
        # lo scrive come "3-7-9, add 9 on top".
        #
        # Le estensioni DICHIARATE (11, 13, e la nona alterata) restano
        # invece tutte: una sigla che si scomoda a scrivere 'alt' o '13' sta
        # nominando proprio quelle note, e scartarle darebbe un accordo
        # plausibile e sbagliato. Il documento le voicizza cosi': 3-5-7-13
        # per un tredicesima, 3-b7-b9-b13 per un alterato.
        scelti = [s.gradi[g] for g in (3, 5, 7) if g in s.gradi]
        scelti.append(s.gradi.get(9, 14))
        scelti.extend(s.gradi[g] for g in (11, 13) if g in s.gradi)
        # Con un'undicesima dichiarata la quinta se ne va: le due cadono a un
        # semitono e quello che si sente e' l'urto. Il documento lo dice due
        # volte -- "5 often omitted", e il suo C7#11 e' E-Bb-D-F#, senza G.
        if 11 in s.gradi:
            scelti = [i for i in scelti if i != s.gradi.get(5)]
        note = [radice + i for i in sorted(scelti)]
    elif voicing == 'quartale':
        # ⚠️ RIFIUTA fuori dal minore settima, e non e' pignoleria. Lo stack
        # di quarte dalla fondamentale produce l'11, la b7 e la b3: su un
        # maggiore settima darebbero sib e mib, che nell'accordo non ci sono.
        # La fonte lo mostra su un minore ("over E Dorian or similar") e su un
        # "F minor"; fuori di li' non dice niente, e non lo si inventa.
        if s.gradi.get(3) != 3 or s.gradi.get(7) != 10:
            raise ValueError(
                f"voicing 'quartale' su {s.testo!r}: lo stack di quarte "
                f"dalla fondamentale vuole terza MINORE e settima MINORE, e "
                f"questo accordo ha {s.gradi.get(3)} e {s.gradi.get(7)}. La "
                f"fonte lo mostra sul minore settima e nient'altro: fuori di "
                f"li' produrrebbe note che l'accordo non dichiara")
        note = [radice + i for i in QUARTE]
    else:                                                   # drop2
        chiuse = [radice + i for i in s.intervalli]
        if len(chiuse) < 4:
            raise ValueError(
                f"voicing 'drop2' su {s.testo!r}: servono almeno quattro "
                f"note e ce ne sono {len(chiuse)}. Il documento descrive il "
                f"drop 2 su voicing di quattro note; su una triade non e' "
                f"definito e non lo invento")
        caduta = chiuse[-2] - 12
        note = sorted(chiuse[:-2] + [chiuse[-1]] + [caduta])

    if s.basso is not None:
        piu_bassa = min(note)
        nota_basso = piu_bassa - ((piu_bassa - s.basso) % 12 or 12)
        note = [nota_basso] + note
    fuori = [y for y in note if not 0 <= y <= 127]
    if fuori:
        raise ValueError(f'{s.testo!r} in registro {registro!r} con voicing '
                         f'{voicing!r} esce dall estensione MIDI: {fuori}')
    return note


#: Quanto un accordo condotto puo' allontanarsi in media dall'ancora che
#: `registro` gli darebbe, in semitoni. Sei e' mezza ottava: lascia ruotare
#: le voci e impedisce di camminare via per ottave.
DERIVA_MASSIMA = 6


def _disposizioni(note: list[int]) -> list[list[int]]:
    """Le disposizioni della STESSA armonia: rotazioni e ottave.

    Ruotare vuol dire portare la voce piu' bassa un'ottava sopra: cambia
    l'ordine delle voci e non le classi di altezza. E' l'unica liberta' che
    ci si prende -- le note restano quelle che il voicing ha scelto.
    """
    v = sorted(note)
    fuori = []
    for k in range(len(v)):
        girata = sorted(v[k:] + [y + 12 for y in v[:k]])
        for ottava in (-24, -12, 0, 12, 24):
            spostata = [y + ottava for y in girata]
            if all(0 <= y <= 127 for y in spostata):
                fuori.append(spostata)
    return fuori


def voci_condotte(spec: str, *, voicing: str = 'chiuso',
                  registro: str = 'do3') -> list[list[int]]:
    """Le altezze di una progressione, con la CONDOTTA DELLE PARTI.

    Ogni accordo dopo il primo si posa nella disposizione che muove meno
    voci rispetto a quello prima. Il primo e' l'ancora e sta dove
    `registro` lo mette, come in `voci()`.

    ⚠️ CAMBIA DOVE, NON QUALI. Le classi di altezza di ogni accordo sono
    esattamente quelle che `voci()` sceglie: qui si scelgono le ottave, mai
    le note. Chi volesse un'altra tensione cambia `voicing`, non questa
    funzione -- e il test lo verifica come invariante.

    ⚠️ PERCHE' NON L'ALTERNANZA «A/B», che e' quello che la casella 7 di
    `docs/repertori/jazz.md` diceva di implementare. La fonte -- il paragrafo
    «Rootless voicings» di `assets/jazz-voicings.md`, skill
    `music-composition` -- NON la specifica in modo implementabile, e per tre
    ragioni indipendenti, tutte verificate in `test_condotta_delle_parti`:

      1. i nomi non sono definiti: la fonte scrive «A» = 3-5-7-9 (or
         7-9-3-5) e «B» = 7-9-3-5 (or 3-5-7-9), poi aggiunge «the naming
         convention depends on the source»;
      2. il suo esempio non usa nessuna delle due forme: il G7 e'
         b7-9-3-13, con la TREDICESIMA al posto della quinta;
      3. la regola che dichiara -- «only one voice moves per chord change»
         -- fallisce sul suo stesso esempio: Dm7 -> G7 muove una voce,
         G7 -> Cmaj7 ne muove TRE.

    Quel che resta solido e' lo SCOPO, «the voice leading is smooth», ed e'
    quello che si implementa. Sul ii-V-I del documento questa funzione da'
    il suo stesso Dm7 e il suo stesso Cmaj7, e in tutto muove SEI semitoni
    contro i sette del suo esempio.

    ⚠️ Resta fuori la SOSTITUZIONE DI TENSIONE -- la 13ma al posto della 5ta
    che il suo G7 fa. E' una scelta di colore, non di condotta, e la fonte
    la mostra una volta senza dire quando si applica: inventarne la regola
    sarebbe esattamente cio' che la casella 7 vieta.
    """
    fuori: list[list[int]] = []
    precedente: list[int] | None = None
    for gruppo in spec.split(SEPARATORE_ACCORDI):
        testo = gruppo.strip()
        if not testo or testo == PAUSA:
            continue
        base = voci(testo, voicing=voicing, registro=registro)
        ancora = sum(base) / len(base)
        if precedente is None or len(base) != len(precedente):
            # ⚠️ Quando il numero di voci cambia -- una triade dopo una
            # settima -- non c'e' una corrispondenza fra le voci, e
            # inventarne una accoppierebbe cose diverse. L'accordo riparte
            # dall'ancora, che e' il comportamento dichiarato di `voci()`.
            scelto = base
        else:
            # ⚠️ IL VINCOLO DI REGISTRO NON E' UN DETTAGLIO: senza, il
            # minimo movimento e' GOLOSO e prende sempre il passo piccolo
            # nella stessa direzione. Misurato sul blues di 12 battute per
            # tre giri, il comping derivava di DICIASSETTE semitoni verso il
            # basso -- da [57,60,63,67] a [40,43,46,50] -- cioe' usciva dal
            # registro in cui era stato messo. Ogni disposizione resta entro
            # mezza ottava, in media, dall'ancora che `registro` dichiara.
            vicine = [c for c in _disposizioni(base)
                      if abs(sum(c) / len(c) - ancora) <= DERIVA_MASSIMA]
            scelto = min(
                vicine or _disposizioni(base),
                key=lambda c: (sum(abs(a - b) for a, b in zip(c, precedente)),
                               # a pari movimento, quella piu' vicina
                               # all'ancora: senza, la scelta fra due
                               # disposizioni equivalenti dipende dall'ordine
                               # in cui sono state generate
                               abs(sum(c) / len(c) - ancora)))
        fuori.append(scelto)
        precedente = scelto
    return fuori


def armonia(spec: str, *, voicing: str = 'chiuso', registro: str = 'do3',
            durata: str | int = '1/4', da: int = 0, velocity: int = 80,
            articolazione: str = 'normale', stacco: int | None = None,
            condotta: bool = True,
            tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[int, list[Note]]:
    """Da `'Dm7 | G7 | Cmaj7'` alle note, raggruppate per altezza.

    E' `accordi()` che parte dai SIMBOLI invece che dalle altezze. Tutto il
    resto e' identico di proposito -- stesso separatore `|`, stesso punto per
    la pausa, stessa forma di ritorno -- perche' cosi' entra in `scrivi()`
    senza che nulla a valle debba sapere da dove viene.

    ⚠️ `condotta=True` E' IL DEFAULT, e dal 29 agosto 2026. Gli accordi si
    posano dove muovono meno voci -- `voci_condotte()`, che spiega anche
    perche' NON e' l'alternanza «A/B». Prima ogni accordo era ancorato a
    `registro` per conto suo, e una progressione usciva come una fila di
    accordi invece che come un comping: era la lacuna dichiarata dalla
    casella 7 di `docs/repertori/jazz.md`. Il PRIMO accordo non si muove in
    nessun caso, quindi `voci()` e un accordo solo non cambiano.
    `condotta=False` da il comportamento di prima.

    Per sapere cosa ha deciso, e soprattutto quali ambiguita' ha sciolto,
    `racconta_armonia()` con gli stessi argomenti.
    """
    if not isinstance(spec, str):
        raise ValueError(f'armonia() vuole una stringa di sigle (es. '
                         f'"Dm7 | G7"), non {type(spec).__name__} ({spec!r})')
    if articolazione not in ARTICOLAZIONI:
        raise ValueError(f'articolazione {articolazione!r} sconosciuta, usare '
                         f'{sorted(ARTICOLAZIONI)}')
    if not spec.strip():
        raise ValueError('armonia(): la sequenza e vuota')
    passo = durata_in_tick(durata, tick_per_battuta=tick_per_battuta)
    if stacco is not None:
        lung = max(1, passo - stacco)
    else:
        lung = max(1, round(passo * ARTICOLAZIONI[articolazione]))

    guidate = (voci_condotte(spec, voicing=voicing, registro=registro)
               if condotta else None)

    out: dict[int, list[Note]] = {}
    k = 0
    for i, gruppo in enumerate(spec.split(SEPARATORE_ACCORDI)):
        testo = gruppo.strip()
        if not testo or testo == PAUSA:
            continue
        pos = da + i * passo
        if guidate is not None:
            altezze = guidate[k]
            k += 1
        else:
            altezze = voci(testo, voicing=voicing, registro=registro)
        for y in altezze:
            out.setdefault(y, []).append(
                Note(pos=pos, length=lung, velocity=velocity))
    return out


def comping(progressione: str, ritmi, *, voicing: str = 'chiuso',
            registro: str = 'do3', velocity: int = 72,
            articolazione: str = 'staccato', condotta: bool = True,
            figura: str | int = '1/8', da: int = 0,
            tick_per_battuta: int = TICK_PER_BATTUTA) -> dict[int, list[Note]]:
    """Il comping: da una progressione (un accordo per battuta) e un RITMO per
    battuta, gli accordi piazzati sui colpi, voicizzati e condotti.

    `ritmi` e' una lista di stringhe (o una sola), una per battuta, di `'x'`
    (colpo) e `'.'` (pausa) -- es. `'x..x....'`, otto crome. Tutte della stessa
    lunghezza, e quella lunghezza per `figura` deve fare una battuta (8 crome,
    16 semicrome...). ⚠️ Una `'x'` sull'ULTIMA cella anticipa il battere della
    battuta dopo: e' cosi' che il comping jazz "spinge".

    E' un COSTRUTTORE DI SPEC sopra `armonia()` -- la collocazione, il voicing e
    la condotta vengono da li', nessuna logica di piazzamento nuova. Nasce da
    `genera_jazz._spec_comping`, promosso a primitiva. Vedi
    docs/istruzioni/comping.md.
    """
    if isinstance(ritmi, str):
        ritmi = [ritmi]
    accordi = [g.strip() for g in progressione.split(SEPARATORE_ACCORDI)]
    if len(accordi) != len(ritmi):
        raise ValueError(
            f'comping(): {len(accordi)} battute di accordi e {len(ritmi)} di '
            f'ritmo -- devono essere uguali (un ritmo per battuta)')
    passo = durata_in_tick(figura, tick_per_battuta=tick_per_battuta)
    if tick_per_battuta % passo:
        raise ValueError(f'comping(): la figura {figura!r} non divide la battuta')
    per_battuta = tick_per_battuta // passo
    gruppi = []
    for b, (accordo, ritmo) in enumerate(zip(accordi, ritmi)):
        if len(ritmo) != per_battuta:
            raise ValueError(
                f'comping(): la battuta {b + 1} ha un ritmo di {len(ritmo)} '
                f'celle, ma con figura {figura!r} una battuta ne vuole '
                f'{per_battuta}')
        for c in ritmo:
            if c not in ('x', PAUSA):
                raise ValueError(
                    f"comping(): cella {c!r} sconosciuta, usare 'x' o '{PAUSA}'")
            gruppi.append(accordo if c == 'x' else PAUSA)
    spec = f' {SEPARATORE_ACCORDI} '.join(gruppi)
    return armonia(spec, voicing=voicing, registro=registro, durata=figura,
                    velocity=velocity, articolazione=articolazione,
                    condotta=condotta, da=da,
                    tick_per_battuta=tick_per_battuta)


# ------------------------------------------------------------ il contrappunto
#
# Il contrappunto e' l'arte di combinare linee melodiche INDIPENDENTI (Piston,
# Counterpoint, 1970). Qui il codice non compone: fa i conti sul rapporto fra
# due linee gia' scritte -- quali intervalli cadono insieme, che moto le lega,
# e dove l'indipendenza si perde. L'AI scrive le due voci; questa e' la lente.

#: Il nome generico dell'intervallo per semitono ridotto (0-11).
_NOME_INTERVALLO = ('unisono', '2a', '2a', '3a', '3a', '4a', 'tritono',
                    '5a', '6a', '6a', '7a', '7a')

#: La specie dell'intervallo, per semitono ridotto. In DUE parti la 4a e'
#: DISSONANTE (Piston, p.125: smette di esserlo nel tre-parti quando ha una
#: nota sotto che la sostiene). Unisono/8a/5a perfette; 3a/6a imperfette;
#: 2a/4a/tritono/7a dissonanti.
_SPECIE_INTERVALLO = ('perfetta', 'dissonante', 'dissonante', 'imperfetta',
                      'imperfetta', 'dissonante', 'dissonante', 'perfetta',
                      'imperfetta', 'imperfetta', 'dissonante', 'dissonante')

#: Un movimento (beat): 4 passi da 24 tick. Il battere su cui la dissonanza
#: pesa di piu' e la parallela si sente meglio.
TICK_PER_MOVIMENTO = TICK_PER_PASSO * PASSI_PER_MOVIMENTO


class Verticale(NamedTuple):
    """Un punto in cui le due voci suonano insieme, e cosa ci si sente."""

    pos: int                       # tick
    a: int | None                  # altezza di A che suona qui (None = pausa)
    b: int | None                  # altezza di B
    intervallo: int | None         # semitoni fra le due, >= 0 (None se pausa)
    nome: str                      # 'unisono', '3a', '5a'... o 'pausa'
    specie: str                    # 'perfetta' | 'imperfetta' | 'dissonante' | '-'
    moto: str | None               # rispetto al verticale pieno precedente
    battere: bool                  # cade su un movimento?


class Contrappunto(NamedTuple):
    """I conti sul rapporto fra due linee -- i fatti, non il giudizio."""

    verticali: list[Verticale]
    moti: dict[str, int]                    # tipo di moto -> quante volte
    paralleli: list[int]                    # posizioni di 5e/8e parallele
    dirette: list[int]                      # 5e/8e raggiunte per moto diretto
    attacchi: tuple[int, int, int]          # (in comune, in A, in B)
    simultaneita: float                     # attacchi in comune / max(A, B)
    picchi: tuple[int | None, int | None]   # posizione del picco di A e di B
    picchi_insieme: bool                    # i due picchi cadono vicini?
    dissonanze_battere: list[int]           # dissonanze cadute sul battere


def _eventi_linea(voce: dict[int, list[Note]]) -> list[tuple[int, int, int]]:
    """Da `y -> [Note]` a `(pos, fine, altezza)` ordinati per posizione."""
    ev = [(n.pos, n.pos + n.length, y)
          for y, note in voce.items() for n in note]
    ev.sort()
    return ev


def _suona_a(eventi: list[tuple[int, int, int]], t: int) -> int | None:
    """L'altezza che suona a `t`: una che ATTACCA li', o quella tenuta.

    Una linea e' monofonica; se in un punto ne trova piu' d'una (una voce che
    porta accordi) prende la piu' acuta, cosi' l'analisi ha comunque un numero.
    """
    attacca = [y for pos, _, y in eventi if pos == t]
    if attacca:
        return max(attacca)
    tiene = [y for pos, fine, y in eventi if pos < t < fine]
    return max(tiene) if tiene else None


def contrappunto(voce_a: dict[int, list[Note]], voce_b: dict[int, list[Note]],
                 *, movimento: int = TICK_PER_MOVIMENTO) -> Contrappunto:
    """L'analisi del rapporto fra DUE linee: intervalli, moti, indipendenza.

    ⚠️ NON COMPONE. Prende due voci gia' scritte (la forma di `melodia()`,
    `linea()`, `armonia()`: `y -> [Note]`) e ne misura il contrappunto. E' la
    divisione del progetto -- l'AI decide le note delle due linee, il codice fa
    i conti sul loro rapporto -- come `voci_condotte()` per il voicing.

    Cosa misura, e da dove viene (Piston, Counterpoint, 1970):
      - a ogni ATTACCO (di A o di B) l'intervallo verticale, e la sua specie
        (perfetta / imperfetta / dissonante). L'accordo delle voci e'
        DIPENDENZA, la dissonanza e' INDIPENDENZA (Introduzione, p.9);
      - il MOTO fra un verticale e il precedente: `contrario` (voci in
        direzioni opposte), `obliquo` (una tiene, l'altra muove), `parallelo`
        (stessa direzione, stesso intervallo), `diretto`/simile (stessa
        direzione, intervallo diverso). Contrario e obliquo fanno il
        contrappunto; il parallelo lo disfa (cap. 5, p.83);
      - le 5e/8e PARALLELE: due voci in 5a o 8a che restano tali muovendo
        insieme collassano in una voce sola (p.83). Sono l'unico vero divieto,
        e ce n'e' la lista;
      - le 5e/8e DIRETTE (nascoste): una 5a o 8a raggiunta per moto simile.
        ⚠️ Piston (p.86) NON le vieta -- "nessuna regola sulle 5e/8e dirette e'
        confermata dalla pratica dei compositori" -- e chiede discernimento,
        non un elenco di divieti. Qui si CONTANO, non si condannano;
      - la SIMULTANEITA' degli attacchi: meno attacchi in comune, piu' le
        voci sono ritmicamente indipendenti (p.72);
      - i PICCHI: se le due linee culminano nello stesso momento hanno poca
        indipendenza di curva (p.76).

    `movimento` e' il tick del battere per marcare le dissonanze forti; il
    default e' un movimento da 96 tick (4/4).
    """
    ea, eb = _eventi_linea(voce_a), _eventi_linea(voce_b)
    onset_a = {pos for pos, _, _ in ea}
    onset_b = {pos for pos, _, _ in eb}
    punti = sorted(onset_a | onset_b)

    verticali: list[Verticale] = []
    moti = {'contrario': 0, 'obliquo': 0, 'diretto': 0, 'parallelo': 0}
    paralleli: list[int] = []
    dirette: list[int] = []
    dissonanze_battere: list[int] = []
    prec: Verticale | None = None       # ultimo verticale PIENO (a e b presenti)

    for t in punti:
        a = _suona_a(ea, t)
        b = _suona_a(eb, t)
        battere = (t % movimento == 0)
        if a is None or b is None:
            verticali.append(
                Verticale(t, a, b, None, 'pausa', '-', None, battere))
            continue
        iv = abs(a - b)
        r = iv % 12
        nome = ('unisono' if iv == 0 else
                '8a' if r == 0 else _NOME_INTERVALLO[r])
        specie = _SPECIE_INTERVALLO[r]
        moto = None
        if prec is not None and prec.a is not None and prec.b is not None:
            da = (a > prec.a) - (a < prec.a)
            db = (b > prec.b) - (b < prec.b)
            if da == 0 or db == 0:
                moto = 'obliquo' if (da or db) else None
            elif da == db:
                moto = 'parallelo' if r == prec.intervallo % 12 else 'diretto'
            else:
                moto = 'contrario'
            if moto:
                moti[moto] += 1
                if moto == 'parallelo' and r in (0, 7):
                    paralleli.append(t)
                elif moto == 'diretto' and r in (0, 7):
                    dirette.append(t)
        if battere and specie == 'dissonante':
            dissonanze_battere.append(t)
        v = Verticale(t, a, b, iv, nome, specie, moto, battere)
        verticali.append(v)
        prec = v

    comuni = len(onset_a & onset_b)
    ta, tb = len(onset_a), len(onset_b)
    simult = comuni / max(ta, tb) if max(ta, tb) else 0.0

    def _picco(ev):
        if not ev:
            return None
        alto = max(y for _, _, y in ev)
        return min(pos for pos, _, y in ev if y == alto)

    pa, pb = _picco(ea), _picco(eb)
    insieme = (pa is not None and pb is not None and abs(pa - pb) < movimento)

    return Contrappunto(verticali, moti, paralleli, dirette,
                        (comuni, ta, tb), simult, (pa, pb), insieme,
                        dissonanze_battere)


def racconta_contrappunto(voce_a: dict[int, list[Note]],
                          voce_b: dict[int, list[Note]], *,
                          movimento: int = TICK_PER_MOVIMENTO,
                          nomi: tuple[str, str] = ('A', 'B')) -> str:
    """Il contrappunto fra due voci, a parole (regola 4).

    ASCII soltanto, come tutto quello che finisce in un `print`: la console di
    Windows e' cp1252 e non regge gli emoji (HANDOFF, 6 settembre 2026).
    """
    an = contrappunto(voce_a, voce_b, movimento=movimento)
    na_, nb_ = nomi
    righe = [f'{na_} contro {nb_} -- {len(an.verticali)} verticali '
             f'(* = sul battere)']
    for v in an.verticali:
        segno = '*' if v.battere else ' '
        if v.a is None or v.b is None:
            righe.append(f'  t{v.pos:<5}{segno} pausa')
            continue
        alto, basso = (v.a, v.b) if v.a >= v.b else (v.b, v.a)
        coppia = f'{nome_altezza(alto)}/{nome_altezza(basso)}'
        moto = f'  {v.moto}' if v.moto else ''
        righe.append(f'  t{v.pos:<5}{segno} {coppia:<12} {v.nome:<8}'
                     f'{v.specie}{moto}')
    m = an.moti
    righe.append(f'moti: contrario {m["contrario"]}, obliquo {m["obliquo"]}, '
                 f'diretto {m["diretto"]}, parallelo {m["parallelo"]}')
    comuni, ta, tb = an.attacchi
    righe.append(f'attacchi in comune: {comuni} su {ta}/{tb} '
                 f'(simultaneita {an.simultaneita:.0%} -- piu bassa, piu '
                 f'indipendenti)')
    if an.paralleli:
        righe.append('!! 5e/8e PARALLELE (le voci collassano in una) a: '
                     + ', '.join(f't{t}' for t in an.paralleli))
    if an.dirette:
        righe.append('5e/8e per moto diretto (Piston p.86: da valutare, non '
                     'vietate) a: ' + ', '.join(f't{t}' for t in an.dirette))
    if an.dissonanze_battere:
        righe.append('dissonanze sul battere (la spezia, purche risolvano) a: '
                     + ', '.join(f't{t}' for t in an.dissonanze_battere))
    pa, pb = an.picchi
    if pa is not None and pb is not None:
        stato = ('INSIEME -- poca indipendenza di curva' if an.picchi_insieme
                 else 'sfasati')
        righe.append(f'picchi: {na_} a t{pa}, {nb_} a t{pb} -- {stato}')
    return '\n'.join(righe)


class Sezione(NamedTuple):
    """Una sezione piazzata sulla timeline dell'arranger."""

    nome: str
    pos: int          # tick d'inizio
    battute: int      # quante battute dura
    lung: int         # durata in tick


def racconta_forma(piano) -> str:
    """La forma stesa, a parole (regola 4). ASCII soltanto (console cp1252)."""
    if not piano:
        return 'forma vuota'
    fine = piano[-1].pos + piano[-1].lung
    totale_battute = sum(s.battute for s in piano)
    righe = [f'forma: {" ".join(s.nome for s in piano)} '
             f'({totale_battute} battute, {fine} tick)']
    da = 1
    for s in piano:
        a = da + s.battute - 1
        righe.append(f'  {s.nome:<6} battute {da:>3}-{a:<3} ({s.battute})')
        da = a + 1
    return '\n'.join(righe)



# -------------------------------------------------------------------- il fill
#
# Il fill e' la transizione nella BATTERIA: una battuta, al giunto fra due
# sezioni. Dove va lo dice la forma (i giunti); cosa cambia lo dice la casella 9
# di docs/repertori/jazz.md, MISURATA su 51 fill jazz (2 batteristi). La firma
# NON e' la densita' -- e' che il ride si ferma e arrivano i tom.

#: Le quote di colpi per strumento, MISURATE (casella 9). ride nel beat 20,4% e
#: nel fill 3,3%; i tom 9,9% -> 29,0%. Sono la firma del fill.
FILL_QUOTA_RIDE_MAX = 0.10      # sopra il 10% il ride "non si e' fermato" (mis. 3,3%)
FILL_QUOTA_TOM_MIN = 0.15       # sotto il 15% "i tom non sono arrivati" (mis. 29,0%)
FILL_DENSITA_MAX = 1.5          # un fill e' ~1,2x il beat (15,7 vs 12,9), non il doppio


def _ruolo_batteria(nome: str) -> str:
    """Riconduce un nome di drum al suo RUOLO, per leggere la firma del fill
    senza dipendere da come e' chiamato il drum in un kit."""
    n = nome.lower()
    if 'tom' in n:
        return 'tom'
    if 'ride' in n:
        return 'ride'
    if 'rull' in n or 'snare' in n:
        return 'rullante'
    if 'cassa' in n or 'kick' in n:
        return 'cassa'
    if 'charl' in n or 'hat' in n or ' hi' in n:
        return 'charleston'
    return n


class Fill(NamedTuple):
    """I conti su un fill, contro la firma misurata -- i fatti, non il giudizio."""

    colpi: tuple[int, int]                 # (beat, fill): colpi totali
    densita: float                         # fill / beat
    quote: dict[str, tuple[float, float]]  # ruolo -> (quota nel beat, nel fill)
    velocita: tuple[float, float]          # (beat, fill): velocity media
    problemi: list[str]                    # cosa lo mette FUORI dal corpus


def _quote_per_ruolo(parte: dict[str, list[Note]]) -> tuple[dict[str, int], int]:
    conta: dict[str, int] = {}
    for nome, ns in parte.items():
        conta[_ruolo_batteria(nome)] = conta.get(_ruolo_batteria(nome), 0) + len(ns)
    return conta, sum(conta.values())


def _velocita_media(parte: dict[str, list[Note]]) -> float:
    tutte = [n.velocity for ns in parte.values() for n in ns]
    return sum(tutte) / len(tutte) if tutte else 0.0


def controlla_fill(beat: dict[str, list[Note]],
                   fill: dict[str, list[Note]]) -> Fill:
    """Controlla un FILL di batteria contro la firma MISURATA (casella 9).

    ⚠️ NON genera il fill: lo scrive l'AI (quali colpi, quali tom), e questo fa
    i conti per dire se sta nel territorio del corpus -- e' il ruolo che il
    corpus ha nel progetto, «prendere gli errori». Come `contrappunto` per le
    due linee.

    `beat` e `fill` sono `ruolo -> [Note]` (dai `passi()` di ogni drum): la
    battuta di groove e la battuta di fill che la sostituisce al giunto. La
    firma del fill (`[MIS]` 51 fill jazz, 2 batteristi -- vedi la cautela nella
    casella 9):

      - il RIDE si ferma: dal 20,4% dei colpi al 3,3%;
      - i TOM arrivano: dal 9,9% al 29,0% -- e' QUESTA la firma, non la densita';
      - la densita' sale di poco: 15,7 colpi contro 12,9, cioe' ~1,2x, non il
        doppio;
      - NON alza la voce: la velocity resta uguale o scende -- un fill non e' un
        crescendo, e' un cambio di strumento.

    `problemi` elenca cosa lo porta fuori dal corpus. Vuoto = il fill ha la firma.
    """
    conta_b, tot_b = _quote_per_ruolo(beat)
    conta_f, tot_f = _quote_per_ruolo(fill)
    q_ride = conta_f.get('ride', 0) / tot_f if tot_f else 0.0
    q_tom = conta_f.get('tom', 0) / tot_f if tot_f else 0.0
    densita = tot_f / tot_b if tot_b else 0.0
    vel_b, vel_f = _velocita_media(beat), _velocita_media(fill)

    ruoli = sorted(set(conta_b) | set(conta_f))
    quote = {r: (conta_b.get(r, 0) / tot_b if tot_b else 0.0,
                 conta_f.get(r, 0) / tot_f if tot_f else 0.0) for r in ruoli}

    problemi = []
    if q_ride > FILL_QUOTA_RIDE_MAX:
        problemi.append(f'il ride non si ferma: {q_ride:.0%} dei colpi, il '
                        f'corpus dice 3% (nel beat era 20%)')
    if q_tom < FILL_QUOTA_TOM_MIN:
        problemi.append(f'i tom non arrivano: {q_tom:.0%} dei colpi, il corpus '
                        f'dice 29% -- e i tom SONO la firma del fill')
    if densita > FILL_DENSITA_MAX:
        problemi.append(f'troppo fitto: {densita:.1f}x il beat, un fill jazz e '
                        f'~1,2x -- raddoppiare i colpi e fuori dal corpus')
    if vel_f > vel_b * 1.05:
        problemi.append(f'e un crescendo: velocity media {vel_f:.0f} contro '
                        f'{vel_b:.0f} del beat -- un fill non alza la voce')
    return Fill((tot_b, tot_f), densita, quote, (vel_b, vel_f), problemi)


def racconta_fill(beat: dict[str, list[Note]],
                  fill: dict[str, list[Note]]) -> str:
    """Il controllo del fill, a parole (regola 4). ASCII soltanto (console cp1252)."""
    f = controlla_fill(beat, fill)
    righe = [f'fill: {f.colpi[1]} colpi contro {f.colpi[0]} del beat '
             f'({f.densita:.1f}x), velocity {f.velocita[1]:.0f} vs {f.velocita[0]:.0f}']
    for ruolo, (qb, qf) in sorted(f.quote.items()):
        righe.append(f'  {ruolo:<12} beat {qb:>4.0%}  fill {qf:>4.0%}')
    if f.problemi:
        righe.append('FUORI dal corpus:')
        righe.extend(f'  - {p}' for p in f.problemi)
    else:
        righe.append('ha la firma del fill (ride giu, tom su, poco piu fitto, non piu forte)')
    return '\n'.join(righe)


# ------------------------------------------------------- reagire alla forma
#
# Il difetto d'origine del progetto, in due parole dell'utente: la batteria
# «suona discontinua rispetto a basso e piano... e non le puoi applicare
# acriticamente». Due guasti in uno: la parte e' UNIFORME (applicata
# acriticamente -- il basso a 4,00 note per battuta, deviazione 0,00) oppure
# VARIA ma SCOLLEGATA da cio' che succede. Una parte che REAGISCE fa il
# contrario: varia, e la sua variazione ha a che fare col resto -- complementa
# la melodia dove tace, si addensa verso il culmine. Qui il codice lo MISURA:
# l'AI scrive le parti, `reazione` dice se reagiscono o no.

def _tutte_le_note(parte) -> list[Note]:
    """Le Note di una parte, sia essa `y -> [Note]`, `drum -> [Note]` o lista."""
    if all(hasattr(parte, field) for field in ("pos", "length", "velocity", "lift")):
        return [parte]
    if isinstance(parte, dict):
        return [n for ns in parte.values() for n in ns]
    return list(parte)


def _densita_per_battuta(parte, battute: int | None = None,
                         tick_per_battuta: int = TICK_PER_BATTUTA) -> list[int]:
    """Quante note cadono in ogni battuta."""
    note = _tutte_le_note(parte)
    if not note:
        return [0] * (battute or 0)
    nb = battute or (max(n.pos for n in note) // tick_per_battuta + 1)
    conta = [0] * nb
    for n in note:
        b = n.pos // tick_per_battuta
        if 0 <= b < nb:
            conta[b] += 1
    return conta


def _deviazione(xs: list[int]) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5


def _pearson(a: list[int], b: list[int]) -> float | None:
    """La correlazione di Pearson, o None se una delle due e' piatta."""
    n = len(a)
    if n < 2:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va == 0 or vb == 0:
        return None
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return cov / (va ** 0.5 * vb ** 0.5)


#: Sotto questa deviazione la parte e' "piatta", cioe' applicata acriticamente.
REAZIONE_PIATTA = 0.75
#: Oltre questa correlazione (in valore assoluto) la parte "reagisce" davvero.
REAZIONE_SOGLIA = 0.30


class Reazione(NamedTuple):
    """I conti su quanto una parte reagisce a un riferimento."""

    densita: list[int]            # note per battuta della PARTE
    densita_rif: list[int]        # note per battuta del RIFERIMENTO
    deviazione: float             # di quanto varia la densita' della parte
    correlazione: float | None    # Pearson parte/riferimento (None se una e' piatta)
    verdetto: str                 # uniforme | scollegata | complementa | segue | varia


def reazione(parte, riferimento, *, battute: int | None = None,
             tick_per_battuta: int = TICK_PER_BATTUTA) -> Reazione:
    """Misura se una parte REAGISCE a un riferimento (la melodia, il comping).

    ⚠️ NON compone: l'AI scrive il basso o la batteria, questo fa i conti per
    dire se reagisce o e' applicata acriticamente. E' il difetto d'origine del
    progetto, misurato -- come `contrappunto` per due linee.

    `parte` e `riferimento` sono note (`y -> [Note]`, `drum -> [Note]`, o una
    lista). Guarda due cose, battuta per battuta:

      - la DEVIAZIONE della densita' della parte: se e' quasi zero, la parte e'
        UNIFORME -- applicata acriticamente (il basso a 4,00 note per battuta,
        deviazione 0,00, era questo);
      - la CORRELAZIONE con il riferimento: una parte che COMPLEMENTA cala dove
        il riferimento e' fitto (correlazione negativa -- call-and-response); una
        che lo SEGUE si addensa con lui (positiva, tipico verso il culmine); una
        che VARIA ma senza correlazione e' SCOLLEGATA -- l'altro difetto,
        «discontinua rispetto a basso e piano».

    `verdetto`: `uniforme` e `scollegata` sono i due guasti; `complementa`,
    `segue` (e `varia`, quando il riferimento e' piatto e non c'e' con cosa
    correlare) sono parti che reagiscono.
    """
    if (isinstance(tick_per_battuta, bool)
            or not isinstance(tick_per_battuta, int)
            or tick_per_battuta <= 0):
        raise ValueError('tick_per_battuta deve essere un intero positivo')
    dp = _densita_per_battuta(parte, battute, tick_per_battuta)
    dr = _densita_per_battuta(riferimento, battute, tick_per_battuta)
    nb = max(len(dp), len(dr))
    dp = dp + [0] * (nb - len(dp))
    dr = dr + [0] * (nb - len(dr))

    dev = _deviazione(dp)
    r = _pearson(dp, dr)
    if dev < REAZIONE_PIATTA:
        verdetto = 'uniforme'
    elif r is None:
        verdetto = 'varia'
    elif r <= -REAZIONE_SOGLIA:
        verdetto = 'complementa'
    elif r >= REAZIONE_SOGLIA:
        verdetto = 'segue'
    else:
        verdetto = 'scollegata'
    return Reazione(dp, dr, dev, r, verdetto)


def racconta_reazione(parte, riferimento, *, battute: int | None = None,
                       nomi: tuple[str, str] = ('parte', 'riferimento'),
                       tick_per_battuta: int = TICK_PER_BATTUTA) -> str:
    """Se una parte reagisce, a parole (regola 4). ASCII soltanto (console cp1252)."""
    re = reazione(parte, riferimento, battute=battute,
                  tick_per_battuta=tick_per_battuta)
    corr = 'piatto' if re.correlazione is None else f'{re.correlazione:+.2f}'
    spiega = {
        'uniforme': 'UNIFORME: applicata acriticamente (non varia)',
        'scollegata': 'SCOLLEGATA: varia ma non c entra col riferimento',
        'complementa': 'complementa: cala dove il riferimento e fitto (reagisce)',
        'segue': 'segue: si addensa col riferimento (reagisce)',
        'varia': 'varia (il riferimento e piatto: niente con cui correlare)',
    }
    return '\n'.join([
        f'{nomi[0]} vs {nomi[1]}: {spiega[re.verdetto]}',
        f'  densita {nomi[0]:<10} {re.densita}',
        f'  densita {nomi[1]:<10} {re.densita_rif}',
        f'  deviazione {re.deviazione:.2f} (sotto {REAZIONE_PIATTA} = piatta), '
        f'correlazione {corr}',
    ])


#: La cella su cui si guarda la presenza di un onset: il movimento (quarto).
#: PIU' FINE della battuta di `reazione()`, ed e' li' la differenza: due parti
#: con la STESSA densita' per battuta ma opposte DENTRO la battuta -- una sul
#: 1-2, l'altra sul 3-4 -- danno reazione muta (stessa densita') e interazione
#: "risponde" (presenza opposta cella per cella).
INTERAZIONE_CELLA = TICK_PER_MOVIMENTO
#: Oltre questa correlazione (in valore assoluto) sulle presenze c'e' relazione.
INTERAZIONE_SOGLIA = 0.30


def _presenza_per_cella(parte, cella: int, ncelle: int | None = None) -> list[int]:
    """0/1 per cella: 1 se un onset cade dentro quella cella."""
    note = _tutte_le_note(parte)
    if not note:
        return [0] * (ncelle or 0)
    nc = ncelle or (max(n.pos for n in note) // cella + 1)
    out = [0] * nc
    for n in note:
        c = n.pos // cella
        if 0 <= c < nc:
            out[c] = 1
    return out


def _celle_con_accento(parte, cella: int, ncelle: int) -> list[int]:
    """Le celle in cui la parte ha un ACCENTO -- velocity nel terzo alto del suo
    range. `[]` se la parte non ha spread di velocity (nessun accento distinto)."""
    note = _tutte_le_note(parte)
    vels = [n.velocity for n in note]
    if not vels or max(vels) == min(vels):
        return []
    soglia = min(vels) + 2 / 3 * (max(vels) - min(vels))
    out = set()
    for n in note:
        if n.velocity >= soglia:
            c = n.pos // cella
            if 0 <= c < ncelle:
                out.add(c)
    return sorted(out)


class Interazione(NamedTuple):
    """I conti sull'interazione a livello di EVENTO fra una parte e un riferimento."""

    presenza: list[int]           # 0/1 per cella, la PARTE
    presenza_rif: list[int]       # 0/1 per cella, il RIFERIMENTO
    correlazione: float | None    # Pearson sulle presenze (neg = risponde nel buco)
    cattura: float | None         # quota degli accenti del rif presi insieme (None se il rif non accenta)
    verdetto: str                 # risponde | insieme | slegato | tace


def interazione(parte, riferimento, *, cella: int = INTERAZIONE_CELLA,
                celle: int | None = None) -> Interazione:
    """Misura se una parte INTERAGISCE col riferimento a livello di EVENTO.

    ⚠️ NON compone: l'AI scrive la parte, questo fa i conti -- come `reazione`
    e `contrappunto`. E' il passo oltre `reazione`, che guarda la densita' per
    BATTUTA: qui si guarda la presenza di un onset per MOVIMENTO, e cosi' si
    coglie la COLLOCAZIONE dentro la battuta, non solo la quantita'.

    Due facce, quelle che l'utente ha nominato:

      - RISPONDE (call-and-response): la parte mette i suoi eventi nei BUCHI del
        riferimento -- correlazione NEGATIVA sulle presenze cella per cella. E'
        "la batteria segue un fraseggio", "rispondi dove lasciano un buco"
        (Riley). ⚠️ Diverso da `reazione.complementa`: due parti con la stessa
        densita' per battuta ma opposte dentro la battuta danno reazione muta e
        qui "risponde";
      - CATTURA (prendere un accento): degli ACCENTI del riferimento, la quota
        che la parte prende insieme (un onset nella stessa cella). E' "il basso
        che raccoglie un accento della batteria", la figura presa insieme.

    `verdetto`: `risponde` (riempie i buchi) e `insieme` (suona sui colpi del
    riferimento: figure se `cattura` e' alta, muro se e' bassa) sono le due
    relazioni; `slegato` e' nessuna delle due; `tace` se la parte non suona.
    `cattura` e' `None` quando il riferimento non ha accenti distinguibili.
    """
    pp = _presenza_per_cella(parte, cella)
    pr = _presenza_per_cella(riferimento, cella)
    nc = max(len(pp), len(pr), celle or 0)
    pp = pp + [0] * (nc - len(pp))
    pr = pr + [0] * (nc - len(pr))

    r = _pearson(pp, pr)
    acc = _celle_con_accento(riferimento, cella, nc)
    cattura = (sum(1 for c in acc if pp[c]) / len(acc)) if acc else None

    if sum(pp) == 0:
        verdetto = 'tace'
    elif r is None:
        verdetto = 'slegato'
    elif r <= -INTERAZIONE_SOGLIA:
        verdetto = 'risponde'
    elif r >= INTERAZIONE_SOGLIA:
        verdetto = 'insieme'
    else:
        verdetto = 'slegato'
    return Interazione(pp, pr, r, cattura, verdetto)


def racconta_interazione(parte, riferimento, *, cella: int = INTERAZIONE_CELLA,
                         celle: int | None = None,
                         nomi: tuple[str, str] = ('parte', 'riferimento')) -> str:
    """L'interazione a parole (regola 4). ASCII soltanto (console cp1252)."""
    it = interazione(parte, riferimento, cella=cella, celle=celle)
    corr = 'piatto' if it.correlazione is None else f'{it.correlazione:+.2f}'
    catt = 'n/d' if it.cattura is None else f'{it.cattura:.0%}'
    spiega = {
        'risponde': 'risponde: mette gli eventi nei BUCHI del riferimento (call-and-response)',
        'insieme': 'insieme: suona sui colpi del riferimento (figure se cattura alta, muro se bassa)',
        'slegato': 'SLEGATO: gli eventi non c entrano coi buchi del riferimento',
        'tace': 'tace: la parte non suona',
    }
    return '\n'.join([
        f'{nomi[0]} vs {nomi[1]}: {spiega[it.verdetto]}',
        f'  presenza {nomi[0]:<10} {it.presenza}',
        f'  presenza {nomi[1]:<10} {it.presenza_rif}',
        f'  correlazione {corr} (neg = risponde), cattura accenti {catt}',
    ])


def racconta_armonia(spec: str, *, voicing: str = 'chiuso',
                     registro: str = 'do3', condotta: bool = True) -> str:
    """Cosa e' diventata ogni sigla, e quali ambiguita' sono state sciolte.

    Regola 4: un'operazione silenziosa non e' correggibile. Qui il rischio
    non e' sbagliare le note -- e' sceglierne di plausibili senza che nessuno
    possa accorgersi che erano un'altra cosa.

    ⚠️ `condotta` c'e' e ha lo STESSO default di `armonia()`, e non e' un
    dettaglio: questa funzione esiste per riferire cosa e' stato scritto, e se
    non conducesse riferirebbe altezze diverse da quelle che finiscono nel
    file. Una funzione che rende conto e sbaglia il conto e' peggio di
    nessuna.
    """
    righe = [f'voicing {voicing!r} ({VOICING[voicing]}), registro {registro}'
             + (', condotta delle parti' if condotta else '')]
    avvisi = []
    guidate = (voci_condotte(spec, voicing=voicing, registro=registro)
               if condotta else None)
    k = 0
    for gruppo in spec.split(SEPARATORE_ACCORDI):
        testo = gruppo.strip()
        if not testo or testo == PAUSA:
            righe.append('  .           pausa')
            continue
        s = sigla(testo)
        if guidate is not None:
            note = guidate[k]
            k += 1
        else:
            note = voci(s, voicing=voicing, registro=registro)
        nomi = ' '.join(nome_altezza(y) for y in note)
        righe.append(f'  {testo:<12}{nomi}')
        if s.letto_come:
            avvisi.append(s.letto_come)
    if avvisi:
        righe.append('letture ambigue sciolte cosi:')
        righe.extend(f'  - {a}' for a in avvisi)
    if condotta:
        righe.append('nota: gli accordi sono CONDOTTI -- ognuno si posa dove '
                     'muove meno voci rispetto al precedente. Cambiano le '
                     'ottave, mai le note')
    else:
        righe.append('nota: ogni accordo e costruito per conto suo, senza '
                     'condotta delle parti fra uno e il successivo')
    return '\n'.join(righe)


# ------------------------------------------------------------------ il cancello
def _grado_e_scarto(y: int, root: int, intervalli) -> tuple[int, int]:
    """(grado assoluto, scarto cromatico) di un'altezza dentro una scala.

    Il grado assoluto conta i gradi da sempre, ottave comprese, cosi' salire
    di N gradi e' una somma sola. Lo SCARTO e' quanti semitoni la nota sta
    sopra il suo grado: vale 0 per le note in scala e 1 o 2 per le altre, ed
    e' il numero che permette di trasporre una nota fuori scala senza
    schiacciarla dentro.
    """
    pc = (y - root) % 12
    ottava = (y - root) // 12
    grado = max(i for i, m in enumerate(intervalli) if m <= pc)
    return ottava * len(intervalli) + grado, pc - intervalli[grado]


def _per_gradi(y: int, root: int, intervalli, gradi: int) -> int:
    """L'altezza `y` spostata di `gradi` dentro la scala, scarto conservato."""
    assoluto, scarto = _grado_e_scarto(y, root, intervalli)
    ottava, grado = divmod(assoluto + gradi, len(intervalli))
    return root + ottava * 12 + intervalli[grado] + scarto
