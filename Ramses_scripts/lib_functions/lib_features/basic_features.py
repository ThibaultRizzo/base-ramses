
import pandas as pd
import numpy as np
##################################################################
def rolling_gen(df, w):
    for i in range(df.shape[0] - w + 1):
        yield pd.DataFrame(df.values[i:i+w, :], df.index[i:i+w], df.columns)
######################################################
def Point_Ref_Simple(S, l):
    # calcule les deux séries de points de référence max et min d'une série
    # pour une moyenne mobile simple de longueur l
    df = pd.DataFrame(S)
    temp = pd.DataFrame(index=df.index, data=np.zeros((len(df), 4)))
    temp.iloc[:l, 0] = df.iloc[:l, 0]
    temp.iloc[:l, 1] = df.iloc[:l, 0]
    temp.iloc[:l, 2] = df.iloc[:l, 0]
    temp.iloc[:l, 3] = df.iloc[:l, 0]

    sma = df.rolling(window=l, center=False).mean()
    sg = (df - sma).apply(np.sign)

    i = l
    sg[:i] = sg.iloc[i][0]
    temp.iloc[:i, 1] = np.min(df.iloc[:i, 0])
    temp.iloc[:i, 2] = np.max(df.iloc[:i, 0])

    if sg.iloc[i, 0] == 1:
        temp.iloc[:i, 0] = np.min(df.iloc[:i, 0])
    else:
        temp.iloc[:i, 0] = np.max(df.iloc[:i, 0])

    for i in range(l, len(S)):

        if sg.iloc[i, 0] > sg.iloc[i - 1, 0]:
            temp.iloc[i, 0] = df.iloc[i, 0]
            temp.iloc[i, 1] = temp.iloc[i - 1, 0]
            temp.iloc[i, 2] = temp.iloc[i - 1, 2]
            temp.iloc[i, 3] = temp.iloc[i, 1]

        elif sg.iloc[i, 0] < sg.iloc[i - 1, 0]:
            temp.iloc[i, 0] = df.iloc[i, 0]
            temp.iloc[i, 1] = temp.iloc[i - 1, 1]
            temp.iloc[i, 2] = temp.iloc[i - 1, 0]
            temp.iloc[i, 3] = temp.iloc[i, 2]

        elif sg.iloc[i, 0] == 1:
            temp.iloc[i, 0] = np.max([temp.iloc[i - 1, 0], df.iloc[i, 0]])
            temp.iloc[i, 1] = temp.iloc[i - 1, 1]
            temp.iloc[i, 2] = temp.iloc[i - 1, 2]
            temp.iloc[i, 3] = temp.iloc[i, 1]

        else:
            temp.iloc[i, 0] = np.min([temp.iloc[i - 1, 0], df.iloc[i, 0]])
            temp.iloc[i, 1] = temp.iloc[i - 1, 1]
            temp.iloc[i, 2] = temp.iloc[i - 1, 2]
            temp.iloc[i, 3] = temp.iloc[i, 2]

    return temp.iloc[:, 1:3]
######################################################
def regime_simple_new(S, l):
    # calcule le regime d'investissement TF d'une série
    # autour d'une moyenne mobile simple
    S = pd.DataFrame(S)
    B = Point_Ref_Simple(S, l)
    pos = pd.DataFrame(np.zeros((len(S), 1)))
    pos.iloc[0, 0] = 0
    S_Loss = S.copy()
    S_Loss.columns = ['S_Loss']

    for i in range(1, len(S)):
        if S.iloc[i, 0] < B.iloc[i, 0]:
            pos.iloc[i, 0] = -1
            S_Loss.iloc[i, 0] = B.iloc[i, 1]

        elif S.iloc[i, 0] > B.iloc[i, 1]:
            pos.iloc[i, 0] = 1
            S_Loss.iloc[i, 0] = B.iloc[i, 0]

        else:
            pos.iloc[i, 0] = pos.iloc[i - 1, 0]
            S_Loss.iloc[i, 0] = S.iloc[i - 1, 0]

    pos.set_index(S.index, inplace=True)
    pos.columns = ['pos']
    sma = S.rolling(window=l, center=False).mean()
    sma.columns = ['sma']
    dist = S.div(S_Loss.values, axis=1) - 1
    dist.columns = ['dist2SLoss']
    dist[pos == 0] = 0
    vout = pd.concat([S, sma, S_Loss, pos, dist], axis=1)

    return vout
######################################################
def max_DDown_abs(S):
# calcule le max drawdown absolu d'une série S sur une longueur l
    S = pd.DataFrame(S)
    DD = (S.cummax() - S)
    return DD.max()[0]
######################################################
def max_DUp_abs(S):
# calcule le max drawup absolu d'une série S sur une longueur l
    S = pd.DataFrame(S)
    DU = (S - S.cummin())
    return DU.max()[0]
######################################################
def corde_path(S):
    # calcule le ratio entre la corde et le chemin total d'un df de prix
    A = np.array(S.copy())

    corde = A[-1] / A[0] - 1
    path = np.sum(np.array([np.abs(A[i] / A[i - 1] - 1) for i in range(1, len(A))]), axis=0)
    path[path == 0] = np.nan

    temp = pd.Series(corde / path, name=S.index[-1])
    return temp
##########################################################
def F_ts_corde_path(S,l1):
# donne le ratio corde/path sur l1 jours d'une série de prix
    temp0= S* np.nan
    z = rolling_gen(S,l1)
    temp = pd.concat([corde_path(item) for item in z],axis=1)
    temp0.loc[temp.T.index] = temp.T
    return temp0.fillna(0)
###########################################################