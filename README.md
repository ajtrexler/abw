# American Bellwethers

A 'bellwether', defined by Wikipedia, is one that indicates or leads trends.  My goal with this project was to identify [PUMAs](https://en.wikipedia.org/wiki/Public_Use_Microdata_Area) (public use microdata areas) that act as the best bellwethers for the rest of America.  In other words, I wanted to see which PUMAs could generate the best predictive models for all of the other PUMAs in the country.  

For this analysis I chose to build models to predict occupations of surveyed individuals, as this was one feature of the person dataset.  In a more complex analysis, one would ideally use secondary datasets (perhaps primary election information or purchasing information) to test whether the 'bellwether PUMAs' identified here are actually any better than the rest of the country in predicting trends and outcomes.

My secondary goals for this project, which were definitely more succesful, were simply to get more accustomed to the machine learning Python library [sklearn](http://scikit-learn.org/stable/) and with Python programming in general.  I'm definitely a Python/programming novice, so I hope readers will excuse any obviously flawed practices or code.  Any comments or suggestions are more than welcome!

### general analysis pipeline:
1. Load the full datasets from the CSV files provided by Kaggle [puma_load.py](https://gitlab.com/atrexler/svm_pumas/blob/0cb16af4be2f7bf25b3e6de82bcf5179a04a75ac/puma_alt_load.py).  I removed the replicate weights columns and replaced NaN values with -1 to simplify analysis later.  Sparse features in the dataset were not scaled but all other features except occupation code (SOCP) were scaled with sklearn preprocessing scale function.
2. Reduce the dimensionality of the data with PCA.  For some of my analysis I used the full dataset as well but the majority was performed using a 20 component PCA-generated dataset.  I actually found that the PCA-reduced dataset was better at building models than the full ~200 feature dataset.  Implementation of the PCA was done with just the standard sklearn PCA module in [puma_load.py](https://gitlab.com/atrexler/svm_pumas/blob/0cb16af4be2f7bf25b3e6de82bcf5179a04a75ac/puma_alt_load.py)
3. [puma_parallel.py](https://gitlab.com/atrexler/svm_pumas/blob/0cb16af4be2f7bf25b3e6de82bcf5179a04a75ac/puma_parallel_pub.py) builds models with sklearn support vector machine (SVM) algorithm.  I chose SVM after a bit of initial fiddling and following the [algorithm selection guide](http://scikit-learn.org/stable/tutorial/machine_learning_map/) provided by sklearn.  In most rounds of the analysis I built a model per-PUMA so I used joblib.Parallel to achieve some parallelization to speed this process up.
4. Use each model to fit a subset of other PUMAs and predict occupations.  Calculate mean scores to evaluate how effective the model was.  I then ranked PUMAs by their mean scores to evaluate how well each PUMA was at predicting behavior (occupations) in the other PUMAs.


[puma_parallel.py](https://gitlab.com/atrexler/svm_pumas/blob/0cb16af4be2f7bf25b3e6de82bcf5179a04a75ac/puma_parallel_pub.py) is the real workhorse code of my analysis.  At the top is the test_puma function, which takes an input PUMA identifier and trains a model using the full dataset from that PUMA.  I use the SVM machine learning algorithm from sklearn with simple inputs, a linear kernel and only 10000 max iterations.  The function then tests that model against 100 randomly selected PUMA (the subpuma variable) and computes scores for how well the model does.

test_puma is called using Parallel from joblib to achieve some parallelization.  Parallel creates a number of workers that each carry out the test_puma call using a different input PUMA.

[results](https://gitlab.com/atrexler/svm_pumas/blob/master/puma_result.md)
**TL;DR: More data is always better.**