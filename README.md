# Counting Cars in Aerial Imagery
In a previous project, I looked at patterns in traffic collisions and created a model to predict hourly crashes in Austin, Texas. While the model was still fairly useful, I was unfortunately unable to find extensive traffic volume data.

Traditionally, this data has been collected using magnetic or piezo-sensors (the strips you drive over),  or human surveyors either in person or via video [[1]](#1). And while computer vision techniques have been applied to this domain, it's often via surveilance cameras. While this is useful for collecting data at a specific instersection or on a certain block, it doesn't give always give a clear picture of how traffic moves around a neighborhood or even a city.

## Possible Solutions
As recently as 1999 the best resolution available commercially in satellite imagery was 80 cm GSD (the length of one pixel represents 80 cm). Not ideal for tracking traffic patterns. However, resolution and refresh rate (due to amount of satellites in orbit) have rapidly increased, making traffic monitoring from aerial imagery and/or space more feasible. The best resolution commercially available at the moment is 30cm, however, space startup [Albedo](https://spacenews.com/introducing-albedo/) promises to make *10cm imagery* available in the near future.

## The Data
I used the COWC (cars overhead with context) dataset produced by Lawrence Livermore National Laboratory. The dataset consists of aerial imagery at 15cm GSD taken over six distinct regions. In total, there are 32,716 unique annotated cars. Below is an example image:
![large_sample](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/large_example.jpg)
Data is collected via aerial platforms but at an angle that mimicks satellite imagery. Labels are provided as a single non-zero pixel.

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
*The sampling script can be found [here.](https://github.com/JacksonPeoples/CarCounting/blob/master/sampling_script.py)* The script also converts single pixel labels into the text format needed by the Yolov3 system.

Ultimately, in scenes such as the previous one, the weighted probabilities produced only a marginally noticeable difference over the course of 100 simulations of 100 samples. The real utility of weighted sampling can be seen in more sparse scenes with higher variability by quadrant. The following histograms plot the average cars present in 100 samples for 100 simulations:
![bootstrap](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/bootstrap.png)

## Training
I decided to use the [Yolov3](https://pjreddie.com/darknet/yolo/) object detection system for its speed. My thought process is that large aerial images contain a vast amount of information (some of the scenes were 13,000x13,000 or 4sq/km) so a useful model would need to quickly iterate over tiles of a large scene. Yolo differs from other models in that it is able to look at the whole image in one pass rather than region proposals created by a separate network. Yolo splits the entire image into an SxS grid and then produces n bounding boxes. For each bounding box, a class probability and offset values are computed. This makes it much faster than other algorithms.

I used 12 scenes in all (omitted any grayscale scenes). I held out one scene for testing after training and used my sampling script to produce 100 random samples of each of the the remaining 11 scenes. I used a 90/10 train/test split. I then trained for 30 epochs (actually 35 because I lost connection to my VM on the first run but was able to start the second run with those weights) on an n1-standard-8 GCP VM instance with 1 NVIDIA Tesla V100. Training took ≈1.5 hours.

![training_metrics](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/results.png)

Training metrics:
  * **Box**: Box refers to the GIoU loss function. IoU (intersection over union) refers to the degree of overlap between our predicted bounding box and the ground truth label. The problem is that in a typical 1-IoU loss function, any labels/predictions that do not intersect at all will result in 0 IoU and not all 0 IoU are equally bad predictions. GIoU introduces a penalty term, *C*, that refers to the smallest box containing both the ground truth label and prediction.
  * **Objectness**: The objectness refers to a loss funtion that quantifies how likely an object of interest is present in a given cell.
  * **Classification**: Classification is irrelevant for this task because we are only looking for cars. Otherwise it would refer to the model's accuracy in classifying objects of interest.
  * **Precision**: the proportion of how many predicted cars are actually cars (true positive/true positive + false positve).
  * **Recall**: the proportion of how many of the actual cars were correctly identified (true positive/true positive + false negative). 
  * **mAP@0.5**: in this case, mAP is actually synonymous with AP(average precision). AP is the average precision for recall values ranging from 0 to 1. It basically measures how well our model can continue to avoid false positives while decreasing the rate of false negatives. In multiclass object detection, mAP refers to the average AP for all classes. *0.5* refers to the IoU threshold for determining a correct classification. 0.5 as a threshold is a common convention but is arbitrarily chosen.
  * **mAP@0.5:.95**: The average AP score at different thresholds ranging from 0.5 to 0.95 in 0.05 increments.
All in all (aside from losing connection to my VM) training was extremely successful. All training metrics/loss functions converged as expected and an AP of .97+ suggests the model would be extremely useful in tracking traffic volume.

## Testing
I reserved a densely populated scene from Utah and randomly produced 10 samples to test the model. Results are as shown:
![pr curve](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/precision_recall_curve.png)
Looks great. Unfortunately, I was unable to determine a method for extracting the predictions and plotting them against ground truth labels with recall/precision metrics for demonstrative purposes. But, as an example, here is an image which I used the model to *detect*(i.e. fed the model with no ground truth labels):
![sample test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test.jpg)
![annotated test](https://github.com/JacksonPeoples/CarCounting/blob/master/PICSforREADME/image_test_2.jpg)
Missed a couple of cars occluded by shadows/trees but passes the eyeball test!

## Results/Improvements
Overall, performance metrics suggest the model would be effective in monitoring traffic volume. Next steps would be to create a pipeline that:
  1. Takes in large aerial imagery
  2. Tiles the imagery into sizes the model can handle
  3. Feeds tiles into the model to create predictions
  4. Pieces predictions back together.
Another potential improvement would be to train the model to identify all types of traffic (the dataset only labeled cars, not commercial trucks). This would provide a clearer picture of traffic activity but ultimately it is likely that car traffic volume is a decent proxy for total traffic volume.

## Helpful Resources
Truly, too many helpful resources to count, but here are a few that helped me:
[The Dataset](https://gdo152.llnl.gov/cowc/)
[YOLO: Real-Time Object Detection](https://pjreddie.com/darknet/yolo/)
[Github repo of the Yolov3 iteration I used](https://github.com/ultralytics/yolov3)
[Guide to Running on a GCP instance](https://github.com/ultralytics/yolov3/wiki/GCP-Quickstart)
[Perfomance Metrics Guide](https://medium.com/swlh/on-object-detection-metrics-ae1e2090bd65)
[Understanding GIoU](https://medium.com/visionwizard/understanding-diou-loss-a-quick-read-a4a0fbcbf0f0)
[Understanding mAP](https://jonathan-hui.medium.com/map-mean-average-precision-for-object-detection-45c121a31173)
[Extemely Helpful Presentation on Object Detection in Aerial Imagery](https://www.youtube.com/watch?v=rjKvXhEXDFs&t=510s)

<a id="1">[1]</a>
'The Development Of Traffic Data Collection Methods' https://medium.com/goodvision/the-development-of-traffic-data-collection-cd87cc65aaab#:~:text=Traditional%20methods%20of%20collecting%20traffic,image%20analysis%20using%20machine%20vision.
