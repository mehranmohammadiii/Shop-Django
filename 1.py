dict={
    '24': {'product': {'count':2,'price':41}}
}
# print(dict['24'])
# print(dict['24']['product'])
# print(dict['24']['product']['count'])
# print(dict['24']['product']['price'])
# print(dict['24']['product'].values())

dic1={
    { "24" : { "count":0 ,"price" : 14000} },
    { "52" : { "count":0 ,"price" : 14000} },
    { "13" : { "count":0 ,"price" : 14000} },
 }

for item in dic1.values():
    print(item)
