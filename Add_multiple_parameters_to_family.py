import sys
import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB

# Get the executing assembly path
executing_assembly_path = Assembly.GetExecutingAssembly().Location

# Get the directory path of the executing assembly
executing_directory_path = System.IO.Path.GetDirectoryName(executing_assembly_path)

# Combine the directory path with the family filename
family_filename = "D:\MBorkowska\Pulpit\Dynamo\Families\MP_Windows_legend.rfa"
family_path = System.IO.Path.Combine(executing_directory_path, family_filename)

# Print the family file path
print(family_path)

def get_shared_parameters_file_path(shared_parameters_filename):
    # Get the current document
    doc = DocumentManager.Instance.CurrentDBDocument

    # Get the current directory path
    current_directory_path = doc.Path

    # Combine the directory path with the shared parameters filename
    shared_parameters_file_path = System.IO.Path.Combine(current_directory_path, shared_parameters_filename)

    return shared_parameters_file_path

# Usage example
shared_parameters_filename = "MP_SharedParameters_Nokia"
shared_parameters_file_path = get_shared_parameters_file_path(shared_parameters_filename)
print(shared_parameters_file_path)


def add_shared_parameters_to_family(family_path, shared_parameters_file):
    # Set up the Revit application and document
    app = DB.DocumentManager.Instance.CurrentUIApplication.Application
    doc = DB.DocumentManager.Instance.CurrentDBDocument

    # Open the family document
    family_doc = app.OpenDocumentFile(family_path)

    # Get the shared parameters definition file
    shared_params_file = app.OpenSharedParameterFile()

    # Create a new shared parameters group
    group_name = "For Script"
    group = shared_params_file.Groups.Create(group_name)

    # Read the shared parameters from the text file
    with open(shared_parameters_file, "r") as file:
        lines = file.readlines()

    # Create shared parameters
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        param_name, param_type, inst_or_type, visible = line.split(",")

        # Create the shared parameter definition
        param_def = group.Definitions.Create(param_name, DB.ParameterType.Length, inst_or_type == "instance")

        # Set the parameter properties
        param_def.Visible = visible.lower() == "true"
        param_def.UserModifiable = True

        # Add the parameter to the family
        if inst_or_type == "instance":
            family_doc.FamilyManager.AddParameter(param_def, DB.FamilyParameterType.Instance)
        else:
            family_doc.FamilyManager.AddParameter(param_def, DB.FamilyParameterType.Type)

    # Save and close the family document
    family_doc.Save()
    family_doc.Close()

    return "Shared parameters added successfully!"

# Usage

result = add_shared_parameters_to_family(family_path, shared_parameters_file)
print(result)
