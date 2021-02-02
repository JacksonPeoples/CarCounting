# Counting Cars in Aerial Imagery
In a previous project, I looked at patterns in traffic collisions and created a model to predict hourly crashes in Austin, Texas. While the model was still fairly useful, I was unfortunately unable to find extensive traffic volume data.

Traditionally, this data has been collected using magnetic or piezo-sensors (the strips you drive over),  or human surveyors either in person or via video [[1]](#1). And while computer vision techniques have been applied to this domain, it's often via surveilance cameras. While this is useful for collecting data at a specific instersection or on a certain block, it doesn't give always give a clear picture of how traffic moves around a neighborhood or even a city.

## Possible Solutions
As recently as 1999 the best resolution available commercially in satellite imagery was 80 cm GSD (the length of one pixel represents 80 cm). Not ideal for tracking traffic patterns. However, resolution and refresh rate (due to amount of satellites in orbit) have rapidly increased, making 

## The Data
![large_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/large_example.jpg)
## Pre-processing
Luckily, when it comes to aerial imagery, many standard techniques for data augmentation are unnecessary:
  * Angles of observation are constant; all from above.
  * Size in frame is also constant.
  * Cars are rotated naturally as they travel in different directions.
  * Translation is accomplished by randomly sampling acrosse different scenes.

However, one possible issue is random samples coming out like this:
![empty_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/empty_example.jpg)

This isn't the end of the world, car-less samples are necessary to train a useful model. However, many of the scenes in this dataset are very sparse and it would be easy to end up with too many empty samples.

My solution was to:
  1. Compute the proportion of total cars in a scene in each quadrant.
  2. Weight the sampling probability based on those proportions.

For example, the following image:
![count_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/count_example.jpg)
Might produce these samples:
<img src="https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/sampled_example.jpg" width="5000">
The sampling script can be found [here.](https://github.com/JacksonPeoples/CarCounting/blob/master/sampling_script.py)

Ultimately, in scenes such as the previous one, the weighted probabilities produced only a marginally noticeable difference over the course of 100 simulations of 100 samples. The real utility of weighted sampling can be seen in more sparse scenes with higher variability by quadrant. The following histograms plot the average cars present in 100 samples for 100 simulations:
![bootstrap](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/bootstrap.png)

## Training

![training_metrics](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/results.png)

## Testing
![pr curve](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/precision_recall_curve.png)
![sample test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test.jpg)
![annotated test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test_2.jpg)

## Results/Improvements


<a id="1">[1]</a>
'The Development Of Traffic Data Collection Methods' https://medium.com/goodvision/the-development-of-traffic-data-collection-cd87cc65aaab#:~:text=Traditional%20methods%20of%20collecting%20traffic,image%20analysis%20using%20machine%20vision.
