import requests

BASE = "http://127.0.0.1:5000/"
x = 10
y = 20 

circle_color_lib = ("green","blue")
circle_color = "green"

pos = circle_color_lib.index(circle_color)
print("Color index is : " , pos)


## Add new record
response = requests.put(BASE + "xy_coor/"+ str(pos), {"x": int(x), "y": int(y)})
print(response.json())

input()

## Read record
response = requests.get(BASE + "xy_coor/0")
print(response.json())

input()

## Update record
response = requests.delete(BASE + "xy_coor/"+ str(pos))
print(response)