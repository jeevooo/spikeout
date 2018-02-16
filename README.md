<p align='left'>
<img src='images/spikeout.png' width='75'>
</p> 

# Spike Out 
## A tool to flag anomalous events

----

## **Table of Contents**
  
- [The Problem: Service Interruptions](#heading)
  * [Managing Server Requests](#sub-heading1)
  * [Spike Out](#sub-heading2)
  * [Goals & Questions](#sub-heading3)
  * [Solutions to the problem](#sub-heading4)
    +  [Pros and Cons](#sub-sub-heading1)
- [The Data](#heading-1)
  * [Time Series](#sub-heading-11)
  * [Data Challenges and Exploration](#sub-heading-12)
- [Models](#heading-2)
  * [ARIMA](#sub-heading-21)
  * [ARIMAX](#sub-heading-22)
      + [Feature Engineering](#sub-sub-heading-221)
  * [LSTM](#sub-heading-23)
      + [Long-range correlations](#sub-sub-heading-231)
      + [LSTM creation](#sub-sub-heading-232)
- [Validation](#heading-3)
  * [Multiple Train-Test Splits](#sub-heading-31)
- [Results](#heading-4)
- [Conclusions](#heading-5)
  * [Future Work](#sub-heading-51)

----

## The Problem: Service Interruptions<a name="heading"></a>
Business' use websites as a tool to interact with their users. When a website's service is unavailable it cost the [business revenue](https://www.forbes.com/sites/kellyclay/2013/08/19/amazon-com-goes-down-loses-66240-per-minute/#6c0b5db5495c). It becomes imperative that business' can maintain their website from service interruptions and to constantly be in connection with their customers. However, there are moments when unseen circumstances lead to sharp changes in users visiting the website. These sharp changes can be understood as anomalous spikes in the typical daily trends of webpage visits. Forecasting anomalies can lead to efficient server management. More specifically, it can allow web server companies to reduce service interruptions, by knowing in advance whether there is a pressing need to accomodate more server requests. 

### Managing Server Requests<a name="sub-heading1"></a>
Currently, servers are designed accomdate requests up to a limit. A pre-determined limit on the number of requsts is set by web server manager at which point the server stops recieving requsts and forms a [cue.](https://serverfault.com/questions/140897/how-does-too-many-requests-make-a-server-crash/) As a result a user will often see a browswer response that reads "503 Service Unavailable". For the purpose of this context we are focusing on legitimate requests to the website and not another instance of this occurrence that is known as a denial-of-service attack [(DOS).](https://en.wikipedia.org/wiki/Denial-of-service_attack) Assuming that the requests are legitimate and despite their best-efforts to set the limit appropriately, web sites have still have service interruptions in recent historytrum.

### Spike Out<a name="sub-heading2"></a>
Spike Out is a tool which uses residuals from model to flag anomalous activity with website visitors. Spike Out is a project I attemped as data science fellow at Insight Data Science. 

### Goals & Questions<a name="sub-heading3"></a>
1) Find model that captures dynaimcs of web-traffic accurately.
  - What is the most approproate time-series models to capture the dynamics of web-traffic data?
2) Predict/Flag anomalous events in the data based on a selected threshold.
  - Based on the current data, what is the best threshold approach?

### Potential Solutions to the problem<a name="sub-heading4"></a>
1) Use a static threshold based on typical peak activity. 
2) Use residuals from model to detect change in webtraffic behaviour. 

#### Pros and Cons<a name="sub-sub-heading1"></a>
For __solution 1__, captuing the peaks can allow us to use forecasted values on the actual data to predict a potential anomalies. In this case we are limiting the lag time between the detection of an anomaly and action to handle the anomaly. However, there is the question of what peaks are typical and atypical. This choice can potentially inflate the threshold and lead to prediction of false negatives (i.e., missing true anomalies). From a business perspective this approach does allow potential savings but being premptive but limits the accuracy of detecting anomalies and can potentially be a risk for adding costs than actual savings.

For __solution 2__, using the residuals inherently places emphasis on modeling the data accurately. Assuming the data can be modeled accurately a second limitation is the lag betwen detection and action. More specifically, as time progresses obersvations will get added to the data and the residual between the actual and predicted value will then inform action. From a business perspective this does lead to a cost because newly acquired data can be anomalous and therefore action will occur after the start of an anomalous event.

----

## The Data<a name="heading-1"></a>
Publicly available web traffic data is made accessible through analytics.usa.gov. A description of the initiative can be found at [DAP](https://www.digitalgov.gov/services/dap/). The site reports various metrics (i.e., active users) of a number of governmental websites every 5 minutes. Here is an example of the obtainable .csv file made by the website on “active users”:

<p align='center'>
<img src='images/clipanalyticsusa.png' width='500'>
</p>

A definition of "active Users" could not be found on the description of the initiative. The working defintion of for active users (AU)  for this analysis is: users that navigated to the page of interest and also navigated to a corresponding link on the page of interest. 

I captured the data every 5 minutes without delay for 18 days in an AWS server. Below is the data pipeline I created:

<p align='center'>
<img src='images/datacollection2.png' width='500'>
</p>

To narrow the field of websites being reported by analytics.usa.gov/, I decided to cut out url’s that were not home pages, such as:

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

### Time Series<a name="sub-heading-11"></a>
When plotting the time series of the tracked websites we immediately notice the presence of weekly trends in the data. To be more specific, the peak number of users during the weekdays are greater than on the weekends.  We also see that the time series is fairly stationary (i.e., does not have a changing mean over time). An augmented Dickey-Fuller test (ADF) provides a confirmation of this observation. 

<p align='center'>
<img src='images/time-series.png' width='500'>
</p>

These types of websites serve as a prime example of why server management system would place a pre-determined limit on the number of requests a website should accommodate. However, what’s of interest is the spike in activity that occurred during the government shutdown. 

Below is the univariate time series data for usps.com/:

<p align='center'>
<img src='images/uspspikes.png' width='500'>
</p>

Looking at the data we notice there are clear spikes in the data that are event-related such as, 1) government-shutdown and, 2) the release of a stamp dedicated to Lena Horne. 

The usps.com/ data will be used for demonstrating the analysis performed in this blog. Specifically the clip of data used to model the dynamics web-traffic is in red. The green will be used to test out of sample predictions.

<p align='center'>
<img src='images/uspstraintest.png' width='500'>
</p>

### Data Challenges and Exploration<a name="sub-heading-12"></a>
Exploration of the data took several parts:
1) Checking the sampling was consistent.

<p align='center'>
<img src='images/samplingcomb.png' width='600' height='250'>
</p>

The figure on top demonstrates that the sampling was not consistent. Therefore, I aggregated that data by the hour, by summing the number of visotors within each hour. This did reduce the number of data points substantially but, I chose this method instead of using the mean because it would add an artifact (spike) to the data. 

2) Assesing the stationarity.

<p align='center'>
<img src='images/rollowingmeanvar.png' width='500'>
</p>

A fairly consisten mean and variation were present, but clear weekday/weekend trends are present.

3) Evaluating the structure. 

<p align='center'>
<img src='images/lag_plot.png' width='400'>
</p>

Clear structure is present in the data demonstrating non-random process.

## Models<a name="heading-2"></a>
Due to exploratory steps taken to above understand the data, the first attempt at modeling web-traffic was with the Autoregressive Integrated Moving Average (ARIMA) and its variation ARIMAX models. Additional analysis of the data lead to the use of an variation of a recurrent neural network (RNN) called the long short-term memory (LSTM) neural network. 

### ARIMA<a name="sub-heading-21"></a>
The ARIMA model can be described as an extension to regression, which uses the weighted sums of lags (AR parameter) combined with weighted sum of errors (MA paramter). The parameters of an ARIMA can be guided by the partial autocorrelation (PACF) and autocorrelation (ACF) functions for the AR (lag feature) and MA (error feature) parameters, respectively. Alternatively, a grid search can be performed. The PACF and ACF were used to guide the choices of parameters. The parameters for the model used were AR(2), MA(5). When fitting the model the ARIMA tended to have a poor fit. 

<p align='center'>
<img src='images/ARIMA.png' width='500'>
</p>

### ARIMAX<a name="sub-heading-22"></a>
The ARIMAX is an extension to the ARIMA which includes a exogenous covariates. The covariate is combined with the linear equation as a weighted value. The inclusion of a covariates changes the data to a multivariate dataset. 
#### Feature Engineering<a name="sub-sub-heading-221"></a>
In order to establish a covariate with the data I thought to encode the dates of government shutdown. In order to verify that the government shutdown was an appropriate covariate, I performed a Granger Causality test. A significant F-test was found showing that the government shutdown is a predictor of active users. The opposite was also tested (i.e., whether active users drive the shut down) and was found to be not significant. ` 

Government shutdown driving active users:
<p align='center'>
<img src='images/shutdriveuser.png' width='500'>
</p>

Active useres driving government shutdown:
<p align='center'>
<img src='images/userdriveshut.png' width='500'>
</p>

Following the inclusions of the feature in the dataset and then fitting an ARIMAX model the fit become much better at capturing the dynamics of the time series. 

<p align='center'>
<img src='images/ARIMAX.png' width='500'>
</p>

### LSTM<a name="sub-heading-23"></a>
#### Long-range correlations<a name="sub-sub-heading-231"></a>
Many complex and dynamical systems possess memory, more specifically called long-range correlations. This idea in a time series can be understood as the variabilty at short time scales being correlated to the variabilty at large time scales. One method for establishing the presence of long-range correlations is with a detrended fluctuation analysis (DFA). More details on the procedure can be found [here](https://www.physionet.org/physiotools/dfa/)

After plugging the time series into the DFA algorithm the data produced a fractal scaling index (FSI) of 1.32. The FSI is calculated by taking the slope of the log-log plot of the window size versus mangitude of fluctuation. For context the fracal scaling index can range from 0-2. An FSI > 1.0 is indication of a long-range correlations. 

<p align='center'>
<img src='images/dfa.png' width='400'>
</p>

With the presence of long-range correlations it became clear that and LSTM model would be appropriate since it can capture long-range dependencies in time series. 

#### LSTM creation<a name="sub-sub-heading-232"></a>
The LSTM model in the 

## Validation<a name="heading-3"></a>
### Validation using multiple Train-Test Splits<a name="sub-heading-31"></a>
Validation in machine learning is typically done with cross-validation. Due to the fact that time series data has temporal connections a typical cross-validation technique is insufficient for testing out the 

Multiple train test splits were used to validate the model. The approach takes a fixed testing length and uses various sizes of the training data to predict the test set. 

<p align='center'>
<img src='images/traintest.png' width='400'>
</p>

## Results<a name="heading-4"></a>
The results of the trian-test splits indicate that the LSTM model performs the best at predicting testing data with various lengths of training data. 

<p align='center'>
<img src='images/comparison.png' width='400'>
</p>

Finally to test whether the LSTM on detecting a spike the data, the peaks (blunted if a spike to avoid skew), was used to define the median. The 75 percentile was then used as the threshold. 

![peaks](https://github.com/jeevooo/spikeout/blob/master/images/peaks.png)

The 75th percentile corresponded to 30298 active users and the predicted value of the timestep at the spike was 30500 active users. According to that threshold and prediction algorithm accurately predicted a spike occurence. 

## Conclusions<a name="heading-5"></a>
Spike Out is currently a proof-of-concept tool which provides a basis for detecting anomalies in web-traffic data. Event-related features show drastic changes in the ability to model active users on websites. Additionally, the LSTM approach shows the best ability to model web-traffic data, partly due to the presence of long-range correlations. The small sample of spikes with the present dataset limited a true test of anomaly detection reliability. However, at first pass the tool appears functional with the current forecasting approach. As a whole, Spike Out adds value to a web server management systems by provding an indication of potential future anomalies based on current and previous web-volume and additional features. 

### Future Work<a name="sub-heading-51"></a>
Future work will aim to capture more data in order to turn the anomaly detection method into a classification problem. This will allow the tool to be tested using a true machine learning approach. Additionally, with an appropriate resolution in sampling (i.e., non-aggregated data), a more sensitive approach for detecting anomalies would be to measure the slope of several forecasts. This is becasue spikes typically have a sharper rise than typical volume rises observed in daily web volume. Lastly, this tool can be expanded by including additional event related features as an automated method by sourcing website related trends, such as tweets, news headlines, and google search results. 



