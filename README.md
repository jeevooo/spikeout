# Spike Out

A tool using forecasts in web traffic to detect anomalous events.

Author: Jeev Kiriella

## **Table of Contents**
  
- [The Problem: Service Interruptions](#heading)
  * [Managing Server Requests](#sub-heading)
  * [Spike Out](#sub-heading)
- [The Data](#heading-1)
  * [analytics.usa.gov](#sub-heading-1)
  * [Time Series](#sub-heading-1)
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
Currently, servers are designed accomdate requests up to a limit. A pre-determined limit on the number of requsts is set by web server manager at which point the server stops recieving requsts and forms a [cue] (https://serverfault.com/questions/140897/how-does-too-many-requests-make-a-server-crash). As a result a user will often see a browswer response that reads "503 Service Unavailable". 
### Spike Out
Spike Out is a tool which uses forecasts of active users on a particular website, in order to detect whether an anomalous event will occur. Spike Out is a project 
## The Data
This is an h1 heading
### Analytics.usa.gov/
This is an h2 heading
### Time Series
This is an h3 heading
## Models
This is an h1 heading
### ARIMA
This is an h2 heading
### ARIMAX
This is an h3 heading
#### Feature Engineering
### LSTM
#### Long-range correlations
## Validation
### Multiple Train-Test Splits
## Results
## Conclusions
Spike Out is currently a proof-of-concept tool which provides a basis for detecting anomalies in web-traffic data. Event-related features show drastic changes in the ability to model active users on websites. Additionally, the LSTM appraoch shows the best ability to model web-traffic data, partly due to the presence of long-range correlations. The small sample of spikes with the present dataset limited a true test of anomaly detection reliability. However, at first pass the tool appears functional with the current forecasting approach. As a whole, Spike Out adds value to a web server management systems by provding an indication of potential future anomalies based on current and previous web-volume and additional features. 
### Future Work
Future work will aim to capture more data in order to turn the anomaly detection method into a classification problem. This will allow the tool to be tested using a true machine learning approach. Additionally, with an appropriate resolution in sampling (i.e., non-aggregated data), a more accurate approach for detecting anomalies would be to measure the slope of several forecasts. This is becasue spikes typically have a sharper rise than typical volume rises observed in daily web volume. Lastly, this tool can be expanded by including an automated mehtod for feature engineering by sourcing website related trends, such as tweets, news headlines, and google search results. 



