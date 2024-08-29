# JamBuster

JamBuster is a project with the goal of creating model for control traffic lights in a Rzeszów city. The project is
based on the data from the OpenStreetMap and the data from the city of Rzeszów. The project based on the data from the
OpenStreetMap and the data from the city of Rzeszów. This map is used for crate a simulation for our model. The model
will be learning with Reinforcement Lerning methods. 


![img.png](/data/img.png)

screen from the simulation

## How to run the simulation only for Linux
1. Clone the repository
2. Install [SUMO](https://sumo.dlr.de/docs/Installing.html)
3. Run in shell:
```shell
cd src/map_p05
make net2poly trips trace sim

```