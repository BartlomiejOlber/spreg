import time
import warnings

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from libpysal.weights import KNN, Kernel, Queen, Rook, fill_diagonal
from sklearn.model_selection import train_test_split

import spreg

warnings.filterwarnings("ignore")


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

results = dict()

for dataset in datasets:
    gdf = gpd.read_file(f"data/{dataset}/{datasets[dataset]['name']}")
    train, test = train_test_split(gdf, test_size=0.2)
    if gdf.geom_type[0] == "Point":
        spatial_weights = Kernel.from_dataframe(train)
        spatial_weights = fill_diagonal(spatial_weights, np.zeros(spatial_weights.n))
    else:
        continue
        spatial_weights = Queen.from_dataframe(train)

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

    # print(spatial_weights.neighbors)
    spatial_weights.plot(gdf)
    plt.show()
    ax = gdf.plot()
    ax.set_axis_off()
    plt.show()
    # ax = gdf.plot(edgecolor='grey', facecolor='w')
    # f, ax = spatial_weights.plot(gdf, ax=ax,
    #                              edge_kws=dict(color='r', linestyle=':', linewidth=1),
    #                              node_kws=dict(marker=''))
    # ax.set_axis_off()
    # plt.show()
print(results)
