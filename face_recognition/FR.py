import cv2 as cv
import face_recognition as fr
import shutil
import os

def encode_faces(folder):
  encoded_faces = []

  for file in os.listdir(folder):
    curr_image = cv.imread(f'{folder}/{file}')
    face_encoding = fr.face_encodings(curr_image)[0]
    person_name = file.split('.')[0]

    encoded_faces.append((face_encoding, person_name))

  return encoded_faces

def create_frame(image, location, label):
  top, right, bottom, left = location
  cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
  cv.rectangle(image, (left, bottom + 20), (right, bottom), (255, 0, 0), cv.FILLED)
  cv.putText(image, label, (left + 3, bottom + 14), cv.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)

def get_face_name(face_to_check):
  for registered_person in encode_faces(r'faces_to_register'):
    encoded_face = registered_person[0]
    name = registered_person[1]
    
    is_registered = fr.compare_faces([encoded_face], face_to_check)
    if is_registered[0]:
      return name
  
  return 'Unknown'

def label_all_faces(file_path):
  image_to_check = cv.imread(file_path)
  all_faces = fr.face_encodings(image_to_check)
  face_locations = fr.face_locations(image_to_check)

  for i in range(len(all_faces)):
    curr_face = all_faces[i]
    curr_face_location = face_locations[i]
    face_name = ' '.join(get_face_name(curr_face).split('_'))

    create_frame(image_to_check, curr_face_location, face_name) 

  cv.imshow('hey', image_to_check)
  cv.waitKey(0)

def get_all_registered_names(folder_path):
  return [' '.join(name.split('.')[0].split('_')) for name in os.listdir(folder_path)]


def make_folders():
  for name in get_all_registered_names(r'faces_to_register/'):
    folder_name = '_'.join(name.split())
    if not os.path.exists(folder_name):
      os.mkdir(folder_name)

  if not os.path.exists('Unknown'):
    os.mkdir('Unknown')

def move_faces_to_folders(folder_path):
  """Creates folders for all registered faces
     then moves images to them If it detected a face. 

  Args:
      folder_path (str): folder path that contains images you want to check and move
  """
  make_folders()

  for file in os.listdir(folder_path):
    image_path = f'{folder_path}/{file}'
    image = cv.imread(image_path)
    all_faces = fr.face_encodings(image)

    for i in range(len(all_faces)):
      curr_face = all_faces[i]
      face_name = get_face_name(curr_face)
      print(f'{face_name} DETECTED!!')

      shutil.copy(image_path, f'{face_name}/{file}')
      print(f'Copied Image from {image_path} to {face_name}/{file}\n\n')


move_faces_to_folders(r'testing')

# for file in os.listdir(r'testing/'):
#   print(file)
#   label_all_faces(r'testing/' + file)
