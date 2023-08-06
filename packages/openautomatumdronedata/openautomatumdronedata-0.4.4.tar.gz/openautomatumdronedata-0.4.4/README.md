![logo](/docs/logo.png)

# Motivation

This package provides an object-oriented structure for loading and analyzing AUTOMATUM DATA datasets. It is intended to enable the rapid use of the dataset in research and development. In addition, a web server-based visualization is provided to give an instant overview of the dataset.


**Download the the dataset from [https://www.automatum-data.com](https://www.automatum-data.com)**

Documentation of this package is available under: [https://openautomatumdronedata.rtfd.io](https://openautomatumdronedata.rtfd.io)

A video with annotated objects can be found **[here.](https://www.youtube.com/watch?v=FTHRNN-XNdY)**


# Installation

The <code>openautomatumdronedata</code>-Utility is a standard PIP package which can be installed as any other PIP package with

```
pip install openautomatumdronedata
```
or depending on your machine
```
pip3 install openautomatumdronedata
```

In addition, the package can also be installed manually, e.g. by placing the sources in your project folder.

# Upgrade

If you have ```openautomatumdronedata``` already installed you can get the latest version with 

```
pip install --upgrade openautomatumdronedata
```

# Change History
Since we update our dataset to keep track with the needs of the user. There are also updates in this library needed. 

In the following table you find which pip package version is compatible with which version of the dataset. You can use pip to directly download a specifc version. The latest version of the dataset is always available on our homepage. 


| **dataset version** | **open.automatum.data version** | **changes** |
|--------------|-----------------|-----------------|
| v1.0 | <= 0.2.1 | |
| v3.0 | >= 0.4.0 |Object to lane assigment,  Object Relations are directly included in the data, Add TTC, TTH, Distance to left and right lane marking |


# Data Structure

The Automatum DATA datasets are strucktured in single <code>recordings</code> with a length of appx. 10 to 18 minutes each. Each <code>recording</code> was captured on a so called <code>location</code>. 

That means there are usually several <code>recordings</code> on each <code>location</code> and the <code>recordings</code> share the common information of the <code>location</code> like the <code>staticWorld (XODR)</code> and the reference point. 

Each <code>recording</code> itself comes in one folder with the following files: 
- **dynamicWorld.json** which contains the dynamic behavior of the objects such as cars, trucks, etc. 
- **staticWorld.xodr**  which contains road geometry in the [OpenDRIVE](https://www.asam.net/standards/detail/opendrive/) format. 
- **recording_name.html**  which contains an overview of the <code>recording</code> with some basic metadata.

## dynamicWorld.json 

| **Variable** | **Description** |
|--------------|-----------------|
|**UTM-Rferencepoint** | Reference point in the world coordinate system in UTM-Format. This reference point is the center of the coordinate system for the given position. The points is given as a tuple of (x \[m\], y \[m\], letter, number) |
|**WGS84-Coordinates** | Referecne point in WGS82 format. |
|**Recording name** | Unique recording name: Streettype_Streetname_LocationName_UUID |
|**UUID** | Unique UUID of the recording |
|**Release** | Release version of the dataset. |
|**Calculation version** | Dict that shows all versions of the the pipeline used to process the recording. |
|**Video Information** | fps and count of containing frames of the recording |
|**Contact an Licencing Information** | Further contact and licence information of the given recording |
|**Object data** | The actual objects data which is described in this documentation. |


Whereby, this Python package has the following objectives: 
- Easy access to the information contained in **dynamicWorld.json** and **staticWorld.xodr**.  
- Avoid effort by writing a parser for the provided data.
- Visualize the data easily in a webbrowser

### How to start coding

The entry point for accessing a dataset is to load a dataset using the ``DroneDataset`` class. You can copy all code snipets one by one and run the code. All snipets together can be found also on the ```hello_world.py``` provided with the sources. 
```python
from openautomatumdronedata.dataset import droneDataset
import os
import numpy as np

path_to_dataset_folder = os.path.abspath("datasets/hw-a9-stammhamm-015-39f0066a-28f0-4a68-b4e8-5d5024720c4e")
dataset = droneDataset(path_to_dataset_folder)
```

this command reads the **dynamicWorld.json** and **staticWorld.xodr** and translates the complete data in to an object-oriented structure. This allows all further data accesses to be made with the instance of the ``drone dataset`` class. Whereby, the ``drone dataset`` class holds the following two subclasses:

## Dynamic World
The dynamic world holds all informations about dynamic objects (cars, trucks, vans) in the dataset and handles the access to objects over the recording time.

You can access the dynamic world by
```python
dynWorld = dataset.dynWorld
```

The dynamic world provides you the following variables:


| **Variable** | **Description** |
|--------------|-----------------|
|**UTM-Rferencepoint** | Reference point in the world coordinate system in UTM-Format. This reference point is the center of the coordinate system for the given position. The points is given as a tuple of (x \[m\], y \[m\], letter, number) |
|**UUID** | Unique UUID of the recording |
|**type** | Type of the object as string |
|**fps** | fps of the recording |
|**delta_t** | Sample time of the recording. \[s\] |
|**frame_count** | Total number of frames of the recording. |
|**maxTime** | Total duration of the recording. \[s\]|
|**DrivenDistanceInMeter** | Total driven distance of all object in the recording. \[m\] |
|**MedianDrivenDistanceInMeter** | Median driven distance of the objects or track length.  \[m\] |


### Example
```python
dynWorld = dataset.dynWorld
print(dynWorld.UUID)
print(dynWorld.frame_count)
print(dynWorld.fps)
print(dynWorld.delta_t)
print(dynWorld.utm_referene_point)
print(dynWorld.maxTime)
print(dynWorld.DrivenDistanceInMeter)
print(dynWorld.MedianDrivenDistanceInMeter)
print(dynWorld.type)
#print(dynWorld.dynamicObjects) # Possible but not recommended. Use further discussed functions.
```

## Dynamic objects

Objects are represented by a set of type specific class:
- ``carObject``
- ``truckObject``
- ``vanObject``
- ``carWithTrailerObject``
- ``motorcycleObject``

For evaluating the type of object, you can use the calls type or the ``type`` member variable which gives you a string. 

All these classes inherited from the base class ```dynamicObject```, which implements the following features. This means you can use all the following features for all object type specific classes.

Per Object the following information are available as scalar:

| **Variable** | **Description** |
|--------------|-----------------|
| **UUID** | Unique UUID of the object |
| **length** | Length of the object \[m\] |
|**width** | Width of the object \[m\] |
|**delta_t** | Time difference between two data points (equal at all objects and with in the ```dynamicObject```) |

Per object the following information are available as vector over time: 

![](docs/VehicleDynamics.png)

| **Variable** | **Description** |
|--------------|-----------------|
| **x_vec** | x-Position of the assumed center of gravity of the object in the local coordinate system |
| **y_vec**  | y-Position of the assumed center of gravity of the object in the local coordinate system |
| **vx_vec** | Velocity in x-direction  **in the vehicle coordinate system** |
| **vy_vec** | Velocity in y-direction  **in the vehicle coordinate system**|
| **ax_vec**  | Acceleration of the object in x-direction **in the vehicle coordinate system** |
| **ay_vec** | Acceleration of the object in y-direction **in the vehicle coordinate system** |
| **jerk_x_vec** | Jerk of the object in X-direction **in the vehicle coordinate system**. Only if available in your dataset, if not the value is None |
| **jerk_y_vec** | Jerk of the object in Y-direction **in the vehicle coordinate system**. Only if available in your dataset, if not the value is None |
| **time** | Vector of the timestamp in the dataset recording for the mention values |
| **psi_vec** | Vector of orientation of objects. |
| **curvature_vec** | Driving Curvature of the object. Only if available in your dataset, if not the value is None |
| **lane_id_vec** | Vector of the ```lane_id``` on which the vehicle drives according to the static world described in the xodr, for details see chapter **Object to lane assignment (OTLA)** |
| **road_id_vec** | Vector of the ```road_id``` on which the vehicle drives according to the static world described in the xodr, for details see chapter **Object to lane assignment (OTLA)** |
| **road_type_list** | List of strings that describes the road type at every time step of the object. Only if available in your dataset, if not the value is None |
| **lane_change_flag_vec** | Vector of bool values, whereby True means that a lane change occurred. In newer Datasets a vector of Integers. Whereby, -1 means lane change to the left, +1 means lane change to the right and 0 means no lane change, for details see chapter **Object to lane assignment (OTLA)**|
| **distance_left_lane_marking** | Distance from the center of gravity of a object (defined by ```x_vec```, ```y_vec```) to the left lane marking, for details see chapter **Distance to lane markings**|
| **distance_right_lane_marking** | Distance from the center of gravity of a object (defined by ```x_vec```, ```y_vec```) to the right lane marking, for details see chapter **Distance to lane markings**|
| **object_relation_dict_list** | List of dicts, whereby every dict describes the object relation at the current time step, for details see chapter **Object Relations** |
| **tth_dict_vec** | List of dicts, whereby every dict describes the **tth** to the related objects at the current time step, for details see chapter **TTC / TTH** |
| **ttc_dict_vec** | List of dicts, whereby every dict describes the **ttc** to the related objects at the current time step, for details see chapter **TTC / TTH** |
| **lat_dist_dict_vec** | List of dicts, whereby every dict describes the **lateral distance** to the related objects at the current time step, for details see chapter **Lateral and Longitudinal Position between Objects** |
| **long_dist_dict_vec** | List of dicts, whereby every dict describes the **longitudinal distance** to the related objects at the current time step, for details see chapter **Lateral and Longitudinal Position between Objects** |



### Example
```python

dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)
dynObject = dynObjectList[-1]

print(dynObject.x_vec)
print(dynObject.y_vec)
print(dynObject.vx_vec)
print(dynObject.vy_vec)
print(dynObject.psi_vec)
print(dynObject.ax_vec)
print(dynObject.ay_vec)
print(dynObject.length)
print(dynObject.width)
print(dynObject.time)
print(dynObject.UUID)
print(dynObject.delta_t) 

```

To keep the size of the dataset files as small as possible the data of the objects is only provided for the time intervale where the object is visitable in the video recording. Therefore, the first element in the time vector is the entry time and the last element the time of exit. 


## Dynamic objects utilities 
To allow an easy access to objects, the following methods are implemented. 


### Total objects included
Returns the total number of included objects
```python
len(dynWorld)
```

### Get all objects at a specific time
Gives you a list of all objects which are included in the first second of the recording.
```python
dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)
```

### Get specific timestamps of an object
```python
print(dynObject.get_first_time()) # Returns the time the object occurs the first time
print(dynObject.get_last_time()) # Returns the time the object occurs the last time
print(dynObject.is_visible_at(10)) # Checks if the object is visible at the given time
```

### Convert a time step to a vector index

To access the object vector based on a defined time step. You can use the function ```next_index_of_specific_time``` to convert a given time into the index of the data vectors at that given time, like

```python
time_vec = np.arange(dynObject.get_first_time(),
                      dynObject.get_last_time(),
                      dynObject.delta_t)
# Print positions
x_vec = dynObject.x_vec
y_vec = dynObject.y_vec
for time in time_vec:
    idx = dynObject.get_object_relation_for_defined_time(time)
    print("At time %0.2f the vehicle is at position %0.2f, %0.2f" % (time, x_vec[idx], y_vec[idx]))
```

## Object to lane assignment (OTLA)
The object-lane mapping is calculated for each object in each time step with the corresponding lane ID.

The x and y position of the object is used as a reference. Thus, the time stamp at which the lane ID changes is when that position passes over the lane marker. 

The lane ID / road ID is defined by the static world of *xodr*, for more details see the static world chapter. Where all lane IDs with the same sign (e.g. positive) belong to one driving direction. Absolutely low IDs belong to a lane closer to the center of the road (between driving directions). Note that a lane ID does not have to start at 0, as there may also be an unnavigable lane near the center of the road. 


**To access the Lane ID use:** 
```python
print(dynObject.lane_id_vec) 
print(dynObject.road_id_vec)  
```

## Distance to lane marking
For each object the current distances were calculated to the next left and right lane marking from ego view.
![](docs/lane_distance.png)

```dl``` and ```dr``` are defined as the orthogonal distance from the center of gravity of the car to the next lane marking. 



## Object Relations 

The object relation describing the relative position between object based on a view of one defined vehicle:

![](docs/ObjectRelation.png)


The object relation are defined as dict of \<relation name\>:\<UUID of other object\>. If an object has no relation to an other then the element is still in the dict, however, the value is ``` None```. 

```python
[ 
    { # Time step 0
        'front_ego': None,
        'behind_ego': '4bc73813-79bc-413c-87ec-e9048514079f',
        'front_left': None,
        'behind_left': None,
        'front_right': None,
        'behind_right': '0df4550c-a21b-4c38-bee3-e03ef4d59afc',
    },
    { #Time step 1
        'front_ego': None,
        'behind_ego': '4bc73813-79bc-413c-87ec-e9048514079f',
        'front_left': None,
        'behind_left': None,
        'front_right': None,
        'behind_right': '0df4550c-a21b-4c38-bee3-e03ef4d59afc',
    } 
    ...
]


```

Therefore, the access is as followed
```python
object_relation_dict = dynObject.object_relation_dict_list[0] 
print(object_relation_dict["front_ego"])
print(object_relation_dict["behind_ego"])
print(object_relation_dict["front_left"])
print(object_relation_dict["behind_left"])
print(object_relation_dict["front_right"])
print(object_relation_dict["behind_right"])
```

## Lateral and Longitudinal Position between Objects

Since the datasets consists also roads with a curvature, objects are not aligned to the coordinate system. Therefore, the lateral and longitudinal distance to the sounding objects in included in new datasets:


![](/docs/Lat_Long_Distance.png)



```python
[ 
    { # Time step 0
        'front_ego': None,
        'behind_ego': '11.3453242342',
        'front_left': None,
        'behind_left': None,
        'front_right': None,
        'behind_right': '12.23107814',
    },
    { #Time step 1
        'front_ego': None,
        'behind_ego': '11.238790123',
        'front_left': None,
        'behind_left': None,
        'front_right': None,
        'behind_right': '12.239001724',
    } 
    ...
]


```

If the data is not included, the lateral and longitudinal distance can be calculated by the function ``get_lat_and_long``. 




```python
dynObject2 = dynObjectList[1]

long_distance, lat_distance = dynObject.get_lat_and_long(1.0, dynObject2)
print(long_distance, lat_distance)

```

## TTC and TTH
For each object the current ```TTC``` and ```TTH``` is calculated **only to every in  ```front``` driving object**. 

![](docs/ttc.png)

The distance ```d``` as base of all calculations is defined as the closest distance of both vehicle centers ```'d```. To compensate for the vehicle length, ```l/2``` of each vehicle was substracted from ```'d```.

### TTC
```TTC``` is calculated as ```d``` / ```velocity difference```. 

If the front car is moving faster than the ego vehicle, a collision is impossible an the ```TTC``` is marked as ```-1```.

### TTH
```TTH``` is calculated as ```d``` / ```velocity ego```. 



# Static World 
We implemented a basic parser for *xodr* with some additional functionality. This parser stores the relevant information in the so called Static World. As the Dynamic World the Static World can be accessed by the dataset class:

```python
statWorld = dataset.statWorld
```

The Static World consist of a hierarchically structure of different classed to represents the *xodr*. Further information of *xodr* can be found **[here.](https://www.asam.net/index.php?eID=dumpFile&t=f&f=4422&token=e590561f3c39aa2260e5442e29e93f6693d1cccd#top-792f18a2-f184-4906-8ba0-717c09b36673)**
We highly recommend to get a basic understanding of *xodr* if lane related information are used. 

To get a fast and good view of an ```xodr``` we highly recommend the easy **[OpenDriveViewer](https://odrviewer.io)** to open and analyze the ```xodr``` files. 

![](docs/open_drive_viewer.png)



# Visualization

This package provides an integrated visualization of the dataset via a web server realized by bokeh.


If you installed the package via pip simply starte the visualization by typing:
```
automatum_vis
```
To start the visualization manually execute the ```start_bokeh.py``` script form the [package source](https://bitbucket.org/automatum/open.automatum.dronedata/src/master/). 

To open a dataset simple copy the absolute path of the dataset folder into the text filed on the top of the webpage. 
By clicking load the dataset will be loaded and visualized. Give it some seconds to load....

![](docs/vis_load.png)

After loading a dataset you should get a comparable view:

![](docs/vis_overview.png)

If you scroll down you find the panel where you can control a live view of the data:
- With Play/Pause you start/stop the animation. 
- With the arrows bellow you can step a single frame.
- The slider allows to change the playback speed.
- The two check boxes allow to show additional data. 
- The "Jump to time" box allows it to jup directly to a picture of interest. 

![](docs/vis_control.png)

Show object relations prints all present relation to each object:

![](docs/vis_object_relations.png)


Show distance lane markings prints the current orthogonal distances of each car to the current lane:

![](docs/vis_lane_marking.png)

To get a lange change, please zoom into the overview picture and hover to a red dot which is indicating a lane change:

![](docs/vis_lane_change.png)

The info box is telling you the UUID of the object which is performing the lane change and also the time step when this is happening. With the time step you can use the "Jump" box to show this time step in the animation. 

# Complete Example
Here you find the complete example of all code snipets from above:

```python
from openautomatumdronedata.dataset import droneDataset
import os
import numpy as np


path_to_dataset_folder = os.path.abspath("datasets/hw-a9-stammhamm-015-39f0066a-28f0-4a68-b4e8-5d5024720c4e")
dataset = droneDataset(path_to_dataset_folder)

dynWorld = dataset.dynWorld

print(dynWorld.UUID)
print(dynWorld.frame_count)
print(dynWorld.fps)
print(dynWorld.delta_t)
print(dynWorld.utm_referene_point)
print(dynWorld.maxTime)
print(dynWorld.DrivenDistanceInMeter)
print(dynWorld.MedianDrivenDistanceInMeter)
#print(dynWorld.dynamicObjects) # Possible but not recommended. Use further discussed functions.

dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)
dynObject = dynObjectList[-1]

print(dynObject.x_vec)
print(dynObject.y_vec)
print(dynObject.vx_vec)
print(dynObject.vy_vec)
print(dynObject.psi_vec)
print(dynObject.ax_vec)
print(dynObject.ay_vec)
print(dynObject.length)
print(dynObject.width)
print(dynObject.time)
print(dynObject.UUID)
print(dynObject.delta_t) 

len(dynWorld) # Returns the number of included object
dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)

print(dynObject.get_first_time()) # Returns the time the object occurs the first time
print(dynObject.get_last_time()) # Returns the time the object occurs the last time
print(dynObject.is_visible_at(10)) # Checks if the object is visible at the given time
 
time_vec = np.arange(dynObject.get_first_time(),
                      dynObject.get_last_time(),
                      dynObject.delta_t)
# Print positions
x_vec = dynObject.x_vec
y_vec = dynObject.y_vec
for time in time_vec:
    idx = dynObject.next_index_of_specific_time(time)
    print("At time %0.2f the vehicle is at position %0.2f, %0.2f" % (time, x_vec[idx], y_vec[idx]))


print(dynObject.lane_id_vec)  
print(dynObject.road_id_vec) 

object_relation_dict = dynObject.object_relation_dict_list[0] 
print(object_relation_dict["front_ego"])
print(object_relation_dict["behind_ego"])
print(object_relation_dict["front_left"])
print(object_relation_dict["behind_left"])
print(object_relation_dict["front_right"])
print(object_relation_dict["behind_right"])

dynObject2 = dynObjectList[1]

long_distance, lat_distance = dynObject.get_lat_and_long(1.0, dynObject2)
print(long_distance, lat_distance)

statWorld = dataset.statWorld 
```
# Disclamer

The implementation of *xodr* via the ```automatum_vis``` can show artefacts or road elements are displayed incorrectly. The *xodr* itself is generated using IPG's *CarMaker* tool and is fully represented. Also not all road elements of the standard are implemented to be shown. 



