import uuid
  
id = uuid.uuid1()
  
# Representations of uuid1()

#print (repr(id.bytes)) # k\x10\xa1n\x02\xe7\x11\xe8\xaeY\x00\x16>\x99\x0b\xdb
int1 = id.int

print (int1)         # 142313746482664936587190810281013480411  

#print (id.hex)         # 6b10a16e02e711e8ae5900163e990bdb