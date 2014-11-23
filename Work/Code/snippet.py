import pandas as p

writer = p.ExcelWriter('results/extendedLassoResults.xlsx')

for i in dfs:
    data = dfs[i]

    def get_winner(row):
        if row['RMSE_L4F'] < min(row['RMSE_T_DF'], row['RMSE_T_CF']):
            return "L4F"
        elif row['RMSE_T_DF'] < min(row['RMSE_L4F'], row['RMSE_T_CF']):
            return "TDF"
        else:
            return "TCF"

    data['Winner'] = data.apply(get_winner, axis=1)

    data.to_excel(writer,'%s'%i)

writer.save()


import pandas as presults = p.read_csv('results/lasso-static-and-dynamic.csv') 
df = p.read_csv('tidydata/stdev.csv')

results['Place'] = results['Unnamed: 0']
keeps = ['RMSE TwitterCF', 'RMSE TwitterDF', 'RMSE_L4F', 'StDev', 'Place']
results = results.merge(df, on='Place', how='outer')
for i in results.columns:
    if i not in keeps:
        del results[i]
        

results = results.dropna()
results.to_csv('results/stdevscatter.csv',index=False)


xl_file = p.ExcelFile('results/extendedLassoResults.xlsx')
dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}

df = p.DataFrame()

for i in dfs:
    temp = dfs[i]
    temp['Place'] = i
    print temp.columns
    keeps = ['Place', 'RMSE_T_DF', 'RMSE_T_CF', 'RMSE L4F', 'Aplha']
    for j in temp.columns:
        if j not in keeps:
            del temp[j]
    df = df.append(temp)
df['Alpha'] = df['Aplha']
del df['Aplha']
df.to_csv('results/alpha-rmse.csv', index=False)
    
