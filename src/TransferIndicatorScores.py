import os, shutil
import pandas as pd
src = './backtestdatabase/'
dst = './database/'
if os.listdir(dst) != []:
    for item in os.listdir(dst):
        shutil.rmtree(os.path.join(dst,item))
        
for item in os.listdir(src):
    s = os.path.join(src,item)
    d = os.path.join(dst,item)
    if os.path.isdir(s):
        shutil.copytree(s,d,symlinks=False, ignore=None)
    else:
        shutil.copy2(s,d)
for item in os.listdir(dst):
    df = pd.read_csv(dst + item + '/trades.csv', index_col= 0)
    df = df[0:0]
    df.to_csv(dst + item + '/trades.csv')
    df = pd.read_csv(dst + item + '/analysis.csv', index_col= 0)
    df = df[0:0]
    df.to_csv(dst + item + '/analysis.csv')
    df = pd.read_csv(dst + item + '/temp.csv', index_col= 0)
    df.to_csv(dst + item + '/query.csv')
    