smiles=""
pn.extension()
from numpy.lib.shape_base import split
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd
from IPython.display import Image
from rdkit.Chem.Draw import DrawingOptions
DrawingOptions.atomLabelFontSize = 55
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
import panel as pn
from oauth2client.service_account import ServiceAccountCredentials

from rdkit import Chem
import pubchempy as pcp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ipywidgets import Button
from IPython.display import display
# Import required modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from ipywidgets import Button
import requests

from rdkit import Chem
import pubchempy as pcp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ipywidgets import Button
from IPython.display import display
# Import required modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from ipywidgets import Button
from ipywidgets import Button, Layout

from rdkit import Chem
from rdkit.Chem import AllChem
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit import*


# Open the Google Sheet file and select the first worksheet
import panel as pn

def help():
  print("This is a smiple python package for chemical database")
  print("\n")
  print("\n")
  print("you should see this video to know how you use this package")

  print("\n")
  print("\n")

help()

import requests
# Define the function to be called when the button is clicked
def create():
  scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
  creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)# upload file in dir
  client = gspread.authorize(creds)
  sheet = client.open("local chemical databse").sheet1#name of google sheet file in my google sheet

  def on_button_click(b):
          print("We are working to save your chemicals in your database in your Google Sheet")
          # Retrieve the values of the input widgets
          name = name_input.value
          lab = lab_input.value
          email = email_input.value
          phone = phone_input.value
          shelf = shelf_input.value
          expired = str(expired_input.value)
          #status = status_input.value
          mass = mass_input.value
          volume = volume_input.value
          density = density_input.value
          pressure= pressure_input.value
          concentration = concentration_input.value

          # Create a dictionary with the retrieved information
          chemical = {
              'Name': name,
              'Lab': lab,
              'Email': email,
              'Phone': phone,
              'Shelf': shelf,
              'Expired': expired,
              
              'Mass': mass,
              'Volume': volume,
              'Density': density,
              'Concentration': concentration,
              'Pressure': pressure
          }
          #sheet.append_row([          chemical['Name'],          chemical['Lab'],          chemical['Email'],          chemical['Phone'],          chemical['Shelf'],          chemical['Expired'],
          #  chemical['Mass'],          chemical['Volume'],          chemical['Density'],          chemical['Concentration'],          chemical['Pressure']    ])        # Add the chemical to a list of chemicals
          #chemicals.append(chemical)
          
          # Print the list of chemicals
          #print(chemicals)

        # Add the input widgets and button to a panel
          # Create a list to store the submitted chemicals
          chemicals = []

          # Add the submit function to the button's on_click event

  ###################################################################################
        # Display the input panel
          smiles = editor.value
          print(smiles)
          mol = Chem.MolFromSmiles(smiles)
          smi=smiles

      ###############IUPACName
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//IUPACName/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          IUPACName= (res.text).strip("\n")


      ###############MolecularFormula
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property/MolecularFormula/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          MolecularFormula= str((res.text).strip("\n"))
          print(MolecularFormula)


      ###############cids
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/cids/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          cids= (res.text).strip("\n")


      ###############Number_of_Atoms
          Number_of_Atoms = mol.GetNumAtoms()


      #################HBondDonorCount
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//HBondDonorCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          HBondDonorCount= (res.text).strip("\n")


      ##############hydrogen_bond_acceptors
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//HBondAcceptorCount/txt")
          hydrogen_bond_acceptors = (res.text).strip("\n")


      ###############sids
          res=str('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/sids/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          sids= str(res)


      ###############aids
          res=str('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/aids/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          aids= str(res)


      ###############aids
          res=str('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/aids/TXT?aids_type=active")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          active_aids= str(res)


      ###########TPSA
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//TPSA/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          TPSA= (res.text).strip("\n")



      ##########
          m2=Chem.AddHs(mol)
          atom_number_with_hydrogen=m2.GetNumAtoms()


      ########log p
          LogP = Descriptors.MolLogP(mol)



      #########Number Radical Electrons
          Number_Radical_Electrons=str(Descriptors.NumRadicalElectrons(Chem.MolFromSmiles(str(smiles))))
          Number_Valence_Electrons=Descriptors.NumValenceElectrons(Chem.MolFromSmiles(str(smiles)))



      ###########tetrahedral

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//AtomStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          tetrahedral = (res.text).strip("\n")


      ###########
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//DefinedAtomStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          Number_of_atoms_with_defined_tetrahedral_sp3_stereo= (res.text).strip("\n")


      ########## UndefinedAtomStereoCount
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//UndefinedAtomStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          Number_of_atoms_with_undefined_tetrahedral_sp3_stereo= (res.text).strip("\n")


      ###########
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smiles)+"/property//BondStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          Total_number__bonds_planar_sp2_stereo_E_Z_configuration= (res.text).strip("\n")

      ###########



          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//Charge/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          total_charge_molecule= (res.text).strip("\n")

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//DefinedBondStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          Number_atoms_with_defined_planar_sp2_stereo= (res.text).strip("\n")

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//unDefinedBondStereoCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          Number_atoms_with_undefined_planar_sp2_stereo= (res.text).strip("\n")
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//CovalentUnitCount/txt")
          #https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CC(=O)C/property/IUPACName/txt
          CovalentUnitCount= (res.text).strip("\n")


      ####################

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//XStericQuadrupole3D/txt")
          The_x_component_of_the_quadrupole_moment_Qx_of_the_first_diverse_conformer_default_conformer_for_compound= (res.text).strip("\n")

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//yStericQuadrupole3D/txt")
          The_y_component_of_the_quadrupole_moment_Qy_of_the_first_diverse_conformer_default_conformer_for_compound= (res.text).strip("\n")

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//zStericQuadrupole3D/txt")
          The_z_component_of_the_quadrupole_moment_Qz_of_the_first_diverse_conformer_default_conformer_for_compound= (res.text).strip("\n")
          

          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/cids/txt?cids_type=component")
          Retriev_mixtures_that_contain_given_molecule_component= (res.text).strip("\n")


          # Save the data to the Google Sheet
          res=requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/'+str(smi)+"/property//Volume3D/txt")
          Analytic_volume_of_the_first_diverse_conformer_default_conformer_for_acompound= (res.text).strip("\n")
        


          # Define the list to insert
          new_values =  ["name","lab","email","phone","shelf","expired","mass","volume",
                        "density","pressure","concentration","Cids","smiles","IUPAC Name","Molecular Formula","LogP","Number of Atoms",
                        "atom number_with hydrogen","HBondDonorCount","hydrogen bond acceptors" ,"TPSA", 
                        "Number_Valence_Electrons","Number Radical Electrons",
                        "Total number of atoms with tetrahedral (sp3) stereo [e.g., (R)- or (S)-configuration","Number of atoms with defined tetrahedral (sp3) stereo.",
                        "Number of atoms with undefined tetrahedral sp3 stereo","Total number bonds planar sp2 stereo E Z configuration", "The total (or net) charge of a molecule,umber of atoms with defined planar (sp2) stereo","Number of atoms with undefined planar (sp2) stereo","Number of atoms with undefined planar (sp2) stereo","Number of atoms with undefined planar (sp2) stereo","CovalentUnitCount",
                        "The x component of the quadrupole moment (Qx) of the first diverse conformer (default conformer) for a compound.",
                        "The y component of the quadrupole moment (Qy) of the first diverse conformer (default conformer) for a compound.",
                        "The z component of the quadrupole moment (Qz) of the first diverse conformer (default conformer) for a compound."
                          "Analytic volume of the first diverse conformer (default conformer) for acompound.","Sids","Aids","Retrieve mixtures that contain a given molecule as a component"
                          ,"active aids"]


          # Replace the first row with the new values
          sheet.update('1:1', [new_values])
          index = 1
          while sheet.cell(index, 1).value != "":
              index += 1

          # insert the list into the first empty row
          row = index
          col = 1
          values = [name,lab,email,phone,shelf,expired,mass,volume,density,pressure,concentration,cids,smiles,IUPACName,MolecularFormula,LogP,Number_of_Atoms,atom_number_with_hydrogen,HBondDonorCount,hydrogen_bond_acceptors,TPSA ,Number_Valence_Electrons,
                    Number_Radical_Electrons,tetrahedral,Number_of_atoms_with_defined_tetrahedral_sp3_stereo,Number_of_atoms_with_undefined_tetrahedral_sp3_stereo,Total_number__bonds_planar_sp2_stereo_E_Z_configuration,
                    total_charge_molecule,Number_atoms_with_defined_planar_sp2_stereo,Number_atoms_with_undefined_planar_sp2_stereo,CovalentUnitCount,    
                    The_x_component_of_the_quadrupole_moment_Qx_of_the_first_diverse_conformer_default_conformer_for_compound,
                    The_y_component_of_the_quadrupole_moment_Qy_of_the_first_diverse_conformer_default_conformer_for_compound,
                    The_z_component_of_the_quadrupole_moment_Qz_of_the_first_diverse_conformer_default_conformer_for_compound,Analytic_volume_of_the_first_diverse_conformer_default_conformer_for_acompound,
                    sids,aids,Analytic_volume_of_the_first_diverse_conformer_default_conformer_for_acompound,active_aids]
          sheet.append_row(values)
          print("done")







      # Create the JSME editor and button widgets
      #editor = JSMEEditor(height=500, width=500, format='smiles')

        # Attach the click event handler to the button

      # Display the widgets
  smiles_list=[]
      # Define a function to add the SMILES string to the list
  def add_smiles_string(sender):

        smiles = editor.value
        smiles_list.append(smiles)
        print("we saved your chemical in your list research so when you finish press search button to see you query chemical in your database",smiles)

    # Define a function to search for the SMILES strings in the Google Sheet
  def search_in_sheet(sender):
      print("Here you are going to see your search chemicals in your database")

      smiles = editor.value
      smiles_list.append(smiles)

      # define an empty list to store the matching rows
      matching_rows = []

      # loop through the search queries and find the matching rows
      for query in smiles_list:
          found_rows = sheet.findall(query)
          if len(found_rows) > 0:
              for row in found_rows:
                  matching_rows.append(sheet.row_values(row.row))
      # add the first row of the sheet to the matching rows
      first_row = sheet.row_values(1)
      matching_rows.insert(0, first_row)

      # create a pandas dataframe from the matching rows
      df = pd.DataFrame(matching_rows)

      # save the dataframe to an Excel file
      excel_file = 'matching_rows.xlsx'
      df.to_excel(excel_file, index=False)
      sentence = 'If you dont see your chemical query, this meams there is no chemical information in your chemical database abouth this query.'
      print(sentence)
      print("Matching rows saved to", excel_file)
      display(df)
    # Create the input boxes
    ###############################################
    # Define the tanimoto_calc function
  def tanimoto_calc(smi1, smi2):
        mol1 = Chem.MolFromSmiles(smi1)
        mol2 = Chem.MolFromSmiles(smi2)
        fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 3, nBits=2048)
        fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 3, nBits=2048)
        s = round(DataStructs.TanimotoSimilarity(fp1,fp2),3)
        return s

  matching_rows = []

  def smilar_click(b):
      print("Here you are going to see smilar chemicals in your database")
      smiles = editor.value
      first_row = sheet.row_values(1)
      matching_rows.insert(0, first_row)
      smiles_column = sheet.col_values(13)[1:]
          # create a pandas dataframe from the matching rows
      for i in range(len(smiles_column)):
        for j in range(i+1, len(smiles_column)):
              similarity = tanimoto_calc(smiles, smiles_column[j])
              xx=(f"The Tanimoto similarity between compounds {i+1} and {j+1} is {similarity}.")
              print(xx) # add the first row of the sheet to the matching rows
              if float(similarity) >= float(0.5):
                row_values = sheet.row_values(j)
                print("searching moleculr is")
                mol = Chem.MolFromSmiles(smiles_column[j])
                display(mol)
                print("smilar compound in your database is")
                mol = Chem.MolFromSmiles(smiles_column[j])
                display(mol)
                found_rows = sheet.row_values(j)
                matching_rows.append(sheet.row_values(j))
      dff = pd.DataFrame(matching_rows)

                # save the dataframe to an Excel file
      excel_file = 'smilar_chemicals.xlsx'
      dff.to_excel(excel_file, index=False)
      sentence = 'If you dont see your chemical query, this meams there is no chemical information in your chemical database abouth this query.'
      print(sentence)
      print("Matching rows saved to", excel_file)
      #display(dff)
    # Get the SMILES strings from the column
  editor = JSMEEditor(height=500, width=500, format='smiles')
      # Compare pairs of compounds and print the similarity score
  Smilarity_button = Button(description='Find smilar chemical in your chemical database ',
                layout=Layout(width='800px', height='50px', margin='20px'))
  Smilarity_button.style.font_weight = 'bold'
  Smilarity_button.on_click(smilar_click)
  ##############################################


      # Create input widgets for user to input their information
  name_input = pn.widgets.TextInput(name='Name:')
  lab_input = pn.widgets.TextInput(name='Lab:')
  email_input = pn.widgets.TextInput(name='Email:')
  phone_input = pn.widgets.TextInput(name='Phone:')
  shelf_input = pn.widgets.TextInput(name='Shelf:')
  expired_input = pn.widgets.DatePicker(name='Expired:')
      #status_input = pn.widgets.Select(name='Status:', options=['Gas', 'Solid', 'Liquid'])
  pressure_input = pn.widgets.TextInput(name='Pressure:')
  volume_input = pn.widgets.TextInput(name='Volume:')
  mass_input = pn.widgets.TextInput(name='mass:')

  density_input = pn.widgets.TextInput(name='Density:')
  concentration_input = pn.widgets.TextInput(name='Concentration:')



      # Create a button to submit the form
  submit_button = pn.widgets.Button(name='Submit', width=300, height=50, button_type='primary', background='#FFA500')
        # Define the inputs for the first row
  row1_inputs = pn.Row(name_input, lab_input, email_input, phone_input, shelf_input)

          # Define the inputs for the second row
  row2_inputs = pn.Row(expired_input, mass_input, volume_input, density_input, concentration_input )
  row3_inputs = pn.Row( pressure_input)

          # Combine the two rows into a column
  inputs2 = pn.Column(row1_inputs, row2_inputs,row3_inputs)
  display(inputs2)

  add_button = Button(description='Add your chemical to list search', layout=Layout(width='800px', height='100px', margin='20px'))
  add_button.style.font_weight = 'bold'
  add_button.on_click(add_smiles_string)


  search_button = Button(description='Search for your chemical in your chemical database', layout=Layout(width='800px', height='100px', margin='20px'))
  search_button.style.font_weight = 'bold'
  search_button.on_click(search_in_sheet)



  buttton = Button(description='Save to your chemical database in Google Sheet',    layout=Layout(width='800px', height='100px', margin='20px'))
  buttton.style.font_weight = 'bold'
  buttton.on_click(on_button_click)

  display(editor, buttton, Smilarity_button, add_button, search_button)

      # Display the widgets
  return display(editor,buttton, Smilarity_button, add_button, search_button)
#create()