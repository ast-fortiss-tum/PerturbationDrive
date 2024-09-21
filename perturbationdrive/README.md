# PerturbationDrive Docs

This ReadMe provides documentation over all functionalities in the perturbation drive folder.

## Table of Contents

- [Image Perturbations](#image-perturbations)
  - [ImagePerturbation Controller](#imageperturbation-controller)
  - [Example](#image-perturbation-example)
- [Simulator](#simulator)
  - [PerturbationSimulator](#perturbationsimulator)
  - [Scenario](#scenario)
  - [ScenarioOutcome](#scenariooutcome)
  - [ImageCallBack](#imagecallback)
- [Automated Driving System](#ads)
- [RoadGenerator](#roadgenerator)
- [PerturbationDrive Controller](#perturbationdrive-controller)
- [Utils](#utils)

## Image Perturbations

The file `perturbationfuncs.py` implements all image perturbations used in this work. Note, that this library uses [OpenCV Python](https://pypi.org/project/opencv-python/) for performing perturbations and hence each method expects an image per OpenCV specification. This is an image with 3 color channels and the dtype `uint8`.
Each perturbation needs an input image and the scale of the perturbation as input. The scale is in the range from 0 to 4. The following table details all perturbations of this library.

| Function Name | Description |
| --------------- | --------------- |
| gaussian_noise          | Statistical noise having the probability density function of the normal distribution     |
| poisson_noise           | Statistical noise having the probability density function of the Poisson distribution     |
| impulse_noise           | Random, sharp, and sudden disturbances, taking the form of scattered bright or dark pixel     |
| defocus_blur            | Simulates the effect of the lens being out of focus via circular disc-shaped kernels     |
| glass_blur              | Simulates the effect of viewing an image through a frosted glass     |
| motion_blur             | Simulates of streaking effect in one direction of the image     |
| zoom_blur               | Simulates a radial blur which emanates from a central point of the image     |
| increase_brightness     | Simulates increased brightness by altering the images value channel     |
| contrast                | Increases the difference in luminance on the image     |
| elastic                 | Moves each image pixel by a random offset derived from a Gaussian distribution     |
| pixelate                | Divides the image into square regions and all pixels in a region get assigned the average pixel value of the region     |
| jpeg_filter             | JPEG compression artifacts     |
| shear_image             | Horizontally replaces each point if a fixed direction by an amount proportional to its signed distance from a given line parallel to that direction     |
| translate_image         | Moves every pixel of the image by the same distance into a certain direction     |
| scale_image             | Increases or decreases the size of an image by a certain factor     |
| rotate_image            | Rotates the image by a certain angle in the euclidean space     |
| fog_mapping             | Applies fog effect to an image using the Diamond-Square algorithm.     |
| splatter_mapping        | Randomly adds black patches of varying size on the image     |
| dotted_lines_mapping    | Randomly adds straight dotted lines on the image     |
| zigzag_mapping          | Randomly adds black zig-zag lines on the image     |
| canny_edges_mapping     | Applies Canny edge detection to highlight images and lay them over the image     |
| speckle_noise_filter    | Granular noise texture degrading the quality of the image     |
| false_color_filter      | Swaps color channels of the image, inverts each color channel or average each color channel with the other channels     |
| high_pass_filter        | Retains high frequency information in the image while reducing the low frequency information in the image, resulting in sharpened image     |
| low_pass_filter         | Calculates the average of each pixel to its neighbors     |
| phase_scrambling        | Also called power scrambling, scrambles all image channels by using Fast Fourier Transform     |
| histogram_equalisation  | Spreads out the pixel intensity in an image via the images histogram resulting in enhancing the contrast of the image     |
| reflection_filter       | Creates a mirror effect to the input image and appends the mirrored image to the bottom of the image     |
| white_balance_filter    | Globally adjusts the intensity of image colors to render white surfaces correctly     |
| sharpen_filter          | Enhances local regions and removes blurring by using the sharpen kernel      |
| grayscale_filter        | Converts all colors to gray tones     |
| posterize_filter        | Reduces the number of distinct colors while maintaining essential image features by quantization of color channels     |
| cutout_filter           | Inserts random black rectangular shapes over the image     |
| sample_pairing_filter   | Randomly samples two regions of the image together. The sampled regions are blended together with a varying alpha value     |
| gaussian_blur           | Blurs the image by applying the Gaussian function on the image     |
| saturation_filter       | Increases or decreases the saturation of the image by increasing or decreasing the saturation channel of the image in the HSV (hue, saturation, lightness) representation of the image     |
| saturation_decrease_filter | Increases or decreases the saturation of the image by increasing or decreasing the saturation channel of the image in the HSV (hue, saturation, lightness) representation of the image  |
| fog_filter              | Simulates fog by reducing the image's contrast and saturation     |
| frost_filter            | Simulates the appearance of frost patterns which form on surfaces during cold conditions     |
| snow_filter             | Simulates the effect of snow falling by artificially inserting snow crystals     |

All of these functions share same parameters and return value:

- Parameters
  - scale: int. Perturbation intensity on a range from 0 to 4.
  - image: ndarray[Any, dtype[dtype=uint8]]. Image which should be perturbed wth pixel values in the range from 0 to 255.
- Returns
  - image: ndarray[Any, dtype[dtype=uint8]]. Perturbed image with pixel values in the range from 0 to 255.

### ImagePerturbation Controller

The class `ImagePerturbation` provides a class interface for performing perturbations on images. This is also the controller used in this framework to provide easy to access perturbations. Note, that this class also provides access to the more advanced perturbations, such as Dynamic Perturbations, Generative Perturbations and Perturbations based on the Attention Map.

#### ImagePerturbation.Class

When the class is initialized, all models for generative perturbations (such as Neural Style Transfer or CycleGAN) are loaded into memory. Furthermore the buffer for applying dynamic perturbations is initialized and all frames are stored in the buffer. Only when the user specified generative perturbations or dynamic perturbations, this preprocessing step is applied.
This class has the following parameters:

- `funcs` (`List[str]`, default: `[]`): List of the function names we want to use as perturbations. If this list is empty, all perturbations from the table above are used.
- `attention_map` (`dict(map: str, model: tf.model, threshold: float, layer: str)`, default: `{}`): States if we perturbated the input based on the attention map and which attention map to use. Possible arguments for map are `grad_cam` or `vanilla`. If you want to perturb based on the attention map you will need to speciy the model, attention threshold as well as the map type here. You can use either the vanilla saliency map or the Grad Cam attention map. If this dict is empty we do not perturb based on the saliency regions. The treshold can be empty and is 0.5 per default. The default layer for the GradCam Map is `conv2d_5`.
- `image_size` (`Tuple[float, float]`: default: `(240, 320)`). Input image size for all perturbations.

By creating a subclass, one can extend the perturbations used in this library. Note, that the minimum requirement for the subclass are implenting the `perturbation` function.

The table below details all function names of the generative and dynamic perturbations

| Function Name | Description |
| --------------- | --------------- |
| candy          |  Applies Neural Styling in this style   |
| la_muse          |  Applies Neural Styling in this style    |
| mosaic          |   Applies Neural Styling in this style   |
| feathers          |  Applies Neural Styling in this style    |
| the_scream          |  Applies Neural Styling in this style    |
| udnie          |  Applies Neural Styling in this style    |
| sim2real          |  Converts images from the SDSandbox Donkey USCII Track to the domain of real world images   |
| dynamic_snow_filter          | Adds artificial snow fall to the input image sequence    |
| dynamic_rain_filter          | Adds artificial rain fall to the input image sequence    |
| dynamic_sun_filter          | Artificially moves a sun across the input image sequence    |
| dynamic_lightning_filter          | Generates multiple lightning strikes over the input image sequence    |
| dynamic_smoke_filter          | Adds artificial smoke clouds to the input image sequence    |

#### ImagePerturbation.perturbation

Perturbs the input image based on the function name given. This class has the following parameters:

- `image` (`ndarray[Any, dtype[dtype=uint8]]`): Input image
- `perturbation_name` (`str`): Name of the perturbation to apply. If the string is empty, no perturbation will be appliesd. All possible perturbation names are detailed in the perturbation tables of this seection.
- `intensity`: (`int`). Perturbation intensity on a range from 0 to 4.

Returns:

- `ndarray[Any, dtype[dtype=uint8]]` The perturbed image resized to the `image_size` dimensions.

### Image Perturbation Example

```Python
from perturbationdrive import poisson_noise, gaussian_noise, ImagePerturbation
import cv2
import numpy as np

height, width = 240, 320
random_image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

# perform perturbations
poisson_img = poisson_noise(0, random_image)
cv2.imshow("Poisson Noise", poisson_img)

gaussian_img = gaussian_noise(4, random_image)
cv2.imshow("Gaussian Noise", gaussian_img)

# this example will fail because the intensity is out of bounds
gaussian_img = gaussian_noise(-1, random_image)

# used the controller for perturbation

controller1 = ImagePerturbation(funcs=["candy", "poisson_noise"])
candy_img = controller1.perturbation(random_image, "candy", 2)

# perturb the image based on the attention map
import tensorflow as tf

# Note: This is a dummy model and does not work
demo_model = tf.keras.Model(inputs=inputs, outputs=outputs)
controller2 = ImagePerturbation(funcs=["candy", "poisson_noise"], attention_map={"map": "grad_cam", "model": demo_model, "threshold": 0.4})
poisson_img = controller1.perturbation(random_image, "poisson_noise", 2)

# this example will fail, because the intensity is out of bounds
__ = controller1.perturbation(random_image, "poisson_noise", 5)
```

### ImagePerturbation Controller Extension

To extend the perturbations used in this library, one can create a subclass of the `ImagePerturbation` class. By overriding the `perturbation` method, one can intercept perturbation calls and add custom functionality.
The following example shows how to create a subclass for a new perturbation called `blackout` (changes all pixel values to black).

```Python
from perturbationdrive import ImagePerturbation
import numpy as np
from typing import List, Tuple, Any

class BlackoutPerturbation(ImagePerturbation):
    def __init__(
        self, 
        funcs: List[str] = [], 
        attention_map: dict = {}, 
        image_size: Tuple[float, float] = (240, 320)
    ):
        # Perform any custom initialization here needed for your perturbation
        print("Custom initialization")
        super().__init__(funcs, attention_map, image_size)

    def perturbation(
        self, 
        image: np.ndarray,
        perturbation_name: str,
        intensity: int
    ) -> np.ndarray[Any, np.dtype[np.uint8]]:
        if perturbation_name != "blackout":
            return super().perturbation(image, perturbation_name, intensity)
        return np.zeros_like(image)

random_image = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
# use the custom perturbation
controller = BlackoutPerturbation(["gaussian_noise"])
# call the blackout perturbation
blackout_img = controller.perturbation(
    random_image, 
    "blackout", 
    2
)
# call the gaussian noise perturbation
# the call will be forwarded to the parent class
gaussian_img = controller.perturbation(
    random_image, 
    "gaussian_noise", 
    2
)
```

## Simulator

The directory `Simulator/` provides all interfaces for running end to end tests in simulators, specifying scenarios and receiving the output of the simulated scenario.

### PerturbationSimulator

`PerturbationSimulator` serves as an abstract base class for creating simulator adapters. It is designed for automated driving system (ADS) simulations, where various scenarios with and without image perturbations are applied to evaluate and test ADS behavior in end to end tests. By creating a subclass for this abstract base class and implementing all methods a new simulator can be integrated into this library.
For examples on creating subclasses of the `PerturbationSimulator` see the examples `examples/udacity` and `examples/self_driving_sandbox_donkey`.

#### PerturbationSimulator.Class

Initilizer for the PerturbationSimulator object. The following

- `max_xte: float` (default = 2.0):
    Maximum cross-track error allowed.
- `simulator_exe_path: str`(default = ""):
    Path to the simulator executable.
- `host: str` (default = "127.0.0.1"):
    Host address for connecting to the simulator.
- `port: int` (default = 9091):
    Port number for the connection.
- `initial_pos: Union[Tuple[float, float, float, float], None]` (default = None):
    Initial position in the format (x, y, z, angle).

#### PerturbationSimulator.connect

Abstract method to connect the simulator instance to the simulator binary. If necessary, launch the binary here and perform all steps needed to ensure a connection. Does not take any parameters.

#### PerturbationSimulator.simulate_scenario

Simulates a single scenario and returns a scenario outcome. Has the following parameters

- `agend: ADS`
    The agent which is tested in this scenario. See [ADS](#ads) for the ADS definition.
- `scenario: Scenario`
    The scenario which should be evaluated on the agent. Before the agent performs any actions in the simulator, this scenario should be build in the simulator. See [Scenario](#scenario) for the scenario definition.
- `perturbation_controller: ImagePerturbation`
    The perturbation controller which is used to perturb the input of the ADS. See [ImagePerturbation](#imageperturbation-controller) for more details.

Returns

- `ScenarioOutcome`: The result of the simulation

#### PerturbationSimulator.tear_down

Tears down the connection to the simulator. If a binary was launched in `connect` this binary should be cleaned up and quit.

### Scenario

The `Scenario` data class is designed to model a scenario in the context of automated driving system (ADS) simulations. It is made up of the waypoints defining the road of the scenario, perturbation function, and perturbation scale. The class has the following parameters:

- `waypoints: Union[str, None]`
    The waypoints define the road of the scenario. All wypoints are made up of (x, y, z)-coordinates seperated by `@`, e.g. `1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0`. If the waypoints are None, the default track of the scenario is used.
- `perturbation_function: str`
    Defines the perturbation of the scenario. Possible perturbation names are all detailed in the tables of section [Image Perturbations](#image-perturbations).
- `perturbation_scale: int`
    Defines the intensity of the perturbation. Must be in the range of `[0;4]` with 0 being a lowest intensity and 4 being the highest intensity.

### ScenarioOutcome

The `ScenarioOutcome` data class defines the result of running a scenario in a simulator. It should be generated when running a simulation. The class has the following parameters:

- `frames: List[int]`
    The frames of the simulation. Is an ordered list starting from 0 going up until the last frame of the perturbation.
- `pos: List[Tuple[float, float, float]]`
    The (x, y, z)-position of the vehicle at every frame of the simulation.
- `xte: List[float]`
    The Cross Track Error of the vehicle at every frame of the simulation. Used as performance measure.
- `speeds: List[float]`
    The speed of the vehicle at every framne of the simulation.
- `actions: List[List[float]]`
    The actions take by the `ADS` at every frame of the simulation. The first value of the list is the steering angle and the second value is the throttle.
- `scenario: Union[Scenario, None]`
    The scenario which has been simulated.
- `isSuccess: bool`
    Binary indicator stating if the scenario resulted in a success or failure.
- `timeout: bool`
    Binary indicator stating if the scenario resulted in a timeout.

Note, that all lists must be of the same length.

Example ScenarioOutcome and Scenario.

```Python
from perturbationdrive import Scenario, ScenarioOutcome

scenario = Scenario(
    waypoints="1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0",
    perturbation_function="gaussian_noise",
    perturbation_scale=1,
)

res = ScenarioOutcome(
    frames=[1, 2, 3],
    pos=[(1., 1., 1.), (1., 2., 1.), (1., 3., 1.)],
    xte=[0.1, 0.2, 0.3],
    speeds=[0.0, 0.1, 0.1],
    actions=[[0.1, 0.1], [0.01, 0.1], [0.15, 0.1]],
    scenario=scenario,
    isSuccess=True,
    timeout=False,
)
```

### OfflineScenarioOutcome

The `OfflineScenarioOutcome` data class defines the result of running a based test on an image. Here we test the model under test on a image which is perturbed to evaluate the difference in driving commands on the perturbed image, the image which has not been perturbed and the grund truth driving actions. This class has the following parameters.

- `image_file_name: str`
    Path to the image used for testing
- `json_file_name: str`
    Path to the json containing the ground truth actions on the image
- `perturbation_function: str`
    Name of the function to perturb the input
- `perturbation_scale: int`
    Intensity of the perturbation on the image
- `ground_truth_actions: List[float]`
    Ground truth actions, e.g. taken by a human driver
- `perturbed_image_actions: List[float]`
    Actions of the model based on the perturbed image
- `normal_image_actions: List[float]`
    Actions of the model based on the normal image

### ImageCallBack

The `ImageCallBack` class provides functionality to view images and text messages on a `pygame` window. This project uses this functionality to display the pertubed image and the actions of the `ADS` during the simulation.

#### ImageCallBack.Class

The `ImageCallBack` class takes the following parameters at initialization.

- `channels: int` (default: 3)
    Amount of color channels on the images displayed.
- `rows: int` (default: 240)
    Height of the images diaplyed in pixels.
- `cols: int` (default: 320)
    Width of the images displayed in pixels.

#### ImageCallBack.display_img

Displays the image and the steering and throttle value

- `img: ndarray[Any, dtype[dtype=uint8]]`
    Image to display
- `steering: str`
    String value of the current steering angle
- `throttle: str`
    String value of the current throttle value
- `perturbation: str`
    Function name of the current perturbation function

#### ImageCallBack.display_waiting_screen

Displays the message `Waiting for the simulator to start` on a black screen. Takes no parameters.

#### ImageCallBack.display_disconnect_screen

Displays the message `Simulator disconnected` on a black screen. Takes no arguments

#### Example

```Python
from perturbationdrive import ImageCallBack
import time

callback = ImageCallBack(3, 220, 220)

callback.display_waiting_screen()

# generate random image
random_image = np.random.randint(0, 256, (220, 220, 3), dtype=np.uint8)
# display random image for 10 seconds
for _ in range(10):
    callback.display_img(random_image, "2", "1", "None")
    time.sleep(1)

callback.display_disconnect_screen()
```

## ADS

`ADS` (Automated Driving System) is an abstract base class designed to simulate the behavior of automated driving systems. It acts as interface for creating implementations of end to end driving systems based on images from a single front facing camera.

This repo contains an example agent implementation in the folder `/examples/ads/` and examples on training such an agent.

### ADS.Class

Initialized the ADS. Here one should load the model and store it in memory as well as warm up the model for faster computation during simulation. Does not have any parameters.

### ADS.action

This method represents a single action step for the automated driving system. It takes as input a image from a single front facing camera in the form of a OpenCV image and outputs an action in the form of a steering angle and throttle value. Takes the following parameters

- `input: ndarray[Any, dtype[uint8]]`
    The image from the single front facing camera of the vehicle as OpenCV image.

Returns:

- `Tuple[Tuple[float, float]]`
    A tuple of tuple pf actions or decisions made by the automated driving system based on the input image. The first tuple value is the steering angle and the second tuple value is the throttle value.

## RoadGenerator

`RoadGenerator` is an abstract base class (ABC) designed for generating new roads in simulations involving automated driving systems (ADS). It provides a standardized approach for creating diverse road scenarios.
The RoadGenerator interface can be used within the `PerturbationDrive Controller` to generate road for a `Scenario`.
All road generators used in this project are implemented simulator independent and can be used with the simulator examples provided in `examples/`.

### RoadGenerator.generate

Abstract method of the `RoadGenerator` interface. This method returns a road string for track generation. It has the following parameters:

- `starting_pos: Tuple[float, float, float, float]`
    Float values of the initial position (x, y, z, width) of the road. This position should correlate with the starting position of the vehicle in the scenario.
- `*args`
    List of freely choosable parameters.
- `**kwargs`
    List of freely choosable keyword parameters.

Returns:

- `str` Returns the string representation of the generated track. The track is defined by its waypoints in (x, y, z)-coordinates and each waypoint is seperated by `@`, e.g. `1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0`.

### RandomRoadGenerator

Implementation of the `RoadGenerator` interface. Generates a random road of choosable length from the selected starting position by randomly generating a set of control nodes and then fitting a Catmull-Rom Spline through all control nodes.

#### RandomRoadGenerator.Class

The class takes the following parameters to configure randomly generated roads:

- `num_control_nodes: int` (default=8)
    Amount of control nodes of the road. The control nodes defines the road shape. Needs to be greater than 1.
- `max_angle: int` (default=90)
    Maximum angle between two different control nodes. Needs to be in range of [0, 360].
- `seg_length: int` (default=25)
    Length between two adjecent control nodes. Needs to be greater than 0.
- `num_spline_nodes: int` (default=20)
    Amount of splines points generated by the Catmull-Rom Spline between the adjacent control nodes. Needs to be greater than 0.
- `initial_node: Tuple[float, float, float, float]` (default=(.0,.0,.0,.0))
    Starting position of the road.

#### RandomRoadGenerator.generate

Generates a random road given a starting position and outputs the string of the road. Takes the following parameters

- `starting_position: Tuple[float, float, float, float]`
    Starting position of the road. This position should correlate with the starting position of the vehicle in the scenario.

Returns:

- `str` Returns the string representation of the generated track. The track is defined by its waypoints in (x, y, z)-coordinates and each waypoint is seperated by `@`, e.g. `1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0`.

#### RandomRoadGenerator Example

```Python
from perturbationdrive import RandomRoadGenerator

generator = RandomRoadGenerator(
    num_control_nodes=10,
    max_angle=60,
    seg_length=15,
    num_spline_nodes=10,
    initial_node=(1.0, 0.0, 0.0, 0.0)
)

generator.generate(starting_pos=(1.0, 2.0, 0.0, 0.0))
```

### CustomRoadGenerator

Implementation of the `RoadGenerator` interface. Generates a road by building the road consisting of a set of waypoints via the given angles and length between two adjacent waypoints. Once all waypoints are generated, a Catmull-Rom Spline is fitted through the road.

#### CustomRoadGenerator.Class

The class takes the following parameters:

- `num_control_nodes: int` (default=8)
    Amount of control nodes of the road. The control nodes defines the road shape. Needs to be greater than 1.
- `max_angle: int` (default=90)
    Maximum angle between two different control nodes. Needs to be in range of [0, 360].
- `seg_length: int` (default=25)
    Length between two adjecent control nodes. Needs to be greater than 0.
- `num_spline_nodes: int` (default=20)
    Amount of splines points generated by the Catmull-Rom Spline between the adjacent control nodes. Needs to be greater than 0.
- `initial_node: Tuple[float, float, float, float]` (default=(.0,.0,.0,.0))
    Starting position of the road.

#### CustomRoadGenerator.generate

Generates a road given a starting position, angles between adjacent waypoints and the segmant lengths between adjacent waypoints and outputs the string of the road. Takes the following parameters

- `starting_position: Tuple[float, float, float, float]`
    Starting position of the road. This position should correlate with the starting position of the vehicle in the scenario.
- `angles: List[int]`
    List of the angles between the adjacent waypoints.
- `seg_lengths: Union[List[int], None]`
   Optional list of the segment length between the adjacent waypoints.

Returns:

- `str` Returns the string representation of the generated track. The track is defined by its waypoints in (x, y, z)-coordinates and each waypoint is seperated by `@`, e.g. `1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0`.

#### CustomRoadGenerator Example

```Python
from perturbationdrive import CustomRoadGenerator

generator = CustomRoadGenerator(
    num_control_nodes=10,
    max_angle=60,
    seg_length=15,
    num_spline_nodes=10,
    initial_node=(1.0, 0.0, 0.0, 0.0)
)

generator.generate(
    starting_pos=(1.0, 2.0, 0.0, 0.0),
    angles=[10, 10, 0, 0, -10, -10, -15, 0, 15, 0],
    seg_lengths=[10, 10, 4, 3, 10, 10, 10, 15, 20, 10],
)
```

## PerturbationDrive Controller

Performs the robustness benchmarking of an ADS by either simulating scenarios in a simulator to perform end to end tests or by iterating over a given dataset to perform model based testing. The ADS is an end to end system, performing actions on the camera image of a single front facing camera. The robustness of the ADS is tested by applying common image perturbations on the input of the ADS.

Note that most of the examples in this section cannot be run due to the usage of `ExampleSimulator` and `ExampleADS`. These classes are placeholders for the actual simulator and ADS used in the examples. For plug and play examples refer to the [Self Driving Sandbox Example](https://github.com/HannesLeonhard/PerturbationDrive/tree/main/examples/self_driving_sandbox_donkey#interface-with-perturbationdrive) or [Udacity Example](https://github.com/HannesLeonhard/PerturbationDrive/blob/main/examples/udacity/README.md#interface-with-perturbationdrive).

### PerturbationDrive.class

The class has the following attributes

- `simulator: PerturbationSimulator`
    Interface to the simulator in which the ADS is tested as defined in section [Simulator](#simulator)
- `ads: ADS`
    System under test as defined in section [ADS](#ads)

### PerturbationDrive.grid_search

Performs a grid search over the search space of perturbations and roads configured as search parameters to find failure cases and determine space within the ADS performs well. The grid search method is highly customizable via the `GridSearchConfig` and follows the following control flow:

1) Initializes the perturbation controller class provided in the config. Per default, the `ImagePerturbation` class is used but any valid subclass can be used.
2) Established a connection to the simulator and waits for the connection to establish.
3) Constructs the initial road waypoints based on the road generator provided in the config. If no road generator is provided, the default road of the simulator is used.
    - The `generate` method of the road generator receives the following parameters: 1. The initial position of the ADS in the simulator. 2. The `road_angles` and `road_lengths` lists of the config. 3. A list of prior simulation results of the grid search. For the initial road generation, this list is empty.
4) Initializes the index pointing to the current perturbation (out of all perturbations provided in the config) with 0 and sets the perturbation scale to 0.
5) Performs the grid search controll flow
    1) Simulates the scenario with the current perturbation (based on the index) and road.
    2) Calls the `config.drop_perturbation(outcome)` lambda function to determine if the perturbation should be dropped from the list of perturbations. If the function returns True, the perturbation is removed from the list else the index is incremented.
    3) If the index is equal to the length of the perturbation list, then
        1) The `config.increment_perturbation_scale(outcomes)` lambda function is called to determine if the perturbation scale should be incremented. If the function returns True, the perturbation scale is incremented and the index is reset to 0 else the index is reset to 0 and the scale not incremented.
        2) If the `config.road_generation_frequency` is set to `RoadGenerationFrequency.AFTER_EARCH_INTENSITY_ITERATION` then the `generate` method of the road generator is called to generate a new road based on the current simulation results.
    4) If either the perturbation scale is equal to 5 or all perturbations have been droped, the grid search loop is terminated.
    5) If the `config.road_generation_frequency` is set to `RoadGenerationFrequency.AFTER_EARCH_INTENSITY_ITERATION` then the `generate` method of the road generator is called to generate a new road based on the current simulation results.
6) Prints a summary of the grid search results to the terminal.
7) Tears down the simulator connection.
8) If a log directory is provided, the results are written to the log file else the simulation outcomes are returned.

Parameters:

- `config: GridSearchConfig`
    The configuration of the grid search allowing to highly customize the grid search to ones desire. The configuration is detailed in the following section.

Returns:

- `Union[None, List[ScenarioOutcome]]` Returns the results of all simulated scenarios if the `config.log_dir` is None, otherwise returns None.

#### GridSearchConfig

The `GridSearchConfig` class provides a configuration for the grid search method of the `PerturbationDrive` class. The class has the following parameters:

- `perturbation_functions: List[str]`
    List of perturbation functions to use. If this list is empty, all perturbation functions detailed in the table in [Image Perturbations](#image-perturbations) are used. Further, the empty perturbation is always included in the list.
- `attention_map: dict(map: str, model: tf.model, threshold: float, layer: str) = {}`
    Determines if the input image is perturbed on the attention map of the SUT or not. If the dict is empty, the input image is not perturbed based on the attention map. The parameters are identical to the [ImagePerturbation class](#imageperturbationclass).
- `road_generator: Union[RoadGenerator, None] = None`
    Road generator to generate new roads for the scenarios. If no road generator is provided, the default road of the simulator is used.
- `road_angles: List[int] = []`
    List of angles between the adjacent waypoints of the road. This list of waypoints is forwarded to the road_generator in road_generate.generate function calls.
- `road_lengths: List[int] = []`
    List of segment lengths between the adjacent waypoints of the road. This list of waypoints is forwarded to the road_generator in road_generate.generate function calls.
- `road_generation_frequency: RoadGenerationFrequency = RoadGenerationFrequency.ONCE`
    Frequency of generating new roads. The frequency can be set to `RoadGenerationFrequency.NEVER` (Never generate a road), `RoadGenerationFrequency.ONCE` (Generate a road once before the grid search), `RoadGenerationFrequency.AFTER_EARCH_INTENSITY_ITERATION` (Generate a road after each scale iteration) or `RoadGenerationFrequency.ALWAYS` (Generate a road after each perturbation function).
- `log_dir: Union[str, None] = "logs.json"`
    Optional directory to log the `ScenarioOutcome`s of each individual `Scenario`. If this param is None, the results are not written to a log file and returned from this method. If this is not None, the logs are written to the file and the `ScenarioOutcome` is not returned from this method.
- `overwrite_logs: bool = True`
    Boolean variable indicating if existing log files should be overwritten, if the `log_dir` already exists. If this is false and the file already exists, the `ScenarioOutcome`s are not written or returned and discarded.
- `image_size: Tuple[float, float] = (240, 320)`
    Image size of the input images during the scenario.
- `drop_perturbation: Callable[[ScenarioOutcome], bool] = lambda outcome: (not outcome.isSuccess) or outcome.timeout`
    Lambda function to determine if a perturbation should be dropped from the list of perturbations. The function receives a `ScenarioOutcome` and returns a boolean value. If the function returns True, the perturbation is removed from the list else the perturbation is kept.
- `increment_perturbation_scale: Callable[[List[ScenarioOutcome]], bool] = lambda outcomes: True`
    Lambda function to determine if the perturbation scale should be incremented after iterating over each perturbation on the current perturbation scale. The function receives a list of `ScenarioOutcome`s and returns a boolean value. If the function returns True, the perturbation scale is incremented else the perturbation scale is not incremented.

#### GridSearch Example

Example:

```Python
from perturbationdrive import (
    PerturbationDrive,
    CustomRoadGenerator,
    GridSearchConfig,
    RoadGenerationFrequency,
)
from examples.self_driving_sandbox_donkey.sdsandbox_simulator import SDSandboxSimulator
from examples.models.dave2_agent import Dave2Agent

# setup demo objects
simulator = SDSandboxSimulator(
    simulator_exe_path="./examples/self_driving_sandbox_donkey/sim/donkey-sim.app",
    host="127.0.0.1",
    port=9091,
    show_image_cb=True,
)
ads = Dave2Agent(model_path="./examples/models/checkpoints/dave_90k_v1.h5")
attention_map = {
    "map": "grad_cam",
    "model": ads.model,
    "threshold": 0.1,
    "layer": "conv2d_5",
}
road_angles = [0, -35, 0, -17, -35, 35, 6, -22]
road_segments = [25, 25, 25, 25, 25, 25, 25, 25]
road_generator = CustomRoadGenerator(num_control_nodes=len(road_angles))

benchmarking_object = PerturbationDrive(
    simulator=simulator,
    ads=ads,
)
config = GridSearchConfig(
    perturbation_functions=["gaussian_noise", "impulse_noise"],

)
# perform grid search as end to end test
benchmarking_object.grid_seach(
    config=config,
    attention_map=attention_map,
    road_generator=road_generator,
    road_angles=road_angles,
    road_segments=road_segments,
    road_generation_frequency=RoadGenerationFrequency.ONCE,
    log_dir=f"./logs/example_logs.json",
    overwrite_logs=True,
    image_size=(240, 320),
    drop_perturbation=(lambda outcome: (not outcome.isSuccess) or outcome.timeout),
    increment_perturbation_scale=(lambda outcomes: True),
)
```

### PerturbationDrive.simulate_scenarios

Simulates a list of scenarios on the simualtor using the SUT to generate actions during the scenario.

Parameters:

- `scenarios: List[Scenario]`
    The list of scenarios which are simulated.
- `attention_map: dict(map: str, model: tf.model, threshold: float, layer: str) = {}`
    Determines if the input image is perturbed on the attention map of the SUT or not. If the dict is empty, the input image is not perturbed based on the attention map. The parameters are identical to the [ImagePerturbation class](#imageperturbationclass).
- `log_dir: Union[str, None] = "logs.json"`
    Optional directory to log the `ScenarioOutcome`s of each individual `Scenario`. If this param is None, the results are not written to a log file and returned from this method. If this is not None, the logs are written to the file and the `ScenarioOutcome` is not returned from this method.
- `overwrite_logs: bool = True`
    Boolean variable indicating if existing log files should be overwritten, if the `log_dir` already exists. If this is false and the file already exists, the `ScenarioOutcome`s are not written or returned and discarded.
- `image_size: Tuple[float, float] = (240, 320)`
    Image size of the input images during the scenario.

Returns:

- `Union[None, List[ScenarioOutcome]]` Returns the results of all simulated scenarios if the `log_dir` is None, otherwise returns None.

Example:

```Python
from perturbationdrive import PerturbationDrive

# setup demo objects
simulator = ExampleSimulator()
ads = ExampleADS()

# demo scenarios
scenarios: List[Scenario] = getDemoScenario()

benchmarking_object = PerturbationDrive(
    simulator=simulator,
    ads=ads,
    perturbation_functions=["gaussian_noise", "impulse_noise"],
    attention_map={},
    road_generator=RandomRoadGenerator(),
    image_size=(240,240)
)

# perform grid search as end to end test
res: List[ScenarioOutcome] = benchmarking_object.simulate_scenarios(
    scenarios=scenarios,
    attention_map={},
    log_dir=None,
    overwrite_logs=False,
    image_size=(240,240)
)
```

### PerturbationDrive.offline_perturbation

Used as for model based testing. Iterates over all images, perturbations and perturbation intensity. On each unique combination of intensity, perturbation and image, we generate driving commands for the normal image and the perturbed image. These commands are stored for later evaluation along with the ground truth actions.
Generates an output in the form of an `OfflineScenarioOutcome` for each unique image and perturbation combination.

Specifications on the dataset:

- The dataset needs to contain the frames and a json file for each frame:
  - The images name needs to be in the format of "`frame number`_`free_string`.{jpg | jpeg | png}" where `free_string` can be any string with length of more than 1
  - The json file name needs to be in the format of "record_`frame number`.json" where the `frame number` needs to correlate to the image
  - The json file needs to contain the ground truth values for steering angle and throttle in the files `user/angle` and `user/throttle`

Parameters:

- `dataset_path: str`
    The path to the dataset.
- `perturbation_functions: List[str]`
    The set of perturbations functions to use. If this list is empty, all perturbation functions detailed in the table in [Image Perturbations](#image-perturbations) are used.
- `attention_map: dict(map: str, model: tf.model, threshold: float, layer: str) = {}`
    Determines if the input image is perturbed on the attention map of the SUT or not. If the dict is empty, the input image is not perturbed based on the attention map. The parameters are identical to the [ImagePerturbation class](#imageperturbationclass).
- `log_dir: Union[str, None] = "logs.json"`
    Optional directory to log the `ScenarioOutcome`s of each individual `Scenario`. If this param is None, the results are not written to a log file and returned from this method. If this is not None, the logs are written to the file and the `ScenarioOutcome` is not returned from this method.
- `overwrite_logs: bool = True`
    Boolean variable indicating if existing log files should be overwritten, if the `log_dir` already exists. If this is false and the file already exists, the `ScenarioOutcome`s are not written or returned and discarded.
- `image_size: Tuple[float, float] = (240, 320)`
    Image size of the input images during the scenario.

Returns:

- `Union[None, List[OfflineScenarioOutcome]]` Returns the results of all evaluated combinations of image, intensity, and perturbation function if the `log_dir` is None, otherwise returns None.

Example:

```Python
from perturbationdrive import PerturbationDrive

# setup demo objects
simulator = ExampleSimulator()
ads = ExampleADS()

# perform grid search as end to end test
res: List[OfflineScenarioOutcome] = benchmarking_object.offline_perturbation(
    dataset_path="./dataset/model_test/",
    perturbation_functions=["gaussian_noise", "impulse_noise"],
    attention_map={},
    log_dir=None,
    overwrite_logs=False,
    image_size=(240,240)
)
```

#### PerturbationDrive.offline_perturbation Dataset Specifications

Image Files

- Format: `{frame_number}_{free_string}.{extension}`
- Components:
  - {frame_number}: A unique identifier for each frame, typically a number. This should correlate directly with the frame number used in the corresponding JSON file.
  - {free_string}: Any string of length greater than one character. This part of the filename can be used for additional descriptive information or identifiers.
  - {extension}: The file extension, indicating the image format. Accepted formats are .jpg, .jpeg, or .png.

JSON Files

- Format: `record_{frame_number}.json`
- Components:
  - record_: A fixed prefix for all JSON files in the dataset.
  - {frame_number}: The same frame number as used in the corresponding image file. This ensures that each JSON file is correctly associated  ith its respective image.
  - .json: The file extension for JSON files.
- JSON File Content
  - Each JSON file must contain the following ground truth values:
    - `user/angle`: The steering angle.
    - `user/throttle`: The throttle value.

## Utils

This section provides documentation on the util scripts which can be used as part of this library.

### GlobalLog

The GlobalLog class is a utility designed for centralized logging across different modules in the PerturbationDrive project. It provides a standardized way to log messages, making it easier to track and debug the system's operations.

#### GloabalLog.class

Takes the following parameters:

- `logger_prefix: str`:
    A prefix used to identify the logger. This allows for the distinction between loggers from different modules.

Checks if a logger with the given prefix already exists. If not, it creates a new logger and sets it up with a specific logging level and format.
The logger is configured to output log messages to the standard output (stdout) using a StreamHandler. The format for log messages is set to display the log level, logger name, and the log message.

#### GloabalLog Functions

- `debug(self, message)`
    Logs a debug message. Useful for detailed information, typically of interest only when diagnosing problems.
- `info(self, message)`
    Logs an informational message. Used for general information about system operation.
- `warn(self, message)`
    Logs a warning message. Indicates that something unexpected happened, or indicative of some problem in the near future (e.g., 'disk space low'). The software is still working as expected.
- `error(self, message)`
    Logs an error message. Due to a more serious problem, the software has not been able to perform some function.
- `critical(self, message)`
    Logs a critical message. A serious error, indicating that the program itself may be unable to continue running.

#### GlobalLog Example

```Python
from perturbationdrive import GlobalLog

# create a new logger
logger = GlobalLog("ExampleLogger")
logger.info("This is an informational message")
logger.warn("This is a warning message")
logger.error("This is an error message")
```

### TrainCycleGAN

You can train your own cycle gan given a dataset of two image domains

```Python
from perturbationdrive import train_cycle_gan

train_cycle_gan(
    input_dir="./relative/path/to/folder",
    output_dir="./relative/path/to/folder",
    image_extension_input="jpg",
    image_extension_output="jpg",
    buffer_size=100,
    batch_size=2,
    early_stop_patience=None,
    epochs=50,
    steps_per_epoch=300,
)
```
