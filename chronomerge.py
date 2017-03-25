a = [[0, 1], [1, 2], [3, 5], [8, 10], [4, 9]]
b = [[0, 2], [3, 10]]

def chronomerge(l):
	s = sorted(l)
	m = []
	for sx, sy in s:
		found = False
		for i, [mx, my] in enumerate(m):
			if mx <= sx <= my <= sy:
				m[i][1] = sy # m[i][1] == my
				found = True
				break
		if not found:
			m.append([sx, sy])
	return m

assert chronomerge(a) == b
