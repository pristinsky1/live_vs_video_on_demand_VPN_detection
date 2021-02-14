# Live vs VOD inside a VPN Detection

Due to the variety, affordability and convenience of online video streaming, there are more subscribers than ever to video streaming platforms. Moreover, the decreased operation of non-essential businesses and increase in the number of people working from home in this past year has further compounded this effect. More people are streaming live lectures, sports, news, and video calls via the internet at home today than we have ever seen before. Internet Service Providers, such as Viasat, are tasked with optimizing  internet connections and tailoring their allocation of resources to fit each unique customer’s needs. With this increase in internet activity, it would be especially beneficial for Viasat to understand what issues arise when customers stream various forms of vide - specifically live video or video on demand!
## Data Cleaning
- snippet of network stats dataframe 
- what the data looks like
- explain the columns 

## Feature Extraction & Analysis
The internet data that we have collected consists of the number of packets and bytes being uploaded and downloaded across a connection. A connection consists of the source and destination IP addresses and ports.With this information, we can potentially find significant features that are key identifiers of internet activity. Using this data, we can look at the flow of packets and bytes sent back and forth over time between the user and destination. Through these findings, we plan to create a machine learning model to predict if a user is streaming live or pre-uploaded video.\par 
Similar to other common approaches to analyze internet network data, we have chosen to look for statistical differences between the flow of packets across a network for live video streaming and vod. The graphs below look at the number of packets sent across a network over time for both twitch live and twitch uploaded videos. 

When looking at the graphs above a few differences are immediately apparent. First, we can see that the live video has a denser graph with more packets coming in more frequently. On the other hand, the vod has more time between each spike but the magnitude of packets coming in at a time is larger. To quantify this key difference, we can take the ratio of time packets are being sent to the time packets are not being sent (packet size is 0). This will tell us how much time during the viewing of the video no packets were being sent from the destination to the user.\par
However, there are many micro spikes that couldn't be observed from the graphs, which would affect the accuracy of the previous method. For example, a noisy VOD traffic may have many small size packet transactions resulting in the ratio of packets transferring being as high as the live video streaming. To eliminate this possible error, we calculate the time between each spike as leisure time (the gap in seconds between each spike). Typically, VOD has more leisure time and live streaming has less. Live streaming requires video providers to consistently send data to their users as they are sending it in real time, this is a key difference in the way live streaming vs. VOD is delivered to viewers. 

Another way to quantify the difference in density of the two video streams is by simply looking at the number of peaks present. There are considerably more spikes in the dense graph for live streaming at smaller sizes, compared to the more spaced out larger spikes in the VOD plot.
With the features we have extracted to distinguish live streaming from VOD, we can use a machine learning model to predict the type of video a chunk of internet data is. 

## Model 
Since we are predicting a binary result of whether the file is VOD or live streaming, we explored classifiers including the SVM, KNeighbors classifier, Logistic Regression classifier and Random Forest classifier. Random Forest classifier achieved the highest accuracy of 99 percent, which is nearly 15 percent better than other models. The possible reason why Random Forest Classifier has the highest accuracy is that the more features we train it, the higher the accuracy would be. However, this classifier takes on average five times longer than other three classifiers. Eventually we trained the model on Zoom data and Twitch traffic and achieved the 99 percent test accuracy. Moreover, we noticed that if we included the YouTube data in the training process, the accuracy of the overall model would be lower by 10 percent. This may due to the fact that YouTube used a different algorithm than zoom and twitch which messed up the model.We plan to explore youtube data further in the coming weeks, and hyper tune our classifier to be able to distinguish different live video content. We also hope to explore the differences between live and VOD within the frequency domain to gather more insight. 

## Results
- confusion matrix of how our model did
- accuracy/precision scores

## Future Work 


![First Image](https://github.com/pristinsky1/live_vs_video_on_demand_VPN_detection/blob/gh-pages/newplot%20(1)%20(1).png)

![Temp](newplot (1) (1).png)

https://pristinsky1.github.io/live_vs_video_on_demand_VPN_detection/
