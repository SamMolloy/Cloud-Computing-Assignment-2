from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)
appName = "myapp"
@app.route("/")
def index():
    return """
Available API endpoints:

GET /containers                     List all containers
GET /containers?state=running      List running containers (only)
GET /containers/<id>                Inspect a specific container
GET /containers/<id>/logs           Dump specific container logs
GET /images                         List all images


POST /images                        Create a new image
POST /containers                    Create a new container

PATCH /containers/<id>              Change a container's state
PATCH /images/<id>                  Change a specific image's attributes

DELETE /containers/<id>             Delete a specific container
DELETE /containers                  Delete all containers (including running)
DELETE /images/<id>                 Delete a specific image
DELETE /images                      Delete all images

"""
#method to list all containers
@app.route('/containers', methods=['GET'])
def containers_index():
    """
    List all containers
 
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool

    """
    #lists the running containers
    if request.args.get('state') == 'running': 
        output = docker('ps')
        resp = json.dumps(docker_ps_to_array(output))
    #lists the inactive containers
    else:
        output = docker('ps', '-a')
        resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

#method to list all the images
@app.route('/images', methods=['GET'])
def images_index():
    """
    List all images 
    
    Complete the code below generating a valid response. 
    """
    #sets the docker command to view all images 
    output = docker('images', '-a') 
    resp =  json.dumps(docker_images_to_array(output))
    return Response(response=resp, mimetype="application/json")

#Method to get a specific container by id
@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    """
    Inspect specific container

    """
    #sets the out put to the docker command to inspect a container by id
    output = docker('inspect', id)
    resp = output

    return Response(response=resp, mimetype="application/json")

#method to get a containers logs
@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
    """
    Dump specific container logs

    """
   #sets the output to the docker command to inspect a containers logs
    output = docker('logs', id)
    resp =  output
    return Response(response=resp, mimetype="application/json")

#method to delete a specific image by id
@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image
       """
    #docker command to force remove an image
    docker ('rmi', '-f', id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

#method to delete a specific container by id
@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed

    """
   #docker command to force remove a container
    docker('rm','-f',  id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

#method to delete all containers
@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangrous!

    """
    #creates an array and reads all of the containers into it
    containers = docker('ps', '-a')
    containerArray = docker_ps_to_array(containers)

    removedContainers = []
   #for loop to read through the array of containers and run the docker rm command on each container by id
    for container in containerArray:

        if container["name"] != appName:
           id = container["id"]
           docker("stop", id)
           docker("rm", id)
           removed = {"id": id}
           removedContainers.append(removed)

    resp = json.dumps(removedContainers)
    return Response(response=resp, mimetype="application/json")
 #method to delete all images
@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangrous!
    """
    #creates an array and reads all of the images into it 
    images = docker("images")
    imageArray = docker_images_to_array(images)
  
    removedImages = []
    #for loop to go through the array and force remove all of the images in it by id
    for image in imageArray:
        if image["name"] != appName:
            id=image["id"]
            docker("rmi", str(id), "-f")
            removed = {"id": id}
            removedImages.append(removed)

    resp = json.dumps(removedImages)
    return Response(response=resp, mimetype="application/json")

#Method to post or create a new container
@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image$
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image$
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image$
    """
   #uses the given image id to make a docker command to create a container using that image
    body = request.get_json(force=True)
    image = body['image']
    args = ('run', '-d')
    id = docker(*(args + (image,)))[0:12]
    return Response(response='{"id": "%s"}' % id, mimetype="application/json")

#method to post or create a new image
@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)

    curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images
    """
   #gets the dockerfile needed to create an image
    dockerfile = request.files['file']
    dockerfile.save ('Dockerfile')
   #command to create the image
    docker ('build', '-t', 'test', '.')
    i = docker_images_to_array(docker('images'))

    resp = '{"id": "%s"}' % i[0]['id']
    return Response(response=resp, mimetype="application/json")

#method to patch a specific container
@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512$
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512$
    """
   #checks if a container is running and if it is it restarts it
    body = request.get_json(force=True)
    try:
        state = body['state']
        if state == 'running':
            docker('restart', id)
    except:
        pass
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

#method to patch an image
@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
   Update image attributes (support: name[:tag])  tag name should be lowercase only

    curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/7f2619ed176$

    """
   #adds or changes the tag of an image
    body = request.get_json(force=True)
    tag = body['tag']
    docker('tag', id, tag)
    
    resp = '{"id: "%s"}' % id
    return Response(response=resp, mimetype="application/json")


def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr.startswith('Error'):
        print 'Error: {0} -> {1}'.format(' '.join(cmd), stderr)
    return stderr + stdout

# 
# Docker output parsing helpers
#

# Parses the output of a Docker PS command to a python List
# 
def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)
    return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs

#
# Parses the output of a Docker image command to a python List
# 
def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)
    return all

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)

