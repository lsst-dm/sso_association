import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

__all__ = ['plotSSOinFOV']

def plotSSOinFOV(ssodf, diadf, xlim=[0,360], ylim=[-90,90], title='', xlabel='RA [deg]', 
                 ylabel='Dec [deg]', ssora='AstRA(deg)', 
                 ssodec='AstDec(deg)', diara='ra', diadec='decl',
                 ssoname='readableName',dpi=800):

    plt.figure(dpi=dpi)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    m = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
    c = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    i=0
    for index,row in ssodf.iterrows():
        plt.scatter(row[ssora],row[ssodec], s=5, label=row[ssoname],c=c[np.mod(i,7)], marker=m[np.mod(i,15)])
        i=i+1
        
    plt.scatter(diadf[diara],diadf[diadec], s=0.5, c='#888888',label='DIASources', marker = '.')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend(bbox_to_anchor=(1.1, 1.0),prop={'size': 2})
    #plt.show()
    plt.savefig('attribution.png')
    
# def plotSSOinFOV(ssodf, diadf, title='', xlabel='RA [deg]', 
#                  ylabel='Dec [deg]', ssora='AstRA(deg)', 
#                  ssodec='AstDec(deg)', diara='ra', diadec='decl',
#                  ssoname='readableName',dpi=800):

#     plt.figure(dpi=dpi)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)

#     m = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
#     c = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

#     i=0
#     for index,row in ssodf.iterrows():
#         plt.scatter(row[ssora],row[ssodec], s=5, label=row[ssoname],c=c[np.mod(i,7)], marker=m[np.mod(i,15)])
#         i=i+1
#     plt.scatter(diadf[diara],diadf[diadec], s=0.5, c='#888888',label='DIASources', marker = MarkerStyle('.', fillstyle = 'none'))

#     plt.legend(bbox_to_anchor=(1.1, 1.0),prop={'size': 2})
#     plt.show()
