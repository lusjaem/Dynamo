import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import sys

def add_shared_parameters_to_project(shared_parameters_file_path):
    try:
        # Get the active document
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document

        # Open the shared parameters file
        shared_params_file = DefinitionFile.Load(doc, shared_parameters_file_path)
        if shared_params_file is None:
            print("Failed to open the shared parameters file.")
            return

        # Get the desired group
        desired_group_name = "Windows"  # Replace with your desired group name
        desired_group = shared_params_file.Groups.get_Item(desired_group_name)
        if desired_group is None:
            print("Desired group not found in the shared parameters file.")
            return

        # Start a transaction
        transaction_name = "Add Shared Parameters"
        transaction = Transaction(doc, transaction_name)
        transaction.Start()

        # Add the shared parameters as project parameters
        for definition in desired_group.Definitions:
            parameter_type = definition.ParameterType
            parameter_group = BuiltInParameterGroup.PG_TEXT  # Replace with your desired parameter group
            is_instance = False
            external_definition = ExternalDefinition.Create(doc, definition.Name, parameter_type)
            ExternalDefinitionUtils.AddParameter(doc, external_definition, parameter_group, is_instance)

        # Commit the transaction
        transaction.Commit()

        print("Shared parameters added successfully.")
    except Exception as ex:
        # Handle any exceptions
        print("Exception: " + str(ex))

# Usage
shared_parameters_file_path = r"D:\MBorkowska\Pulpit\Dynamo\Shared Parameters\MP_SharedParameters_mb.txt"
add_shared_parameters_to_project(shared_parameters_file_path)