# Analysis of geospatial data

This project analyzes data from the Foursquare social network. We extract data from places frequented in the city of New York. A number of analyzes are performed on several key metrics in network theory.

### New York map 

![New York](https://raw.githubusercontent.com/macio-matheus/analysis-geospatial-data/develop/docs/nymap.png)

### Network Graph 

![graph](https://raw.githubusercontent.com/macio-matheus/analysis-geospatial-data/develop/docs/network.png)

### Communities

![Community](https://raw.githubusercontent.com/macio-matheus/analysis-geospatial-data/develop/docs/community.png)


### Usage
First of all, build the container using docker-compose and then you can 
access the Jupyter that is ready to be used.

#### Run with docker compose
```sh
cd analysis-geospatial-data
docker-compose up -d
```

#### Accessing Jupyter
```sh
http://<your-ip>:8888/tree
```

#### Ports
```sh
    - 8888 => Jupyter
```

### DockerHub
```sh
https://hub.docker.com/r/maciomatheus/jupyter_notebook_data_science/
```

### Team

- Henrique Lima (https://github.com/henriquelima1408)
- Julio Sales (https://github.com/jsalesba)
- Mácio Matheus Arruda (https://github.com/macio-matheus)
- Victor Outtes (https://github.com/victorouttes)