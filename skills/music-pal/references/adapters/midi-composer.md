# MIDI Composer → MusicPal → esecutore

Percorso operativo `[DEC]`, verificato sui tool MCP installati il 2026-10-10.
MIDI Composer è un server separato con strumenti atomici di teoria musicale,
generazione e scrittura MIDI. È distinto dalla vecchia skill `music-composer`
citata negli archivi. MusicPal decide intenzione, vincoli, sviluppo e revisione;
MIDI Composer costruisce il materiale richiesto. L'esecutore assegna i suoni.
Non è una nuova fonte di copertura musicologica né una garanzia di qualità.

## Preparare e generare

1. Fissa ruoli, registri numerici MIDI, metro, BPM, durata in quarti, sezioni,
   contrasto e vincoli. Segui il [percorso breve](../demo-breve.md) per una demo.
2. Scopri gli strumenti effettivamente installati e leggine lo schema. Per
   armonia puoi concatenare `degrees_to_chords` / `roman_to_chords` e
   `voice_leading`; per una figura `motif_grammar` e `notes_from_degrees`;
   per accompagnamento `chord_pattern`, `bass_line`, `euclidean_rhythm`.
   Scegli i parametri per il gesto musicale, non per esaurire i tool disponibili.
3. Scrivi con `notes_to_midi`, `arrange_to_midi` o `arrange_song`. Quest'ultimo
   combina sezioni `{bars, tracks}` nella sequenza `form`: tempi locali alla
   sezione, nomi delle parti stabili per unirle. Verifica lo schema corrente
   anche dei campi interni delle tracce; non inventare campi per eventi arbitrari.
4. Rendi espliciti velocity normale e accentata, `step_beats`, `sustain`, swing
   e unità dello swing. Nel renderer `O` è accento, `o` attacco normale, `.` pausa;
   **non è** l'alfabeto `X/x/o/.` di `musica.passi`. Con `sustain=true` una pausa
   può prolungare la nota precedente: meno attacchi non significa più silenzio.
   Non sommare swing del renderer e swing già impresso nelle note.
5. Conserva argomenti esatti delle chiamate, risultati utili e MIDI originale.
   Usa il percorso restituito dal tool; se ricevi solo base64, decodificalo in
   un file locale. Usa una cartella di lavoro scelta per questa richiesta;
   non distribuire brani privati insieme alla libreria.

Esempio minimo degli argomenti di `notes_to_midi` verificati sul server installato:

```json
{
  "notes": ["D4", "F4", "A4", "C5"],
  "rhythm": "O.o.o.O.",
  "step_beats": 0.5,
  "velocity": 72,
  "accent_velocity": 108,
  "sustain": false,
  "swing": 0.5,
  "tempo": 128,
  "program": 0,
  "file_name": "idea.mid"
}
```

Sono otto celle / quattro quarti: quattro note MIDI 62, 65, 69, 72 agli onset
0, 1, 2, 3, durate 1/2, velocity 108, 72, 72, 108. Il silenzio finale fa parte
della durata della frase. MIDI Composer usa **C4 = MIDI 60**; Ableton chiama lo
stesso numero C3. Non trasporre le note per conservare il nome dell'ottava.

## Importare e verificare

La libreria Python MusicPal deve essere installata nell'ambiente che esegue
questo codice; copiare soltanto la skill non installa Python o il server MCP.
Il parser storico è già in `musicpal.midi` (ereditato da DelugePal).
Per questo flusso usa `musicpal.midi_import`: lettura rigorosa, senza dipendenze
esterne e senza I/O verso Live o Deluge.

```python
import json
from pathlib import Path
from musicpal.midi_import import read

song = read("idea.mid", length_beats=4)
# Conservare un manifest accanto al MIDI originale, senza sovrascriverlo.
with Path("idea.audit.json").open("x", encoding="utf-8") as audit:
    json.dump(song.to_dict(), audit, indent=2)

for track in song.tracks:
    print(track.index, track.name, track.end_tick, track.events)

# Solo dopo aver ispezionato gli eventi: in questo esempio il program GM
# viene sostituito dall'assegnazione esplicita di uno strumento nell'esecutore.
parts = song.patterns(omit_events={"program_change"})
for part in parts:
    print(part.track_index, part.channel, part.length_beats, part.pattern.to_dict())
```

