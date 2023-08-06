#Libraries----------------------------------------------------------------------

"""
Dependencies and modules necessary for analytical functions to work
"""

#Cheminformatics
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Descriptors
from rdkit.Chem import PandasTools
from rdkit import DataStructs

#Data processing
import pandas as pd


#General
import collections




def molecule_check(data,*args):

    """
    #Function allows to visualise molecules of interest as well as returns a  data frame that containts information on the 
    selected list of molecules. It is recommended not to select more than 20 molecules at a time to draw the structures.

    #Input values: data frame with "CID" (compound ID) and "SMILES" (smiles column). Please note, the IDs for columns need to   #              match the examples.

    #Additional input: arguments for "CID", e.g. "2821293". If none is selected first 10 structures will be drawn. Names for
    #                   compounds have to be in a string format.

    #Output values: structure visualisation and a data frame that can be used for further visualisations.

    """
    #Data preparation----------------------------------------------------------------------

    data=pd.read_csv(data)

    #Error handling

    

    if "CID" not in data.columns:
        print("Your data frame does not containd 'CID' value")
        return data.head(5)
    if "SMILES" not in data.columns:
        print("Your data frame does not containd 'SMILES' value")
        return data.head(5)

    if len(data.SMILES)<5:
        print("You have less than five entries reconsider to add more data")
        return data
    
    data['CID'] = data['CID'].apply(str)
   
    values=args
    if len(values)>0:
        for val in values:
            if val not in list(data.CID):
                print("Missing value: %s" % val)
                return data.head(5)
    elif len(values)==0:
        if len(data.CID)>10:
            values=list(data.CID[1:10])
        else:
            values=list(data.CID)


    mol_list=[]
    for mol in data.SMILES:
        rdkit_mol=Chem.MolFromSmiles(mol)
        mol_list.append(rdkit_mol)

    #add column
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
        data.loc[index,"Rotatable_bond_count"]=Descriptors.NumRotatableBonds
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

    #add molecule images
    
    PandasTools.AddMoleculeColumnToFrame(data, smilesCol='SMILES', molCol="Molecule")

   
    index=list(data.CID.isin(values))
    
    data=data.loc[index,:]
 
    #draw molecules
    PandasTools.FrameToGridImage(data, column= 'Molecule', molsPerRow=4,subImgSize=(150,150),legendsCol= "CID")

    return(data)
