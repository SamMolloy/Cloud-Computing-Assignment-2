import os

menu = {}
menu['1']="GET all containers"
menu['2']="GET running containers"
menu['3']="GET specific container (id)"
menu['4']="GET specific container logs" 
menu['5']="GET all images"
menu['6']="POST new image"
menu['7']="POST new container"
menu['8']="PATCH container(id) state" 
menu['9']="PATCH image(id) attributes"
menu['10']="DELETE specific container (id)"
menu['11']="DELETE all containers"
menu['12']="DELETE specific image (id)"
menu['13']="DELETE all images"
menu['14']="Exit"

while True: 
  options=menu.keys()
  options.sort()

  
  print "Available API endpoints:"
  for entry in options: 
    print entry, menu[entry]
  selection=raw_input("Please Select:") 
  if selection =='1': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers | python -mjson.tool")
  elif selection == '2': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers?state=running | python -mjson.tool")
  elif selection == '3':
    id=raw_input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers/%s | python -mjson.tool" % id)
  elif selection == '4': 
    id=raw_input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Content-Type: application/json' http://35.195.34.113:8080/containers/%s/logs | python -mjson.tool" % id)
  elif selection == '5':
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/images | python -mjson.tool")
  elif selection == '6': 
    os.system("curl -H 'Accept: application/json' -F file=@whale-say.Dockerfile http://35.195.34.113:8080/images")
  elif selection == '7':
    id=raw_input("Please Enter Image ID/Name:")
    os.system("curl -X POST -H 'Content-Type: application/json' http://35.195.34.113:8080/containers -d '{\"image\": \"%s\"}'" % id)
  elif selection == '8': 
    id=raw_input("Please Enter Container ID:")
  elif selection == '8': 
    os.system("curl -X PATCH -H 'Content-Type: application/json' http://104.155.112.73:8080/containers/%s -d '{\"state\": \"running\"}'" % id)
  elif selection == '9':
    id=raw_input("Please Enter Image ID:")
    os.system("curl -s -X PATCH -H 'Content-Type: application/json' http://35.195.34.113:8080/images/%s -d '{\"tag\": \"test:1.0\"}'" % id)
  elif selection == '10': 
    id=raw_input("Please Enter Image ID:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://35.195.34.113:8080/containers/%s" % id)
  elif selection == '11':
    os.system("curl -s -X DELETE -H 'Content-Type: application/json' http://35.195.34.113:8080/containers")
 elif selection == '12': 
    id=raw_input("Please Enter Image ID:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://35.195.34.113:8080/images/%s" % id)
  elif selection == '13':
    os.system("curl -s -X DELETE -H 'Content-Type: application/json' http://35.195.34.113:8080/images")
  elif selection == '14': 
    break
  else: 
    print "Unknown Option Selected!" 
