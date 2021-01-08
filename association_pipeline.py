# This file is part of the LSST Solar System Processing.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
The LSST SSO attribution pipeline
is part of the
LSST Solar System Processing
Implementation: Python 3.6, S. Eggl 20201206
"""


import sso_association as sso

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# path to Survey pointing SQL Database
surveyDBpath='HiTS_2015.db'
# Epoch for start of Survey [MJD]
surveyt0mjd=57070
# number of visits
numberOfVisits=10
# Survey FoV radius [deg]
surveyFoVrDeg=1.5

# path to observed DIA database
diaDBpath="association.db"
# limit entries?
Limit = 100000


#####################################
# PIPLELINE STARTS HERE
#####################################

# Download MPCORB file
sso.getmpcorb()

# Convert MPCORB file to ObjectInField format
#sso.mpcorb2oorb('MPCORB.DAT.gz', 'mpcorb.ssm', nOutFiles=1, compression='gzip')

# Define Survey Database Query for ObjectInField
surveyDbQuery="SELECT observationId,observationStartMJD,ra,dec,angle FROM ObsHistory order by observationStartMJD"

# Create configuration file for ObjectInField
sso.createOIFConfig(populationModel='mpcorb_test.ssm',observerMPCID='W84',
                    surveyDB=surveyDBpath,spkt0=surveyt0mjd, nDays=10, 
                    spkstep=0.5, nbodyTF='T', 
                    firstVisit=1,nVisits=numberOfVisits,
                    surveyDbQuery=surveyDbQuery,
                    fovType='instrument_circle.dat', rFovDeg=surveyFoVrDeg,
                    oifInputFile='oif.config',
                    oifOutputFile='sso_predictions',oifOutputFileFormat='csv')


# Run ObjectInField
os.system('oif oif.config -f')


# Gather DIA sources from association.db
associationdb = sqlite3.connect(diaDBpath)
cursor = associationdb.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if(Limit>0):
    associationsql = """SELECT * FROM DiaSource LIMIT """ + str(Limit)
else:
    associationsql = """SELECT * FROM DiaSource """ 
    
diadf=pd.read_sql_query(associationsql, associationdb)

ssodf=pd.read_csv('sso_predictions.csv',sep=',', header=0)


assoc=sso.associateDIA2SSO(diadf,ssodf,rOnSky=2,diara='ra',
                           diadec='decl',ssora='AstRA(deg)',
                           ssodec='AstDec(deg)',diaId='diaSourceId',
                           ssoId='ObjID',dId='dOnSky(arcsec)')


#############################################
# LIST ASSOCIATED OBJECTS BY NAME
#############################################

mpcorb=sso.read_mpcorb('MPCORB.DAT.gz',compression='gzip')
mpcorb.rename(columns={'objectId':'ObjID'},inplace=True)
ssoFound=ssodf.join(mpcorb, on="ObjID",rsuffix='_MPC')
outputCols=['readableName','H','a','e','V','AstRA(deg)',
            'AstDec(deg)','AstRARate(deg/day)','AstDecRate(deg/day)']
ssoFound[outputCols].to_csv('attributed_sso.csv',sep=',')


#############################################
# VISUALIZATION
#############################################

sso.plotSSOinFOV(ssoFound, diadf,xlim=[149,151.5],ylim=[1,3.5])
