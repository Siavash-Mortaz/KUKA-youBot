# KUKA youBot (Color-Recognition and Object Placement)

![Logic Chart](https://github.com/Siavash-Mortaz/KUKA-youBot/blob/main/Images/Logic%20Chart.jpg)
The strategic workflow involves the robot initially surveying the environment via camera recognition color to identify objects. Subsequently, the robot must distinguish between tables and boxes (cubes) and recognize their respective colors. After identifying an object and determining its nature, the robot is guided to select a specific box, such as a red one, tracking, moving toward, and picking it up. This process repeats as the robot searches for an appropriate table, exemplified by a red table. Once located, the robot places the red box on it, resumes searching for other boxes, and positions them on designated tables. 
The project utilizes the Cyberbotics Ltd.'s webots software, a free and open-source 3D robot simulator widely employed in industry, education, and research.
![Environment](https://github.com/Siavash-Mortaz/KUKA-youBot/blob/main/Images/Environment.jpg)

![Camera](https://github.com/Siavash-Mortaz/KUKA-youBot/blob/main/Images/Camera.jpg)
 I integrated youBots into the simulated environment and added a basic camera to the robot's 'bodySlot.' The camera, positioned strategically below the KUKA logo, featured color recognition parameters in the 'recognitionColors' section.

 ## Demo
 ![Camera](https://github.com/Siavash-Mortaz/KUKA-youBot/blob/main/Images/Rec.gif)
