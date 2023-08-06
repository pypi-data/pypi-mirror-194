import re

import PyMDL

# for i in range(1, 6):
#     res = PyMDL.search('Open', page=i)
#     ls = res.get_all()
#     print(f'\n---- End of page {i} ----\n')

# for i in range(1, 3):
#     mv = PyMDL.search('gold', page=i)
#     if not mv:
#         break
#     for j in mv:
#         print("Getting:", j)
#         page = mv.get(j)
#     # full = ppl.get_all()
#     print('\n--------\n')
#
# ppl = PyMDL.search_people('Logan')
# print(ppl.get(ppl[0]).name)
# print(ppl.get(ppl[0]).dob)
# print(ppl.get(ppl[0]).works)

# mv1 = PyMDL.info('https://mydramalist.com/36269-doctor-playbook')
# mv2 = PyMDL.info('https://mydramalist.com/26136-parasite-war')
# print(mv2)
# print(mv2.reco)
# mv3 = PyMDL.info('https://mydramalist.com/23429-parasite')
# mv3.get_recommendations()
# print(mv3.reco)
# mv1.save('out.json')
# print(mv2.aka)
# mv2.save('out.json')
# mv3.save('out.json')

# ser = PyMDL.search('What\'s wrong with secretary Kim')
# print(ser)
# print(ser.get(ser[0]).save('out.json'))


mvs = PyMDL.search('Gold')
mv = mvs.get_all(4)
for i in mv:
    print(i.title)
#     i.save('out.json')
# ppl = PyMDL.search_people('Lee min Ho')
# print(ppl)
# person = ppl.get_all()
# for i in person:
#     print(f"Saving: {i.name}")
#     i.save('ppl.json')

# print(PyMDL.search('Gold', 1, 'Japanese Movie'))
