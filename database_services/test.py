from RDBService import  *

#print(get_by_prefix("bs3363", "products", "name", ""))
all_users = find_by_template("bs3363","customers",{})
print(all_users)