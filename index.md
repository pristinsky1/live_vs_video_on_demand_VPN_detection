

## Live vs. Video on Demand inside VPN Detection
## Overview
&ensp; Due to the variety, affordability and convenience of online video streaming, there are more subscribers than ever to video streaming platforms. Moreover, the decreased operation of non-essential businesses and increase in the number of people working from home in this past year has further compounded this effect. More people are streaming live lectures, sports, news, and video calls via the internet at home today than we have ever seen before. 

&ensp; In March 2020, Youtube saw a 2.5x increase in the amount of time people spent streaming live video. Twitch more than doubled their hours of content in three months after the start of the pandemic. There is a huge boom in the video content world, and it does not seem to be slowing down anytime soon.  Internet Service Providers, such as Viasat, are tasked with optimizing  internet connections and tailoring their allocation of resources to fit each unique customer’s needs. With this increase in internet activity, it would be especially beneficial for Viasat to understand what issues arise when customers stream various forms of video.

&ensp; This model is meant to be used in conjunction with another pipeline that can first verify that video streaming is occurring within a VPN tunnel. Using our findings, we can further classify what type of video a user is streaming, to help gain a better understanding of user activity to ultimately enhance user experience.


## Data Collection
&ensp; The internet data that we have collected consists of the number of packets and bytes uploaded and downloaded across a connection. A connection consists of the source and destination IP addresses and ports. Using this data, we can look at the flow of packets and bytes sent back and forth over time between the user and destination.With this information, and lots of exploratory data analysis we were able to find some key identifiers that can help us distinguish what type of video is being played. Below is an example file:
![Dataset Snippet](image.png)

- **Time**: Timestamp when the data is recorded
- **IP1**: IP address of the user
- **Port1**:  Port of the user
- **IP2**: IP address of the server
- **Port2**: Port of the server
- **Proto**: IP Protocol number
- **1 ->2 Bytes**: The size in bytes of the packet in the upload direction
- **2 ->1 Bytes**: The size in bytes of the packet in the download direction
- **1 ->2 Pkts**: The number of Packets in the upload direction
- **2 ->1 Pkts**: The number of Packets in the download direction
- **packet_times**: The time when each packet arrived in milliseconds
- **packet_sizes**: The size in bytes of the packet excludes link layer headers
- **packet_dirs**: The directrion where the packet came from. 1 means it is from IP1 (user). 2 means it is from IP2 (server).

## Dataset Overview
&ensp; We have chosen to generate network data from platforms that offer both live and VoD content, such as Youtube and Twitch, as well as data from platforms such as Netflix, Facebook Live, Radio.com, Amazon Prime, Hulu, and Zoom (live video calls). Through an extensive dataset drawing from multiple providers we were able to create a robust model that can identify when a user is streaming a VoD or a live video. The dataset breakdown is as follows:
![Dataset Platform](dataset.png)

## Feature Extraction & Analysis
&ensp; With the data we have generated, and lots of exploratory data analysis we were able to find some key identifiers that can help us distinguish what type of video is being played. We first want to compare the number of bytes that are downloaded when watching a video on demand vs. live video, this can give us insight on how different internet activities send their information.

&ensp; We can compare how twitch delivers their videos on demand vs their live videos in the graphs below:

![Number of Bytes Downloaded](newplot%20(1).png)

&ensp; The graph above shows a side by side comparison of the number of downloaded bytes (how many bytes the destination IPs, Twitch here, sends back to the Source, aka the user) over a network for a five minute chunk (300 seconds) of Twitch Video on Demand and a Twitch Live Video. As we can see in the graphs above, there are some very prominent differences in the way VOD and Live Video is delivered. First, we can see that the graph for VOD is much more sparse than the one for live video. There is a spike of content delivered nearly exactly ten seconds apart, whereas for video on demand the spikes are very dense and content is delivered nearly every second. We can also see that the scale of bytes for the two videos differ. VOD has over two times as many bytes per spike, whereas live video has smaller spikes but more often.

&ensp; The graph above shows a side by side comparison of the number of downloaded bytes (how many bytes the destination IPs, Twitch here, sends back to the Source, aka the user) over a network for a five minute chunk (300 seconds) of Twitch Video on Demand and a Twitch Live Video. As we can see in the graphs above, there are some very prominent differences in the way VOD and Live Video is delivered. First, we can see that the graph for VOD is much more sparse than the one for live video. There is a spike of content delivered nearly exactly ten seconds apart, whereas for video on demand the spikes are very dense and content is delivered nearly every second. We can also see that the scale of bytes for the two videos differ. VOD has over two times as many bytes per spike, whereas live video has smaller spikes but more often. 

&ensp; To quantify this difference in density between the two types of videos, we can look at the number of peaks present for bytes downloaded within a five minute chunk of video. The graphs below highlight where each spike is, using the mean number of bytes downloaded as a lowerbound. Using this lower bound can help us filter out any noise that can be present when collecting network data at lower magnitudes.


![Twitch VoD: Peaks in Bytes Downloaded](newplot%20(2).png)
![Twitch Live: Peaks in Bytes Downloaded](newplot%20(3).png)

&ensp; It is clear that Live video has a much larger number of spikes than the VoD. To account for this in our model, we can create a feature that counts the number of spikes in a five minute video chunk.

