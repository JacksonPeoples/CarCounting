# Counting Cars in Aerial Imagery
In a previous project, I looked at patterns in traffic collisions and created a model to predict hourly crashes in Austin, Texas. While the model was still fairly useful, I was unfortunately unable to find extensive traffic volume data.

Traditionally, this data has been collected using magnetic or piezo-sensors (the strips you drive over),  or human surveyors either in person or via video [[1]](#1). And while computer vision techniques have been applied to this domain, it's often via surveilance cameras. While this is useful for collecting data at a specific instersection or on a certain block, it doesn't give always give a clear picture of how traffic moves around a neighborhood or even a city.

## Possible Solutions
As recently as 1999 the best resolution available commercially in satellite imagery was 80 cm GSD (the length of one pixel represents 80 cm). Not ideal for tracking traffic patterns. However, resolution and refresh rate (due to amount of satellites in orbit) have rapidly increased, making 

## The Data
![large_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/large_example.jpg)
## Pre-processing
![empty_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/empty_example.jpg)
![count_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/count_example.jpg)
<img src="https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/sampled_example.jpg" width="5000">

![bootstrap](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/bootstrap.jpg)


<a id="1">[1]</a>
'The Development Of Traffic Data Collection Methods' https://medium.com/goodvision/the-development-of-traffic-data-collection-cd87cc65aaab#:~:text=Traditional%20methods%20of%20collecting%20traffic,image%20analysis%20using%20machine%20vision.
