import getopt, sys
from biomart import BiomartServer
from io import StringIO
from os import listdir
from os import walk
import glob
import pandas as pd

server = BiomartServer('http://www.ensembl.org/biomart')
hsap = server.datasets['hsapiens_gene_ensembl']

def strand_fix(i):
    if i == 1:
        return('+')
    elif i == -1:
        return('-')
    else:
        return('invalid strand')

def get_bed_data(extGeneNames):
    response = hsap.search({
        'filters': {
            'external_gene_name' : extGeneNames
            },
        'attributes' : [
            "chromosome_name",
            "start_position",
            "end_position",
            "strand",
            "external_gene_name"
        ]
    }, header = 0)
    return(response)

def main():
    mypath = '/home/sebastian/Data/Tremethick/Breast/Xenografts/gene_sets/*.csv'
    myfiles = glob.glob(mypath)
    
    for i in myfiles:
        tab1 = pd.read_csv(i)
        n = i.split('.')[0]   
        for index, row in tab1.iterrows():
            extGeneNames = row['SymName'].split(',')
            resp = get_bed_data(extGeneNames)
            pd1 = pd.read_csv(StringIO(resp.text), sep = '\t', header = None)
            strand = pd1[3].transform(lambda x: strand_fix(x))
            pd1[3] = strand
            pd1[5] = '.'
            pd1[[0,1,2,3,5,4]]
            pd1.sort_values(by=0, inplace=True)
            pd1.to_csv(n + '/' + row[0] + '.bed', sep='\t', header=False, index=False)



