   
import matplotlib.pyplot as plt
import numpy as np
import scipy 
from scipy.interpolate import interp1d



def parameter_optimization(x_data, y_data, training_fraction = 0.8, normalize_y = True, params = None, training_subset = None, measurement_standard_deviation = 0.0):
    """
    Draft for a parameter optimization scheme
    
    Takes as input the dataset (x_data, y_data) and the 
    fraction (a float in the interval 0.0 - 1.0) of datapoints
    to use as training data.
    """
    n = int(training_fraction*x_data.shape[0])
    
    # special first iteration
    if params is None:
        params = np.ones(x_data.shape[1])*-2.0 #*0.001
    #training_subset = np.random.choice(x_data.shape[0], n, replace = False)
    if training_subset is None:
        training_subset = np.ones(x_data.shape[0], dtype = bool)
        training_subset[n:] = False
    else:
        if len(training_subset)<len(y_data):
            # assume index element array
            ts = np.zeros(len(y_data), dtype = bool)
            ts[training_subset] = True
            training_subset = ts
            
            
    #print(training_subset)
    #print(x_data[training_subset])
        
    #print(training_subset)
    y_data_n = y_data*1
    if normalize_y:
        y_data_n*=y_data_n.max()**-1
        
    
    def residual(params, x_data = x_data, y_data=y_data_n, training_subset = training_subset):
        test_subset = np.ones(x_data.shape[0], dtype = bool)
        test_subset[training_subset] = False
        regressor = Regressor(x_data[training_subset] , y_data[training_subset], measurement_standard_deviation=measurement_standard_deviation) 
        regressor.params = 10**params
        #energy = np.sum((regressor.predict(x_data[test_subset]) - y_data[test_subset])**2)
        energy = np.sum((regressor.predict(x_data) - y_data)**2)
        return energy
    
    
    ret = minimize(residual, params)
    #print(ret)
    return 10**ret["x"]

def parameter_tuner_3d(all_x, all_y, n, measurement_standard_deviation = 0.0, params0 = np.array([1., 1.0, 1.0])):
    """
    Interactive (widget for Jupyter environments) parameter tuner 
    for the gpr module 

    Authors: Audun Skau Hansen and Ayla S. Coder 
    """


    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button



    training_x = all_x[n]
    training_y = all_y[n]
    
    regressor = Regressor(training_x, training_y, measurement_standard_deviation = measurement_standard_deviation, params = params0)


    # The parametrized function to be plotted
    def f(params1, params2, params3):
        regressor.params = 10**np.array([params1, params2, params3])
        return regressor.predict(all_x)



    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    plt.plot(np.arange(len(all_y))[n], all_y[n], "o", markersize = 10, label = "training data", color = (0,0,.5))
    plt.plot(all_y, "o", label = "true values", color = (.9,.2,.4))
    plt.legend()
    line, = plt.plot( f(1,1,1), ".-", lw=1, color = (.9,.9,.2))

    ax.set_xlabel('Time [s]')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.4, bottom=0.25)
    
    init_values = [1.0, 1.0, 1.0]
    if params0 is not None:
        init_values = [np.log10(i) for i in params0]

    # Make a vertically oriented slider to control the amplitude
    param1 = plt.axes([0.1, 0.3, 0.02, 0.5])
    param_slider1 = Slider(
        ax=param1,
        label="log(P1)",
        valmin=-10,
        valmax=10,
        valinit=init_values[0],
        orientation="vertical"
    )

    # Make a vertically oriented slider to control the amplitude
    param2 = plt.axes([0.2, 0.3, 0.02, 0.5])
    param_slider2 = Slider(
        ax=param2,
        label="log(P2)",
        valmin=-10,
        valmax=10,
        valinit=init_values[1],
        orientation="vertical"
    )

    # Make a vertically oriented slider to control the amplitude
    param3 = plt.axes([0.3, 0.3, 0.02, 0.5])
    param_slider3 = Slider(
        ax=param3,
        label="log(P3)",
        valmin=-10,
        valmax=10,
        valinit=init_values[2],
        orientation="vertical"
    )



    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata( f(param_slider1.val,param_slider2.val,param_slider3.val)) 
        fig.canvas.draw_idle()



    # register the update function with each slider
    #freq_slider.on_changed(update)
    param_slider1.on_changed(update)
    param_slider2.on_changed(update)
    param_slider3.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        param_slider1.reset()
        param_slider2.reset()
        param_slider3.reset()
    
    button.on_clicked(reset)
    
    
 
    plt.show()


