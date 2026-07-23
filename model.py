from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


X=df[
[
"Age",
"Total Sales"
]
]


y=df["Customer Type"]


X_train,X_test,y_train,y_test=train_test_split(
X,y,
test_size=0.2,
random_state=42
)


model=RandomForestClassifier()

model.fit(
X_train,
y_train
)


accuracy=model.score(
X_test,
y_test
)

print(
"Model Accuracy:",
accuracy
)
