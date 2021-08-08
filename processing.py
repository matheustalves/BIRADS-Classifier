import numpy as np
from PIL import Image, ImageOps
import os
import glob
import random
from skimage.feature import greycomatrix, greycoprops
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import time

def classify(descriptors, distances, angles, resolutions, quantizations, input_image = None):
	sample_folders = os.listdir("Dataset")

	train_features = []
	train_labels = []

	test_features = []
	test_labels = []

	for label in sample_folders:
		cur_path = "Dataset/" + label
		
		temp_dataset = glob.glob(cur_path + "/*.png")
		random.shuffle(temp_dataset)
		temp_train, temp_test = train_test_split(temp_dataset, train_size = int(0.75*len(temp_dataset)))

		for file in temp_train:
			img = Image.open(file)
			img = ImageOps.equalize(img)
			w, h = img.size

			tmp_matrix = []

			for descriptor in descriptors:
				for resolution in resolutions:
					if w != resolution:
						img.resize((resolution, resolution))

					for quantization in quantizations:
						img = img.quantize(quantization)
						np_img = np.array(img)

						glcm = greycomatrix(np_img, distances=distances, angles=angles, levels=quantization, symmetric=True, normed=True)

						tmp_matrix.append(greycoprops(glcm, descriptor).flatten())

			train_features.append(np.array(tmp_matrix))
			train_labels.append(int(label))

		for file in temp_test:
			img = Image.open(file)
			img = ImageOps.equalize(img)
			w, h = img.size

			tmp_matrix = []

			for descriptor in descriptors:
				for resolution in resolutions:
					if w != resolution:
						img.resize((resolution, resolution))
						
					for quantization in quantizations:
						img = img.quantize(quantization)
						np_img = np.array(img)

						glcm = greycomatrix(np_img, distances=distances, angles=angles, levels=quantization, symmetric=True, normed=True)

						tmp_matrix.append(greycoprops(glcm, descriptor).flatten())


			test_features.append(np.array(tmp_matrix))
			test_labels.append(int(label))


	# Prepara Imagem ou recorte escolhido para classificação
	chosen_img_features = []

	if input_image != None:
		img = ImageOps.equalize(input_image)
		w, h = img.size

		for descriptor in descriptors:
			for resolution in resolutions:
				if w != resolution:
					img.resize((resolution, resolution))

				for quantization in quantizations:
					img = img.quantize(quantization)
					np_img = np.array(img)

					glcm = greycomatrix(np_img, distances=distances, angles=angles, levels=quantization, symmetric=True, normed=True)

					chosen_img_features.append(greycoprops(glcm, descriptor).flatten())

	chosen_img_features = np.array(chosen_img_features)

	print("[STATUS] Construindo o classificador...")
	clf_svm = LinearSVC(dual=False, max_iter=2000)

	train_features = np.array(train_features)
	train_labels = np.array(train_labels)

	test_features = np.array(test_features)
	test_labels = np.array(test_labels)

	nsamples, nx, ny = train_features.shape
	d2_train_dataset = train_features.reshape((nsamples, nx*ny))

	print("[STATUS] Treinando o classificador...")
	clf_svm.fit(d2_train_dataset, train_labels)

	correct_sum = 0

	conf_matrix = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

	# Predict Test samples
	for i in range(len(test_features)):
		prediction = clf_svm.predict(test_features[i].reshape(1,-1))[0]
		
		if prediction.astype(int) == test_labels[i]:
			correct_sum += 1

		conf_matrix[test_labels[i]][prediction.astype(int)] += 1

	especificidade = 0
	for i in range(0,4):
		for j in range(0, 4):
			if j != i:
				especificidade += conf_matrix[j][i]/300 

	especificidade = 1 - especificidade

	print(f"Classificações corretas no dataset de teste: {correct_sum}")
	print(f"Acurácia: {correct_sum/len(test_features)}")
	print(f"Matriz de Confusão: \n {conf_matrix}")
	print(f"Especificidade: {especificidade}")

	chosen_prediction = clf_svm.predict(chosen_img_features.reshape(1,-1))[0]
	print(f"Classificação da Imagem: {chosen_prediction}")
