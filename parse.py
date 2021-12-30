freqs = []
with open('hrLex_v1.3') as f:
    for line in f:
        niz = line.split()
        rijec = niz[0]
        frek = float(niz[-1])
        if frek > 3e-6:
            freqs.append((frek, rijec))
freqs.sort(reverse=True)
for frek, rijec in freqs:
    print(rijec, frek)
