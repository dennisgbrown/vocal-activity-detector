# -*- coding: utf-8 -*-
"""
### Compile and plot results from VAD runs.
###
### Authors: Dennis Brown, Shannon McDade, Jacob Parmer
###
### Created: April 15, 2021
"""

import csv
import plotly.graph_objects as go
import numpy as np

def compile_results(input_folder, target_noise_loudnesses, output_fileroot):
    outfile1 = open(output_fileroot + '_acc.csv', "w")
    outfile2 = open(output_fileroot + '_psas.csv', "w")
    outfile3 = open(output_fileroot + '_psan.csv', "w")
    outfile4 = open(output_fileroot + '_pnas.csv', "w")
    outfile5 = open(output_fileroot + '_pnan.csv', "w")

    datalist = ['test-clean']
    for loudness in target_noise_loudnesses:
        datalist.append('test-clean-db' + str(loudness))

    num_data_sets = len(datalist)
    acc = np.zeros((num_data_sets * num_data_sets, 3))
    psas = np.zeros((num_data_sets * num_data_sets, 3))
    psan = np.zeros((num_data_sets * num_data_sets, 3))
    pnas = np.zeros((num_data_sets * num_data_sets, 3))
    pnan = np.zeros((num_data_sets * num_data_sets, 3))

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

    dataset_id = 0
    for dataset in datalist:
        outfile1.write(dataset)
        outfile2.write(dataset)
        outfile3.write(dataset)
        outfile4.write(dataset)
        outfile5.write(dataset)
        model_id = 0
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
            acc[dataset_id * num_data_sets + model_id][0] = dataset_id
            acc[dataset_id * num_data_sets + model_id][1] = model_id
            acc[dataset_id * num_data_sets + model_id][2] = total_acc / signal_count
            psas[dataset_id * num_data_sets + model_id][0] = dataset_id
            psas[dataset_id * num_data_sets + model_id][1] = model_id
            psas[dataset_id * num_data_sets + model_id][2] = total_psas / event_count * 100
            psan[dataset_id * num_data_sets + model_id][0] = dataset_id
            psan[dataset_id * num_data_sets + model_id][1] = model_id
            psan[dataset_id * num_data_sets + model_id][2] = total_psan / event_count * 100
            pnas[dataset_id * num_data_sets + model_id][0] = dataset_id
            pnas[dataset_id * num_data_sets + model_id][1] = model_id
            pnas[dataset_id * num_data_sets + model_id][2] = total_pnas / event_count * 100
            pnan[dataset_id * num_data_sets + model_id][0] = dataset_id
            pnan[dataset_id * num_data_sets + model_id][1] = model_id
            pnan[dataset_id * num_data_sets + model_id][2] = total_pnan / event_count * 100
            infile.close()
            model_id += 1
        outfile1.write('\n')
        outfile2.write('\n')
        outfile3.write('\n')
        outfile4.write('\n')
        outfile5.write('\n')
        dataset_id += 1
    outfile1.close()
    outfile2.close()
    outfile3.close()
    outfile4.close()
    outfile5.close()

    return acc, psas, psan, pnas, pnan

def main():

    # Get/write data
    input_folder = '../results/'
    target_noise_loudnesses = [-160, -80, -40, -20, -10, -5, 0]
    output_fileroot = '../results/compiled_results'
    acc, psas, psan, pnas, pnan = compile_results(input_folder, target_noise_loudnesses, output_fileroot)
    print('Done -- see files starting with', output_fileroot)

    # Plots
    labels = ['orig']
    for noise in target_noise_loudnesses: labels.append(str(noise))

    accx, accy, accz = acc.T
    psasx, psasy, psasz = psas.T
    psanx, psany, psanz = psan.T
    pnasx, pnasy, pnasz = pnas.T
    pnanx, pnany, pnanz = pnan.T

    fig = go.Figure(data=[go.Mesh3d(name='Accuracy', x=accx, y=accy, z=accz, color='red', opacity=0.50),
                          go.Mesh3d(name='PSAS', x=psasx, y=psasy, z=psasz, color='blue', opacity=0.50),
                          go.Mesh3d(name='PSAN', x=psanx, y=psany, z=psanz, color='green', opacity=0.50),
                          go.Mesh3d(name='PNAS', x=pnasx, y=pnasy, z=pnasz, color='yellow', opacity=0.50),
                          go.Mesh3d(name='PNAN', x=pnanx, y=pnany, z=pnanz, color='purple', opacity=0.50)])
    fig.update_traces(showlegend = True)
    fig.update_layout(
        scene = dict(
            xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(len(labels))),
                ticktext = labels
            ),
            yaxis = dict(
                tickmode = 'array',
                tickvals = list(range(len(labels))),
                ticktext = labels
            ),
            xaxis_title='Data set',
            yaxis_title='Model',
            zaxis_title='Percent'
        )
    )
    fig.show()


if __name__ == '__main__':
    main()
