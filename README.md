# bi_exercise
The code for fetching data from S3 bucket, upload data to remote postgresql db and visualize data.

## Prerequisites
* AWS CLI [configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)
* installing code dependencies:
```
virtualenv env
pip install -r requirements.txt
```
* Change database connection params in *config/database.ini*
## Data loading

```
python main.py
```

## SQL function code
The function code for Cumulative Distribution calculation could be found in *plpgsql/cdf.sql*

## Data visualisation
```
python plot_cdf.py
```
## Results

Cumulative Dist for all records

![all](https://github.com/KosBar49/bi_exercise/blob/develop/results/cdf_all.png)

Cumulative Dist for [2019-12-18, 2020-01-03] window

![window](https://github.com/KosBar49/bi_exercise/blob/develop/results/cdf_window.png)

Clumulative Dist for [2020-01-29, 2020-01-30] window

![window](https://github.com/KosBar49/bi_exercise/blob/develop/results/cdf_window2.png)


