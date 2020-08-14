import numpy as np
import pandas as pd
import sqlite3


def addVisitId(df,ccdVisitName='ccdVisitId',colName='VisitId'):
    """"""
    df[colName]=(df[ccdVisitname].values/100).astype(int)
    return df


def diaSourcesFromSQL(path,diaSourceTable='DiaSource', limit=100000):
    """"""
    
    db = sqlite3.connect(path)
    cursor=db.cursor()
    
    qery = "SELECT * FROM "+diaSourceTable+" LIMIT "+str(limit)
    
    dia=pd.read_sql_query(qery, db)
    cols=dia.columns
    
    addVisitId(dia)
    
    
    return dia

def getFOVRadius(df,obsTimeName='midPointTai', safetyFactor=1.05 )
    """"""
    grp=df.groupby(obsTimeName)
    t0= np.fromiter(grp.groups.keys(),dtype='float')[0]
    
    dft0=df[df[obsTimeName]==t0]
    
    rRA=0.5*(diat0.ra.max()-diat0.ra.min())
    rDEC=0.5*(diat0.decl.max()-diat0.decl.min())
    rFOV=max(rRA,rDEC)*safetyFactor
    
    return rFOV
    
#def makePointingsDBfromCSV(path2csv,)    

