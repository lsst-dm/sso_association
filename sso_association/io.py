import numpy as np
import pandas as pd
import sqlite3

__all__ = ['addVisitId','createOIFConfig','diaSourcesFromSQL','getFOVRadius']




def addVisitId(df,ccdVisitName='ccdVisitId',colName='VisitId'):
    """"""
    df[colName]=(df[ccdVisitname].values/100).astype(int)
    return df


def createOIFConfig(populationModel='mpcorb.ssm',observerMPCID='W84',
                    surveyDB='HiTS_2015.db',spkt0=57070, nDays=10, 
                    spkstep=0.2, nbodyTF=True, 
                    firstVisit=1,nVisits=12,
                    fovType='instrument_circle.dat', rFovDeg=1.5, 
                    outputFile='input.config.tst'):

    
    """Create input config file for ObjectInField survey simulator.
    https://github.com/AsteroidSurveySimulator/objectsInField
    
    Parameters:
    -----------
    populationModel ... name of input file containing orbit data of asteroids in oorb format
    observerMPCID   ... name of minor planet center observer id for location of observatory e.g. 'W84'
    surveyDB        ... data base containing survey data such as epoch, RADEC, orientation on sky, seeing, ...
    spkt0           ... starting epoch for generating ephemeris of asteroids in populaitonModel [MJD], e.g. '57070' 
    nDays           ... number of days from start to create ephemeris for 
    spkstep         ... maximum step for ephemeris generation
    nbodyTF         ... N-Body propagation (True/False). If False propagation is 2body wrt the Sun
    firstVisit      ... ID of first visit in observation campaing to be considered
    nVisits         ... number of visits past the first visit to consider.
    fovType         ... Field of View type defined in input file, e.g. circle, camera -> 'instrument_circle.dat' 
    rFovDeg         ... radius of Field of View in degrees.
    outputFile      ... prints output to file with name outputFile
    
    Returns:
    --------
    Prints 
    
    """
    
    nl = "\n"
    with open(outputFile, 'w') as f:

        oifConfigFile=["[ASTEROID] \n"+ 
        "Population model    = "+str(populationModel)+nl+ 
        "SPK T0              = "+ str(spkt0) + nl +
        "nDays               = " + str(nDays) + nl + 
        "SPK step            = " + str(spkstep) + nl +
        "nbody               = " + str(nbodyTF) + nl + nl +
        "[SURVEY] \n" +
        "Survey database     = " + str(surveyDB) + nl +
        "Field1              = " + str(firstVisit) + nl +
        "nFields             = " + str(nVisits) + nl +
        "Telescope           = " + str(observerMPCID) + nl + nl +
        "[CAMERA] \n" +
        "Camera              = " +str(fovType) + nl +
        "Threshold           = " + str(rFovDeg) + nl
        ]
                    
        f.write(oifConfigFile[0])

def diaSourcesFromSQL(path,diaSourceTable='DiaSource', limit=100000):
    """"""
    
    db = sqlite3.connect(path)
    cursor=db.cursor()
    
    qery = "SELECT * FROM "+diaSourceTable+" LIMIT "+str(limit)
    
    dia=pd.read_sql_query(qery, db)
    cols=dia.columns
    
    addVisitId(dia)
    
    
    return dia

def getFOVRadius(df,obsTimeName='midPointTai', safetyFactor=1.05):
    """"""
    grp=df.groupby(obsTimeName)
    t0= np.fromiter(grp.groups.keys(),dtype='float')[0]
    
    dft0=df[df[obsTimeName]==t0]
    
    rRA=0.5*(diat0.ra.max()-diat0.ra.min())
    rDEC=0.5*(diat0.decl.max()-diat0.decl.min())
    rFOV=max(rRA,rDEC)*safetyFactor
    
    return rFOV
    
#def makePointingsDBfromCSV(path2csv,)    

