import re, os

os.chdir(r'C:\Users\SHAKTI\Downloads\DEMON-X')

results = {}

# Extract strings from DEMON-X.sh
with open('DEMON-X.sh', 'rb') as f:
    data = f.read()
strings = re.findall(b'[\x20-\x7e]{4,}', data)
results['DEMON-X'] = [s.decode('utf-8','ignore') for s in strings]

# Extract strings from each .ko file
for fname in ['5.10.ko','5.15.ko','6.1.ko','6.12.ko','6.18.ko','6.6.ko']:
    path = os.path.join('driver_ko_670', fname)
    if not os.path.exists(path):
        continue
    with open(path, 'rb') as f:
        data = f.read()
    strings = re.findall(b'[\x20-\x7e]{4,}', data)
    results[fname] = [s.decode('utf-8','ignore') for s in strings]

# Write all strings to readable text files
for name, strs in results.items():
    outpath = f'{name}_strings.txt'
    with open(outpath, 'w', encoding='utf-8') as out:
        out.write(f'# Strings extracted from {name}\n')
        out.write(f'# Total: {len(strs)} strings\n\n')
        seen = set()
        for s in sorted(set(strs)):
            if s not in seen:
                out.write(s + '\n')
                seen.add(s)
    print(f'Written: {outpath} ({len(strs)} strings)')

print('\nDone! All strings extracted to readable .txt files.')
