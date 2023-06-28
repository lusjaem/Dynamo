#edited by Magdalena Borkowska
import System
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *
# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# The inputs to this node will be stored as a list in the IN variables.
shared_parameters_file_path = IN[0]  #  the first item in the input list
parameter_group_keys = IN[1]  #  the second item in the input list, a list of parameter group names

# Read the shared parameters file
shared_parameters = []
with open(shared_parameters_file_path, "r") as file:
    for line in file:
        shared_parameters.append(line.strip())

# Generate the parameter group dictionary
parameter_group_dict = {group_name: i for i, group_name in enumerate(parameter_group_keys)}

# Get the active Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Start a transaction
transaction = Transaction(doc, "Add Shared Parameters")
transaction.Start()

# Add the shared parameters to the family's Family Types manager
family_manager = doc.FamilyManager
generated_groups = []  # List to store the generated parameter groups
for param_name in shared_parameters:
    # Determine the parameter group
    parameter_group = parameter_group_dict.get(param_name, BuiltInParameterGroup.PG_DATA)

    # Create the parameter
    parameter = family_manager.AddParameter(param_name, parameter_group, True)

    # Set other parameter properties as needed
    # ...

    # Add the parameter group to the generated groups list
    generated_groups.append(parameter_group)

# Commit the transaction
transaction.Commit()

# Save and close the family file
doc.Save()
doc.Close(False)

# Assign the generated groups as output
OUT = generated_groups
