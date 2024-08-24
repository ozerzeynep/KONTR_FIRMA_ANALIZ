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

dfN = pd.read_excel("KONTR.xlsx")        #Çalışma sayfası dahil edilir

df = dfN.copy()   #Datanın kopyası üzerinden projeye devam ediliyor

df.head(3)      #Çalışma sayfasının ilk üç değeri getirilir

df.tail(3)           #Çalışma sayfasının son üç değeri getirilir

df.info()           #Özet bilgiler alınır

df.columns      #Datanın kolon isimleri getirilir

df.describe().T    #Özet İstatistiksel bilgiler alınır

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

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.regplot(x=y_train, y=y_train_pred, ci=None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel('Gerçek Eğitim Değerleri')
plt.ylabel('Tahmini Eğitim Değerleri')
plt.title('Eğitim Verileri için Lınear Regresyon Doğrusu')
plt.grid(True)



plt.subplot(1, 2, 2)
sns.regplot(x=y_test, y=y_test_pred, ci=None, scatter_kws={"alpha":0.7, "color":"green"}, line_kws={"color":"red"})
plt.xlabel('Gerçek Test Değerleri')
plt.ylabel('Tahmini Test Değerleri')
plt.title('Test Verileri İçin Lınear Regresyon Doğrusu')
plt.grid(True)

plt.tight_layout()
plt.show()

start_train_time = time.time()                              #RANDOM FOREST REGRESSOR KULLANIMI
rf = RandomForestRegressor()
model2 = rf.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred2 = rf.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred2)
train_mae = mean_absolute_error(y_train, y_train_pred2)
train_kare = r2_score(y_train,y_train_pred2)


start_test_time = time.time()
y_test_pred2 = rf.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred2)
test_mae = mean_absolute_error(y_test, y_test_pred2)
test_kare = r2_score(y_test, y_test_pred2)



print(f"Train_MSE: {train_mse}")
print(f"Train_MAE: {train_mae}")
print(f"Train_R2:{train_kare}")
print(f"Train_Time: {total_time1}")
print(f"Test_MSE: {test_mse}")
print(f"Test_MAE:{test_mae}")
print(f"Test_R2: {test_kare}")
print(f"Test_Time:{total_time2}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred2, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin Random Forest Regression Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred2, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin Random Forest Regression Doğrusu")

plt.tight_layout()
plt.show()

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


y_train_pred3 = best_model.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred3)
train_mae = mean_absolute_error(y_train, y_train_pred3)
train_r2 = r2_score(y_train, y_train_pred3)

start_test_time = time.time()
y_test_pred3 = best_model.predict(x_test_scaled)
end_test_time = time.time()
total_test_time = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred3)
test_mae = mean_absolute_error(y_test, y_test_pred3)
test_r2 = r2_score(y_test, y_test_pred3)

print(f"Train Time: {total_train_time}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_r2}")
print(f"Test Time: {total_test_time}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_r2}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred3, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin XGB Regression Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred3, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin XGB Regression Doğrusu")

plt.tight_layout()
plt.show()

start_train_time = time.time()
dc = DecisionTreeRegressor()                            #DECISION TREE REGRESSOR KULLANIMI
model4 = dc.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = time.time()

y_train_pred4 = dc.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred4)
train_mae = mean_absolute_error(y_train, y_train_pred4)
train_kare = r2_score(y_train, y_train_pred4)

start_test_time = time.time()
y_test_pred4 = dc.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred4)
test_mae = mean_absolute_error(y_test, y_test_pred4)
test_kare = r2_score(y_test, y_test_pred4)


print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2:{test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred4, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin DECISION TREE Regression Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred4, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin DECISION TREE Regression Doğrusu")

plt.tight_layout()
plt.show()

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

y_train_pred5 = best_model.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred5)
train_mae = mean_absolute_error(y_train, y_train_pred5)
train_kare = r2_score(y_train, y_train_pred5)

start_test_time = time.time()
y_test_pred5 = best_model.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred5)
test_mae = mean_absolute_error(y_test, y_test_pred5)
test_kare = r2_score(y_test, y_test_pred5)


print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred5, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin SVR Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred5, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin SVR Doğrusu")

plt.tight_layout()
plt.show()

start_train_time = time.time()                          #LASSO KULLANIMI
ls = Lasso(alpha=0.1)
model6 = ls.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred6 = ls.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred6)
train_mae = mean_absolute_error(y_train, y_train_pred6)
train_kare = r2_score(y_train, y_train_pred6)


