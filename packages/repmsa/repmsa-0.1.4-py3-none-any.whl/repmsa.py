from Bio import AlignIO,SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
import pandas as pd
import numpy as np
from collections import Counter

class RankMatrix():
    """
    Calculate the representetive from a Multiple Sequence Alignment by creating an identity matrix
    and scoring them
    """

    def __init__(self,filename):
        self.__fname=filename
        self.dm=self.__create_dm()
        self.df=self.__convert_df()
        self.ranked=self.__rank()

    def __create_dm(self):  #creating an Percentage Identity Matrix (PIM) from a MSA file
        alignment = AlignIO.read(self.__fname,"fasta")
        calculator = DistanceCalculator('identity')
        dm = calculator.get_distance(alignment)
        return dm

    def __convert_df(self): #convert PIM into a DataFrame
        columns=self.dm.names
        self.__ids=self.dm.names
        dataf = pd.DataFrame(self.dm.matrix, columns=columns, index=self.__ids)
        np.fill_diagonal(dataf.values,'NaN')    #Fill the self sequences with NaN so it does not get considered
        return dataf

    def __rank(self):
        list_to_rank=list()
        for x in self.__ids:
            list_to_rank.extend(list(self.df.index[self.df[x] == self.df[x].min()]))   #get the minValue of a column and then get all the ids in the row those are equal that minValue
        ranked_list=Counter(list_to_rank).most_common()
        self.id_iter=iter(ranked_list)#store the ranked list in an iterator
        return ranked_list#,self.itemiter

    def topids(self):
        return next(self.id_iter,'End of List')

    def seq_by_id(self,id): #returns the sequence from MSA by a sequence ID (as a SeqIO object so the attributes of SeqIO still can be used)
        record_dict = SeqIO.index(self.__fname, "fasta")
        record_dict = record_dict[id].seq
        return record_dict
