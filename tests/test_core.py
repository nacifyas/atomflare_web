from www.dal.service import ServiceDAL 

serviceDAL = ServiceDAL()
res = serviceDAL.get_all_services()

print(res)