Oppure per la sola ispezione:

```powershell
python -m musicpal.midi_import idea.mid --length-beats 4 --output idea.audit.json
```

Il manifest conserva hash SHA-256 del sorgente, PPQ, tracce anche vuote, canali,
note, velocity di attacco/rilascio, fine di ogni traccia e payload degli altri
eventi. I tempi delle note sono frazioni esatte di quarto: nessuna quantizzazione.
`length_beats` può estendere il silenzio fino alla durata prevista, mai tagliare
il sorgente. Senza questo argomento viene usata la massima fine traccia del MIDI:
non assumere che coincida sempre con la durata richiesta al generatore.

`patterns()` separa per **indice traccia e canale**, senza fondere nomi uguali.
Ogni parte riceve la lunghezza comune del brano; le tracce senza note restano
nel manifest, non generano pattern. Nomi e canali non sono assegnazioni di ruolo:
abbinali esplicitamente a basso, batteria, accordi, melodia o altri ruoli.

Program change, CC (anche il pedale), pitch bend, pressure, SysEx e meta-eventi
non rappresentabili bloccano `patterns()`. Esamina `tracks[].events`, gestiscili
con l'esecutore o elenca in `omit_events` soltanto i tipi che decidi di omettere,
motivandolo. La lista è una scelta esplicita di conversione, non una richiesta
automatica di nuovo permesso all'utente. Il manifest mantiene comunque gli eventi.
Non usare `omit_events` indiscriminatamente per far passare l'importazione.

Tempo e metro costanti sono accessibili da `song.tempo_us_per_quarter` e
`song.meter`; in loro assenza valgono i default MIDI 120 BPM e 4/4. Le mappe
variabili restano negli eventi ma non sono convertibili con `patterns()`:
servono una gestione dedicata della timeline o un renderer appropriato.
Non sostituire una mappa variabile con il primo BPM/metro trovato.

Sono accettati SMF 0/1 con PPQ. Formato 2, SMPTE, note non chiuse, note di durata
zero e sovrapposizioni dello stesso pitch sullo stesso canale/traccia vengono
rifiutati, senza riparazioni tacite. Note-on con velocity zero equivale a note-off
con lift implicito 64; un note-off esplicito mantiene la velocity ricevuta,
anche zero. Il manifest non è un codec per riscrivere un SMF byte per byte:
conserva sempre il MIDI originale. Per revisioni dei metadati usa un editor MIDI
che sappia rappresentarli, non il vecchio lettore permissivo come scorciatoia.

## Consegnare e rivedere

Per Producer Pal leggi [l'adapter](producer-pal.md) e gli schemi correnti.
`render_notes(part.pattern)` mantiene tutte le velocity di attacco e converte
i nomi d'ottava. La notazione non esprime il lift: MIDI Composer nel test corrente
scrive note-off con velocity zero, quindi il serializer richiede una scelta
esplicita, ad esempio `render_notes(part.pattern, discard_lift=True)` dopo aver
accettato questa limitazione per gli strumenti scelti. Dichiarala nella consegna.
La lunghezza `part.length_beats`, il tempo `60000000 / song.tempo_us_per_quarter`,
il metro, il routing e i suoni vanno impostati separatamente. Per DelugePal usa
[il suo adapter](deluge-pal.md) e la conversione in tick del [contratto](contract.md).

Rileggi le note dall'esecutore e confronta pitch, onset, durata e velocity,
oltre a lunghezza e routing. Per un confronto sonoro usa gli stessi strumenti,
effetti e livelli; la sintesi di anteprima `midi_to_audio` non sostituisce quel
confronto. Specifica se l'audio è stato davvero ascoltato.

Per una revisione conserva baseline, richiesta e nuovo risultato. Dichiara
**Tengo / Cambio / Direzione / Resta regolabile**; confronta gli eventi e verifica
che le altre parti e gli intervalli esclusi siano identici. Se il renderer non
consente di preservare esattamente gli eventi vincolati, modifica il pattern
importato e usa l'adapter anziché rigenerare l'intero brano.
Chiudi con [Previsto / Realizzato / Da verificare all'ascolto](../verifica-finale.md).
