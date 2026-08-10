from ucimlrepo import fetch_ucirepo

dataset = fetch_ucirepo(id=863)
X = dataset.data.features #input variables
y = dataset.data.targets #risk level (target variable) low, mid, high

print(X.head())  #print first 5 rows of the input variables
print(X.shape) #print the shape of the input variables


print(y.value_counts()) #print the number of samples for each risk level
