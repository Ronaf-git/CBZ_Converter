import os
import importlib
from types import FunctionType

# Package name is functions (this can be omitted but keeps it clear)
package_name = "functions"
package_path = os.path.dirname(__file__)

# Dynamically import all modules from the package and make all functions callable
for filename in os.listdir(package_path):
    # Only consider Python files (excluding __init__.py)
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Remove '.py' extension
        try:
            # Dynamically import the module
            module = importlib.import_module(f'.{module_name}', package=package_name)

            # Loop through all attributes in the module
            for attribute_name in dir(module):
                # Get the attribute from the module
                attribute = getattr(module, attribute_name)

                # Check if the attribute is callable 
                if isinstance(attribute, FunctionType):
                    # Add the function to the global namespace
                    globals()[attribute_name] = attribute
                    print(f"Function {attribute_name} from module {module_name} is now callable in main.")
                else:
                    print(f"{attribute_name} is not callable, skipping.")
        except Exception as e:
            print(f"Failed to import module {module_name}: {e}")
