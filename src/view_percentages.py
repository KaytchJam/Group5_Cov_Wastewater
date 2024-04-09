import pandas as pd
import numpy as np

def chain_iter(lista, listb, iterations, func):
    for i in range(iterations):
        func(lista[i], listb[i])

def get_poverty_percentage(df):
    population = df["DP05_0001E"].values
    below_poverty = df["S1701_C02_001E"].values

    n = len(population)
    buf = [] * n
    chain_iter(population, below_poverty, n, lambda a, b: buf.append(b / a))
    return buf

def get_education_percentage(df):
    population = df["DP05_0001E"].values
    under_18_bachelors = df["S1501_C01_005E"].values
    over_18_bachelors = df["S1501_C01_012E"].values

    n = len(population)
    buf = [] * n
    chain_iter(population, np.add(under_18_bachelors, over_18_bachelors), n, lambda a, b: buf.append(b / a))
    return buf

def main():
    df = pd.read_csv("preservation/Zip_Key_Demographic_Data_2022.csv", index_col=False)
    pov = get_poverty_percentage(df)
    # print(pov)
    
    edu = get_education_percentage(df)
    # print(edu)

    percents = pd.DataFrame(zip(pov,edu), columns=["Below Poverty Line %", "Bachelor Degree Total %"], index=None)
    merged = pd.concat([df, percents], axis=1)
    merged = merged.drop(["Unnamed: 0"], axis=1)
    merged.to_csv("output/Zip_With_Percentages.csv", index=False)
    # print(merged)

if __name__ == "__main__":
    main()