U='\nv|velocity|m/s\nt|time|s\nth|angle|rad\nR|length/radius|m\nF|force|N\nm|mass|kg\nx|position/displacement|m\nr|length/radius|m\nT|time|s\nW|energy/work|J\nd|position/displacement|m\nKf|kinetic energy|J\nKi|kinetic energy|J\nU|energy/work|J\nP|power|W\nw|angular velocity|rad/s\ntor|torque|N*m\nl|length/radius|m\nph|angle|rad\nq1|charge|C\nq2|charge|C\nEf|electric field|N/C\nq|charge|C\nflux|electric flux|N*m^2/C\nA|area|m^2\nlam|line charge density|C/m\nsig|surface charge density|C/m^2\nQ|charge|C\nrhoq|volume charge density|C/m^3\nnc|signed charge count|1\nV|voltage|V\ndV|voltage|V\nC|capacitance|F\nkd|dielectric constant|1\nC1|capacitance|F\nC2|capacitance|F\nue|energy density|J/m^3\nV0|voltage|V\nVb|voltage|V\ncur|current|A\nres|resistance|ohm\nrhoe|resistivity|ohm*m\nn|carrier density|1/m^3\nvd|drift speed|m/s\njcur|current density|A/m^2\nres1|resistance|ohm\nres2|resistance|ohm\nemf|voltage|V\nri|resistance|ohm\ntau|time|s\nB|magnetic field|T\nNm|turn count|1\nnt|turns per length|1/m\ncur0|current|A\nmom|magnetic moment|A*m^2\nfluxB|magnetic flux|Wb\ndflux|magnetic flux|Wb\nind|inductance|H\nub|energy density|J/m^3\nQ0|charge|C\n'
def row(data, index):
    start = 0
    for i in range(index):
        start = data.find('\n', start) + 1
    end = data.find('\n', start)
    return data[start:] if end < 0 else data[start:end]

def titles(data):
    out = []
    start = 0
    while start < len(data):
        out.append(data[start:data.find('|', start)])
        end = data.find('\n', start)
        if end < 0:
            break
        start = end + 1
    return out

def entry(data, index):
    title, eq, names, domains, note, methods = row(data, index).split('|')
    names = names.split(',')
    specs = []
    for i, n in enumerate(names):
        start = U.find('\n' + n + '|') + 1
        name, label, unit = U[start:U.find('\n', start)].split('|')
        specs.append((name, label, unit, domains[i]))
    inverses = []
    polys = []
    for m in methods.split(';'):
        parts = m[2:].split(',') if len(m) > 2 else []
        polys.append(parts if m[0] == 'P' else [])
        inverses.append(['@'] * max(1, len(parts) - 1) if m[0] == 'P' else parts)
    return (title, eq, specs, inverses, note, polys)
