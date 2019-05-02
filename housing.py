import time

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import logbook
import sys
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier

predict_log = logbook.Logger('<Logging>')


def load_data(train_file, test_file):
    t0 = time.time()
    predict_log.trace('Loading file to python.')

    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file)

    t1 = time.time()

    predict_log.trace('File loaded to python in {} ms'.format(int(1000*(t1-t0))))

    return train, test


def main():
    tstart = time.time()
    train_file = 'datasets/housing/housing_train.csv'
    test_file = 'datasets/housing/housing_test.csv'

    train, test = load_data(train_file, test_file)  # function created

    house_train, house_test, y, df = clean_data(train, test)  # specific for housing data set

    x = house_train

    predict_log.trace("Performing Prediction: Performing prediction using Random Forest")

    final_model = RandomForestRegressor(n_estimators=400, random_state=22)
    final_model.fit(x, y)

    predict_log.trace("Performing Prediction: Fitting the data")

    test_preds = final_model.predict(house_test)

    predict_log.trace("Performing Prediction: Saving prediction to CSV file")

    output = pd.DataFrame({'Id': test.Id,
                           'SalePrice': test_preds})
    output.to_csv('datasets/submission_test.csv', index=False)

    tfinal = time.time()

    predict_log.trace("DONE! All process took {} seconds ".format(int(tfinal-tstart)))


def clean_df(df):
    pass


