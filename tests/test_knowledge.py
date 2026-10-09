"""Integrity, portability and truthful coverage of the extracted knowledge."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/music-pal'
REF=SKILL/'references'
IDS=[1,2,3,4,5,6,7,8,9,11]

def slots(text):
    matches=list(re.finditer(r'^## (\d+)\. ([^\n]+)',text,re.M))
    result=[]
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(text)
        lines=[x.strip() for x in text[m.end():end].splitlines() if x.strip()]
        result.append((int(m[1]),m[2],lines[0] if lines else ''))
    return result

class KnowledgeTests(unittest.TestCase):
    def test_all_originals_and_line_ranges_preserved(self):
        manifest=json.loads((SKILL/'provenance/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(manifest['files']),55)
        self.assertEqual(len({x['source'] for x in manifest['files']}),55)
        for entry in manifest['files']:
            with self.subTest(source=entry['source']):
                data=(SKILL/entry['snapshot']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(),entry['source_sha256'])
                self.assertEqual(len(data.decode('utf-8').splitlines()),entry['original_lines'])
                next_line=1
                for block in entry['blocks']:
                    self.assertEqual(block['start_line'],next_line)
                    self.assertGreaterEqual(block['end_line'],block['start_line'])
                    self.assertIn(block['route'],['music','deluge','split'])
                    next_line=block['end_line']+1
                self.assertEqual(next_line,entry['original_lines']+1)
                neutral=(SKILL/entry['neutral']).read_bytes()
                self.assertEqual(hashlib.sha256(neutral).hexdigest(),entry['neutral_sha256'])

    def test_all_repertori_preserve_musical_slot_states(self):
        self.assertEqual(len(list((REF/'repertori').glob('*.md'))),7)
        for path in (REF/'repertori').glob('*.md'):
            original=SKILL/'provenance/delugepal/docs/repertori'/path.name
            old={i:(title,lead) for i,title,lead in slots(original.read_text(encoding='utf-8')) if i!=10}
            new=slots(path.read_text(encoding='utf-8'))
            self.assertEqual([i for i,_,_ in new],IDS,path.name)
            def status(lead):
                return 'empty' if lead.startswith('**Vuota') else 'partial' if lead.startswith('**Parziale') else 'filled'
            for i,title,lead in new:
                self.assertEqual(title,old[i][0],(path.name,i))
                self.assertEqual(status(lead),status(old[i][1]),(path.name,i))

    def test_matrix_matches_neutral_repertori(self):
        rows={}
        for line in (REF/'MUSICA.md').read_text(encoding='utf-8').splitlines():
            m=re.search(r'\]\(repertori/([^)]+)\)',line)
            if m:
                cells=[c.strip() for c in line.strip('|').split('|')]
                rows[m[1]]=cells[1:]
        self.assertEqual(len(rows),7)
        for filename,values in rows.items():
            expected=[]
            for _,_,lead in slots((REF/'repertori'/filename).read_text(encoding='utf-8')):
                expected.append('○' if lead.startswith('**Vuota') else '◐' if lead.startswith('**Parziale') else '●')
            self.assertEqual(values,expected,filename)

    def test_no_machine_execution_in_canonical_knowledge(self):
        patterns=[r'\bfrom delugexml\b',r'\bMU\.',r'\.venv[/\\]',r'/SONGS/',r'inputTickMagnitude',r'swingInterval',r'write_file\(',r'parse_file\(']
        for folder in [REF/'repertori',REF/'istruzioni']:
            for p in folder.glob('*.md'):
                text=p.read_text(encoding='utf-8')
                for pattern in patterns:
                    self.assertIsNone(re.search(pattern,text),(p.name,pattern))

    def test_links_work_after_installing_folder_alone(self):
        with tempfile.TemporaryDirectory(dir=ROOT, prefix="knowledge-install-") as tmp:
            copy=Path(tmp)/'music-pal';shutil.copytree(SKILL,copy)
            active=[copy/'SKILL.md',*list((copy/'references').rglob('*.md'))]
            for p in active:
                text=p.read_text(encoding='utf-8')
                for link in re.finditer(r'\[[^\]\n]+\]\(([^)\n]+)\)',text):
                    target=link[1].split('#',1)[0]
                    if not target or re.match(r'https?://|mailto:',target):continue
                    resolved=(p.parent/target).resolve()
                    self.assertTrue(resolved.is_relative_to(copy.resolve()),(p.name,target))
                    self.assertTrue(resolved.exists(),(p.name,target))

    def test_navigation_routes_every_instruction(self):
        self.assertEqual(len(list((REF/'istruzioni').glob('*.md'))),46)
        nav=(REF/'navigation.md').read_text(encoding='utf-8')
        for p in (REF/'istruzioni').glob('*.md'):
            self.assertIn(f'(istruzioni/{p.name})',nav)

    def test_negative_and_partial_evidence_not_promoted(self):
        trama=(REF/'istruzioni/brano-completo.md').read_text(encoding='utf-8')
        for phrase in ['TRAMA02','esito negativo','TRAMA06','367','123','58 battute']:
            self.assertIn(phrase,trama)
        idm=(REF/'repertori/idm.md').read_text(encoding='utf-8')
        self.assertIn('**Parziale.**',idm)
        self.assertIn('Non conta come copertura riuscita',idm)
        common=(REF/'MUSICA.md').read_text(encoding='utf-8')
        self.assertIn('| classica · barocca · antica | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |',common)
        self.assertIn('Le caselle si riempiono SU DOMANDA',common)
        self.assertIn('Il corpus dà RELAZIONI, non superfici',common)

    def test_musical_patterns_survive_executable_example_removal(self):
        manifest=json.loads((SKILL/'provenance/manifest.json').read_text(encoding='utf-8'))
        for entry in manifest['files']:
            original=(SKILL/entry['snapshot']).read_text(encoding='utf-8')
            neutral=(SKILL/entry['neutral']).read_text(encoding='utf-8')
            for code in re.findall(r"```(?:python)?\s*\n(.*?)```",original,re.S):
                for pattern in re.findall(r"['\"]([xXo.]{4,})['\"]",code):
                    self.assertIn(pattern,neutral,(entry['source'],pattern))

    def test_comping_example_keeps_exact_rhythm_and_anticipation(self):
        text=(REF/'istruzioni/comping.md').read_text(encoding='utf-8')
        for value in ['Dm7','G7','Cmaj7','otto crome','x..x...x','x..x....','0; 1,5; 3,5','anticipa il battere']:
            self.assertIn(value,text)

    def test_dub_preserves_musical_effects_and_does_not_inherit_adapter_limit(self):
        text=(REF/'repertori/reggae-dub.md').read_text(encoding='utf-8')
        for value in ['..x.o.X.o.x.o.X.','..o.....X...x.X.','..x...x...x...x.','.oo..oo..oo..oo.','non è una prescrizione musicale','colpi singoli','Delay e riverbero sono strumenti compositivi']:
            self.assertIn(value,text)
        self.assertNotIn('la 10,',text)
        self.assertNotIn('si **lascia\nfuori**',text)

    def test_shared_sound_design_and_exact_note_events_survive(self):
        common=(REF/'MUSICA.md').read_text(encoding='utf-8')
        for value in ['Non esiste una soglia universale','Base e profondità','delay e il riverbero','spostamento rispetto al ciclo']:
            self.assertIn(value,common)
        walking=(REF/'istruzioni/walking.md').read_text(encoding='utf-8')
        for row in ['| 0 | 41 | 96 |','| 96 | 45 | 96 |','| 192 | 48 | 192 |','| 384 | 46 | 96 |']:
            self.assertIn(row,walking)
        self.assertIn('96 tick per quarto',walking)

    def test_attribution_and_license_context_preserved(self):
        text=(REF/'FONTI.md').read_text(encoding='utf-8')
        for term in ['CC BY 4.0','MIT','ODbL','DbCL','Gillick','Cheston','Pfleiderer','1294','456','1150']:
            self.assertIn(term,text)

if __name__=='__main__': unittest.main()
