if (!require("MLmetrics")) install.packages("MLmetrics")
library(MLmetrics)
if (!require("spdep")) install.packages("spdep")
library(spdep)
if (!require("spatialreg")) install.packages("spatialreg")
library(spatialreg)

sf_use_s2(FALSE)
source("load.R")


set.seed(101)

x_names= I(list(c('NROOM', 'DWELL', 'NBATH', 'PATIO', 'FIREPL', 'AC', 'BMENT', 'NSTOR', 'GAR', 'AGE', 'CITCOU',
            'LOTSZ', 'SQFT'), c('accommodat', 'review_sco', 'bedrooms', 'bathrooms', 'beds'),
          c('nhousingUn', 'recHouses', 'nMobileHom', 'yearBuilt', 'nBadPlumbi', 'nBadKitche', 'nRooms',
            'nBedrooms', 'medHHinc', 'Population', 'Males', 'Females', 'Under5', 'MedianAge', 'White', 'Black',
            'AmericanIn', 'Asian', 'Hispanic', 'PopInHouse', 'nHousehold', 'Families', 'householdS', 'familySize')))
file_names=c("baltim.shp","prenzlauer.shp","houses2000.shp")
y_name=c("PRICE","price","houseValue")
datasets = data.frame(row.names=c("baltimore","berlin","california"), file_name=file_names, y_name=y_name, x_names=x_names)

for(i in 3:3) {
  row <- datasets[i,]
  filename <- file.path("data", rownames(datasets)[i], row["file_name"])
  data <- vect(filename)
  data = sf::st_as_sf(data)
  data$id <- 1:nrow(data)
  
  # plot(data)
  # next
  
  sample <- sample.int(n = nrow(data), size = floor(.8*nrow(data)), replace = F)
  train <- data[sample, ]
  test  <- data[-sample, ]
  y = as.data.frame(test[,unlist(row["y_name"])])[,1]

  if (st_geometry_type(data[1,]) == "POINT"){
    data.nb <- knn2nb(knearneigh(data, k=3), row.names=data$id)
    train.nb <- knn2nb(knearneigh(train, k=3), row.names=train$id)
  } else if (st_geometry_type(data[1,]) == "POLYGON") {
    data.nb <- poly2nb(data)
    train.nb <- poly2nb(train)
  }
  lw <- nb2listw(data.nb, zero.policy = T)
  lw_train <- nb2listw(train.nb, zero.policy = T)
  
  formula_string = paste(row["y_name"], " ~ ", paste(unlist(row["x_names"]), collapse=" + "),sep = "")
  formula <- as.formula(formula_string)

  start_time <- Sys.time()
  ols <- lm(formula, data=train)
  train_time <- Sys.time()
  preds <- predict(ols, test)
  pred_time <- Sys.time()
  print(paste(mean(y), sd(y), MAE(preds, y), MAE(preds, y)/mean(y), train_time-start_time, pred_time - train_time, sep = "  "))

  start_time <- Sys.time()
  lag_model <- lagsarlm(formula, data=train, listw=lw_train, zero.policy = T)
  train_time <- Sys.time()
  lag_model$call = ols$terms
  preds_lag <- predict(lag_model, newdata=test, listw=lw, pred.type="trend")
  pred_time <- Sys.time()
  print(paste(mean(y), sd(y), MAE(preds_lag, y), MAE(preds_lag, y)/mean(y), train_time-start_time, pred_time - train_time, sep = "  "))

  start_time <- Sys.time()
  error_model <- errorsarlm(formula, data=train, lw_train, zero.policy = T)
  train_time <- Sys.time()
  error_model$call = ols$terms
  preds_error <- predict(error_model, newdata=test, listw=lw)
  pred_time <- Sys.time()
  print(paste(mean(y), sd(y), MAE(preds_error, y), MAE(preds_error, y)/mean(y), train_time-start_time, pred_time - train_time, sep = "  "))
}
