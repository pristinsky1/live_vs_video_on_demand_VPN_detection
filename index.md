

## Live vs. Video on Demand inside VPN Detection
## Overview
&ensp; Due to the variety, affordability and convenience of online video streaming, there are more subscribers than ever to video streaming platforms. Moreover, the decreased operation of non-essential businesses and increase in the number of people working from home in this past year has further compounded this effect. More people are streaming live lectures, sports, news, and video calls via the internet at home today than we have ever seen before. 

&ensp; In March 2020, Youtube saw a 2.5x increase in the amount of time people spent streaming live video. Twitch more than doubled their hours of content in three months after the start of the pandemic. There is a huge boom in the video content world, and it does not seem to be slowing down anytime soon.  Internet Service Providers, such as Viasat, are tasked with optimizing  internet connections and tailoring their allocation of resources to fit each unique customer’s needs. With this increase in internet activity, it would be especially beneficial for Viasat to understand what issues arise when customers stream various forms of video.

&ensp; We have chosen to generate network data from platforms that offer both live and VoD content, such as Youtube and Twitch, as well as data from platforms such as Netflix, Facebook Live, Radio.com, Amazon Prime, Hulu, and Zoom (live video calls). Through an extensive dataset drawing from multiple providers we were able to create a robust model that can identify when a user is streaming a VoD or a live video. This model is meant to be used in conjunction with another pipeline that can first verify that video streaming is occurring within a VPN tunnel. Using our findings, we can further classify what type of video a user is streaming, to help gain a better understanding of user activity to ultimately enhance user experience.


## Data
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



## Feature Extraction & Analysis
&ensp; The internet data that we have collected consists of the number of packets and bytes being uploaded and downloaded across a connection. A connection consists of the source and destination IP addresses and ports.With this information, we can potentially find significant features that are key identifiers of internet activity. Using this data, we can look at the flow of packets and bytes sent back and forth over time between the user and destination. Through these findings, we plan to create a machine learning model to predict if a user is streaming live or pre-uploaded video.

&ensp; Similar to other common approaches to analyze internet network data, we have chosen to look for statistical differences between the flow of packets across a network for live video streaming and vod. The graphs below look at the number of packets sent across a network over time for both twitch live and twitch uploaded videos.

![Packet_Download_Size_Live](newplot%20(1)%20(1).png)
![Packet_Download_Size_VOD](newplot%20(2)%20(1).png)

&ensp; When looking at the graphs above a few differences are immediately apparent. First, we can see that the live video has a denser graph with more packets coming in more frequently. On the other hand, the vod has more time between each spike but the magnitude of packets coming in at a time is larger. To quantify this key difference, we can take the ratio of time packets are being sent to the time packets are not being sent (packet size is 0). This will tell us how much time during the viewing of the video no packets were being sent from the destination to the user.

&ensp; However, there are many micro spikes that couldn't be observed from the graphs, which would affect the accuracy of the previous method. For example, a noisy VOD traffic may have many small size packet transactions resulting in the ratio of packets transferring being as high as the live video streaming. To eliminate this possible error, we calculate the time between each spike as leisure time (the gap in seconds between each spike). Typically, VOD has more leisure time and live streaming has less. Live streaming requires video providers to consistently send data to their users as they are sending it in real time, this is a key difference in the way live streaming vs. VOD is delivered to viewers. 

&ensp; Another way to quantify the difference in density of the two video streams is by simply looking at the number of peaks present. There are considerably more spikes in the dense graph for live streaming at smaller sizes, compared to the more spaced out larger spikes in the VOD plot.
With the features we have extracted to distinguish live streaming from VOD, we can use a machine learning model to predict the type of video a chunk of internet data is. 

## Model 
&ensp; Since we are predicting a binary result of whether the file is VOD or live streaming, we explored classifiers including the SVM, KNeighbors classifier, Logistic Regression classifier and Random Forest classifier. Random Forest classifier achieved the highest accuracy of 99 percent, which is nearly 15 percent better than other models. The possible reason why Random Forest Classifier has the highest accuracy is that the more features we train it, the higher the accuracy would be. However, this classifier takes on average five times longer than other three classifiers. Eventually we trained the model on Zoom data and Twitch traffic and achieved the 99 percent test accuracy. Moreover, we noticed that if we included the YouTube data in the training process, the accuracy of the overall model would be lower by 10 percent. This may due to the fact that YouTube used a different algorithm than zoom and twitch which messed up the model.We plan to explore youtube data further in the coming weeks, and hyper tune our classifier to be able to distinguish different live video content. We also hope to explore the differences between live and VOD within the frequency domain to gather more insight. 

## Results
- confusion matrix of how our model did
- accuracy/precision scores

## Future Work 
