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
*The sampling script can be found [here.](https://github.com/JacksonPeoples/CarCounting/blob/master/sampling_script.py)*

Ultimately, in scenes such as the previous one, the weighted probabilities produced only a marginally noticeable difference over the course of 100 simulations of 100 samples. The real utility of weighted sampling can be seen in more sparse scenes with higher variability by quadrant. The following histograms plot the average cars present in 100 samples for 100 simulations:
![bootstrap](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/bootstrap.png)

## Training

![training_metrics](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/results.png)

Training metrics:
  * **Box**: Box refers to the GIoU loss function. IoU (intersection over union) refers to the degree of overlap between our predicted bounding box and the ground truth label. The problem is that in a typical 1-IoU loss function, any labels/predictions that do not intersect at all will result in 0 IoU and not all 0 IoU are equally bad predictions. GIoU introduces a penalty term, *C*, that refers to the smallest box containing both the ground truth label and prediction.
  * **Objectness**: The objectness refers to a loss funtion that quantifies how likely an object of interest is present in a given cell.
  * **Classification**: Classification is irrelevant for this task because we are only looking for cars. Otherwise it would refer to the model's accuracy in classifying objects of interest.
  * **Precision**: the proportion of how many predicted cars are actually cars (true positive/true positive + false positve).
  * **Recall**: the proportion of how many of the actual cars were correctly identified (true positive/true positive + false negative). 
  * **mAP@0.5**: in this case, mAP is actually synonymous with AP(average precision). AP is the average precision for recall values ranging from 0 to 1. It basically measures how well our model can continue to avoid false positives while decreasing the rate of false negatives. In multiclass object detection, mAP refers to the average AP for all classes. *0.5* refers to the IoU threshold for determining a correct classification. 0.5 as a threshold is a common convention but is arbitrarily chosen.
  * **mAP@0.5:.95**: The average AP score at different thresholds ranging from 0.5 to 0.95 in 0.05 increments.


## Testing
![pr curve](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/precision_recall_curve.png)
![sample test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test.jpg)
![annotated test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test_2.jpg)

## Results/Improvements


<a id="1">[1]</a>
'The Development Of Traffic Data Collection Methods' https://medium.com/goodvision/the-development-of-traffic-data-collection-cd87cc65aaab#:~:text=Traditional%20methods%20of%20collecting%20traffic,image%20analysis%20using%20machine%20vision.
