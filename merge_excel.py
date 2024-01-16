import pandas as pd
file1 = pd.read_excel('Sentiment 1.xlsx')
file2 = pd.read_excel('Sentiment 2.xlsx')
file3 = pd.read_excel('Sentiment 3.xlsx')
merged_data = pd.concat([file1, file2, file3], ignore_index=True)
merged_data.to_excel('sentiment_fullcorpus.xlsx', index=False)
