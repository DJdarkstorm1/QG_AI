str0=" Agent:007_Bond; Coords:(40,74); Items:gun,money,gun; Mission:2025-RESCUE-X "

str1=str0.strip()
#print(f"|{str1}|")
str2=str0.split("; ")
#print(f"|{str2}|")

agent_name=str2[0].split(':')[1]
coords=str2[1].split(':')[1].strip("()").split(',')
coords_num=(int(coords[0]),int(coords[1]))
#print(f"|{agent_name}|")
#print(f"|{coords}|")
#print(f"|{coords_num}|")
item_name=str2[2].split(':')[1].split(',')
item_set={item_name[0],
          item_name[1],
          item_name[2]}
#print(f"|{item_name}|")
#print(f"|{item_set}|")
# mission=str2[3].split(':')[1].split('-')[1]
mission=str2[3].split(':')[1][5::]
'''
mission_name=mission[5::]
print(f"|{mission_name}|")
'''

#print(f"|{mission}|")

info_dict={"Agent":agent_name,
      "Coords":coords_num,
      "Item":item_set,
      "Mission":mission}
print("dict:",info_dict)
