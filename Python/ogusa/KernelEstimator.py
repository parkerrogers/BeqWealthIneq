import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from scipy.stats import norm
from scipy.stats import kde
import seaborn

def MVKDE(S, J ,proportion_matrix = None, filename = None, plot = False,  bandwidth = .25):
    '''
    Generates a Multivariate Kernel Density Estimator and returns a matrix
    representing a probability distribution according to given age categories,
    and ability type categories.

    Inputs:
        S                     = scalar, the number of age groups in the model.

        J                     = scalar, the number of ability type groups in the model.

        proportion_matrix     = [S, J], array containing the proportion matrix created
                                by SCFExtract.py. This argument would be used if you are
                                passing in the proportion_matrix directly

        filename              = string, the file name of the .txt document that contains 
                                the original proportion matrix created by SCFExtract.py.
                                Use this argument if you have saved the proportion matrix 
                                in a .txt file

        plot                  = boolean, whether or not you want a plot of the probability
                                distribution generated by your given age and ability type 
                                groups.

        bandwidth             = scalar, used in the smoothing of the kernel. Higher bandwidth 
                                creates a smoother kernel.
       
    Functions called: 
        kde.gaussian_kde      = scipy function that generates a Kernel 
                                Density Estimator from given data

    Objects in function:
        proportion_matrix     = [78, 7], array containing the proportion (0 < x < 1) of 
                                the total bequests that each age-income category receives. 
                                Derived in SCFExtract.py

        age_probs             = [78,], array containing the frequency, or how many times, 
                                that random drawn numbers fell into the 78 different age bins

        income_probs          = [7,], array containing the frequency, or how many times, 
                                that random drawn numbers fell into the 7 different ability 
                                type bins

        age_frequency         = [70000,], array containing repeated age values for each 
                                age number at the frequency given by the age_probs vector 

        xmesh                 = complex number, the number of age values that will be 
                                evaluated in the Kernel Density Estimator.

        freq_mat              = [70000, 2], array containing age_frequency and 
                                income_frequency stacked

        density               = object, class given by scipy.stats.gaussian_kde. 
                                The Multivariate Kernel Density Estimator for the given data set.

        age_min, age_max      = scalars, the minimum and maximum age values and minimum 
        income_min, income_max  and maximum income values 
        

        agei                  = [S, J], array containing the age values to be evaluated in 
                                the Kernel Estimator (ranging from 18-90)

        incomei               = [S, J], array containing the income values to be evaluated 
                                in the Kernel Estimator (ranging from 1-7)

        coords                = [2, S*J], array containing the raveled values of agei 
                                and incomei stacked

        estimator             = [S, J], array containing the new proportion values for 
                                s age groups and e ability type groups that are evaluated 
                                using the Multivariate Kernel Density Estimator

        estimator_scaled       = [S, J], array containing the new proportion values for 
                                s age groups and e ability type groups that are evaluated using 
                                the Multivariate Kernel Density Estimator, but scaled so that 
                                the sum of the array is equal to one.

    Returns: estimator_scaled
    '''
    if proportion_matrix is None:
        proportion_matrix = np.loadtxt(filename, delimiter = ',')
    proportion_matrix_income = np.sum(proportion_matrix, axis = 0)
    proportion_matrix_age = np.sum(proportion_matrix, axis = 1)
    age_probs = np.random.multinomial(70000,proportion_matrix_age)
    income_probs = np.random.multinomial(70000, proportion_matrix_income)
    age_frequency = np.array([])
    income_frequency = np.array([])
    age_mesh = complex(str(S)+'j')
    income_mesh = complex(str(J)+'j')

    j = 18
    '''creating a distribution of age values'''
    for i in age_probs:
        listit = np.ones(i)
        listit *= j
        age_frequency = np.append(age_frequency, listit)
        j+=1

    k = 1
    '''creating a distribution of ability type values'''
    for i in income_probs:
        listit2 = np.ones(i)
        listit2 *= k
        income_frequency = np.append(income_frequency, listit2)
        k+=1

    freq_mat = np.vstack((age_frequency, income_frequency)).T
    density = kde.gaussian_kde(freq_mat.T, bw_method=bandwidth)
    age_min, income_min = freq_mat.min(axis=0)
    age_max, income_max = freq_mat.max(axis=0)
    agei, incomei = np.mgrid[age_min:age_max:age_mesh, income_min:income_max:income_mesh]
    coords = np.vstack([item.ravel() for item in [agei, incomei]])
    estimator = density(coords).reshape(agei.shape)
    estimator_scaled = estimator/float(np.sum(estimator))
    if plot == True:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(agei,incomei, estimator_scaled, rstride=5)
        ax.set_xlabel("Age")
        ax.set_ylabel("Ability Types")
        ax.set_zlabel("Received proportion of total bequests")
        plt.show()
    return estimator_scaled
