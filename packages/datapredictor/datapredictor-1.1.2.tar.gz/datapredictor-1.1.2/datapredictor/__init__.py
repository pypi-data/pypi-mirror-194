from sklearn.metrics import (r2_score,
                             mean_squared_error,
                             mean_absolute_error,
                             mean_absolute_percentage_error,
                             )
from sklearn.linear_model import (LinearRegression,
                                  Lasso,
                                  BayesianRidge,
                                  Ridge,
                                  LassoLars)
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (RandomForestRegressor,
                              ExtraTreesRegressor,
                              BaggingRegressor,
                              HistGradientBoostingRegressor
                              )

from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np


class Datapredictor:
    def __init__(self, data, predict_col, file_name, similar_file_name):
        self.data = data
        self.predict_col = predict_col
        self.file_name = file_name
        self.similar_file_name = similar_file_name

    def data_predict(self):
        x = self.data
        x = x.drop(self.predict_col, axis=1)
        y = self.data[self.predict_col]
        X_train, X_validation, Y_train, Y_validation = train_test_split(x, y, random_state=45)
        ############################################################1
        model_1 = LinearRegression().fit(X_train, Y_train)
        pred_1 = model_1.predict(X_validation)
        ############################################################2
        model_2 = DecisionTreeRegressor().fit(X_train, Y_train)
        pred_2 = model_2.predict(X_validation)
        ############################################################3
        model_3 = RandomForestRegressor().fit(X_train, Y_train)
        pred_3 = model_3.predict(X_validation)
        ############################################################4
        model_4 = Lasso().fit(X_train, Y_train)
        pred_4 = model_4.predict(X_validation)
        ############################################################5
        model_5 = BayesianRidge().fit(X_train, Y_train)
        pred_5 = model_5.predict(X_validation)
        ############################################################6
        model_6 = LassoLars().fit(X_train, Y_train)
        pred_6 = model_6.predict(X_validation)
        ############################################################7
        model_7 = Ridge().fit(X_train, Y_train)
        pred_7 = model_7.predict(X_validation)
        ############################################################8
        model_8 = BaggingRegressor().fit(X_train, Y_train)
        pred_8 = model_8.predict(X_validation)
        ############################################################9
        model_9 = HistGradientBoostingRegressor().fit(X_train, Y_train)
        pred_9 = model_9.predict(X_validation)
        ############################################################10
        model_10 = ExtraTreesRegressor().fit(X_train, Y_train)
        pred_10 = model_10.predict(X_validation)
        # return model_1,pred_1,model_2,pred_2,model_3,pred_3,model_4,pred_4,model_5,pred_5,model_6,pred_6,model_7,pred_7,model_8,pred_8,model_9,pred_9,model_10,pred_10
        dtf = {
            "LinearRegression": [*pred_1],
            "DecisionTreeRegressor": [*pred_2],
            "RandomForestRegressor": [*pred_3],
            "Lasso": [*pred_4],
            "BayesianRidge": [*pred_5],
            "LassoLars": [*pred_6],
            "Ridge": [*pred_7],
            "BaggingRegressor": [*pred_8],
            "HistGradientBoostingRegressor": [*pred_9],
            "ExtraTreesRegressor": [*pred_10],
        }
        dtf2 = pd.DataFrame(dtf)
        csv_file = dtf2.to_csv(f"{self.file_name}.csv")
        data_1 = pd.read_csv(f"{self.file_name}.csv")
        all_r2_result = {
            "LinearRegression": [r2_score(Y_validation, data_1["LinearRegression"]),
                                 mean_squared_error(Y_validation, data_1["LinearRegression"]),
                                 mean_absolute_error(Y_validation, data_1["LinearRegression"]),
                                 mean_absolute_percentage_error(Y_validation, data_1["LinearRegression"]),
                                ],
            "DecisionTreeRegressor": [r2_score(Y_validation, data_1["DecisionTreeRegressor"]),
                                      mean_squared_error(Y_validation, data_1["DecisionTreeRegressor"]),
                                      mean_absolute_error(Y_validation, data_1["DecisionTreeRegressor"]),
                                      mean_absolute_percentage_error(Y_validation, data_1["DecisionTreeRegressor"]),
                                      ],
            "RandomForestRegressor": [r2_score(Y_validation, data_1["RandomForestRegressor"]),
                                      mean_squared_error(Y_validation, data_1["RandomForestRegressor"]),
                                      mean_absolute_error(Y_validation, data_1["RandomForestRegressor"]),
                                      mean_absolute_percentage_error(Y_validation, data_1["RandomForestRegressor"]),
                                      ],
            "Lasso": [r2_score(Y_validation, data_1["Lasso"]), mean_squared_error(Y_validation, data_1["Lasso"]),
                      mean_absolute_error(Y_validation, data_1["Lasso"]),
                      mean_absolute_percentage_error(Y_validation, data_1["Lasso"]),
                      ],
            "BayesianRidge": [r2_score(Y_validation, data_1["BayesianRidge"]),
                                 mean_squared_error(Y_validation, data_1["BayesianRidge"]),
                                 mean_absolute_error(Y_validation, data_1["BayesianRidge"]),
                                 mean_absolute_percentage_error(Y_validation, data_1["BayesianRidge"]),
                                 ],
            "LassoLars": [r2_score(Y_validation, data_1["LassoLars"]),
                               mean_squared_error(Y_validation, data_1["LassoLars"]),
                               mean_absolute_error(Y_validation, data_1["LassoLars"]),
                               mean_absolute_percentage_error(Y_validation, data_1["LassoLars"]),
                               ],
            "Ridge": [r2_score(Y_validation, data_1["Ridge"]), mean_squared_error(Y_validation, data_1["Ridge"]),
                      mean_absolute_error(Y_validation, data_1["Ridge"]),
                      mean_absolute_percentage_error(Y_validation, data_1["Ridge"]),
                      ],
            "BaggingRegressor": [r2_score(Y_validation, data_1["BaggingRegressor"]),
                                 mean_squared_error(Y_validation, data_1["BaggingRegressor"]),
                                 mean_absolute_error(Y_validation, data_1["BaggingRegressor"]),
                                 mean_absolute_percentage_error(Y_validation, data_1["BaggingRegressor"]),
                                 ],
            "HistGradientBoostingRegressor": [r2_score(Y_validation, data_1["HistGradientBoostingRegressor"]),
                             mean_squared_error(Y_validation, data_1["HistGradientBoostingRegressor"]),
                             mean_absolute_error(Y_validation, data_1["HistGradientBoostingRegressor"]),
                             mean_absolute_percentage_error(Y_validation, data_1["HistGradientBoostingRegressor"]),
                            ],
            "ExtraTreesRegressor": [r2_score(Y_validation, data_1["ExtraTreesRegressor"]),
                                    mean_squared_error(Y_validation, data_1["ExtraTreesRegressor"]),
                                    mean_absolute_error(Y_validation, data_1["ExtraTreesRegressor"]),
                                    mean_absolute_percentage_error(Y_validation, data_1["ExtraTreesRegressor"]),
                                    ],
        }
        all_r2_result_1 = pd.DataFrame(all_r2_result, index=["r2_score", "mean_squared_error", "mean_absolute_error",
                                                             "mean_absolute_percentage_error"])
        score_result = all_r2_result_1.to_csv(f"{self.similar_file_name}.csv")

        return f"{self.file_name} was created successfully:)\n{self.similar_file_name} was created successfully!"
