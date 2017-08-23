######### 02
fig, axes = plt.subplots(1, 4)
line = np.linspace(-3, 3, 20)
for i, ax in enumerate(axes):
    ax.plot(line ** (i + 1))

######### 03
housing.plot(x='latitude', y='longitude', kind='scatter', c='population')

housing.plot(x='latitude', y='longitude', kind='scatter', c='population', alpha=.5, cmap='viridis')


# could have also done kind='hexbin' but that doesn't show us a helpful docstring:
# housing.plot(x='latitude', y='longitude', kind='hexbin', C='population', cmap='viridis')
housing.plot.hexbin(x='latitude', y='longitude', C='population', cmap='viridis', linewidth=0)

housing.plot.hexbin(x='latitude', y='longitude', C='population', cmap='viridis', reduce_C_function=sum, linewidth=0)



fig, axes = plt.subplots(2, 3, subplot_kw={'xticks': (), 'yticks': ()})
for column, ax in zip(housing.columns[2:-2], axes.ravel()):
    if column in ['housing_median_age', 'median_income']:
        reduce = np.mean
    else:
        reduce = np.sum
    housing.plot.hexbin(x='latitude', y='longitude', C=column, cmap='viridis', reduce_C_function=reduce, linewidth=0, ax=ax)
    ax.set_title(column)
plt.tight_layout()


 housing.plot.hexbin(x='latitude', y='longitude', C='median_house_value', cmap='viridis', linewidth=0)


# two outliers:
print((housing_nonull.population > 20000).sum())
pd.plotting.scatter_matrix(housing_nonull.iloc[:, 2:-2], c=housing_nonull.population > 20000, cmap='tab10');
plt.figure()
plt.scatter(housing_nonull.latitude, housing_nonull.longitude, c=plt.cm.tab10((housing_nonull.population > 20000).astype(int)), s=3)

# vs dependent variable:
fig, axes = plt.subplots(4, 2)
for ax, column in zip(axes.ravel(), continuous_dependent):
    ax.scatter(housing_nonull[column], housing_nonull['median_house_value'], alpha=.01)
    ax.set_title(column)
plt.tight_layout()

# vs dependen variable with seaborn

sns.pairplot(housing_nonull, x_vars=continuous_dependent, y_vars=["median_house_value"],
             kind="scatter", plot_kws={'alpha': .01, 'edgecolor': None});
# we'll see a nice way in the next notebook

####### 4
# for the housing data
housing = pd.read_csv("data/housing.csv")

housing.head()

housing_dummies = pd.get_dummies(housing)
housing_dummies.head()

# ridge regression on housing
from sklearn.linear_model import Ridge

housing = pd.read_csv("data/housing.csv")
housing = housing.dropna(axis=0)
housing_dummies = pd.get_dummies(housing)
housing_dummies.head()
y = housing_dummies.pop("median_house_value")
X = housing_dummies
print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
ridge = Ridge()

ridge.fit(X_train_scaled, y_train)
ridge.score(X_test_scaled, y_test)
