# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import networkx as nx
from braket.aws import AwsDevice
from braket.circuits import Circuit


def device_connectivity_graph(device: AwsDevice) -> nx.Graph:
    connectivity = getattr(device.properties.paradigm, "connectivity", None)
    num_qubits = getattr(device.properties.paradigm, "qubitCount", -1)

    if connectivity is None:
        raise ValueError("Given device does not have connectivity attribute")

    is_fully_connected = getattr(connectivity, "fullyConnected", False)

    # no need to further check graph if fully connected.
    if is_fully_connected:
        graph = nx.complete_graph(num_qubits)

        return graph

    connectivityGraph = getattr(connectivity, "connectivityGraph", None)
    if connectivityGraph is None:
        raise ValueError("Given hardware does not have connectivity graph.")

    adj_list = [f"{key} {' '.join(val)}" for key, val in connectivityGraph.items()]

    return nx.parse_adjlist(adj_list)


def _get_adjacency_list(graph: nx.Graph) -> list[tuple[int, int]]:
    edge_set = set()

    for edge in graph.edges():
        # ignoring the weight if any
        a, b = int(edge[0]), int(edge[1])
        # ordering to (min, max)
        a, b = min(a, b), max(a, b)

        if (a, b) not in edge_set:
            edge_set.add((a, b))

    return list(edge_set)


def graph_state_circuit(device: AwsDevice) -> Circuit:
    graph = device_connectivity_graph(device)
    num_qubits = getattr(device.properties.paradigm, "qubitCount", -1)

    adj_list = _get_adjacency_list(graph)

    circ = Circuit()
    for a, b in adj_list:
        circ.cz(control=a, target=b)

    circ.h(range(num_qubits))

    return circ
