from django.shortcuts import render
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from traceback import format_exc
from django.conf import settings
import text_to_image
import PIL
from PIL import Image
import os
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request,'index.html')


def encrypt(request):
    if request.method=='POST':
        
        input_value = request.POST['iptextarea']
        input_value = str(input_value)
        inp_conversion = Fernet(settings.ENCRYPT_KEY)
        encrypt_text = inp_conversion.encrypt(input_value.encode('ascii'))
        encrypted_text = base64.urlsafe_b64encode(encrypt_text).decode('ascii')
        
        encrypted_image = text_to_image.encode(encrypted_text,'image.png') #converting encrypted data into image
        encrypted_image = Image.open(encrypted_image) #converted

        #encrypted_image = encrypted_image.resize((300,300))
        image_path = 'C:/Users/Ganesh vamsi/MY PROJECTS/image-encrypt-decrypt/image_en_de/static/temp_img/image.png'
        encrypted_image.save(image_path,'PNG') #saving the image temporarly
        '''
        image = PIL.Image.open(image_path)
        w,h=image.size
        print('44444444444555555',w,h)
        image.close()
        '''
        with open(image_path,'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        ctx = dict()
        ctx['encrypted_image'] = image_data
        os.remove(image_path,dir_fd=None)
        sentence = 'Download the below encrypted image'
        ctx['sentence']=sentence
        ctx['enalbe_disable'] = 'enabled' #output and download btn visibility
        return render(request,'encrypt.html',ctx)
    return render(request,'encrypt.html',{'enalbe_disable':'disabled'})

def decrypt(request):
    if request.method=='POST': 

        try:
            encrypted_image = request.FILES['uploadedimage']
        except:
            return render(request,'decrypt_image.html')
        
        fs = FileSystemStorage()
        filename = fs.save(encrypted_image.name,encrypted_image)
        uploaded_file_url = fs.url(filename)
        img_path = 'C:/Users/Ganesh vamsi/MY PROJECTS/image-encrypt-decrypt/image_en_de/temp_op_img/'+filename
        #img_path=img_path
        decrypted_data = text_to_image.decode(img_path)
        try:
            encrypted_value = base64.urlsafe_b64decode(decrypted_data)
            decryption_value = Fernet(settings.ENCRYPT_KEY)
            decryted_text = decryption_value.decrypt(encrypted_value).decode('ascii')
            sentence = 'He/she wants to say : ' 
            os.remove(img_path,dir_fd=None)
            return render(request,'decrypt_image.html',{'sentence':sentence,'decrypt_text':decryted_text})
        except Exception as e:
            logging.getLogger('error_logger').error(traceback.format_exc())
            sentence = 'encrypted code u enteres is wrong please check it once'
            os.remove(img_path,dir_fd=None)
            return render(request,'decrypt_image.html',{'sentence':sentence,'decrypt_text':'  '})

    return render(request,'decrypt_image.html')




'''

def decrypt(request):
    if request.method=='POST':
        encrypted_value = request.POST['optextarea']
        try:
            encrypted_value = base64.urlsafe_b64decode(encrypted_value)
            decryption_value = Fernet(settings.ENCRYPT_KEY)
            decryted_text = decryption_value.decrypt(encrypted_value).decode('ascii')
            print('***********************',decryted_text)
            sentence = 'He/she wants to say : ' 

            return render(request,'decrypt_image.html',{'sentence':sentence,'decrypt_text':decryted_text})
        except Exception as e:
            logging.getLogger('error_logger').error(traceback.format_exc())
            sentence = 'encrypted code u enteres is wrong please check it once'
            return render(request,'decrypt_image.html',{'sentence':sentence,'decrypt_text':'  '})

    return render(request,'decrypt_image.html')



'''