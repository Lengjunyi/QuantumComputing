from qiskit import QuantumCircuit

qc = QuantumCircuit(6)

# Oracle output 1 only when input = "10010 (中国联通)"
def oracle(c:QuantumCircuit):
    for i in [1,2,4]:
        c.x(i)
    c.mcx([0,1,2,3,4], 5)
    for i in [1,2,4]:
        c.x(i)


# step 1: prepare state.
# 5 is the output bit so only consider case of 1
for n in range(5):
    qc.h(n)
qc.x(5)

# bits -> VWVWVWVWVW.....
# 4 = round(pi/4*sqrt(2^5))
for t in range(4):
    # step 2: V-gate. use identity HXH=Z here as we have oracle as black box
    qc.h(5)
    oracle(qc)
    qc.h(5)

    # step 3: W-gate. again, HXH=Z. this is actually -W but shouldn't matter
    for i in range(5):
        qc.h(i)
    for i in range(5):
        qc.x(i)
    qc.h(4)
    qc.mcx([0,1,2,3], 4)
    qc.h(4)
    for i in range(5):
        qc.x(i)
    for i in range(5):
        qc.h(i)

# step 4: measure
qc.measure_all()

print(qc.draw())

from qiskit.primitives.sampler import Sampler
sampler = Sampler()
job = sampler.run(qc, shots=2000)
result = job.result()
for k,v in result.quasi_dists[0].items():
    print(bin(k)[:1:-1], "state appear with frequency", v)
    # should expect "100101" appear the most
