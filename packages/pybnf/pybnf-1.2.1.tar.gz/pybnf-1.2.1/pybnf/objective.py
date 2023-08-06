"""Classes defining various objective functions used for evaluating points in parameter space"""

from scipy.special import loggamma

from .printing import PybnfError, print1

import numpy as np


class ObjectiveCalculator:
    """
    Wrapper for all of the objects needed for the workers to calculate the objective function value.
    Contains the objective function, exp_data_dict, and constraint tuple
    """

    def __init__(self, objective, exp_data_dict, constraints):
        self.objective = objective
        self.exp_data_dict = exp_data_dict
        self.constraints = constraints

    def evaluate_objective(self, sim_data_dict, pset, show_warnings=True):
        """
        Evaluate the objective using the input simulation data and the info contained in this object
        :param sim_data_dict: Dictionary of the form {modelname: {suffix1: Data1}} containing the simulated data objects
        :param show_warnings: If True, print warnings about unused data
        :type show_warnings: bool
        :return:
        """
        
        
        return self.objective.evaluate_multiple(sim_data_dict, self.exp_data_dict, pset, self.constraints, show_warnings)



class ObjectiveFunction(object):
    """
    Abstract class representing an objective function
    Subclasses customize how the objective value is calculated from the quantitative exp data
    The base class includes all the support we need for constraints.
    """

    def evaluate_multiple(self, sim_data_dict, exp_data_dict, pset, constraints=(), show_warnings=True):
        """
        Compute the value of the objective function on several data sets, and return the total.
        Optionally may pass an iterable of ConstraintSets whose penalties will be added to the total
        :param sim_data_dict: Dictionary of the form {modelname: {suffix1: Data1}} containing the simulated data objects
        :type sim_data_dict: dict
        :param exp_data_dict: Dictionary of the form {modelname: {suffix1: Data1}} containing experimental Data objects
        :type exp_data_dict: dict
        :param constraints: Iterable of ConstraintSet objects containing the constraints that we should evaluate using
        the simulated data
        :type constraints: Iterable of ConstraintSet
        :param show_warnings: If True, print warnings about unused data
        :type show_warnings: bool
        :return:
        """
        try:
            self.pset = pset
            for p in self.pset:
                if p.name == 'r__FREE':
                    self.r = p.value
                elif p.name == 'sigma__FREE':
                    self.sigma = p.value
                else:
                    pass    
        except AttributeError:
            constraints = pset
            pass

        with np.errstate(all='ignore'):  # Suppress numpy warnings printed to terminal
            total = 0.
            
            # Dictionary mapping suffix strings to experimental Data objects
            # exp_data_dict = self.conf.exp_data

            if not sim_data_dict:
                return np.inf
            else:
                for model in sim_data_dict:
                    for suffix in sim_data_dict[model]:
                        # Suffixes might exist in sim_data_dict that do not have experimental data.
                        # Need to check for that here.
                        if suffix in exp_data_dict[model]:
                            val = self.evaluate(sim_data_dict[model][suffix], exp_data_dict[model][suffix],
                                                show_warnings=show_warnings)
                            if val is None:
                                return None
                            total += val
                for cset in constraints:
                    total += cset.total_penalty(sim_data_dict)

                return total

    def evaluate(self, sim_data, exp_data, show_warnings=True):
        """
        :param sim_data: A Data object containing simulated data
        :type sim_data: Data
        :param exp_data: A Data object containing experimental data
        :type exp_data: Data
        :return: float, value of the objective function, with a lower value indicating a better fit.
        :param show_warnings: If True, print warnings about unused data
        :type show_warnings: bool
        """
        raise NotImplementedError("Subclasses must override evaluate()")


