from PIL import Image
import face_recognition

input_folder = ".\\input\\"
intput_file_name = input_folder + "2.png"
input_image = face_recognition.load_image_file(intput_file_name)
face_locations = face_recognition.face_locations(input_image, number_of_times_to_upsample=0, model="cnn")
print("{} faces found.".format(len(face_locations)))

output_folder = ".\\output\\"
for (iter, raw_face) in enumerate(face_locations):
    top, right, bottom, left = raw_face
    print("Face #{} is located at T:{}//L:{}//B:{}//R:{}.".format(iter, top, left, bottom, right))
    scaling_x = int((right - left) / 5)
    scaling_y = int((bottom - top) / 4)
    _each_face_image = input_image[top-scaling_y:bottom+scaling_y, left-scaling_x:right+scaling_x]
    each_face_image = Image.fromarray(_each_face_image)
    output_filename = intput_file_name + "-" + str(iter) + ".png"
#   each_face_image.save(output_filename, None, "append")
    each_face_image.save(output_filename)
    