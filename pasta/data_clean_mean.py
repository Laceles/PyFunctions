

def clean_null(dataset, substitute):
  dataset2 = dataset.select_dtypes(include= ['float', 'int'])
  Ncolumns = list(dataset2.columns)
  if substitute == 'mean':
    for x in Ncolumns:
      y = dataset2[x].mean()
      dataset2[x].fillna(y, inplace = True)
  if substitute == 'median':
    for x in Ncolumns:
      y = dataset2[x].median()
      dataset2[x].fillna(y, inplace = True)
  return dataset2