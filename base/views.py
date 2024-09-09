from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from  .models import RoomMember
from django.views.decorators.csrf import csrf_exempt


def getToken(request):
    appId='39d298fe511f4b0a84c44ff4f00729be'
    appCertificate ='066ee9fe14d44688bbbf24f2a42840a5'
    channelName= request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeSeconds= 3600*24
    currentTimeStamp= time.time()
    privilegeExpiredTs= currentTimeStamp + expirationTimeSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid },safe=False)
# Create your views here.
def lobby(request):
    return render(request,'base/lobby.html')

# def room(request):
#     return render(request,'base/room.html')
def room(request, room_name):
    context = {'room_name': room_name}
    return render(request, 'base/room.html', context)

@csrf_exempt
def createMember(request):
    data=json.loads(request.body)
    member,created= RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']},safe=False)


# def getMember(request):
#     uid =request.GET.get('uid')
#     room_name=request.GET.get('room_name')

#     member=RoomMember.objects.get(
#         uid=uid,
#         room_name=room_name
#     )

#     name=member.name
#     return JsonResponse({'name':member.name},safe=False)
def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

    return JsonResponse({'name': member.name}, safe=False)



# @csrf_exempt
# def deleteMember(request):
#     data=json.loads(request.body)

#     member= RoomMember.objects.get(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )
#     member.delete()
#     return JsonResponse('Member deleted',safe=False)
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

    return JsonResponse({'message': 'Member deleted'}, safe=False)
