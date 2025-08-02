from .functions import load_config

commands = load_config("commands.yaml")

nb_bytes_per_token_cmd = commands["nb_bytes_per_token_cmd"]
nb_bytes_per_token_addr = commands["nb_bytes_per_token_addr"]
nb_bytes_per_token_data = commands["nb_bytes_per_token_data"]

nb_token_to_compare_reg_cmp = commands["REGWR"]["tokens"]["data"]//2 # due to mask token
nb_token_to_compare_mem_cmp = commands["MEMWR"]["tokens"]["data"]

# Length of cmd : not used 
dict_cmd_number_token: dict[str,int] = {
    "REGRD": commands["REGWR"]["tokens"]["cmd"],
    "MEMRD": commands["MEMWR"]["tokens"]["cmd"],
    "MEMRDM": commands["MEMWRM"]["tokens"]["cmd"],
    "REGWR": commands["REGWR"]["tokens"]["cmd"],
    "MEMWR": commands["MEMWR"]["tokens"]["cmd"],
    "MEMWRM": commands["MEMWRM"]["tokens"]["cmd"], 
}

# Length of addr :
dict_addr_number_token: dict[str,int] = {
    "REGRD": commands["REGWR"]["tokens"]["addr"], 
    "MEMRD": commands["MEMWR"]["tokens"]["addr"],
    "REGWR": commands["REGWR"]["tokens"]["addr"],
    "MEMWR": commands["MEMWR"]["tokens"]["addr"],
}

# Length of write data :
dict_data_number_token_to_write: dict[str,int] = {
    "REGWR": commands["REGWR"]["tokens"]["data"],
    "MEMWR": commands["MEMWR"]["tokens"]["data"],
    "MEMWRM": commands["MEMWRM"]["tokens"]["data"], 
}

# Length of read data :
dict_data_number_token_to_read: dict[str, int] = {
    "REGRD": commands["REGWR"]["tokens"]["data"]//2, # due to mask token
    "MEMRD": commands["MEMWR"]["tokens"]["data"],
    "MEMRDM": commands["MEMWRM"]["tokens"]["data"],
}