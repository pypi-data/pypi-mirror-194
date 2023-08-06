import numpy as np
from collections import Counter

'''
z_axis = -np.array([0, 0, 1], dtype=np.float64)
orientations = [[z_axis, 0.0]]
print(orientations)

objects = dict()
part = 0
objects[part] = {"mesh": list()}
objects[part]["mesh"].append([1, 2, 3])
objects[part]["name"] = "part1"
part = part+1
objects[part] = {"mesh": list()}
for k, v in objects.items():
    print(k)
    print(v["mesh"])
    print("----------")
print(objects.items())

content = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
content2 = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
num = int(len(content) / 3)
mesh = np.array(content, dtype=np.float64)
mesh.reshape((num, 3, 3))
print(mesh)
print(mesh.shape[0])
print(mesh.shape[1])

test1 = [[[1, 2, 3],
          [2, 3, 4],
          [3, 4, 5],
          [4, 5, 6],
          [5, 6, 7],
          [6, 7, 8]],
        [[4, 5, 6],
         [5, 6, 7],
         [6, 7, 8],
         [7, 8, 9],
         [8, 9, 10],
         [9, 10, 11]]]

test2 = [[[1, 2, 3]],
        [[4, 5, 6]]]

test = np.hstack((test2, test1))
print(test)

print('----------')
print(test[:, 0, :])
print('----------')
test1 = np.array(test1, dtype=np.float64)
test12 = test1[:, 0, :]
print(test12)
notali = np.sum(test12 * test12, axis=1) < 15
print(notali)
mesh_not = test1[np.logical_not(notali)]
print(mesh_not)
print('----------')
orient = Counter()
for index in range(len(test1)):
    print(test1[index, 0])
    print(tuple(test1[index, 0] + 0.0))
    print(orient[tuple(test1[index, 0] + 0.0)])
    orient[tuple(test1[index, 0] + 0.0)] += test1[index, 5, 0]
print('--------------')
print(orient[tuple(test1[0, 0] + 0.0)])
print('--------------')
print(orient[tuple(test1[1, 0] + 0.0)])
print(orient.most_common(1))
print('--------------')
z_axis = -np.array([0, 0, 1], dtype=np.float64)
orientations = [[z_axis, 0.0]]
print(orientations)
results = np.empty((len(orientations), 7), dtype=np.float64)
for idx, item in enumerate(orientations):
    orientation = -1 * np.array(item[0], dtype=np.float64)

    results[idx, 0] = orientation[0]
    results[idx, 1] = orientation[1]
    results[idx, 2] = orientation[2]

    print(results[idx, 0])
    print(results[idx, 1])
    print(results[idx, 2])
'''
tot_normalized_orientations = [[1, 2, 3],
                               [4, 5, 6],
                               [7, 8, 9],
                               [1, 2, 3],
                               [4, 5, 6],
                               [3, 6, 9],
                               [1, 2, 3],
                               [4, 5, 6],
                               [4, 2, 6],
                               [10, 5, 7],
                               [1, 2, 3]]
tot_normalized_orientations = np.array(tot_normalized_orientations, dtype=np.float64)
# orientations = [[1], [2], [3], [4], [5], [6], [7], [8]]
orientations = np.inner(np.array([1, 1e3, 1e6]), tot_normalized_orientations)
print(orientations)
print('--------------------')
orient = Counter(orientations)
top_n = orient.most_common(5)
print(top_n)
print('--------------------')
top_n = list(filter(lambda x: x[1] > 2, top_n))
print(top_n)
print('--------------------')
candidate = list()
for sum_side, count in top_n:
    # tot_normalized_orientations[orientations == sum_side]返回满足条件的面的法向量,用unique将重复法向量去掉,
    # 留下一个,并且将这一个出现的次数返回
    # 即face_unique和face_count
    # np.unique 去除重复元素,并且按照元素由小到大返回,还要返回每个元素出现的次数
    print(sum_side)
    print('--------------------')
    face_unique, face_count = np.unique(tot_normalized_orientations[orientations == sum_side], axis=0,
                                        return_counts=True)
    candidate += [[list(face_unique[i]), count] for i, count in enumerate(face_count)]
    print('candidate')
    print(candidate)
    print('--------------------')
print(candidate)