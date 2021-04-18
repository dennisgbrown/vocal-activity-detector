# -*- coding: utf-8 -*-
"""
### Authors: Dennis Brown, Shannon McDade, Jacob Parmer
###
### Created: April 15, 2021
"""

import csv

def compile_results(input_folder, target_noise_loudnesses, output_fileroot):
    outfile1 = open(output_fileroot + '_acc.csv', "w")
    outfile2 = open(output_fileroot + '_psas.csv', "w")
    outfile3 = open(output_fileroot + '_psan.csv', "w")
    outfile4 = open(output_fileroot + '_pnas.csv', "w")
    outfile5 = open(output_fileroot + '_pnan.csv', "w")

    datalist = ['test-clean']
    for loudness in target_noise_loudnesses:
        datalist.append('test-clean-db' + str(loudness))

    outfile1.write('dataset\\model')
    outfile2.write('dataset\\model')
    outfile3.write('dataset\\model')
    outfile4.write('dataset\\model')
    outfile5.write('dataset\\model')
    for model in datalist:
        outfile1.write(',' + model + '_acc')
        outfile2.write(',' + model + '_psas')
        outfile3.write(',' + model + '_psan')
        outfile4.write(',' + model + '_pnas')
        outfile5.write(',' + model + '_pnan')
    outfile1.write('\n')
    outfile2.write('\n')
    outfile3.write('\n')
    outfile4.write('\n')
    outfile5.write('\n')

    for dataset in datalist:
        outfile1.write(dataset)
        outfile2.write(dataset)
        outfile3.write(dataset)
        outfile4.write(dataset)
        outfile5.write(dataset)
        for model in datalist:
            input_filename = input_folder + 'results_model_' + model + '_data_' + dataset + '_cm.csv'
            # print('Reading', input_filename)
            infile = open(input_filename)
            reader = csv.DictReader(infile)
            signal_count = 0.0
            total_acc = 0.0
            event_count = 0.0
            total_psas = 0.0
            total_psan = 0.0
            total_pnas = 0.0
            total_pnan = 0.0
            for row in reader:
                # print(float(row[' pc_accuracy']))
                signal_count += 1.0
                event_count += float(row[' checks'])
                total_acc += float(row[' pc_accuracy'])
                total_psas += float(row[' psas'])
                total_psan += float(row[' psan'])
                total_pnas += float(row[' pnas'])
                total_pnan += float(row[' pnan'])
            outfile1.write(', %.2f' % (total_acc / signal_count))
            outfile2.write(', %.2f' % (total_psas / event_count))
            outfile3.write(', %.2f' % (total_psan / event_count))
            outfile4.write(', %.2f' % (total_pnas / event_count))
            outfile5.write(', %.2f' % (total_pnan / event_count))
            infile.close()
        outfile1.write('\n')
        outfile2.write('\n')
        outfile3.write('\n')
        outfile4.write('\n')
        outfile5.write('\n')

    outfile1.close()
    outfile2.close()
    outfile3.close()
    outfile4.close()
    outfile5.close()


def main():
    input_folder = '../results/'
    target_noise_loudnesses = [-160, -80, -40, -20, -10, -5, 0, 5]
    output_fileroot = '../results/compiled_results'
    compile_results(input_folder, target_noise_loudnesses, output_fileroot)
    print('Done -- see files starting with', output_fileroot)


if __name__ == '__main__':
    main()