&ensp; Another way to quantify this difference in density, is to look at how frequently these spikes are occuring. Below we can see a graph that plots what time each spike occurs for VoD and live Video. 

![Time of Peak in 5 minute Chunk of Live vs VoD Video](newplot%20(4).png)

&ensp; As we can see, the peaks for live video are much closer together than those for VoD. Each peak is about 10 seconds apart for VoD, whereas peaks for Live Videos are pretty consistently appearing. To account for this difference, we can draw out a feature that measures the time in seconds for the interval between peaks in a 5 minute chunk of video!

&ensp; We can also look at the data in the frequency domain!
![Time series, MB binned in 2 second intervals](newplot%20(5).png)

&ensp; When looking at the graph above, we can see that this data in the time domain binned at every 2 second intervals looks quite different when comparing video on demand to live. The VOD data appears to be bursts, with way larger spikes than the live data, while the live appears to be more sporadic with the packet sizes coming in rapidly. One of the most interesting things was that we saw that VOD has a lot of packet sizes at zero, while live data has nearly no zeros. This led us to explore a possible feature packet zeros, as shown above the graph with the value counts for pct_zeros. The red horizontal line at the 0.01 threshold indicates that any value below 0.01 will be counted, with the VOD data having a large amount and live having basically zero.

![Frequency Transform (Hz) after binned in 2 second intervals](newplot%20(6).png)

&ensp; This graph above shows the data for both VOD and live in the frequency domain. This means that we transformed the data, which we used Welch's method to compute. Right away we noticed that the peaks for VOD were way higher than live, as well as the height difference between the peaks and the troughs. From this, we developed a feature max prominence/mean which finds the largest height difference and normalizes it with the average power spectral density value. As well, we also looked into developing two other features, 0.1Hz/mean and 0.2Hz/mean. If you play around with interactive plot and zoom in, you can see that at every 0.1Hz and 0.2Hz, there are peaks or troughs which differed in sizes when looking at vod vs live. These Hz values showed enough of a difference between VOD and Live that we decided to find the minimum .1 and .2 Hz values present in each dataset and normalize them to create the potential features visible above the graph, with streaming on average having larger values than live.

## Features
&ensp; **The features we extracted that we have described above are as follows:**
- **Valid Packet Rate** - this feature finds the ratio of time that there is a valid packet being sent within the 5 minute chunk of video. This is created by grouping the data by the time column, to count the number of valid packets (packet size > 0) that are downloaded in the 2->1Bytes column in the five minute chunk of video. Then,this is calculated by dividing the number of valid packets with the total time. 
- **Number of Peaks** - This feature finds the number of  peaks that are greater than the mean of the 2 ->1 Bytes columns. It is calculated by the find_peaks method from the scipy library.
- **Interval gaps** - This feature looks at the total length of intervals between the peaks of the spikes in the 2 ->1 Bytes column. The peak of spikes is defined when the value is greater than the mean of the 2 ->1 Bytes column. And then, by subtracting the time difference between peaks, the length of intervals between peaks is calculated. Then, by summing the lengths of intervals, the total interval gaps are found. 
- **Packet Zeros** - This feature finds the percentage of packets that are zero (below the 0.01 threshold), with the % being the value returned per dataset. It is calculated by finding the total number of packets below the 0.01 threshold in the 2->1 direction multiplied by 100 then divided by the length of the binned 2s intervals.
- **Max Prominence / Mean** - This feature looks at the dataset in the frequency domain, then finds the maximum height present between a peak and trough and normalizes it. This normalized comparison is done in the 2->1 direction, and is calculated by binning the 2->1Packet Sizes into 2 second intervals, applying Welch’s method to transform the data to the frequency domain, and then using a find peaks method to find the max prominence present in the dataset.
- **peak_0.1Hz_norm**  - This feature grabs the minimum .1Hz value found within the transformed data in the frequency domain and normalizes it. This spectral feature is calculated by binning the 2->1Packet Sizes into 2 second intervals, and applies Welch’s method to transform the data to the frequency domain before looking at all the values occurring every 0.1Hz to find the minimum.
- **peak_0.2Hz_norm** - This feature grabs the minimum .2Hz value found within the transformed data in the frequency domain and normalizes it. This spectral feature is calculated by binning the 2->1Packet Sizes into 2 second intervals, and applies Welch’s method to transform the data to the frequency domain before looking at all the values occurring every 0.2Hz to find the minimum.


## Model 
&ensp; Since we are predicting a binary result of whether the file is VOD or live streaming, we explored classifiers including the SVM, KNeighbors classifier, Logistic Regression classifier and Random Forest classifier. Random Forest classifier achieved the highest accuracy of 99 percent, which is nearly 15 percent better than other models. The possible reason why Random Forest Classifier has the highest accuracy is that the more features we train it, the higher the accuracy would be. However, this classifier takes on average five times longer than other three classifiers. Eventually we trained the model on Zoom data and Twitch traffic and achieved the 99 percent test accuracy. Moreover, we noticed that if we included the YouTube data in the training process, the accuracy of the overall model would be lower by 10 percent. This may due to the fact that YouTube used a different algorithm than zoom and twitch which messed up the model.We plan to explore youtube data further in the coming weeks, and hyper tune our classifier to be able to distinguish different live video content. We also hope to explore the differences between live and VOD within the frequency domain to gather more insight. 

## Results
- confusion matrix of how our model did
- accuracy/precision scores

## Future Work 
