# -*- coding: utf-8 -*-
"""
### compare.py: Perform F- and t-test on two data sets; plot comparative histogram of data.
###
### Authors: Dennis Brown, Shannon McDade, Jacob Parmer
###
### Created: April 15, 2021
"""

import matplotlib.pyplot as plt
import numpy
import scipy.stats as stats
import csv


def read_file(input_filename, parm):
    """
    Read the given parameter from the given file and return array of data
    """
    # print('Reading', input_filename)
    infile = open(input_filename)
    reader = csv.DictReader(infile)
    vals = []
    for row in reader:
        vals.append(float(row[' ' + parm]))

    return numpy.array(vals)


def do_it(model1, dataset1, model2, dataset2, parm):

    # Read the data
    title1 = 'model-' + model1 + '-dataset-' + dataset1
    title2 = 'model-' + model2 + '-dataset-' + dataset2

    combo_fileroot = title1 + '-vs-' + title2

    filename1 = 'results_model_test-clean'
    if (model1 != 'orig'): filename1 += '-db' + model1
    filename1 += '_data_test-clean'
    if (dataset1 != 'orig'): filename1 += '-db' + dataset1
    filename1 += '_cm.csv'

    filename2 = 'results_model_test-clean'
    if (model2 != 'orig'): filename2 += '-db' + model2
    filename2 += '_data_test-clean'
    if (dataset2 != 'orig'): filename2 += '-db' + dataset2
    filename2 += '_cm.csv'

    # No point comparing a results file with itself
    if (filename1 == filename2): return

    vals1 = read_file('../results/' + filename1, parm)
    vals2 = read_file('../results/' + filename2, parm)

    # runs = numpy.linspace(1, len(vals1), num = len(vals1), endpoint=True)


    # Calculate F-Test Two-Sample for Variances
    mean1 = numpy.mean(vals1)
    mean2 = numpy.mean(vals2)
    var1 = numpy.var(vals1, ddof=1)
    var2 = numpy.var(vals2, ddof=1)
    obs = len(vals1)
    ft_df = obs - 1
    f = var1/var2
    ft_p = stats.f.cdf(f, ft_df, ft_df)
    alpha = 0.05
    fcrit = stats.f.ppf(alpha, ft_df, ft_df)

    have_equal_variances = False

    # print('-----------------------------')
    # print('\\begin{figure}[H]')
    # print('\\caption{' + title1 + ' vs. ' + title2 + ' -- Best values over ' + str(obs) + ' runs}')
    # print('\\centering')
    # print('\\includegraphics[width=8cm]{' + combo_fileroot + parm + '.png}')
    # print('\\label{fig:' + combo_fileroot + parm + '}')
    # print('\\end{figure}')
    # print()
    # print('\\begin{table}[H]')
    # print('\\centering')
    # print('\\caption{F-Test for ' + title1 + ' vs. ' + title2 + ' with $\\alpha = ' + str(alpha) + '$}')
    # print('\\label{tab:ftest-' + combo_fileroot + parm + '}')
    # print('\\begin{tabular}{lll}')
    # print('\\hline')
    # print(' & ' + title1 + ' & ' + title2 + ' \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Mean}     & \\multicolumn{1}{l|}{' + str(mean1) + '} & \\multicolumn{1}{l|}{' + str(mean2) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Variance}     & \\multicolumn{1}{l|}{' + str(var1) + '} & \\multicolumn{1}{l|}{' + str(var2) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Observations}     & \\multicolumn{1}{l|}{' + str(obs) + '} & \\multicolumn{1}{l|}{' + str(obs) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{df}     & \\multicolumn{1}{l|}{' + str(ft_df) + '} & \\multicolumn{1}{l|}{' + str(ft_df) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{F}     & \\multicolumn{1}{l|}{' + str(f) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{P(F$\leq$f) one-tail}     & \\multicolumn{1}{l|}{' + str(ft_p) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{F Critical one-tail}     & \\multicolumn{1}{l|}{' + str(fcrit) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\end{tabular}')
    # print('\\end{table}')
    # print()

    # if (abs(mean1) > abs(mean2)) and (f < fcrit):
    #     print('\\noindent abs(mean 1) $>$ abs(mean 2) and F $<$ F Critical implies equal variances.')
    #     have_equal_variances = True
    # if (abs(mean1) > abs(mean2)) and (f > fcrit):
    #     print('\\noindent abs(mean 1) $>$ abs(mean 2) and F $>$ F Critical implies unequal variances.')
    #     have_equal_variances = False
    # if (abs(mean1) < abs(mean2)) and (f > fcrit):
    #     print('\\noindent abs(mean 1) $<$ abs(mean 2) and F $>$ F Critical implies equal variances.')
    #     have_equal_variances = True
    # if (abs(mean1) < abs(mean2)) and (f < fcrit):
    #     print('\\noindent abs(mean 1) $<$ abs(mean 2) and F $<$ F Critical implies unequal variances.')
    #     have_equal_variances = False
    # print()


    # Calculate T-Test Two-Sample for equal or unequal variances
    tt_df = (obs * 2) - 2
    tcrit_two_tail = stats.t.ppf(1.0 - (alpha/2), tt_df)
    (tstat, tt_p_two_tail) = stats.ttest_ind(vals1, vals2, equal_var=have_equal_variances)

    # print('\\begin{table}[H]')
    # print('\\centering')
    # print('\\caption{t-Test for ' + title1 + ' vs. ' + title2 + ' with ')
    # if (have_equal_variances):
    #     print('Equal Variances}')
    # else:
    #     print('Unequal Variances}')
    # print('\\label{tab:ttest-' + combo_fileroot + parm + '}')
    # print('\\begin{tabular}{lll}')
    # print('\\hline')
    # print(' & ' + title1 + ' & ' + title2 + ' \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Mean}     & \\multicolumn{1}{l|}{' + str(mean1) + '} & \\multicolumn{1}{l|}{' + str(mean2) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Variance}     & \\multicolumn{1}{l|}{' + str(var1) + '} & \\multicolumn{1}{l|}{' + str(var2) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{Observations}     & \\multicolumn{1}{l|}{' + str(obs) + '} & \\multicolumn{1}{l|}{' + str(obs) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{df}     & \\multicolumn{1}{l|}{' + str(tt_df) + '} & \\multicolumn{1}{l|}{' + str(ft_df) + '} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{t Stat}     & \\multicolumn{1}{l|}{' + str(tstat) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{P(T$\leq$t) two-tail}     & \\multicolumn{1}{l|}{' + str(tt_p_two_tail) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\multicolumn{1}{|l|}{t Critical two-tail}     & \\multicolumn{1}{l|}{' + str(tcrit_two_tail) + '} & \\multicolumn{1}{l|}{} \\\\ \\hline')
    # print('\\end{tabular}')
    # print('\\end{table}')
    # print()

    # if (abs(tstat) > abs(tcrit_two_tail)):
    #     print('\\noindent abs(t Stat) $>$ abs(t Critical two-tail) so we reject the null hypothesis -- the two samples are statistically different.')
    #     print('The average improvement of ' + title1 + ' over ' + title2 + ' is ' + str(mean1 - mean2) + '.')
    # else:
    #     print('\\noindent abs(t Stat) $<$ abs(t Critical two-tail) so we accept the null hypothesis -- the two samples are NOT statistically different.')
    # print('-----------------------------')


    print(parm + ': ' + title1 + ' vs ' + title2 + ': ', end = '')
    if (abs(tstat) > abs(tcrit_two_tail)):
        print(str(mean1 - mean2))
    else:
        print('NOT different')


    # Plot the data
    # bins = numpy.arange(0, 100)
    # plt.hist([vals1, vals2], bins, label = [title1, title2])

    # plt.title(parm + ': ' + title1 + ' and ' + title2)
    # plt.xlabel(parm)
    # plt.ylabel('Number of signals')
    # plt.legend(loc='upper left')
    # plt.grid(True)

    # plt.savefig('../plots/' + combo_fileroot + '.png', dpi = 600)

    # plt.clf()


def main():
    datasets = ['orig', '-160', '-80', '-40', '-20', '-10', '-5', '0']
    # parms = ['pc_accuracy', 'psas', 'psan', 'pnas', 'pnan']
    # datasets = ['orig', '-160', '-80', '-40']
    parms = ['pc_accuracy']

    for parm in parms:
        for model1 in datasets:
            for dataset1 in datasets:
                for model2 in datasets:
                    for dataset2 in datasets:
                        do_it(model1, dataset1, model2, dataset2, parm)


if __name__ == '__main__':
    main()