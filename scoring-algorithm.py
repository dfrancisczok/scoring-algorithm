import math
import sys

# Populize your data set
# You can freely modify the number of columns and lines
S0 = (
	# A B C D E F G H I K  
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # a 
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # b 
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # c
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # d
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # e
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # f
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # g 
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # h 
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # i 
	( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), # k
    )

sigma0 = 1.0  

N = len(S0)

def print_vector(name, V):
	sys.stdout.write("%s [ " % name)
	for i in range(0, len(V)):
		if (V[i] < 0):
			sys.stdout.write(" --")
		else:	sys.stdout.write("%3d" % math.trunc(V[i] * 100))
		if i < len(V) - 1:
			sys.stdout.write(", ")
	sys.stdout.write(" ] \n")

# Normalize scores
S = [ [ 1.0 for i in range(0, N) ] for j in range(0, N) ]
for i in range(0, N):
	sum = 0.0
	for j in range(0, N):
		if i != j:
			sum += S0[i][j]
	for j in range(0, N):
		if i != j:
			S[i][j] = S0[i][j] * 1.0 * (N - 1) / sum
		else:	S[i][j] = -1.0

first = True
for s in S:
	print_vector("Scoring matrix: " if first else "                ", s)
	first = False
sys.stdout.write("\n")

W = [ 1.0 for i in range(0, N) ]
Z = [ 1.0 for i in range(0, N) ]

for n in range(0, 20):
	# Average score
	R = [ 0.0 for i in range(0, N) ]
	for j in range(0, N): 
		assum = 0.0
		wzsum = 0.0
		for i in range(0, N):
			if i != j:
				wz = W[i] * Z[i]
				assum += wz * S[i][j]
				wzsum += wz
		R[j] = assum / wzsum

	# Normalize average
	rsum = 0.0
	for i in range(0, N):
		rsum += R[i]
	for i in range(0, N):
		R[i] = R[i] * N / rsum

	# Goodwill factor
	for i in range(0, N): 
		sigma = 0.0
		for j in range(0, N): 
			if i != j:
				delta = R[j] - S[i][j]
				sigma += delta * delta
		sigma = math.sqrt(sigma / N)
		W[i] = math.exp(-sigma / sigma0)
		Z[i] = R[i]

	# Normalize weights
	wsum = 0.0
	for i in range(0, N):
		wsum += W[i]
	for i in range(0, N):
		W[i] = W[i] * N / wsum

	# Results
	if n == 0:
		print_vector("Raw scores:     ", R)

# punishment factor
RR = [ 0.0 for i in range(0, N) ]
for i in range(0, N):
	RR[i] = R[i] * W[i]
rrsum = 0.0
for i in range(0, N):
	rrsum += RR[i]
for i in range(0, N):
	RR[i] = RR[i] * N / rrsum
print_vector("Adjusted scores:", R)
print_vector("Punished scores:", RR)
print_vector("Fairness factor:", W)
