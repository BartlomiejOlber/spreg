import geopandas as gpd
import spreg
import numpy as np
import time
import matplotlib.pyplot as plt
from libpysal.weights import KNN, Kernel, Rook, fill_diagonal, Queen
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, mean_absolute_error

datasets = {
    "baltimore": {
        "name": "baltim.shp",
        "y_name": "PRICE",
        "x_names": ['NROOM', 'DWELL', 'NBATH', 'PATIO', 'FIREPL', 'AC', 'BMENT', 'NSTOR', 'GAR', 'AGE', 'CITCOU',
                    'LOTSZ', 'SQFT']
    },
    "berlin": {
        "name": "prenzlauer.shp",
        "y_name": "price",
        "x_names": ['accommodat', 'review_sco', 'bedrooms', 'bathrooms', 'beds']
    },
    "california": {
        "name": "houses2000.shp",
        "y_name": "houseValue",
        "x_names": ['nhousingUn', 'recHouses', 'nMobileHom', 'yearBuilt', 'nBadPlumbi', 'nBadKitche', 'nRooms',
                    'nBedrooms', 'medHHinc', 'Population', 'Males', 'Females', 'Under5', 'MedianAge', 'White', 'Black',
                    'AmericanIn', 'Asian', 'Hispanic', 'PopInHouse', 'nHousehold', 'Families', 'householdS',
                    'familySize']
    }
}


def inference_ols(model, x):
    return spreg.spu.spdot(x, model.betas).flatten()


def inference_lag(model, x):
    xtx = spreg.spu.spdot(x.T, x)
    xtxi = np.linalg.inv(xtx)
    y_pred_ols = spreg.spu.spdot(x, model.betas).flatten()
    xty = spreg.spu.spdot(x.T, self.y)
    xtyl = spreg.spu.spdot(x.T, ylag)
    b0 = spreg.spu.spdot(xtxi, xty)
    b1 = spreg.spu.spdot(xtxi, xtyl)
    b = b0 - model.rho * b1
    xb = spreg.spu.spdot(model.x, b)

    self.predy_e = inverse_prod(
        w.sparse, xb, self.rho, inv_method="power_exp", threshold=epsilon
    )


def inference_error(model, x):
    return spreg.spu.spdot(x, model.betas).flatten()


results = dict()

for dataset in datasets:
    gdf = gpd.read_file(f"data/{dataset}/{datasets[dataset]['name']}")
    # print(gdf.geom_type)
    train, test = train_test_split(gdf, test_size=0.2)
    if gdf.geom_type[0] == "Point":
        spatial_weights = Kernel.from_dataframe(train)
        spatial_weights = fill_diagonal(spatial_weights, np.zeros(spatial_weights.n))
    else:
        spatial_weights = Queen.from_dataframe(train)
        continue

    spatial_weights.transform = 'r'
    x_names = datasets[dataset]['x_names']
    y_name = datasets[dataset]['y_name']
    y = train[y_name].to_numpy()
    x = train[x_names].to_numpy()
    results[dataset] = dict()
    start = time.time()
    model_ols = spreg.OLS(y, x, w=spatial_weights, name_x=x_names, name_y=y_name)
    results[dataset]["time_ols"] = time.time() - start
    start = time.time()
    model_lag = spreg.ML_Lag(y, x, w=spatial_weights, name_x=x_names, name_y=y_name)
    results[dataset]["time_lag"] = time.time() - start
    start = time.time()
    model_error = spreg.ML_Error(y, x, w=spatial_weights, name_x=x_names, name_y=y_name)
    results[dataset]["time_error"] = time.time() - start

    y_test = test[y_name].to_numpy()
    x_test = test[x_names].to_numpy()
    x_test, _, _ = spreg.USER.check_constant(x_test, x_names)
    y_pred_ols = inference_ols(model_ols, x_test)
    results[dataset]["ols"] = mean_absolute_percentage_error(y, model_ols.predy)
    results[dataset]["lag"] = mean_absolute_percentage_error(y, model_lag.predy)
    results[dataset]["error"] = mean_absolute_percentage_error(y, model_error.predy)

    # y_pred_lag = inference_lag(model_lag, x_test)
    # y_pred_error = inference_error(model_error, x_test)
    # print(mean_squared_error(y_test, y_pred_ols), mean_squared_error(y_test, y_pred_lag),
    #       mean_squared_error(y_test, y_pred_error))
    # print(spatial_weights.neighbors)
    # spatial_weights.plot(gdf)
    # plt.show()
    # ax = gdf.plot()
    # ax.set_axis_off()
    # plt.show()
    # ax = gdf.plot(edgecolor='grey', facecolor='w')
    # f, ax = spatial_weights.plot(gdf, ax=ax,
    #                              edge_kws=dict(color='r', linestyle=':', linewidth=1),
    #                              node_kws=dict(marker=''))
    # ax.set_axis_off()
    # plt.show()
print(results)