# -*- coding: utf-8 -*-
"""KONTR_ANALIZ.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gztd3SyvTnQac6J_uoGwU1Y2eybCHTGt
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression           #Gerekli kütüphaneler import edildi
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")

df = pd.read_excel("KONTR.xlsx")        #Çalışma sayfası dahil edilir

df.head(3)      #Çalışma sayfasının ilk üç değeri getirilir

df.tail(3)           #Çalışma sayfasının son üç değeri getirilir

df.info()           #Özet bilgiler alınır

df.columns      #Datanın kolon isimleri getirilir

df.describe().T     #Özet İstatistiksel bilgiler alınır

df.shape      #Satrı sütün sayısı öğrenilir

df.isnull().any()     #Data içinde boş değer varmı kontrol edilir

df['Hac.'] = df['Hac.'].str.replace("M", "")

df.head(3)

plt.figure(figsize=(16,6))
plt.plot(df['Tarih'], df['Şimdi'], label='Kapanış Fiyatı')
plt.title("KAPANIŞ FİYATI", fontsize=15, fontweight='bold')
plt.xlabel("Tarih", fontsize = 13)
plt.xticks(rotation =50)
plt.ylabel("Fiyat", fontsize =13)
plt.show()

y= df[["Şimdi"]]
x= df.drop(["Şimdi", "Tarih","Hac."], axis=1)

x_train, x_test, y_train, y_test =train_test_split(x,y, train_size=0.70, random_state=21)

scaler = StandardScaler()

x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

start_train_time = time.time()                      #LINEAR REGRESSOR KULLANIMI
lm = LinearRegression()
model = lm.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time


y_train_pred = lm.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)


start_test_time = time.time()
y_test_pred = lm.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time


test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)



print(f"Train_MSE: {train_mse}")
print(f"Train_MAE: {train_mae}")
print(f"Train_R2: {train_kare}")
print(f"Train_Time: {total_time1}")
print(f"Test_MSE: {test_mse}")
print(f"Test_MAE: {test_mae}")
print(f"Test_R2:{test_kare}")
print(f"Test_Time:{total_time2}")

start_train_time = time.time()                              #RANDOM FOREST REGRESSOR KULLANIMI
rf = RandomForestRegressor()
model2 = rf.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred = rf.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train,y_train_pred)


start_test_time = time.time()
y_test_pred = rf.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)



print(f"Train_MSE: {train_mse}")
print(f"Train_MAE: {train_mae}")
print(f"Train_R2:{train_kare}")
print(f"Train_Time: {total_time1}")
print(f"Test_MSE: {test_mse}")
print(f"Test_MAE:{test_mae}")
print(f"Test_R2: {test_kare}")
print(f"Test_Time:{total_time2}")

xgb_params = {
    'n_estimators': [100, 200, 300],                        #XGB REGRESSOR KULLANILDI
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}

xgb = XGBRegressor()
grid_search = GridSearchCV(estimator=xgb, param_grid=xgb_params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=1)


start_train_time = time.time()
grid_search.fit(x_train_scaled, y_train)
best_model = grid_search.best_estimator_
end_train_time = time.time()
total_train_time = end_train_time - start_train_time

print("En İyi Parametreler: ", grid_search.best_params_)
print("En İyi CV Skoru (Negatif MSE): ", -grid_search.best_score_)


y_train_pred = best_model.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = best_model.predict(x_test_scaled)
end_test_time = time.time()
total_test_time = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"Train Time: {total_train_time}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_r2}")
print(f"Test Time: {total_test_time}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_r2}")

start_train_time = time.time()
dc = DecisionTreeRegressor()                            #DECISION TREE REGRESSOR KULLANIMI
model4 = dc.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = time.time()

y_train_pred = dc.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = dc.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)


print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2:{test_kare}")

svr_params = {                              #SVR KULLANIMI
    'C': [0.1, 1, 10],
    'epsilon': [0.01, 0.1, 0.2],
    'kernel': ['linear', 'rbf']
}

svr = SVR()
grid_search = GridSearchCV(estimator=svr, param_grid=svr_params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=1)

start_train_time = time.time()
model5 = grid_search.fit(x_train_scaled, y_train)
best_model = grid_search.best_estimator_
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

print("En İyi Parametreler: ", grid_search.best_params_)
print("En İyi CV Skoru (Negatif MSE): ", -grid_search.best_score_)

y_train_pred = best_model.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = best_model.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)


print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

start_train_time = time.time()                          #LASSO KULLANIMI
ls = Lasso(alpha=0.1)
model6 = ls.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred = ls.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)


start_test_time = time.time()
y_test_pred = ls.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)

print(f"Train Time: {total_time1}")
print(f"Train MSE:{train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time:{total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

start_train_time = time.time()
ridge = Ridge(alpha=1.0)                                #RIDGE KULLANIMI
model7 = ridge.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred = ridge.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = ridge.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

start_train_time = time.time()
elastic_net = ElasticNet(alpha=1.0, l1_ratio=0.5)               #ELASTICNET KULLANIMI
model8 = elastic_net.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred = elastic_net.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = elastic_net.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

start_train_time = time.time()
knn = KNeighborsRegressor(n_neighbors=5)                  #K NEIGHBORS REGRESSOR KULLANIMI
model9 = knn.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred = knn.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_kare = r2_score(y_train, y_train_pred)

start_test_time = time.time()
y_test_pred = knn.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_kare = r2_score(y_test, y_test_pred)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

