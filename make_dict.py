import json

targets = [''.join(l.strip().split(',')).upper() for l in open('words.csv', encoding='utf-8').read().splitlines()[1:] if l.strip()]
valid_words = json.load(open('valid_words.json', encoding='utf-8'))
packed = ''.join(valid_words)

content = []
content.append('// Auto-generated Wordle Dictionary from words.csv and official English 5-letter dictionary')
content.append(f'window.WORDLE_TARGET_WORDS = {json.dumps(targets)};')
content.append(f'window.WORDLE_VALID_WORDS_PACKED = "{packed}";')
content.append('window.WORDLE_VALID_WORDS = new Set(window.WORDLE_VALID_WORDS_PACKED.match(/.{5}/g));')
content.append('window.WORDLE_TARGET_WORDS.forEach(function(w) { window.WORDLE_VALID_WORDS.add(w); });')

with open('words.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content) + '\n')

print(f"words.js written successfully! Targets: {len(targets)}, Valid Words: {len(valid_words)}")
