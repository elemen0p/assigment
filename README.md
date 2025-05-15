# Prometheus Custom Service Discovery
In Trigo's solution there are many proprietary sensors based on embedded microcontrollers running bare-metal OS under hard resources limit (low cpu, low memory). Those sensors cannot run any modern tools such as Docker, Consul agents and so on but do expose an http server with a dedicated metrics endpoint.

In addition, the store operators can change the participating sensors so the inventory of sensors can be updated quite often.

In this exercise, we will implement a custom service discovery mechanism for [Prometheus](https://prometheus.io/). This will ensure that Prometheus continues to monitor the correct sensor inventory, even as the sensor configuration changes dynamically.

# Exercise
The inventory service] will be used to expose an http endpoint that yields a list of hosts of the current active sensors.

Specifically, invoking the following command:
```
curl -XGET http://localhost:1337/inventory
```
will yield the current sensors hostnames to monitor:
```
[
    "sensor_1",
    "sensor_2",
    "sensor_12",
    ...
]
```

Your goal in this exercise is to:
* Implement a custom service discovery for Prometheus which queries the described endpoint (in the `inventory service`) and yields a target group containing the sensors targets.
* Write a minimal docker-compose / helm chart that runs the entire stack, having a Prometheus instance trying to scrape the sensors inventory with an exposed HTTP port (tcp/9090).

# Additional Notes
* Don't modify the `inventory service` code.
* Clone this repository and upload your solution to your personal account (don't fork), and then provide us with a link (and permissions).
* You have up to 2 hours to complete the exercise.
* Feel free to code it in any language you would like and use any framework / library / snippet of code you find.
* We are available to answer any questions you may have, so feel free to ask :smile:.

# My solution
According to this guide: https://blog.incidenthub.cloud/A-Beginners-Guide-To-Service-Discovery-in-Prometheus and prometheus docs, it seems that our inventory service doesn't serve the metrics on the right format that prometheus and http_sd expects.
In order to find a solution I'm using an adapter.py file which take the target from the invnetory service and save it as a file with the right targets and labels format. This file is then being used as a shared volume between the container runs adapter.py and the container runs prometheus.
On prometheus.yml we using a file_sd_configs in order to pull the target from the file (the shared volume) and we pulling each 30 seconds.
* adapter.py - Adapter script which takes the targets served by the inventory service and save them in the right format into a file
* docker-compose.yml - Orchestrates the creation of the inventory-service (now the image is saved on my public repo), the adapter container and the prometheus container
* prometheus.yml - The config file indicates where we get the targets from

# Final result
![image](https://github.com/user-attachments/assets/b0590435-facc-4c19-a7f1-80ab40ca2c5d)

![image](https://github.com/user-attachments/assets/ecbed8d6-a756-4982-af1a-006fcb1642a2)
