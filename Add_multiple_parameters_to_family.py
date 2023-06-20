import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

def add_shared_parameters_to_family(family_path, shared_parameters_file_path):
    # Start a transaction
    TransactionManager.Instance.EnsureInTransaction(doc)

    # Open the Revit family document for editing
    fam_doc = doc.FamilyManager.OpenEditableFamily(family_path)

    # Load the shared parameters file
    def_file_path = ModelPathUtils.ConvertUserVisiblePathToModelPath(shared_parameters_file_path)
    def_file = fam_doc.Application.OpenSharedParameterFile()
    def_file.Import(def_file_path)

    # Get the shared parameter group and definition from the file
    group_name = 'My Parameters'  # Replace with your desired group name
    group = def_file.Groups.get_Item(group_name)
    param_defs = group.Definitions

    # Add the shared parameters to the family
    for param_def in param_defs:
        fam_doc.FamilyManager.AddParameter(param_def, BuiltInParameterGroup.PG_DATA)

    # Save and close the family document
    fam_doc.Save()
    fam_doc.Close(False)

    # End the transaction
    TransactionManager.Instance.TransactionTaskDone()

# Get the current Dynamo Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Usage example
family_path = "C:/path/to/family.rfa"
shared_parameters_file_path = "C:/path/to/shared_parameters.txt"
add_shared_parameters_to_family(family_path, shared_parameters_file_path)