def acquire_model_optimas(model,  bounds = None, resolution = 6, distance_threshold = .05, xi = .1):
    """
    Return possible 3D model minimas within bounds
    in a resolution^Nd grid, where Nd is the number of dimensions
    if bounds is none,  uses the model limits
    
    ## Keyword arguments
    
    model - the regression model
    bounds - the upper and lower limits/constraints for the search interval 
    resolution - the number of grid segments in each direction
    distance_threshold - minimal euclidean distance where two optimas are considered distinct
    xi - the exploration parameter for the optimizer
    
    ## Returns
    
    A numpy array containing elements of optimas, 
    [x,y,z, f(x,y,z), var(x,y,z)]
    
    """
    
    if bounds is None:
        bounds = np.array([np.min(model.training_data_X, axis =0), np.max(model.training_data_X, axis =0)])
    else:
        bounds = bounds.T
    
    # set up a initial guess list for the sweeps
    x = np.linspace(-1,1,resolution)
    xi = range(resolution)
    
    
    
    search_grid = np.array(np.meshgrid(*[x for i in range(bounds.shape[1])])).reshape(bounds.shape[1],-1).T
    search_grid_indx = np.array(np.meshgrid(*[xi for i in range(bounds.shape[1])])).reshape(bounds.shape[1],-1).T
    values = interp1d([0,1], np.array(bounds.T))(np.linspace(0,1,resolution))
    design_pattern = np.zeros(np.array(search_grid_indx.shape), dtype = float)
    
    

    for i in range(len(bounds.T)):
        design_pattern[:,i] = values[i][search_grid_indx[:, i]]     

        
    dim = bounds.shape[1]
    results = np.zeros((design_pattern.shape[0], dim + 3), dtype = float)
    
    # perform sweep and collect optimas
    for i in range(design_pattern.shape[0]):
        opt, optfun, suc = model.predict_sample_optimum( design_pattern[i],  xi = xi, bounds = bounds )
        val, var = model.predict(opt.reshape(-1,3), return_variance = True)
        results[i, :dim] = opt
        results[i, dim] = val
        results[i, dim+1] = var
        results[i, dim+2] = suc
       
    
    # Extract unique optimas 
    pts = results[:,:dim].T
    distances = np.sum((pts[:,:, None] - pts[:, None, :])**2, axis = 0)**.5
    selected = np.zeros(distances.shape[0], dtype = bool)
    
    optimas = []
    for i in range(distances.shape[0]):
        if not selected[i]:
            # add optima to stack
            optimas.append(results[i])
            
            # truncate all other optimas within distance threshold
            selected[distances[i]<distance_threshold] = True
    
    optimas = np.array(optimas)
    
    # sort in increasing order
    optimas = optimas[np.argsort(optimas[:, dim])]
    
    # remove unconverged
    optimas = optimas[optimas[:, dim+2]==1]
    
    # remove the ones above known minimum
    optimas = optimas[optimas[:, dim]<np.min(model.training_data_Y)]
    
    # return results
    return optimas[:, :dim+2]


def data_projection(regressor, axes = [0], resolution = 20, center = None):
    """
    Project high-dimensional regressor predictions onto smaller 
    spaces.
    
    Author: Audun Skau Hansen
    
    Arguments
    ===

    regressor  = a gpr regressor 
    axis      = indices of axis to sweep over
    resolution = resolution of sweeps along all axes
    center     = (optional) set center point of sweep (default is middle of the region)
    
    Examples
    ===
    
    x, y = data_projection(regressor, axes = [0]) -> 
    all axes except 0 are kept fixed at the mean values (or center values), 
    while 0 is allowed to vary inside the fitting region.
    plot(x[0], y) 
    
    x, y = data_projection(regressor, axes = [1,2]) -> 
    all axes except 1 and 2 are fixed to mean values (or center values)
    while 1 and 2 are allowed to map a surface in the fitting region.
    contourf(x[0], x[1], y)
    
    """
    

    # extract fitting regions (only internal datapoints will be predicted)
    mean  = np.mean(regressor.training_data_X, axis =0 )
    if center is not None:
        mean = np.array(center)

    #print(regressor.training_data_X)
    bound = np.max(regressor.training_data_X, axis = 0)-np.min(regressor.training_data_X, axis = 0)
    #print(mean, bound)
    lower_bound = mean - bound
    upper_bound = mean + bound


    # create a grid wherein the datapoints are interpolated
    grid = []
    for i in range(len(lower_bound)):
        grid.append(np.linspace(-bound[i], bound[i], resolution))

    #if center is None:
    #    center = np.zeros(len(mean), dtype = float)


    mgrid = list(mean) #[0 for i in range(len(center))]
    for i in range(len(axes)):
        mgrid[axes[i]] = grid[axes[i]]  + mean[axes[i]]
        


    prediction_grid = np.array(np.meshgrid(*mgrid)).reshape(len(mean), -1)

    # return prediction to user
    x = [] # list to contain the relevant grid-points    
    for i in range(len(axes)):
        x.append(mgrid[axes[i]])
    
    return x, regressor.predict(prediction_grid.T).reshape([resolution for i in range(len(axes))])

def one_dimensional_plots(x_data, proposed_new_x, reg, y_labels, x_labels):
    """
    Author: Ayla S. Coder
    """
    import matplotlib.pyplot as plt
    # Where y_labels and x_labels are arrays of strings 
    
    plt.figure(figsize=(8, 5)) # Sets the figure size
    
    rows = int(len(x_data[0])/3) # The amount of rows of plots in the figure
    
    dimensions = len(x_data[0]) # The amount of dimensions evaluated.
    
    # For loop to set up each subplot
    for i in range (dimensions):
        
        # This function is documented on Btjeneste website. If you're curious, run the command help(bt.analysis.data_projection)
        x,y = data_projection(reg, axes = [i], center = proposed_new_x, resolution = 100)
        
        # Sets up the i-th subplot
        ax = plt.subplot(rows, dimensions, i+1)
    
        ax.set_ylabel(y_labels[i], fontsize = 15)
        ax.set_xlabel(x_labels[i], fontsize = 15)
        ax.grid()
       # What is plotted in each plot:
        ax.plot(x[0], y)
        
    plt.show()