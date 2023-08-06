#Libraries----------------------------------------------------------------------

"""
Dependencies and modules necessary for analytical functions to work
"""

#Cheminformatics
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import PandasTools
from rdkit import DataStructs

#Data processing
import pandas as pd

#General
import collections

#Data preparation functions----------------------------------------------------------------------

def data_prep(data,*args):

    """
    #Function provides a snapshot of the input data as well as returns a processed data file to include information on
    #chemical descriptors, atomic composition, chemicle structure features.

    #Input values: path to a csv file that containds compound ID 'CID' and smiles 'SMILES' columns. These columns
                    have to be named as described above.
                    Additional columns can be passed as arguments if, for example, the data file contains other columns of 
                    interest.
    #Output values: data frame with added chemical descriptors. The output could be integrated into dowstream 
                    analyses,  databases, or used to visualise the structures.

    """
    #Data preparation----------------------------------------------------------------------
    data=pd.read_csv(data)
    values=args

    #Error handling
    for val in values:
        if val not in data.columns:
            print("Missing value: Please check the name of columns you are trying to input")
            return data.head(5)
    

    if "CID" not in data.columns:
        print("Your data frame does not containd 'CID' value")
        return data.head(5)
    if "SMILES" not in data.columns:
        print("Your data frame does not containd 'SMILES' value")
        return data.head(5)

    if len(data.SMILES)<5:
        print("You have less than five entries reconsider to add more data")
        return data


    #Prepare and molecular descriptors
    if len(args)>0:
            
        data=data[["CID","SMILES",*args]] #unpack arguments
        mol_list=[]
    else:
        data=data[["CID","SMILES"]]
        mol_list=[]

    for mol in data.SMILES:
        rdkit_mol=Chem.MolFromSmiles(mol)
        mol_list.append(rdkit_mol)

    #add a column for Rdkit molecular structures
    data["Rdkit_mol"]=mol_list

    #Add descriptor columns
    data["Atom_number"]=""
    data["MW"]=""
    data["TSPA"]=""
    data["HBD_count"]=""
    data["HBA_count"]=""
    data["Rotatable_bond_count"]=""
    data["Aromatic_atom_count"]=""
    data["S_count"]=""
    data["F_count"]=""
    data["N_count"]=""
    data["P_count"]=""
    data["MolLogP"]=""
    data["Ring_number"]=""
    data["Number_heterocycles"]=""
    data["Heavy_atom_number"]=""
    data["AP"]=""

    #calculate features
    for index in range(0, data.shape[0]):
        
        mol=data.loc[index,"Rdkit_mol"]
        mol_smiles=collections.Counter(data.loc[index,"SMILES"])
        data.loc[index,"Atom_number"]=mol.GetNumAtoms()
        data.loc[index,"MW"]=Descriptors.MolWt(mol)
        data.loc[index,"MolLogP"]=Descriptors.MolLogP(mol)

        data.loc[index,"TSPA"]=Chem.rdMolDescriptors.CalcTPSA(mol)
        data.loc[index,"Heavy_atom_number"]=Descriptors.HeavyAtomCount(mol)
        data.loc[index,"HBD_count"]=Chem.rdMolDescriptors.CalcNumHBD(mol)
        data.loc[index,"HBA_count"]=Chem.rdMolDescriptors.CalcNumHBA(mol)
        data.loc[index,"Rotatable_bond_count"]=Descriptors.NumRotatableBonds(mol)
        data.loc[index,"Number_heterocycles"]=Chem.Lipinski.NumAromaticRings(mol)
        data.loc[index,"Aromatic_atom_count"]=sum([ mol.GetAtomWithIdx(i).GetIsAromatic() for i in range(mol.GetNumAtoms())])
    
        
        data.loc[index,"Ring_number"]=Chem.rdMolDescriptors.CalcNumRings(mol)

        if("S" in mol_smiles.keys()):
            data.loc[index,"S_count"]= mol_smiles["S"]
        else:
            data.loc[index,"S_count"]= 0

        if("N" in mol_smiles.keys()):
            data.loc[index,"N_count"]= mol_smiles["N"]
        else:
            data.loc[index,"N_count"]= 0
        if("F" in mol_smiles.keys()):
            data.loc[index,"F_count"]= mol_smiles["F"]
        else:
            data.loc[index,"F_count"]= 0
        if("P" in mol_smiles.keys()):
            data.loc[index,"P_count"]= mol_smiles["P"]
        else:
            data.loc[index,"P_count"]= 0

        if(data.loc[index,"Heavy_atom_number"]>0):
            data.loc[index,"AP"]=data.loc[index,"Aromatic_atom_count"]/data.loc[index,"Heavy_atom_number"]
        else:
            data.loc[index,"AP"]=0


    return(data)