class SummationObjective(ObjectiveFunction):
    """
    Represents a type of objective function in which we perform some kind of summation over all available experimental
    data points individually.
    """

    def __init__(self, ind_var_rounding=0):
        # Keep track of which warnings we've printed, so we only print each one once.
        self.warned = set()
        self.rounding = ind_var_rounding

    def evaluate(self, sim_data, exp_data, show_warnings=True):
        """
        :param sim_data: A Data object containing simulated data
        :type sim_data: Data
        :param exp_data: A Data object containing experimental data
        :type exp_data: Data
        :param show_warnings: If True, print warnings about unused data
        :type show_warnings: bool
        :return: float, value of the objective function, with a lower value indicating a better fit.
        """
        
        indvar = min(exp_data.cols, key=exp_data.cols.get)  # Get the name of column 0, the independent variable

        compare_cols = set(exp_data.cols).intersection(set(sim_data.cols))  # Set of columns to compare
        # Warn if experiment columns are going unused
        if show_warnings:
            self._check_columns(exp_data.cols, compare_cols)
        try:
            compare_cols.remove(indvar)
        except KeyError:
            raise PybnfError('The independent variable "%s" in your exp file was not found in the simulation data.'
                             % indvar)

        func_value = 0.0
        # Iterate through rows of experimental data
        for rownum in range(exp_data.data.shape[0]):

            if self.rounding == 0:
                # Figure out the corresponding row number in the simulation data
                # Find the row number of sim_data column 0 that is almost equal to exp_data[rownum, 0]
                sim_row = np.argmax(np.isclose(sim_data[indvar], exp_data.data[rownum, 0], atol=0.))
                # If no such column existed, sim_row will come out as 0; need to check for this and skip if it happened
                if sim_row == 0 and not np.isclose(sim_data[indvar][0], exp_data.data[rownum, 0], atol=0.):
                    raise PybnfError('Experimental data includes %s=%s, but that %s is not in the simulation output. '
                                     % (indvar, exp_data.data[rownum, 0], indvar))
            elif self.rounding == 1:
                # Take the closest row to the exp data
                sim_row = np.argmin(abs(sim_data[indvar] - exp_data.data[rownum, 0]))
                # Warn if there was really nothing close
                diff = abs(sim_data[indvar][sim_row] - exp_data.data[rownum, 0])
                if diff > 1. and diff / exp_data.data[rownum, 0] > 0.1:
                    warnstr = indvar + str(exp_data.data[rownum, 0])  # An identifier so we only print the warning once
                    if show_warnings and warnstr not in self.warned:
                        print1("Warning: For exp point %s=%s, used sim data at %s=%s" %
                               (indvar, exp_data.data[rownum, 0], indvar, sim_data[indvar][sim_row]))
                        self.warned.add(warnstr)
            else:
                raise PybnfError('Possible values for ind_var_rounding are 0 or 1.')

            for col_name in compare_cols:
                if np.isnan(exp_data.data[rownum, exp_data.cols[col_name]]):
                    continue

                cur_sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]

                if np.isnan(cur_sim_val) or np.isinf(cur_sim_val):
                    return None
                func_value += self.eval_point(sim_data, exp_data, sim_row, rownum, col_name) \
                    * exp_data.weights[rownum, exp_data.cols[col_name]]

        return func_value

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        """
        Calculate the objective function for a single point in the data
        This evaluation is what differentiates the different objective functions.
        :param sim_data: The simulation Data object
        :param exp_data: The experimental Data object
        :param sim_row: The row number to look at in sim_data
        :param exp_row: The row number to look at in exp_data
        :param col_name: The column name to look at  (same for the sim_data and the exp_data)
        :return:
        """
        raise NotImplementedError('Subclasses of SummationObjective must override eval_point')

    def _check_columns(self, exp_cols, compare_cols):
        """
        Check that all exp_cols are being read in compare_cols; give a warning if not.
        :param exp_cols: Iterable of all experimental data column names
        :param compare_cols: Iterable of the names being used
        :return: None
        """
        missed = set(exp_cols).difference(set(compare_cols))
        if len(missed) > 0:
            raise PybnfError('The following experimental data columns were not found in the simulation output: '
                             + str(missed))


