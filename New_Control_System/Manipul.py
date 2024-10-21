import numpy as np
Q1 = int(input())
Q2 = int(input())
Q1 += 1e-6
Q2 += 1e-6
A1 = np.array([np.cos(np.deg2rad(Q1)), -np.sin(np.deg2rad(Q1)), 0.055, np.sin(np.deg2rad(Q1)), np.cos(np.deg2rad(Q1)),
               0, 0, 0, 1]).reshape(3, 3)
A2 = np.array([np.cos(np.deg2rad(Q2)), -np.sin(np.deg2rad(Q2)), 0.1, np.sin(np.deg2rad(Q2)), np.cos(np.deg2rad(Q2)),
               0, 0, 0, 1]).reshape(3, 3)
A3 = np.array([1, 0, 0.12, 0, 1, 0, 0, 0, 1]).reshape(3, 3)
A = (A1.dot(A2)).dot(A3)
A3_inv = np.linalg.inv(A3)
A_Q1Q2 = A.dot(A3_inv)
Q1 = np.rad2deg(np.arccos(10 * (A_Q1Q2[0][2] - 0.055)))
Q2 = np.rad2deg(np.atan2(A_Q1Q2[1][0], A_Q1Q2[0][0])) - Q1
if Q2 < 0:
    Q2 += 360
Q1 = round(Q1)
Q2 = round(Q2)
print(A)