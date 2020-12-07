import sys

num_in_party = 0
declarations = []
party_responses = ''


for l in sys.stdin:
    if l.strip() == '':  # end of party group
        s = "".join(sorted(party_responses))
        declarations += [{'n': num_in_party, 'r': s}]
        num_in_party = 0
        party_responses = ''
    else:
        party_responses += l.strip()
        num_in_party += 1

if party_responses != '':
    s = "".join(sorted(party_responses))
    declarations += [{'n': num_in_party, 'r': s}]

g_total = 0

for p in declarations:
    n = 0
    responses = set([c for c in p['r']])
    for r in responses:
        if p['r'].count(r) == p['n']:
            n += 1
    g_total += n

print(g_total)
