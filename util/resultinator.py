# -*- coding: utf-8 -*-
"""
### Authors: Dennis Brown, Shannon McDade, Jacob Parmer
###
### Created: April 15, 2021
"""

import csv

def compile_results(input_folder, target_noise_loudnesses, output_filename):
    outfile = open(output_filename, "w")

    datalist = ['test-clean']
    for loudness in target_noise_loudnesses:
        datalist.append('test-clean-db' + str(loudness))

    outfile.write('dataset\\model')
    for model in datalist:
        outfile.write(',' + model)
    outfile.write('\n')

    for dataset in datalist:
        outfile.write(dataset)
        for model in datalist:
            input_filename = 'results_model_' + model + '_data_' + dataset + '.csv'
            # print('Reading', input_filename)
            infile = open(input_filename)
            reader = csv.DictReader(infile)
            count = 0.0
            total = 0.0
            for row in reader:
                # print(float(row[' pc_accuracy']))
                count += 1.0
                total += float(row[' pc_accuracy'])
            outfile.write(', %.2f' % (total / count))
            infile.close()
        outfile.write('\n')

    outfile.close()


def main():
    input_folder = '.'
    target_noise_loudnesses = [-160, -80, -40, -20, -10, -5, 0, 5]
    output_filename = 'compiled_results.csv'
    compile_results(input_folder, target_noise_loudnesses, output_filename)
    print('Done -- see', output_filename)


if __name__ == '__main__':
    main()
