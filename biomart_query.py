import getopt, sys
from biomart import BiomartServer
from io import StringIO


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
    tab1 = pd.read_csv('Z:\scratch\mcf10a-xenografts\gene_sets\GeneSetTest_HALLMARK_Hs_LZtumor_vs_WT4.csv')
    extGeneNames = tab1.iloc[0].SymName.split(',')
    resp = get_bed_data(extGeneNames)
    pd1 = pd.read_csv(StringIO(resp.text), sep = '\t', header = None)
    strand = pd1[3].transform(lambda x: strand_fix(x))
    pd1[3] = strand
    pd1[5] = '.'
    pd1[[0,1,2,3,5,4]]
    pd1.sort_values(by=0, inplace=True)
    pd1.to_csv('Z:\scratch\mcf10a-xenografts\gene_sets\GeneSetTest_HALLMARK_Hs_LZtumor_vs_WT4.bed', sep='\t', header=False, index=False)

