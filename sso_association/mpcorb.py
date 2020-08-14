import pandas as pd
from astropy.time import Time

__all__ = ['read_mpcorb','mpcorb2oorb','unpack_mpc_date', 'convertMPCEpoch', skiprows=43]


def read_mpcorb(path2mpcorb):
    """Read IAU Minor Planet Center Orbit format (2020) from txt file.
    
    Parameters:
    -----------
    path2mpcorb... path to MPCORB.DAT file
    
    Returns:
    --------
    mpcorb ... pandas DataFrame containing MPCORB data
    
    """
    mpcorb_col_numbers=[(0,7),(8,13),(14,19),(20,25),(26,35),(37,46),
                (48,57),(59,68),(70,79),(80,91),(92,103),(106,116),
                (117,122),(123,126),(127,136),(137,141),
                (142, 145),(146,149),(150,160),(166,194),(194,202)]
    col_names=['ObjID','H','G','epoch','M','argperi','node','i',
               'e','n','a','reference',
               'N_Obs', 'N_Opp', 'yr_1st&last_Obs', 'r.m.s',
               'coarsePerts', 'precisePerts', 'computer',
               'readableName', 'lastObs']
    dtp=[str,float,float,str,float,float,float,float,float,float,float]
    dtypes=dict(zip(col_names,dtp))

    mpcorb=pd.read_fwf(path2mpcorb,skiprows=skiprows,colspecs=mpcorb_col_numbers,
                       names=col_names,dytpe=dtypes,index_col=False)
    
    mpcorb.dropna(subset=['a', 'e','i','node','argperi','M','epoch', 'r.m.s'],inplace=True)
    return mpcorb

def mpcorb2oorb(mpcorb, nOutFiles=0, pathOut='oorb-dat'):
    """Convert IAU Minor Planet Center Orbit format (2020) to openorb format.
    
    Parameters:
    -----------
    mpcorb    ... pandas DataFrame containing MPCORB data
    nOutFiles ... number of files for output (0 will return a pandas Dataframe in oorb format)
    pathOut   ... path and filename for output files
    
    Returns:
    --------
    nOutFiles == 0:
        mpcorb ... orbits in oorb format
    nOutFiles == 1:
        one file containing all orbits in oorb format
    nOutFiles > 1
        nOutFiles files containing chunks of orbits in oorb format
    """
    
    mpcorb['q']=mpcorb['a'].values*(1.-mpcorb['e']).values
    mpcorb['FORMAT']='COM'
    strs=mpcorb['epoch'].values.astype(str)
    mpcorb2=mpcorb.apply(convertMPCEpoch,axis=1)
    mpcorb2['t_p']=mpcorb2['epoch'].values-np.divide(mpcorb2['M'].values,mpcorb2['n'].values)
    mpcorb2['P']=360/mpcorb2['n'].values
    mpcorb2.rename(columns={'epoch':'t_0'},inplace=True)
    mpcorb=mpcorb2[['ObjID','FORMAT', 'q', 'e', 'i','node', 'argperi', 't_p', 'H', 't_0']]
    
    if (nOutFiles == 0):
        return mpcorb
    elif (nOutFiles == 1):
        mpcorb.to_csv(pathOut, sep=' ', index=False)
        return
    else:        
        mpcorbArray=np.array_split(mpcorb,nOutFiles)
        for i in range(len(mpcorbArray)):
            mpcorbArray[i].to_csv(pathOut+'_'+str(i), sep=' ', index=False)
        return
            
            
def unpack_mpc_date(packed_date):
    """ Unpack IAU Minor Planet Center dates.
    See https://minorplanetcenter.net/iau/info/PackedDates.html
    for MPC documentation on packed dates.
    Examples:
        1998 Jan. 18.73     = J981I73
        2001 Oct. 22.138303 = K01AM138303
        
    Parameters:
    -----------
    packed_date ... string containing packed date e.g. J981I73
    
    
    Returns:
    --------
    t.mjd   ... astropy time object in MJD format
    """
    packed_date = str(packed_date)

    year=1000
    #if(packed_date[0]=='I' or packed_date[0]=='J' or packed_date[0]=='K'):
    if(packed_date[0]=='I'):
        year=1800
    elif(packed_date[0]=='J'):
        year=1900
    elif(packed_date[0]=='K'):    
        year=2000
    
    year += int(packed_date[1:3])

    # Month is encoded in third column.
    month = _mpc_lookup(packed_date[3], packed_date)
    day = _mpc_lookup(packed_date[4], packed_date)
    if len(packed_date) > 5:
        fractional_day = packed_date[5:]
        
#     return [year, month, day]    
    isot_string = '%d-%02d-%02d' % (year, month, day)
    t = Time(isot_string, format='isot', scale='tt')
    return t.mjd


def _mpc_lookup(x,packed_date):
    """ Convert the single character dates into integers.
    """
   
    try:
        x = int(x)
    except ValueError:
        x = ord(x) - 55
    if x < 0 or x > 31:
        print(packed_date)
        raise ValueError
    return x

def convertMPCEpoch(df, epochName='epoch'):
    """Convert packed MPC epoch for orbits to MJD epoch.
    
    Parameters:
    -----------
    df        ... pandas DataFrame containing MPC packed epoch
    epochName ... column name for epoch
    
    Returns:
    --------
    df ... pandas DataFrame with substituted epoch.
    """
    try:
        df[epochName] = unpack_mpc_date(df[epochName])
    except:
        print(df['epoch'])
    return df
