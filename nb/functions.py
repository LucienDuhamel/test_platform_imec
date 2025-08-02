import yaml

def is_empty(arg : str):
    """
    Checks if the given argument is empty or None.
    
    Args:        arg (str): The argument to check.
 
    Returns:
        bool: True if the argument is empty or None, False otherwise.
    """
    if (arg is None or arg == ""):
        return True 
    else :
        return False
    
    
    
def load_config(path: str) -> dict:
    """
    Loads the configuration from a YAML file.   
    
    Args:
        path (str): Path to the YAML configuration file.
        
    Returns:
        dict: Parsed configuration data.
    """
    
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config