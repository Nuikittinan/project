
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from .serializers import TodolistSerializer, UserSerializer
from .models import Todolist
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login
#GET Data
@api_view(['GET'])
def all_todolist(request):
    alltodolist = Todolist.objects.all() #ดึงข้อมูลจาก model Todolist 
    serializer = TodolistSerializer(alltodolist,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)





@api_view(['POST'])
def post_todolist(request):
    if request.method == 'POST':
        serializer = TodolistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_todolist(request,TID):
    todo = Todolist.objects.get(id=TID)
    if request.method == 'PUT':
        data ={}
        serializer = TodolistSerializer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['status'] = 'updated'
            return Response(data=data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_todolsit(request,TID):
    todo = Todolist.objects.get(id=TID)
    if request.method == 'DELETE':
        delete = todo.delete()
        data = {}
        if delete:
            data['status']='deleted'
            statuscode = status.HTTP_200_OK
        else:
            data['status']='failed'
            statuscode =status.HTTP_400_BAD_REQUEST
        return Response(data=data,status=statuscode)

@api_view(['POST', 'GET'])
def register_app(request):
    if request.method == 'POST':
        data = request.data.copy()
        username = data.get('username')
        password = data.get('password')
        userclass = data.get('userclass')
        firstname = data.get('first_name')
        print(data)
        if username != '' and password != ''and firstname != '':

            # Create User ระดับทั่วไป สามารถดูข้อมูลต่าง ๆ ได้แต่ไม่สามารถแก้ไขหรือ Add User คนอื่น ๆ ได้
            if userclass == 'User':
                try:
                    user = User.objects.create_user(username = username, password = password,firstname = firstname)
                    user.save()
                    return Response(status = status.HTTP_201_CREATED)
                except:
                    return Response(status = status.HTTP_400_BAD_REQUEST)


            else:
                try:
                    user = User.objects.create_superuser(username = username, password = password,first_name = firstname)
                    user.save()
                    return Response(status = status.HTTP_201_CREATED)
                except:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
@api_view(['POST', 'GET'])
def login_app(request):
    if request.method == 'POST':
        try:
            data = request.data.copy()
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                # Check user input ว่าเป็น SuperUser หรือไม่
                alldata_get = User.objects.get(username = username)
                serializer = UserSerializer(alldata_get)
                # เป็น SupurUser return True
                if serializer.data['is_superuser'] == True:
                    return Response(serializer.data['is_superuser'], status = status.HTTP_200_OK)
                # ไม่เป็น SupurUser return false
                else:
                    return Response(serializer.data['is_superuser'], status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)




data = [
    {
        "title":"labtop คืออะไร?",
        "subtitle":"คอมพิวเตอร์ คือ อุปกรณ์ที่ใช้สำหรับการคำนวณและทำงานอื่นๆ?",
        "image_url":"https://raw.githubusercontent.com/Nuikittinan/BasicAPI/main/computer.jpg",
        "detail":"คอมพิวเตอร์มาจากภาษาละตินว่า Computare ซึ่งหมายถึง การนับ หรือ การคำนวณพจนานุกรม ฉบับราชบัณฑิตยสถาน พ.ศ. 2525 ให้ความหมายของคอมพิวเตอร์ไว้ว่า/n/nเครื่องอิเล็กทรอนิกส์แบบอัตโนมัติ ทำหน้าที่เหมือนสมองกล ใช้สำหรับแก้ปัญหาต่างๆ ที่ง่ายและซับซ้อนโดยวิธีทางคณิตศาสตร์\n\nคอมพิวเตอร์ จึงเป็นเครื่องจักรอิเล็กทรอนิกส์ที่ถูกสร้างขึ้นเพื่อใช้ทำงานแทนมนุษย์ ในด้านการคิดคำนวณและสามารถจำข้อมูล ทั้งตัวเลขและตัวอักษรได้เพื่อการเรียกใช้งานในครั้งต่อไป  นอกจากนี้ ยังสามารถจัดการกับสัญลักษณ์ได้ด้วยความเร็วสูง โดยปฏิบัติตามขั้นตอนของโปรแกรม คอมพิวเตอร์ยังมีความสามารถในด้านต่างๆ อีกมาก อาทิเช่น การเปรียบเทียบทางตรรกศาสตร์ การรับส่งข้อมูล การจัดเก็บข้อมูลในตัวเครื่องและสามารถประมวลผลจากข้อมูลต่างๆ ได้ การทำงานของคอมพิวเตอร์"
    },
    {
        "title":"มาเขียนโปรแกรมกัน!",
        "subtitle":"บทความนี้จะแนะนำการเริ่มต้นเขียนโปรแกรม",
        "image_url":"https://raw.githubusercontent.com/Nuikittinan/BasicAPI/main/program.jpg",
        "detail":"การเขียนโปรแกรมคอมพิวเตอร์ (อังกฤษ: Computer programming) หรือเรียกให้สั้นลงว่า การเขียนโปรแกรม (อังกฤษ: Programming) หรือ การเขียนโค้ด (Coding) เป็นขั้นตอนการเขียน ทดสอบ และดูแลซอร์สโค้ดของโปรแกรมคอมพิวเตอร์ ซึ่งซอร์สโค้ดนั้นจะเขียนด้วยภาษาโปรแกรม ขั้นตอนการเขียนโปรแกรมต้องการความรู้ในหลายด้านด้วยกัน เกี่ยวกับโปรแกรมที่ต้องการจะเขียน และขั้นตอนวิธีที่จะใช้ ซึ่งในวิศวกรรมซอฟต์แวร์นั้น การเขียนโปรแกรมถือเป็นเพียงขั้นหนึ่งในวงจรชีวิตของการพัฒนาซอฟต์แวร์"
    },
    {
        "title":"Flutter คือ?",
        "subtitle":"Tools สำหรับออกแบบ UI ของ Google",
        "image_url":"https://raw.githubusercontent.com/Nuikittinan/BasicAPI/main/app.jpg",
        "detail":"Flutter คือ Framework ที่ใช้สร้าง UI สำหรับ mobile application ที่สามารถทำงานข้ามแพลตฟอร์มได้ทั้ง iOS และ Android ในเวลาเดียวกัน โดยภาษาที่ใช้ใน Flutter นั้นจะเป็นภาษา dart ซึ่งถูกพัฒนาโดย Google และที่สำคัญคือเป็น open source ที่สามารถใช้งานได้แบบฟรี ๆ อีกด้วย"
    }
   

]

def Home(request):
    return JsonResponse(data=data,safe=False,json_dumps_params={'ensure_ascii': False})

# Create your views here.