class ColumnSummationObjective(ObjectiveFunction):
    """
    Represents a type of objective function in which we perform some kind of summation for one column at a time.
    The assumption is that the independent variable is the same for each row.
    """

    def __init__(self, ind_var_rounding=0):
        # Keep track of which warnings we've printed, so we only print each one once.
        self.warned = set()
        self.rounding = ind_var_rounding

    def evaluate(self, sim_data, exp_data, show_warnings=True):
        """
        :param sim_data: A Data object containing simulated data
        :type sim_data: Data
        :param exp_data: A Data object containing experimental data
        :type exp_data: Data
        :param show_warnings: If True, print warnings about unused data
        :type show_warnings: bool
        :return: float, value of the objective function, with a lower value indicating a better fit.
        """

        indvar = min(exp_data.cols, key=exp_data.cols.get)  # Get the name of column 0, the independent variable

        compare_cols = set(exp_data.cols).intersection(set(sim_data.cols))  # Set of columns to compare
        # Warn if experiment columns are going unused
        if show_warnings:
            self._check_columns(exp_data.cols, compare_cols)
        try:
            compare_cols.remove(indvar)
        except KeyError:
            raise PybnfError('The independent variable "%s" in your exp file was not found in the simulation data.'
                             % indvar)

        func_value = 0.0
        # Iterate through rows of experimental data
        for col_name in compare_cols:
            func_value += self.eval_column(sim_data, exp_data, col_name)

        return func_value

    def eval_column(self, sim_data, exp_data, col_name):
        """
        Calculate the objective function for a single column in the data
        This evaluation is what differentiates the different column based objective functions.
        :param sim_data: The simulation Data object
        :param exp_data: The experimental Data object
        :param col_name: The column name to look at  (same for the sim_data and the exp_data)
        :return:
        """
        raise NotImplementedError('Subclasses of SummationObjective must override eval_point')

    def _check_columns(self, exp_cols, compare_cols):
        """
        Check that all exp_cols are being read in compare_cols; give a warning if not.
        :param exp_cols: Iterable of all experimental data column names
        :param compare_cols: Iterable of the names being used
        :return: None
        """
        missed = set(exp_cols).difference(set(compare_cols))
        if len(missed) > 0:
            raise PybnfError('The following experimental data columns were not found in the simulation output: '
                             + str(missed))


class ChiSquareObjective(SummationObjective):

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        try:
            # Todo: Check for this and throw the error before all the workers get created.
            sd_col = exp_data.cols[col_name + '_SD']
        except KeyError:
            raise PybnfError('Column %s_SD not found' % col_name,
                 "Column %s_SD was not found in the experimental data. When using the chi_sq objective function, your "
                 "data file must include a _SD column corresponding to each experimental variable, giving the standard "
                 "deviations of that variable. " % col_name)
        exp_sigma = exp_data.data[exp_row, sd_col]
        return 1. / (2. * exp_sigma ** 2.) * (sim_val - exp_val) ** 2.

    def _check_columns(self, exp_cols, compare_cols):
        """
        Check that all exp_cols are being read in compare_cols; give a warning if not.
        :param exp_cols: Iterable of all experimental data column names
        :param compare_cols: Iterable of the names being used
        :return: None
        """
        missed = set(exp_cols).difference(set(compare_cols).union(set(['%s_SD' % s for s in compare_cols])))
        if len(missed) > 0:
            raise PybnfError('The following experimental data columns were not found in the simulation output: '
                             + str(missed))

class ChiSquareObjective_Dynamic(SummationObjective):

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        
        exp_sigma = self.sigma
        val = 1. / (2. * exp_sigma ** 2.) * (sim_val - exp_val) ** 2. + np.log(exp_sigma)
        return val

class SumOfSquaresObjective(SummationObjective):

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        return (sim_val - exp_val) ** 2.


