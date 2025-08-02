nb_bytes_per_token_cmd = config["TEST_FILE"]["nb_bytes_per_token_cmd"]
nb_bytes_per_token_addr = config["TEST_FILE"]["nb_bytes_per_token_addr"]
nb_bytes_per_token_data = config["TEST_FILE"]["nb_bytes_per_token_data"]

nb_token_to_compare_reg_cmp = cmd_dict["REGWR"]["tokens"]["data"]//2 # due to mask token
nb_token_to_compare_mem_cmp = cmd_dict["MEMWR"]["tokens"]["data"]

# Length of cmd : not used 
dict_cmd_number_token: dict[str,int] = {
    "REGRD": cmd_dict["REGWR"]["tokens"]["cmd"],
    "MEMRD": cmd_dict["MEMWR"]["tokens"]["cmd"],
    "MEMRDM": cmd_dict["MEMWRM"]["tokens"]["cmd"],
    "REGWR": cmd_dict["REGWR"]["tokens"]["cmd"],
    "MEMWR": cmd_dict["MEMWR"]["tokens"]["cmd"],
    "MEMWRM": cmd_dict["MEMWRM"]["tokens"]["cmd"], 
}

# Length of addr :
dict_addr_number_token: dict[str,int] = {
    "REGRD": cmd_dict["REGWR"]["tokens"]["addr"], 
    "MEMRD": cmd_dict["MEMWR"]["tokens"]["addr"],
    "REGWR": cmd_dict["REGWR"]["tokens"]["addr"],
    "MEMWR": cmd_dict["MEMWR"]["tokens"]["addr"],
}

# Length of write data :
dict_data_number_token_to_write: dict[str,int] = {
    "REGWR": cmd_dict["REGWR"]["tokens"]["data"],
    "MEMWR": cmd_dict["MEMWR"]["tokens"]["data"],
    "MEMWRM": cmd_dict["MEMWRM"]["tokens"]["data"], 
}

# Length of read data :
dict_data_number_token_to_read: dict[str, int] = {
    "REGRD": cmd_dict["REGWR"]["tokens"]["data"]//2, # due to mask token
    "MEMRD": cmd_dict["MEMWR"]["tokens"]["data"],
    "MEMRDM": cmd_dict["MEMWRM"]["tokens"]["data"],
}