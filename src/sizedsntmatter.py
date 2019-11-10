import gym, numpy
ENVS = []
states = []
observations = []
for i in range(0,4):
    ENVS.append(gym.make('CartPole-v0'))
    observations.append(ENVS[i].reset())
states = [
    #   Sportier Agent
    numpy.array([-0.7147494,  -0.42867257, -0.82550574,  0.30217533,  0.66425145,  0.8554445, 0.32042119, -0.65587011,  0.70247635, -0.24385584, -0.16744136,  0.07596199, 0.42395802, -0.40647903, -0.71307407, -0.20487693,  0.06588612, -0.04159331, 0.07094222,  0.05854932,  0.62036367,  0.30299705, -0.86366105, -0.09308881])
    #   Theoretically sportier agent
    ,numpy.array([ 0.77183292, -0.48092819, -0.17124069,  0.98513674, -0.13510315,  0.30103147, -0.60691039, -0.93704527, -0.12095691, -0.53841486, -0.46367681, -0.51790653,  0.46707824,  0.45896793, -0.9771947,   0.86683368,  0.56668673, -0.56151766,  0.04503849,  0.76839038, -0.40798313, -0.16680482, -0.57124574,  0.19232203])
    #   Basic Agent
    ,numpy.array([0.69133231, -0.20516511, -0.75820921, 0.26613669, 0.27673464, -0.36717599,-0.26046508, -0.28477222, 0.52321166, -0.80721378, 0.29428328, 0.29825771,0.80397947, -0.326007, -0.34943436, -0.57278871, -0.98233225, -0.84820036,-0.52714673, -0.57732037, 0.99911137, -0.84907632, 0.49275814, -0.89989096])
    #   Efficient Agent
    ,numpy.array([-0.0673488,   0.15093039, -0.30519962,  0.82178046,  0.39858328, -0.65576278,  0.79081779, -0.42864653,  0.83986874, -0.96502037, -0.08191183,  0.69564841,  0.58258724, -0.25880789,  0.13003199,  0.71662854,  0.34579705,  0.0854043, -0.5552963,   0.72586686,  0.1579585,  -0.51027632,  0.75733486,  0.56903343])
]

while True:
    for i in range(0,4):
        ENVS[i].render()
        observations[i] = ENVS[i].step(int(numpy.round(((numpy.matmul((numpy.matmul((2 / (1 + numpy.exp(-0.5 * observations[i]))) - 1, states[i][0:16].reshape(4, 4)) + states[i][16:20]), states[i][20:24].reshape(4, 1)))+1)/2)))[0]
