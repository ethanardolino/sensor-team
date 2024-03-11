import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt
import numpy as np

class Specs18650:
    outer_r = 9e-3
    length = 65e-3
    thickness = 220e-6
    inner_r = outer_r - thickness
    k = 0.43

    def max_temp(self, row):
        t_init = row['max_cell_temp']
        heat_loss= row['heat_loss']
        num = (heat_loss*np.log(self.outer_r/self.inner_r) / (2*np.pi*self.k*self.length)) + t_init
        return num

def clean_battery_failure_data() -> pd.DataFrame:
    data = pd.read_excel('../data/battery_failure.xlsx', sheet_name='Battery Failure Databank')
    # create internal sql databse connection
    engine = create_engine('sqlite://').connect()
    # create 'battery' table in sql engine
    data.to_sql('battery', con=engine, if_exists='replace', index=False)
    
    # clean the data
    with open('./battery_failure_cleaning.sql', 'r') as f:
        query = text(f.read())
    result = engine.execute(query)
    return pd.DataFrame(result.fetchall(), columns=result.keys())

def cell_energy_released():
    # separate data by cell type
    data: pd.DataFrame = clean_battery_failure_data()
    cell18650 = data[data.format == '18650']
    cell21700 = data[data.format == '21700']
    cellDCell = data[data.format == 'D-Cell']

    results = {}
    for cell_type, cell_data in {'18650': cell18650, '21700': cell21700, 'dCell': cellDCell}.items():
        model = LinearRegression()
        
        energy = cell_data['avg_energy']
        capacity = cell_data[['capacity']]
        model.fit(capacity, energy)
        
        energy_prediction = model.predict(capacity)
        plt.plot(capacity, energy_prediction, marker='o', label='Predicted')
        plt.plot(capacity, energy, marker='s', label='Actual')
        plt.title(f'Energy v Capacity for cell type={cell_type}')
        plt.xlabel('Capacity (Ah)')
        plt.ylabel('Energy Realeased(kJ)')
        print(f'MSE: {mse(energy, energy_prediction)}')
        results[cell_type] = (model.coef_, model.intercept_)
        plt.show()
    return results

def cell_max_temp():
    # separate data by cell type
    cell_specs = Specs18650()
    data: pd.DataFrame = clean_battery_failure_data()
    cell18650 = data.loc[(data.format == '18650') & (data.trigger!='Nail'), ["max_cell_temp", "heat_loss", "capacity"]]
    cell18650['max_temps'] = cell18650.apply(cell_specs.max_temp, axis=1)
    
    model = LinearRegression()
    
    max_temp = cell18650['max_cell_temp']
    capacity = cell18650[['capacity']]
    model.fit(capacity, max_temp)
    
    max_temp_prediction = model.predict(capacity)
    plt.plot(capacity, max_temp_prediction, marker='o', label='Predicted')
    plt.plot(capacity, max_temp, marker='s', label='Actual')
    plt.title(f'Max Temp v Capacity for cell type=18650')
    plt.xlabel('Capacity (Ah)')
    plt.ylabel('Max Temp (C)')
    plt.show()
    print(f'MSE: {mse(max_temp, max_temp_prediction)}')
    return {'18650': (model.coef_, model.intercept_)}
    

def est(parameters: dict, amps:float, value:str):
    for cell, (slope, y_int) in parameters.items():
        print(f'(cell={cell})Estimated {value} w/ {amps}Ah: {slope[0]*amps + y_int}')

if __name__ == '__main__':
    # print(est(cell_energy_released(), 60, "energy"))
    cell_max_temp()

