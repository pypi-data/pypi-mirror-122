# CPNTools4Py

CPNTools4Py is a small python 3 scripts. These scripts support parsing of xml file which export color petri net from CPNTools, 
define a data structure for Petri nets and labelled partial orders.
It is completely open source and be used in academia.

## First Example

A very simple example, to what you appetite:
```py
import cpntools4py
xml_doc = cpntools4py.read_xml('<path_to_xml_file>')
cpn = cpntools4py.CPN(xml_doc)

print(cpn.places) # Get places
```

## Reference

### Module `cpntools4py`
This is CPNTools4Py main module, it holds the various Petrei net elements, arcs, places, transitions.

### Method `cpntools4py.read_xml`
```py
def read_xml(file_path):
```
Read Xml file editing by CPNTools.
```py
xml_doc = read_xml('/path/to/PetriNet.xml')
```
**Call API**
- `str file_path`: Input the XML file of Petri nets editing by CPNTools.
- `return root Element`: Return an object that holds the root element of the node information of CPNTools.

### Method `cpntools4py.to_snakes`
```py
def to_snakes(cpn)
```
Convert to SNAKES from CPNTools
```py
xml_doc = cpntools4py.read_xml('<path_to_xml_file>')
cpn = cpntools4py.CPN(xml_doc)
net = cpntools4py.to_snakes(cpn)
```
**Call API**
- `object CPN`: Input the CPN object.
- `return object net`: return the SNAKES net object.

### Module `cpntools4py.petri_net`
This is CPNTools4Py data structure module, it holds the various Petrei net elements, arcs, places, transitions.

### Class `Place`
A place of a Petri net.
`Place` class has 4 variables, each of which returns `id`, `text`, `type` and `tokens`.
Each variable holds the Place name, color attirbute, and initial marking set by CPNTools. Since id is an identification
number, it is automatically assinged at the time of generation by CPNTools.
```py
xml_doc = cpntools4py.read_xml('<path_to_xml_file>')
cpn = cpntools4py.CPN(xml_doc)

for place in cpn.places:
	print(place.id)
	# 'id0123456789'
```

### Class `Transitions`
A Transition of a Petri net.
`Transition` class has 3 variables, each of which returns `id`, `text` and `time`.
Each variable holds the Transition name and time inscription. id is and identification number.

```py
xml_doc = cpntools4py.read_xml('<path_to_xml_file>')
cpn = cpntools4py.CPN(xml_doc)

for transition in cpn.transitions:
	print(transition.text)
	# 'Trans1'
```

### Class `Arc`
A Arc of a Petri net.
`Arc`　class has 4 variables, each of which returns `id`, `orientation`, `placeend` and `transend`.
The `Arc` class holds the connection information between places and transitions. `orientation` holds the orientation of the arc, `placened` and `tranend` holdes the nodes to be connected.

```py
xml_doc = cpntools4py.read_xml('<path_to_xml_file>')
cpn = cpntools4py.CPN(xml_doc)

for arc in cpn.arcs:
	print(arc.orientation)
	# 'PtoT'
```