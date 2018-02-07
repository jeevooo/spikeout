# Spike Out

A tool using forecasts in web traffic to detect anomalous events.

Author: Jeev Kiriella

## **Table of Contents**
  
- [The Problem: Service Interruptions](#heading)
  * [Managing Server Requests](#sub-heading)
  * [Spike Out](#sub-heading)
- [The Data](#heading-1)
  * [Time Series](#sub-heading-1)
  * [Exploration](#sub-heading-1)
- [Models](#heading-2)
  * [Arima](#sub-heading-2)
  * [ARIMAX](#sub-heading-2)
      + [Feature Engineering](#sub-sub-heading-2)
  * [LSTM](#sub-heading-2)
      + [Long-range correlations](#sub-sub-heading-2)
- [Validation](#heading-3)
  * [Multiple Train-Test Splits](#sub-heading-3)
 - [Results](#heading-4)
 - [Conclusions](#heading-5)
  * [Future Work](#sub-heading-5)

<!-- toc -->

## The Problem: Service Interruptions
Business' use websites as a tool to interact with their users. When a website's service is unavailable it cost the [business revenue](https://www.forbes.com/sites/kellyclay/2013/08/19/amazon-com-goes-down-loses-66240-per-minute/#6c0b5db5495c). It becomes imperative that business' can maintain their website from service interruptions and to constantly be in connection with their customers. However, there are moments when unseen circumstances lead to sharp changes in users visiting the website. These sharp changes can be understood as anomalous spikes in the typical daily trends of webpage visits. Forecasting anomalies can lead to efficient server management. More specifically, it can allow web server companies to reduce service interruptions, by knowing in advance whether there is a pressing need to accomodate more server requests. 

### Managing Server Requests
Currently, servers are designed accomdate requests up to a limit. A pre-determined limit on the number of requsts is set by web server manager at which point the server stops recieving requsts and forms a [cue.] (https://serverfault.com/questions/140897/how-does-too-many-requests-make-a-server-crash) As a result a user will often see a browswer response that reads "503 Service Unavailable". For the purpose of this blog we are focusing on legitimate requests to the website and not another instance of this occurrence that is known as a denial-of-service attack [(DOS).] (https://en.wikipedia.org/wiki/Denial-of-service_attack) Assuming that the requests are legitimate and despite their best-efforts to set the limit appropriately, web sites have still have service interruptions in recent history (LINKS).

### Spike Out
Spike Out is a tool which uses forecasts of active users on a particular website, in order to detect whether an anomalous event will occur. Spike Out is a project I attemped as data science fellow at Insight Data Science. 

## The Data
Publicly available web traffic data is made accessible through analytics.usa.gov. A description of the initiative can be found at [DAP.] (https://www.digitalgov.gov/services/dap/). The site reports various metrics (i.e., active users) of a number of governmental websites every 5 minutes. Here is an example of the obtainable .csv file made by the website on “active users”. 

<clip of .csv>


I captured the data every 5 minutes without delay for 18 days in an AWS server. To narrow the field of websites being reported by analytics.usa.gov/, I decided to cut out url’s that were not home pages, such as:

1)	usps.com/
2)	weather.gov/
3)	medicare.gov/
4)	nasa.gov/
5)	irs.gov/
6)	cdc.gov/
7)	defense.gov/
8)	ssa.gov/
9)	va.gov/
10)	usajobs.com/

<image of collection>

### Time Series
When plotting the time series of the tracked websites we immediately notice the presence of weekly trends in the data. To be more specific, the peak number of users during the weekdays are greater than on the weekends (see Figure 1).  We also see that the time series is fairly stationary (i.e., does not have a changing mean over time Figure 2). An augmented Dickey-Fuller test (ADF) provides a confirmation of this observation. 

These types of websites serve as a prime example of why server management system would place a pre-determined limit on the number of requests a website should accommodate. However, what’s of interest is the spike in activity that occurred during the government shutdown. 

By capturing the typical peaks of the data, a threshold can be determined. Based on two standard deviations above the mean or if the data is not normally distributed, the 75th percentile around the median can be used as threshold.

### Exploration
Exploration of the data took several parts:
1) Checking the sampling was consistent.
2) Assesing the stationarity.
3) Evaluating the structure. 

## Models
Due to exploratory steps taken to above understand the data, the first attempt at modeling web-traffic was with the Autoregressive Integrated Moving Average (ARIMA) and its variation ARIMAX models. Additional analysis of the data lead to the use of an variation of a recurrent neural network (RNN) called the long short-term memory (LSTM) neural network. 

### ARIMA
The ARIMA model can be described as an extension to regression, which uses the weighted sums of lags combined with weighted sum of errors (MA part)
### ARIMAX
The ARIMAX is an extension to the ARIMA which includes a covariate to 
#### Feature Engineering
### LSTM
#### Long-range correlations
Many complex and dynamical systems possess memory, more specifically called long-range correlations. This idea in a time series can be understood as the variabilty at short time scales being correlated to the variabilty at large time scales. One method for establishing the presence of long-range correlations is with a detrended fluctuation analysis (DFA). More details on the procedure can be found [here.](https://www.physionet.org/physiotools/dfa/).

After plugging the time series into the DFA algorithm the data produced a fractal scaling index (FSI) of 1.32. For context the fracal scaling index can range from 0-2. An FSI > 1.0 is indication of a long-range correlations. 

With the presence of long-range correlations it became clear that and LSTM model would prove appropriate since it can capture long-range dependencies in time series. 

## Validation
Validation in machine learning
### Multiple Train-Test Splits
Multiple train test splits were used to validate the model. The approach takes a fixed testing length and uses various sizes of the training data to predict the test set. 


![traintest](https://github.com/jeevooo/spikeout/blob/master/images/traintest.png)


## Results
The results of the trian-test splits indicate that the LSTM model performs the best at predicting testing data with various lengths of training data. 



## Conclusions
Spike Out is currently a proof-of-concept tool which provides a basis for detecting anomalies in web-traffic data. Event-related features show drastic changes in the ability to model active users on websites. Additionally, the LSTM approach shows the best ability to model web-traffic data, partly due to the presence of long-range correlations. The small sample of spikes with the present dataset limited a true test of anomaly detection reliability. However, at first pass the tool appears functional with the current forecasting approach. As a whole, Spike Out adds value to a web server management systems by provding an indication of potential future anomalies based on current and previous web-volume and additional features. 
### Future Work
Future work will aim to capture more data in order to turn the anomaly detection method into a classification problem. This will allow the tool to be tested using a true machine learning approach. Additionally, with an appropriate resolution in sampling (i.e., non-aggregated data), a more accurate approach for detecting anomalies would be to measure the slope of several forecasts. This is becasue spikes typically have a sharper rise than typical volume rises observed in daily web volume. Lastly, this tool can be expanded by including an automated mehtod for feature engineering by sourcing website related trends, such as tweets, news headlines, and google search results. 



