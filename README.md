# BlueROV2
This repository is for the handling of all things BlueROV2 related, including sensors in the payload

## Overview

APPG would like to create undersea images and maps of “ghost gear” (lost fishing gear), using visual and sonar images. We will be attempting to implement a SLAM algorithm. The first step of SLAM is to get time synchronized data from the inertial frame of the robot, and any sensors that give information about the environment surrounding the robot. Combining these data can help the creation of a 3D map of the environment, and the track that the robot followed through it. Constructing these maps is useful for localization of ghost gear, and of other interesting locations on the seafloor. If done in real time, SLAM can help with navigation. 

## About the BlueROV2

For this SLAM algorithm, we will have several types of data to pull from our several types of sensors. For initial positioning, we can dead reckon with the onboard IMU data. This IMU data is not recommended for use in an advanced SLAM algorithm, because of the low quality sensors that make up the IMU. The primary sensors that we hope to use for SLAM are the Omniscan450 side scan sonars, made by Cerulean, the ping altimeter, made by BlueRobotics, the SBL, made by Waterlinked. The Ping360 is not actually that helpful for SLAM in the field, we think. The onboard camera can be used for target verification, if the ROV is close enough/if the visibility is adequate.

In addition to the onboard sensors, we hope to make SLAM more reliable and geo-confident by using side scan images from an AUV side scan survey. The AUV we currently have access to can create geo-referenced side scan images. We hope to be able to use the geo-referenced side scan images to put the side scan images from the ROV in more context, adding another verification stream to the SLAM algorithm.

**Visual description:**
<img width="1821" alt="Screenshot 2025-04-01 at 2 57 41 PM" src="https://github.com/user-attachments/assets/97627937-10de-4f7c-93cb-9c3c6bb5aaac" />

## Decoding the raw data
Use the following folders to help you parse the data from the onboard sensors
- [Ping 360 and 1D Echosounder](pings/README_ping.md)
- [Omniscan450 - Side scan sonar](omniscan450)
- [Telemetry](telemetry)

## APPG Deployments
For data contact coanderson@ucsd.edu
- :sunny: Keck pool 3/6/2025
- :speedboat: Beyster 3/24/2025
- :ship: Shana Rose 4/18/2025
