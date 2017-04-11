import pandas as pd
from datetime import datetime, timedelta



def load_data(fname):
	df = pd.read_csv(fname)
	return df


def data_preprocessing(df):
	start = datetime(2001, 1, 1, 0, 0, 0)
	end = datetime(2001, 1, 1, 23, 0, 0)
	time_list = []
	while start < end:
		time_list.append([start.strftime("%H:%M:%S.%f")[:-4].replace('.',':'), 0])
		start = start + timedelta(seconds=0.01)

	df_index = pd.DataFrame(time_list)
	df_index.columns = ['time', 'blank']
	df_index = df_index.set_index('time')
	print(df_index)

	df.columns = ['date', 'time', 'kind', 'r1', 'r2']
	df = df.drop('date', 1)
	df = df.set_index('time')
	df1 = df.loc[df['kind']=='USD/JPY']
	df2 = df.loc[df['kind']=='EUR/JPY']
	df3 = df.loc[df['kind']=='EUR/USD']
	df1.columns = ['kind', 'UJ1', 'UJ2']
	df2.columns = ['kind', 'EJ1', 'EJ2']
	df3.columns = ['kind', 'EU1', 'EU2']
	df1 = df1.drop('kind', 1)
	df2 = df2.drop('kind', 1)
	df3 = df3.drop('kind', 1)
	df4 = pd.concat([df_index, df1, df2, df3], axis=1)
	df4 = df4.drop('blank', 1)
	df4 = df4.interpolate()
	df4 = df4.fillna(method='pad')
	df4 = df4.dropna()
	return df4

if __name__ == '__main__':	
	fname = "FOREX_0to23.csv"
	data = load_data(fname)
	data = data_preprocessing(data)
