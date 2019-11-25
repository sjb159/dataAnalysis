'''
Created on 29 Oct 2019

@author: wvx67826
'''
import matplotlib.pyplot as plt
import numpy as np
from Tools import Tools 
from lmfit import models
from scipy import signal
import math
import random
def generate_model(spec):
    composite_model = None
    params = None
    x = spec['x']
    y = spec['y']
    x_min = np.min(x)
    x_max = np.max(x)
    x_range = x_max - x_min
    y_max = np.max(y)
    for i, basis_func in enumerate(spec['model']):
        prefix = 'm%i_' %i
        model = getattr(models, basis_func['type'])(prefix=prefix)
        if basis_func['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']: # for now VoigtModel has gamma constrained to sigma
            model.set_param_hint('sigma', min=1e-6, max=x_range)
            model.set_param_hint('center', min=x_min, max=x_max)
            model.set_param_hint('height', min=1e-6, max=1.1*y_max)
            model.set_param_hint('amplitude', min=1e-6)
            # default guess is horrible!! do not use guess()
            default_params = {
                prefix+'center': x_min + x_range * random.random(),
                prefix+'height': y_max * random.random(),
                prefix+'sigma': x_range * random.random(),
            }
        else:
            raise NotImplemented('model %f not implemented yet' %basis_func["type"])
        if 'help' in basis_func:  # allow override of settings in parameter
            for param, options in basis_func['help'].items():
                model.set_param_hint(param, **options)

        model_params = model.make_params(default_params, **basis_func.get('params', {}))
        if params is None:
            params = model_params
        else:
            params.update(model_params)
        if composite_model is None:
            composite_model = model
        else:
            composite_model = composite_model + model
    return composite_model, params

def update_spec_from_peaks(spec, model_indicies, peak_widths=(10, 25), **kwargs):
    x = spec['x']
    y = spec['y']
    x_range = np.max(x) - np.min(x)
    peak_indicies, _ = signal.find_peaks(y, **kwargs)
    print peak_indicies
    np.random.shuffle(peak_indicies)
    for peak_indicie, model_indicie in zip(peak_indicies.tolist(), model_indicies):
        model = spec['model'][model_indicie]
        if model['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']:
            params = {
                'height': y[peak_indicie],
                'sigma': x_range / len(x) * np.min(peak_widths),
                'center': x[peak_indicie]
            }
            if 'params' in model:
                model.update(params)
            else:
                model['params'] = params
        else:
            raise NotImplemented('model  not implemented yet' )
    return peak_indicies


    
dr = Tools.ReadWriteData()
folder = "S://Science//I10//LYSMO//data//"
scans =186093
dr.read_file("%s%s.dat" %(folder,scans))
data = dr.get_data()

y = data["ifioft"]
x = data["ddth"]
spec = {
    'x': x,
    'y': y,
    'model': [
        { 'type': 'GaussianModel',
            'params': {'center': 51.3, 'height': 0.3, 'sigma': 0.01},
            'help': {'center': {'min': 51.0, 'max': 51.5}}},
        {'type': 'GaussianModel',
            'params': {'center': 51.35, 'height': 0.05, 'sigma': 0.02},
            'help': {'center': {'min': 51.3, 'max': 51.7}}},
        {'type': 'GaussianModel',
            'params': {'center': 51.9, 'height': 0.05, 'sigma': 0.02},
            'help': {'center': {'min': 51.8, 'max': 52.1}}},
    ]
}


spec = {
    'x': x,
    'y': y,
    'model': [
        { 'type': 'GaussianModel'}
         ,
        { 'type': 'GaussianModel'}
         ,
        { 'type': 'GaussianModel'}
         ,
    ]
}



peaks_found = update_spec_from_peaks(spec, [0, 1, 2], height = 0.008, width = 0.6 )
fig, ax = plt.subplots()
ax.scatter(spec['x'], spec['y'], s=4)
for i in peaks_found:
    ax.axvline(x=spec['x'][i], c='black', linestyle='dotted')
plt.semilogy()
plt.show()

model, params = generate_model(spec)
output = model.fit(spec['y'], params, x=spec['x'])
fig, gridspec = output.plot(data_kws={'markersize': 1})
plt.semilogy()
plt.show()

