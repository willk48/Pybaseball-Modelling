import pandas as pd
import numpy as np
import pybaseball
from pybaseball import batting_stats
pybaseball.cache.enable()
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler


#Create helper function to apply to each player in the batting database
def next_season(p):
    p = p.sort_values("Season")
    p["Next_WAR"] = p["WAR"].shift(-1)
    return p

#load the csv from pybaseball, only from the last few years, and only for players with more than 150 ABs
def load():
    batting_stats(2017, end_season=2023, qual=150, ind=1).to_csv('batting_stats_150.csv', index=False)
    dataset = pd.read_csv('batting_stats_150.csv')
    #makes it only players with multiple seasons
    dataset = dataset.groupby("IDfg", group_keys=False).filter(lambda x: x.shape[0] > 1)
    null_variables = dataset.isnull().sum() #find nulls (cant have for ML)
    full_variables = list(dataset.columns[null_variables == 0]) #gets list of all non nulls
    batting = dataset[full_variables].copy() #updates to only non nulls
    #drop unnecessary identifiers
    batting = batting.drop('Dol', axis=1)
    batting = batting.drop('Team', axis=1)
    batting = batting.drop('Age Rng', axis=1)
    #batting = batting.drop('Unnamed: 0', axis=1)
    batting = batting.drop('IDfg', axis=1)
    batting = batting.drop('L-WAR', axis=1)
    #create a row for next WAR
    batting = batting.groupby("Name", group_keys=False).apply(next_season)
    return batting

def split(batting):
    X = batting.drop(['Name', 'Next_WAR'], axis=1)
    y = batting['Next_WAR']
    bat_copy=batting.copy()
    bat_copy2=batting.copy()
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y, test_size=0.75, random_state=12345)
    batting.sort_values("Season")
    X_train_temp=bat_copy[bat_copy["Season"]<2023]
    X_train_temp=X_train_temp[X_train_temp["PA"]>300]
    X_train_names = X_train_temp.dropna()
    X_train=X_train_names.drop(['Name','Next_WAR'],axis=1)
    y_train=X_train_names['Next_WAR']
    X_test_temp=bat_copy2[bat_copy2["Season"]>2022]
    #X_test_temp=X_test_temp[X_test_temp["PA"]>300]
    players_2023=X_test_temp.drop(['Next_WAR'],axis=1)
    X_test=players_2023.drop(['Name'],axis=1)
    y_test=X_test_temp['Next_WAR']
    return X_train, X_test, y_train, y_test, players_2023

def train_pred(X_train, X_test, y_train, y_test, players):
    lasso = Lasso(alpha=0.1)
    lasso.fit(X_train, y_train)
    y_pred = lasso.predict(X_test)
    players['Prediction'] = y_pred.tolist()
    diff=np.subtract(y_pred,players['WAR'])
    players['Increase'] = diff.tolist()
    test=players.copy()
    test=test[test["Increase"]>1.25]
    test=test[test["Age"]<27]
    #test=test[test["WAR"]<3]
    test.sort_values("Increase")
    return test
    
def main():
    dataset = load()
    X_train, X_test, y_train, y_test, players_23 = split(dataset)
    out = train_pred(X_train, X_test, y_train, y_test, players_23)
    
    out1 = out.copy()
    out1 = out.loc[:, out.columns.intersection(["Season","Name","Age", "WAR", "Next_WAR", "Prediction", "Increase"])]

    print(out1)

if __name__ == "__main__":
    main()