def clean_data(train, test):

    """features = ['MSSubClass', 'MSZoning', 'LotArea', 'Street', 'LotShape', 'LandContour', 'Utilities',
                'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle',
                'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'RoofStyle', 'RoofMatl',
                'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure',
                'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'Heating',
                'HeatingQC', 'CentralAir', 'Electrical', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea',
                'BedroomAbvGr', 'KitchenAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 'Functional', 'Fireplaces',
                'FireplaceQu', 'GarageType', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond', 'WoodDeckSF',
                'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MoSold', 'YrSold']"""

    t0 = time.time()
    predict_log.trace('Cleaning the data.')

    y = train.SalePrice
    x_train = train.drop(['Id', 'SalePrice'], axis=1)  # .loc[:,features]
    x_test = test.drop('Id', axis=1)  # .loc[:,features]
    x_test['Type'] = 'test'
    x_train['Type'] = 'train'

    df = pd.concat([x_train, x_test], sort=False)

    predict_log.trace('Cleaning the data: Filling up NULL MSZoning Values')

    df.loc[(df.MSZoning.isna()) & (df.MSSubClass == 30) & (df.Street == 'Grvl'), 'MSZoning'] = 'C (all)'
    df.loc[(df.MSZoning.isna()) & (df.Street == 'Pave'), 'MSZoning'] = 'RL'

    predict_log.trace('Cleaning the data: Filling up NULL values for Utilities and Veneer')

    df.loc[df.Utilities.isna(), 'Utilities'] = 'AllPub'

    df.loc[df.MasVnrArea.isna(), 'MasVnrArea'] = 0.0

    predict_log.trace('Cleaning the data: Filling up NULL values Basement with Square feet with 0 and Quality with NB')

    df.loc[(df.TotalBsmtSF.isna()), ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']] = [0.0, 0.0, 0.0, 0.0]

    df.loc[(df.BsmtQual.isna() & df.BsmtCond.isna()), ['BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1',
                                                       'BsmtFinType2']] = ['NB', 'NB', 'NB', 'NB', 'NB']

    predict_log.trace("Cleaning the data: Label all other records which has NA values "
                      "in some of the column to 'TA' or Good Quality")

    # Label all other records which has NA values in some of the column to 'TA' or Good Quality
    df.loc[(df.BsmtQual.isna() & df.BsmtCond.notna()), 'BsmtQual'] = 'TA'
    df.loc[(df.BsmtCond.isna() & df.BsmtQual.notna()), 'BsmtCond'] = 'TA'
    df.loc[(df.BsmtExposure.isna() & df.BsmtQual.notna()), 'BsmtExposure'] = 'Gd'
    df.loc[df.BsmtFinType2.isna() & df.BsmtQual.notna(), 'BsmtFinType2'] = 'GLQ'

    # Fix NULL Electrical
    df.loc[(df.Electrical.isna()), 'Electrical'] = 'SBrkr'

    df.loc[df.KitchenQual.isna(), 'KitchenQual'] = 'TA'

    predict_log.trace("Cleaning the data: Fixing records for fire places ")
    # Make all No Fireplace records as NF
    df.loc[df.FireplaceQu.isna(), 'FireplaceQu'] = 'NF'

    predict_log.trace("Cleaning the data: Fixing records for garage ")
    # Based on mean records, fill in incomplete data for Garage.
    df.loc[df.GarageCars.isna(), ['GarageCars', 'GarageArea', 'GarageQual', 'GarageCond']] = [2.0, 420.0, 'TA', 'TA']

    # Based on mean records, fill in incomplete data for Garage.
    df.loc[(df.GarageType.notna() & df.GarageQual.isna()), ['GarageQual', 'GarageCond']] = ['TA', 'TA']

    # Fill all no garage records as NG
    df.loc[df.GarageType.isna(), ['GarageYrBlt', 'GarageFinish',
                                  'GarageType', 'GarageQual', 'GarageCond']] = ['NG', 'NG', 'NG', 'NG', 'NG']

    df.loc[df.Functional.isna(), 'Functional'] = 'Typ'
    df.loc[df.Alley.isna(), 'Alley'] = 'NoAc'

    df.loc[df.LotFrontage.isna(), 'LotFrontage'] = 69.0
    df.loc[df.Exterior1st.isna(), ['Exterior1st', 'Exterior2nd']] = ['Other', 'Other']
    df.loc[((df.MasVnrType.isna()) & (df.MasVnrArea == 0.0)), 'MasVnrType'] = 'NV'
    df.loc[(df.MasVnrType.isna()), 'MasVnrType'] = 'BrkFace'
    df.loc[df.BsmtFullBath.isna(), ['BsmtFullBath', 'BsmtHalfBath']] = [0.0, 0.0]

    df.loc[df.GarageYrBlt.isna(), 'GarageFinish'] = 'Fin'
    df.loc[((df.GarageYrBlt.isna()) & (df.YearRemodAdd == 1983)), 'GarageYrBlt'] = 1983
    df.loc[((df.GarageYrBlt.isna()) & (df.YearRemodAdd == 1999)), 'GarageYrBlt'] = 1999
    df.loc[((df.PoolQC.isna()) & (df.PoolArea > 0)), 'PoolQC'] = 'TA'
    df.loc[((df.PoolQC.isna()) & (df.PoolArea == 0)), 'PoolQC'] = 'NP'
    df.loc[df.Fence.isna(), 'Fence'] = 'NF'
    df.loc[df.MiscFeature.isna(), 'MiscFeature'] = 'NF'
    df.loc[df.SaleType.isna(), 'SaleType'] = 'Othr'

    predict_log.trace("Classifying data: Performing one hot encoding for the data")

    df_onehot = df.copy()

    # df_onehot_Zoning = pd.get_dummies(df_onehot.loc[:, 'MSZoning'])
    # df_onehot_Lot = pd.get_dummies(df_onehot.loc[:, ['LotFrontage', 'LotArea', 'LotShape']])

    df_type = df_onehot.loc[:, 'Type']
    df_onehot = df_onehot.drop('Type', axis=1)
    df_onehot = pd.get_dummies(df_onehot)
    df_onehot = pd.concat([df_onehot, df_type], axis=1)

    house_train = df_onehot.loc[df_onehot.Type == 'train', :]
    house_train = house_train.drop('Type', axis=1)

    house_test = df_onehot.loc[df_onehot.Type == 'test', :]
    house_test = house_test.drop('Type', axis=1)

    predict_log.trace("Classifying data: Done performing one hot encoding")

    t1 = time.time()
    predict_log.trace("Classifying data: Returning required value, train, test, y and dataframe")

    predict_log.trace("Classifying data: Cleaning data done in {} ms".format(int(1000*(t1-t0))))

    return house_train, house_test, y, df


def init_logging(filename: str = None):
    level = logbook.TRACE  # trace, error, notices and warnings

    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = 'Logging is initialized, level {}, mode {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename)

    logger = logbook.Logger('Startup')
    logger.notice(msg)


if __name__ == '__main__':
    init_logging('logs/housing.log')
    main()

