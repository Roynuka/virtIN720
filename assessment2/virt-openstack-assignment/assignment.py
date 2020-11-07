#!/usr/bin/env python
import argparse
import openstack

conn = openstack.connect(cloud_name='openstack')


IMAGE = 'ubuntu-minimal-16.04-x86_64'
FLAVOUR = 'c1.c1r1'
KEYPAIR = 'nukar1-key'
NETWORK = 'nukar1-net'
SECURITY = 'assignment2'
SUBNET = 'nukar1-subnet'
ROUTER = 'nukar1-rtr'
SERVERLIST = [ 'nukar1-web', 'nukar1-app', 'nukar1-db' ]

public_net = conn.network.find_network('public-net')



#print the current network to prove that the connectivity is successful
print('------------------------------------------------------------------------')
print('Connection the server:')
print(conn,'\n')

def create():
    ''' Create a set of Openstack resources '''
	
	#creating server
	#SERVER = 'nukar1-server'
print('creating network')

#network variables
network = conn.network.find_network(NETWORK)
subnet = conn.network.find_subnet(SUBNET)
router = conn.network.find_router(ROUTER)

if network is None:
	network = conn.network.create(name='nukar1-net')
	print ("Network created!!")
else:
	print("this network already exists")
	
print("creating subnet...")
	
if subnet:
	print("Subnet already exists")
else:
	subnet = conn.network.create_subnet(
	name=SUBNET,
    network_id=network.id,
	ip_version='4',
	cidr='192.168.50.0/24',
	gateway_ip='192.168.50.1'
)
print("Subnet created")

	#create router
	
print("creating router...")

if router:
	print("Router already exists")
else:
	router = conn.network.create_router(
	name=ROUTER,
	external_gateway_info={'network_id': public_net.id})
	conn.network.add_interface_to_router(router, subnet.id)
print("Router created")


#launch instaces

image = conn.compute.find_image(IMAGE)
flavour = conn.compute.find_flavor(FLAVOUR)
keypair = conn.compute.find_keypair(KEYPAIR)
security_group = conn.network.find_security_group(SECURITYGROUP)


		
##create servers

print("creating servers...")
for server in SERVERLIST:
	check_server = conn.compute.find_server(server)
	if check_server:
		print("Servers already exist")

	else:
		new_server = conn.compute.create_server(
		name=server,
		image_id=image.id,
		flavor_id=flavour.id,
		networks=[{"uuid": network.id}],
		key_name=keypair.name,
		security_groups=[{"name": security.name}]
	)
		new_server = conn.compute.wait_for_server(new_server)
print(" [" + server + "] server created")

            # Associate Floating IP address to nukar1-web
if server == 'nukar1-web':
                print("Associating floating IP address to WEB server......")
                floating_ip = conn.network.create_ip(floating_network_id=public_net.id)
                web_server = conn.compute.find_server('nukar1-web')
                conn.compute.add_floating_ip_to_server(web_server, floating_ip.floating_ip_address)
                print("Floating IP address has been allocated to WEB server")


	

	



pass

def run():
    ''' Start  a set of Openstack virtual machines
    if they are not already running.
    '''
print("Checking servers status...")
for server in SERVERLIST:
            check_server = conn.compute.find_server(server)
            if check_server:
                check_server = conn.compute.get_server(check_server)
            if check_server.status == "ACTIVE":
                print(" [" + server + "] server is currently active")
            elif check_server.status == "SHUTOFF":
                print(" [" + server + "] server is currently shutoff")
                print("Starting [" + server + "]  server......")
                conn.compute.start_server(check_server)
                print(" [" + server + "] server is active")
	
pass

def stop():
    ''' Stop  a set of Openstack virtual machines
    if they are running.
    '''
	
print("stopping servers....")
for server in SERVERLIST:
		server_check = conn.compute.find_server(server)
if server_check:
            server_check = conn.compute.get_server(server_check)
            if server_check.status == "ACTIVE":
                print(" [" + server + "] server is currently active")
                print("Starting [" + server + "] server......")
                conn.compute.stop_server(check_server)
                print(" [" + server + "] server currently not running")
            elif server_check.status == "SHUTOFF":
                print(" [" + server + "] has already been shutdown")
		
		
	
pass

def destroy():
    ''' Tear down the set of Openstack resources 
    produced by the create action
    '''
	server_list = ['nukar1-web', 'nukar1-app', 'nukar1-db']
    for serv in server_list:
        server = connection.compute.find_server(serv)
        if server is None:
            print(serv + " server does not exist")
        else:
            connection.compute.delete_server(server)
            print(serv + "server has been deleted")
    nukar1_rtr = connection.network.find_router('nukar1-rtr')
    if nukar1_rtr is None:
        print("router already does not exist")
    else:
        connection.network.delete_router(nukar1_rtr)
        print("router has been deleted")
    time.sleep(5)
    nukar1_subnet = connection.network.find_subnet('nukar1-subnet')
    if tawaab1_subnet is None:
        print("subnet already does not exist")
    else:
        connection.network.delete_subnet(tawaab1_subnet)
        print("subnet has been deleted")
    nukar1_network = connection.network.find_network('nukar1-network')
    if nukar1_network is None:
        print("network already does not exist")
    else:
        connection.network.delete_network(tawaab1_network)
        print("network has been deleted")
		
		


	
pass

def status():
    ''' Print a status report on the OpenStack
    virtual machines created by the create action.
    '''


	

	
for server in conn.compute.servers():
		check_server = conn.compute.find_server(server)
		print(server.name)
		
if check_server:
            check_server = conn.compute.get_server(check_server)
            check_server_ip = check_server["addresses"][NETWORK][0]["addr"]

            # Display IP and floating IP address of WEB server if it exists,
            if server == 'nukar1-web':
                check_server_floating_ip = check_server["addresses"][NETWORK][1]["addr"]
            else:
                check_server_floating_ip = "Not found"            
            print("Server Name: [" + server + "]")
            print("Server IP: [" + check_server_ip + "]")
            print("Server Floating IP: [" + check_server_floating_ip + "]")
            print("Server Status: [" + check_server.status + "]")
else:
            print("Server [" + server + "] does not exist")		
		
for image in conn.compute.images():
		print(image.name)
pass
	
	 


### You should not modify anything below this line ###
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation',
                        help='One of "create", "run", "stop", "destroy", or "status"')
    args = parser.parse_args()
    operation = args.operation

    operations = {
        'create'  : create,
        'run'     : run,
        'stop'    : stop,
        'destroy' : destroy,
        'status'  : status
        }

    action = operations.get(operation, lambda: print('{}: no such operation'.format(operation)))
    action()