start_test_time = time.time()
y_test_pred6 = ls.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred6)
test_mae = mean_absolute_error(y_test, y_test_pred6)
test_kare = r2_score(y_test, y_test_pred6)

print(f"Train Time: {total_time1}")
print(f"Train MSE:{train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time:{total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred6, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin Lasso Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred6, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin Lasso Doğrusu")

plt.tight_layout()
plt.show()

start_train_time = time.time()
ridge = Ridge(alpha=1.0)                                #RIDGE KULLANIMI
model7 = ridge.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred7 = ridge.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred7)
train_mae = mean_absolute_error(y_train, y_train_pred7)
train_kare = r2_score(y_train, y_train_pred7)

start_test_time = time.time()
y_test_pred7 = ridge.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred7)
test_mae = mean_absolute_error(y_test, y_test_pred7)
test_kare = r2_score(y_test, y_test_pred7)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred7, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin Rıdge Regression Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred7, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin Rıdge Regression Doğrusu")

plt.tight_layout()
plt.show()

start_train_time = time.time()
elastic_net = ElasticNet(alpha=1.0, l1_ratio=0.5)               #ELASTICNET KULLANIMI
model8 = elastic_net.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred8 = elastic_net.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred8)
train_mae = mean_absolute_error(y_train, y_train_pred8)
train_kare = r2_score(y_train, y_train_pred8)

start_test_time = time.time()
y_test_pred8 = elastic_net.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred8)
test_mae = mean_absolute_error(y_test, y_test_pred8)
test_kare = r2_score(y_test, y_test_pred8)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred8, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin ELASTICNET Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred8, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin ELASTICNET Doğrusu")

plt.tight_layout()
plt.show()

start_train_time = time.time()
knn = KNeighborsRegressor(n_neighbors=5)                  #K NEIGHBORS REGRESSOR KULLANIMI
model9 = knn.fit(x_train_scaled, y_train)
end_train_time = time.time()
total_time1 = end_train_time - start_train_time

y_train_pred9 = knn.predict(x_train_scaled)
train_mse = mean_squared_error(y_train, y_train_pred9)
train_mae = mean_absolute_error(y_train, y_train_pred9)
train_kare = r2_score(y_train, y_train_pred9)

start_test_time = time.time()
y_test_pred9 = knn.predict(x_test_scaled)
end_test_time = time.time()
total_time2 = end_test_time - start_test_time

test_mse = mean_squared_error(y_test, y_test_pred9)
test_mae = mean_absolute_error(y_test, y_test_pred9)
test_kare = r2_score(y_test, y_test_pred9)

print(f"Train Time: {total_time1}")
print(f"Train MSE: {train_mse}")
print(f"Train MAE: {train_mae}")
print(f"Train R2: {train_kare}")
print(f"Test Time: {total_time2}")
print(f"Test MSE: {test_mse}")
print(f"Test MAE: {test_mae}")
print(f"Test R2: {test_kare}")

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
sns.regplot(x= y_train, y= y_train_pred9, ci =None, scatter_kws={"alpha":0.7, "color":"blue"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Eğitim Değerleri")
plt.ylabel("Tahmini Eğitim Değerleri")
plt.title("Eğitim Verileri İçin K NEIGHBORS Doğrusu")
plt.grid(True)


plt.subplot(1,2,2)
sns.regplot(x= y_test, y= y_test_pred9, ci=None, scatter_kws={"alpha": 0.7, "color": "green"}, line_kws={"color":"red"})
plt.xlabel("Gerçek Test Değerleri")
plt.ylabel("Tahmini Test Değerleri")
plt.title("Test Verileri İçin K NEIGHBORS Doğrusu")

plt.tight_layout()
plt.show()

models = ['Linear Regression', 'Random Forest Regression', 'XGB REGRESSOR', 'DECISION TREE REGRESSOR', 'SVR', 'LASSO', 'RIDGE', 'ELASTICNET', 'K NEIGHBORS REGRESSOR']
r2_skor = [0.9994, 0.9998, 0.9999, 1.0, 0.9992, 0.9990, 0.9991, 0.9762, 0.9982]

plt.figure(figsize=(16, 6))
sns.barplot(x=models, y=r2_skor, palette="magma")
plt.title('Model R² Scores Comparison', fontsize=16)
plt.xlabel('Models', fontsize=14)
plt.ylabel('R² Score', fontsize=14)
plt.ylim(0.95, 1.02)
plt.xticks(rotation=45, ha='right', fontsize=12)

for index, value in enumerate(r2_skor):
    plt.text(index, value + 0.002, f'{value:.4f}', ha='center', fontsize=12)

plt.show()