class SumOfDiffsObjective(SummationObjective):

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        return abs(sim_val - exp_val)


class NormSumOfSquaresObjective(SummationObjective):
    """
    Sum of squares where each point is normalized by the y value at that point, ((y-y')/y)^2
    """

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        return ((sim_val - exp_val) / exp_val) ** 2.


class AveNormSumOfSquaresObjective(SummationObjective):
    """
    Sum of squares where each point is normalized by the average value of that variable,
    ((y-y')/ybar)^2
    """

    def evaluate(self, sim_data, exp_data, show_warnings=True):
        # Precalculate the average of each exp column to use for all points in this call.
        self.aves = {name: np.average(exp_data[name]) for name in exp_data.cols}
        return super().evaluate(sim_data, exp_data, show_warnings)

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        return ((sim_val - exp_val) / self.aves[col_name]) ** 2.


class NegBinLikelihood_Dynamic(SummationObjective):
    """
    Negative binomial likelihood with r as a free param
    """

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val_1 = sim_data.data[sim_row -1, sim_data.cols[col_name]]
        sim_val_2 = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]   
        if '_Cum' in col_name:
            sim_val = sim_val_2 - sim_val_1
        else:
            sim_val = sim_data.data[sim_row, sim_data.cols[col_name]] 
        if sim_row == 0:
            sim_val = sim_data.data[sim_row, sim_data.cols[col_name]] 
        if exp_val >= 0:
            prob = np.clip(self.r / (self.r + sim_val), 1e-10, 1 - 1e-10)
            # log(1e-10+stats.nbinom.pmf(incidents[i], n=r, p=prob))
            assert isinstance(self.r, float)
            val = loggamma(exp_val + self.r) - loggamma(exp_val + 1) - loggamma(self.r) + self.r * np.log(prob) + \
                   exp_val * np.log(1 - prob)
        
            return abs(val)
        else:
            return 0
            
class NegBinLikelihood(SummationObjective):
    """
    Negative binomial likelihood
    """

    def __init__(self, r, ind_var_rounding):
        super().__init__(ind_var_rounding)
        self.r_static = r

    def eval_point(self, sim_data, exp_data, sim_row, exp_row, col_name):
        sim_val = sim_data.data[sim_row, sim_data.cols[col_name]]
        exp_val = exp_data.data[exp_row, exp_data.cols[col_name]]
        if exp_val >= 0:
            prob = np.clip(self.r_static / (self.r_static + sim_val), 1e-10, 1 - 1e-10)
            # log(1e-10+stats.nbinom.pmf(incidents[i], n=r, p=prob))
            assert isinstance(self.r_static, float)
            val =  loggamma(exp_val + self.r_static) - loggamma(exp_val + 1) - loggamma(self.r_static) + self.r_static * np.log(prob) + \
                   exp_val * np.log(1 - prob)
            return abs(val)       
        else:
            return 0

class KLLikelihood(ColumnSummationObjective):
    """
    The Kullback-Leibler likelihood.
    It should be more efficient in parameter fitting as numerical experiments suggest
    """

    def eval_column(self, sim_data, exp_data, col_name):
        sim_column = sim_data[:, sim_data.cols[col_name]]
        exp_column = exp_data[:, exp_data.cols[col_name]]
        return sum(exp_column * np.log(sim_column / sum(sim_column)))


class ConstraintCounter(ObjectiveFunction):
    """
    An objective function that just counts the numbered of failed constraints
    Used only in model checking
    """

    def evaluate_multiple(self, sim_data_dict, exp_data_dict, constraints=(), show_warnings=True):
        """
        Count the number constraints that are not satisfied by the simulation data.
        Experimental (quantitative) data is ignored
        """
        total = 0.
        for cset in constraints:
            total += cset.number_failed(sim_data_dict)
        return total

    def evaluate(self, sim_data, exp_data, show_warnings=True):
        raise NotImplementedError("ConstraintCounter does not implement evaluate()")
