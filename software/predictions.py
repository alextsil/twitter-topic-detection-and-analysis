pos = 0
neg = 0
myvars = {}
with open("tweet_predictions.txt") as myfile:
    for line in myfile:
        name, var = line.partition(",")[::2]
        myvars[name.strip()] = float(var)
        if float(var) == 1.0:
            pos=pos+1
        else:
            neg=neg+1
print("# positive tweets:",pos)
print("Percentage",pos/(pos+neg)*100)
print("# negative tweets:",neg)
print("Percentage",neg/(pos+neg)*100)
print("Total number of tweets:",pos+neg)