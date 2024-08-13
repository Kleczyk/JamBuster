import xml.etree.ElementTree as ET
import random


def parse_network_connections(net_file):
    tree = ET.parse(net_file)
    root = tree.getroot()

    # Dictionary to store connections between edges
    connections = {}
    for connection in root.findall('connection'):
        from_edge = connection.attrib['from']
        to_edge = connection.attrib['to']

        if from_edge not in connections:
            connections[from_edge] = []
        connections[from_edge].append(to_edge)

    return connections


def build_route_from_node(start_edge, connections, route_length):
    route = [start_edge]

    current_edge = start_edge
    for _ in range(route_length - 1):
        if current_edge in connections and connections[current_edge]:
            next_edge = random.choice(connections[current_edge])
            route.append(next_edge)
            current_edge = next_edge
        else:
            break  # Stop if there are no more valid connections

    return route


def generate_random_routes(net_file, output_file, num_routes=10, route_length=5, vehicles_per_time_step=10):
    # Parse the network file to extract edge IDs and connections
    tree = ET.parse(net_file)
    root = tree.getroot()

    edges = []
    edge_allow_classes = {}

    for edge in root.findall('edge'):
        if 'id' in edge.attrib and not edge.attrib['id'].startswith(':'):  # Skip internal edges
            lanes = edge.findall('lane')
            allow_classes = set()
            for lane in lanes:
                if 'allow' in lane.attrib:
                    allow_classes.update(lane.attrib['allow'].split())
            edges.append(edge.attrib['id'])
            edge_allow_classes[edge.attrib['id']] = allow_classes

    if len(edges) == 0:
        print("No edges found in the network.")
        return

    # Parse network connections
    connections = parse_network_connections(net_file)

    # Define vehicle types with the vClass and shape attributes
    vehicle_types = {
        "car": {"vClass": "cable_car", "accel": "0.8", "decel": "4.5", "sigma": "0.5", "length": "5", "maxSpeed": "70", "guiShape": "passenger"},
        "bicycle": {"vClass": "bicycle", "accel": "1.0", "decel": "2.5", "sigma": "0.5", "length": "2", "maxSpeed": "15", "guiShape": "bicycle"},
    }

    person_types = {
        "pedestrian": {"vClass": "pedestrian", "accel": "1.5", "decel": "1.0", "sigma": "0.5", "length": "0.5", "maxSpeed": "5", "shape": "pedestrian"}
    }

    routes_root = ET.Element('routes')

    # Add vehicle type definitions
    for v_type, attrs in vehicle_types.items():
        ET.SubElement(routes_root, 'vType', id=v_type, **attrs)

    # Add person type definitions
    for p_type, attrs in person_types.items():
        ET.SubElement(routes_root, 'vType', id=p_type, **attrs)

    entities = []

    # Generate random routes and vehicles/persons
    for i in range(num_routes):
        # Start at a random edge (node)
        start_edge = random.choice(edges)
        route_edges = build_route_from_node(start_edge, connections, route_length)
        allow_class = edge_allow_classes[route_edges[0]]

        # Choose a vehicle or person type that is allowed on the first edge of the route
        if "car" in allow_class:
            entity_type = "car"
            is_person = False
        elif "bicycle" in allow_class:
            entity_type = "bicycle"
            is_person = False
        elif "pedestrian" in allow_class:
            entity_type = "pedestrian"
            is_person = True
        else:
            continue  # Skip route if no valid type is allowed

        route_id = f"route_{i}"
        color = f"{random.random()},{random.random()},{random.random()}"
        route = ET.SubElement(routes_root, 'route', id=route_id, color=color, edges=" ".join(route_edges))

        # Group vehicles/persons by departure time
        depart_time = (i // vehicles_per_time_step) * 10  # Increase depart time every vehicles_per_time_step

        for j in range(random.randint(1, 3)):  # Random number of entities per route (1 to 3)
            entity_id = f"{'person' if is_person else 'veh'}_{i}_{j}"
            entity_color = f"{random.random()},{random.random()},{random.random()}"

            if is_person:
                entities.append({
                    'type': 'person',
                    'id': entity_id,
                    'route': route_id,
                    'depart': depart_time,
                    'color': entity_color
                })
            else:
                entities.append({
                    'type': 'vehicle',
                    'id': entity_id,
                    'vType': entity_type,
                    'route': route_id,
                    'depart': depart_time,
                    'color': entity_color
                })

    # Sort all entities (vehicles and persons) by their departure time
    entities.sort(key=lambda x: x['depart'])

    # Add sorted entities to the XML tree
    for entity in entities:
        if entity['type'] == 'vehicle':
            ET.SubElement(routes_root, 'vehicle',
                          id=entity['id'],
                          type=entity['vType'],
                          route=entity['route'],
                          depart=str(entity['depart']),
                          color=entity['color'])
        elif entity['type'] == 'person':
            person = ET.Element('person', id=entity['id'], depart=str(entity['depart']))
            ET.SubElement(person, 'walk', route=entity['route'], color=entity['color'])
            routes_root.append(person)

    # Write the routes to the output file
    tree = ET.ElementTree(routes_root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)
    print(f"Generated {num_routes} routes and saved to {output_file}.")


# Specify your input network file and output routes file
net_file = 'map.net.xml'
output_file = 'routes.rou.xml'

# Generate routes
generate_random_routes(net_file, output_file, num_routes=5000, route_length=100, vehicles_per_time_step=100)
