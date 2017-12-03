import os

#Setting layout of menu system
menuOptions = {}
menuOptions['1']="GET all containers"
menuOptions['2']="GET running containers"
menuOptions['3']="GET specific container (id)"
menuOptions['4']="GET specific container logs" 
menuOptions['5']="GET all images"
menuOptions['6']="POST new image"
menuOptions['7']="POST new container"
menuOptions['8']="PATCH container(id) state" 
menuOptions['9']="PATCH image(id) attributes"
menuOptions['10']="DELETE specific container (id)"
menuOptions['11']="DELETE all containers"
menuOptions['12']="DELETE specific image (id)"
menuOptions['13']="DELETE all images"
menuOptions['14']="Exit"


while True: 
  menu=menuOptions.keys()
  menu.sort()

  
  print "Available Options:"
  for entry in menuOptions: 
    print entry, menuOptions[entry]
  picked=raw_input("Please Select:")
  #GET all container
  if picked =='1': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers | python -mjson.tool")
  #Get running containers
  elif picked == '2': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers?state=running | python -mjson.tool")
 #Get specific container
  elif picked == '3':
    id=raw_input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/containers/%s | python -mjson.tool" % id)
 #GET specific container logs
  elif picked == '4': 
    id=raw_input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Content-Type: application/json' http://35.195.34.113:8080/containers/%s/logs | python -mjson.tool" % id)
 #GET all images
  elif picked == '5':
    os.system("curl -s -X GET -H 'Accept: application/json' http://35.195.34.113:8080/images | python -mjson.tool")
 #POST new image
  elif picked == '6': 
    os.system("curl -H 'Accept: application/json' -F file=@whale-say.Dockerfile http://35.195.34.113:8080/images")
 #POST new container
  elif picked == '7':
    id=raw_input("Please Enter Image ID/Name:")
    os.system("curl -X POST -H 'Content-Type: application/json' http://35.195.34.113:8080/containers -d '{\"image\": \"%s\"}'" % id)
 #PATCH specific container
  elif picked == '8': 
    id=raw_input("Please Enter Container ID:") 
    os.system("curl -X PATCH -H 'Content-Type: application/json' http://104.155.112.73:8080/containers/%s -d '{\"state\": \"running\"}'" % id)
 #PATCH specific image
  elif picked == '9':
    id=raw_input("Please Enter Image ID:")
    os.system("curl -s -X PATCH -H 'Content-Type: application/json' http://35.195.34.113:8080/images/%s -d '{\"tag\": \"test:1.0\"}'" % id)
 #DELETE Specific container
  elif picked == '10': 
    id=raw_input("Please Enter Container ID:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://35.195.34.113:8080/containers/%s" % id)
 #DELETE all containers
  elif picked == '11':
    os.system("curl -s -X DELETE -H 'Content-Type: application/json' http://35.195.34.113:8080/containers")
 #DELETE specific image
  elif picked == '12': 
    id=raw_input("Please Enter Image ID:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://35.195.34.113:8080/images/%s" % id)
  #DELETE all images
  elif picked == '13':
    os.system("curl -s -X DELETE -H 'Content-Type: application/json' http://35.195.34.113:8080/images")
 #Exit the app
  elif picked == '14': 
    break
 #asks for another valid entry if the user enters an invalid number
  else: 
    print "Please enter a valid menu option" 
