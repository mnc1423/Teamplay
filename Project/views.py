from django.shortcuts import render

# Create your views here.
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect , get_object_or_404
import urllib
from django.urls import reverse
from django.utils import timezone
# 페이지네이션 구현
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def auth_test(request):
    try:
        check={'project_name' : request.session['project_name']}
        check['user_name'] = request.session['user_name']
    except:
        check = False
    return check




# 모두의 팀플 처음 접속 화면 함수
def moduMain(request):
    check = auth_test(request)
    if request.method == 'POST' and 'btn1' in request.POST: # request.method == 'POST' and 'btn1' in request.POST
        form = ProjectForm(request.POST)
        return redirect('projectMake')
    elif request.method == 'POST' and 'btn2' in request.POST:
        form = ProjectForm(request.POST)
        return redirect('join')

    else:
        form = ProjectForm(request.POST)
        return render(request, 'Project/main.html', {'form': form, 'check':check})





# 프로젝트 생성 함수
def projectMake(request):
    check = auth_test(request)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        project_name_input = str(request.POST['project_name'])
        user_Qset = Projects.objects.filter(project_name=project_name_input)  # 이미 등록되있는경우 중복가입 x (로그인함수 설명보기)
        if len(user_Qset) == 1:  # 길이를 사용하는 이유 로그인함수에서 설명되있음.
            messages.error(request, 'duplicate account is not allowed')
            return redirect('projectMake')

        if form.is_valid():
            form.save()  # 회원이 입력한 폼 저장
            return redirect('makeAdmin')
    else:
        form = ProjectForm()
        return render(request, 'Project/projectMake.html', {'check':check, 'form': form})




# 프로젝트 생성시 admin계정 만드는 함수
def makeAdmin(request):
    check = auth_test(request)
    if request.method == "POST":
        form = InviteForm(request.POST)
        project_name_input = str(request.POST['project_name'])

        project_Qset = Projects.objects.filter(project_name=project_name_input)  # 같은 프로젝트 이름을 입력하지 않은 경우
        if len(project_Qset) == 0:  # 길이를 사용하는 이유 로그인함수에서 설명되있음.
            messages.error(request, 'please write project name same')
            return redirect('makeAdmin')

        elif form.is_valid():
            form.save()  # 회원이 입력한 폼 저장
            return redirect('join')
    else:
        form = InviteForm()
        return render(request, 'Project/makeAdmin.html', {'check':check, 'form': form})




# 프로젝트 접속 함수
def join(request):
    check = auth_test(request)

    if request.method == "POST":
        form = JoinForm(request.POST)  # form = email, password
        user_name_input = str(request.POST['user_name'])  # 사용자가 사용자이름
        project_name_input = str(request.POST['project_name'])  # 사용자가 입력한 프로젝트 이름
        project_password_input = str(request.POST['project_password'])  # 사용자가 입력한 프로젝트 비밀번호
        user_Qset = ProjectUser.objects.filter(project_name=project_name_input, user_name=user_name_input)  # 데이터베이스에서 사용자가 프로젝트이름과 일치하는 프로젝트행 가져옴
        project_Qset = Projects.objects.filter(project_name=project_name_input)
        project_name = project_name_input

        if len(user_Qset) == 0:  # 데이터베이스에 일치하는 프로젝트가 있으면 len ==1, 없으면 0 // 존재하든 안하든 쿼리셋 객체는 생성이 되는데, 일치하는 학번이 없으면 안이 비어서 길이가 0
            messages.error(request, 'login failed, wrong user name or not registrated name or you are not in this project')
            return redirect('join')

        if len(project_Qset) != 0:
            password_saved = str(project_Qset.values('project_password')[0]['project_password'])
            project_root = str(project_Qset.values('project_root')[0]['project_root'])

            if project_password_input == password_saved:  # 입력비밀번호 == DB에 저장된 비밀번호
                request.session.modified = True  # 세션 수정여부 True(세션 = 쿠키의 암호화 버전)

                # request.session['cookie key'] = 'value' (session은 dictionary 형태)
                request.session['project_name'] = user_Qset.values('project_name')[0]['project_name']
                request.session['user_name'] = user_Qset.values('user_name')[0]['user_name']

                return redirect(reverse('mainProject', kwargs={'project_name':project_name})) #'project_root' : project_root,
            else:
                messages.error(request, 'join failed, wrong project password')
                return redirect('join')

    else:
        form = JoinForm()
        return render(request, 'Project/joinProject.html', {'check':check,'form': form})


def allMainProject(request, project_name):
    check = auth_test(request)
    posts = ProjectFiles.objects.filter(project_name=project_name)
    posts = posts.order_by('-origin_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'Project/projectMain.html', {
        'project_name': project_name,
        'posts': posts,
        'check ': check,
        'max_index': max_index, })


#mainporoject 페이지!
def mainProject(request, project_name):
    check = auth_test(request)
    print(check['project_name'])
    #project_Qset = Projects.objects.filter(project_name=check['project_name'])
    project_Qset = get_object_or_404(Projects, project_name=check['project_name'])

    #  Project의 project_root 와 같은 ProjectFiles에서  parent_file_id, file_id 의 값이 동일한 게시물만 보여줌
    #if project_Qset.values('project_root')[0]['project_root'] != None:
    if project_Qset.project_root != None:
        project_Qset = Projects.objects.filter(project_name=project_name)
        print(project_Qset)
        project_root = str(project_Qset.values('project_root')[0]['project_root'])
        parent = ProjectFiles.objects.filter(file_id = project_root)
        children = ProjectFiles.objects.filter(parent_file_id = project_root)
        posts = parent | children #queryset merge
        posts = posts.order_by('-origin_date')

        paginator = Paginator(posts, 6)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
            print("PageNotAnInteger")
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        max_index = len(paginator.page_range)
        return render(request, 'Project/projectMain.html', {
            'project_name': project_name,
            'posts': posts,
            'check ': check,
            'max_index': max_index, })


    #모든 게시물들을 보여줌
    else:
        check = auth_test(request)
        posts = ProjectFiles.objects.filter(project_name = project_name)
        print(posts)
        posts = posts.order_by('-origin_date')
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
            print("PageNotAnInteger")
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        max_index = len(paginator.page_range)
        return render(request, 'Project/projectMain.html', {
                'project_name': project_name,
                'posts': posts,
                'check ' : check,
                'max_index': max_index,})

#메인 브랜치(루트) 설정하는 함수
def setBranch(request, project_name):
    check = auth_test(request)
    post = get_object_or_404(Projects, project_name=project_name)
    project_name = post.project_name

    if request.method == "POST":
        form = BranchSetForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    else:
        form = BranchSetForm(instance=post)
    return render(request, 'Project/projectBranch.html', {'project_name' : project_name, 'post': post,'form': form, 'check':check})



def newFile(request, project_name):
    check = auth_test(request)
    if request.method == "GET":
        form = FileForm()
    elif request.method == "POST":
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.origin_date = timezone.now()
            post.final_date = timezone.now()
            post.user_name=check['user_name']
            post.project_name=check['project_name']
            post.save()
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    ctx = {
        'project_name' : project_name,
        'form': form,
        'check': check
    }
    return render(request, 'Project/projectEdit.html', ctx)



def del_file(old_file, new_file):
    if old_file != new_file:
        old_file.delete()
    return new_file


def editFile(request, project_name, file_title):
    check = auth_test(request)
    post = get_object_or_404(ProjectFiles, file_title=file_title)
    old_file=post.file
    if request.method == "POST":
        form = FileForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.final_date = timezone.now()
            new_file=post.file
            post.file=del_file(old_file, new_file)
            post.save()
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    else:
        form = FileForm(instance=post)
    return render(request, 'Project/projectEdit.html', {'project_name': project_name, 'post': post,'form': form, 'check': check})



def fileDetail(request, project_name, file_title):
    check = auth_test(request)
    post = get_object_or_404(ProjectFiles, project_name=project_name, file_title=file_title)
    return render(request, 'Project/projectDetail.html', {'post': post, 'check': check,
                                                          'file_title': file_title,
                                                          'project_name': project_name,})



def fileRemove(request, project_name, file_title):
    post = get_object_or_404(ProjectFiles, project_name=project_name, file_title=file_title)
    post.delete()
    return redirect(reverse('mainProject', kwargs={'project_name': project_name}))



#memo함수
def memo(request, project_name):
    check = auth_test(request)
    post = get_object_or_404(Projects, project_name=project_name)
    if check==False:
        return render(request, 'Project/mainProject.html')

    if request.method == "POST":
        form = MemoForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    else:
        form = MemoForm(instance=post)
    return render(request, 'Project/memo.html', {'project_name' : project_name,'post': post,'form': form, 'check':check})




#일정 함수 (project_edit함수 참고)
def schedule(request, project_name):
    check = auth_test(request)
    post = get_object_or_404(Projects, project_name=project_name)
    if check==False:
        return render(request, 'Project/mainProject.html')

    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    else:
        form = ScheduleForm(instance=post)
    return render(request, 'Project/schedule.html', {'project_name' : project_name,'post': post,'form': form, 'check':check})




#팀원관리 함수
def members(request, project_name):
    check = auth_test(request)

    if request.method == "POST":
        form = InviteForm(request.POST)
        user_name_input = str(request.POST['user_name'])
        project_name_input = request.session['project_name']
        user_Qset = ProjectUser.objects.filter(user_name=user_name_input)  # 이미 등록되있는경우 중복가입 x (로그인함수 설명보기)

        if len(user_Qset) == 1:  # 길이를 사용하는 이유 로그인함수에서 설명되있음.
            messages.error(request, 'Registrating duplicate name is not allowed')
            return redirect(reverse('members', kwargs={'project_name': project_name}))

        if (project_name != project_name_input):
            messages.error(request, '현재 프로젝트에서 다른 프로젝트로 접근할 수 없습니다!!')
            return redirect(reverse('members', kwargs={'project_name': project_name}))

        if form.is_valid():
            form.save()  # 회원이 입력한 폼 저장
            return redirect(reverse('mainProject', kwargs={'project_name': project_name}))
    else:
        form = InviteForm()
        return render(request, 'Project/members.html', {'project_name': project_name, 'check': check, 'form': form})





#관리자 비밀번호 체크 함수 (members설정)
def adminCertificate(request, project_name):
    check = auth_test(request)

    if request.method == "POST":
        form = AdminCertificationForm(request.POST)
        #project_name_input = str(request.session['project_name'])
        admin_password_input = str(request.POST['admin_password'])
        project_Qset = Projects.objects.filter(project_name=project_name)

        if len(project_Qset) != 0:
            password_saved = str(project_Qset.values('admin_password')[0]['admin_password'])
            print(password_saved)

            if admin_password_input == password_saved:  # 입력비밀번호 == DB에 저장된 비밀번호
                return redirect(reverse('members', kwargs={'project_name':project_name}))
            else:
                messages.error(request, 'Wrong admin password')
                return redirect(reverse('adminCertification', kwargs={'project_name': project_name}))

    else:
        form = AdminCertificationForm()
        return render(request, 'Project/projectAdminCertification.html', {'project_name': project_name, 'check':check, 'form': form})


#관리자 비밀번호 체크 함수 (브랜치설정)
def branchAdminCertificate(request, project_name):
    check = auth_test(request)

    if request.method == "POST":
        form = AdminCertificationForm(request.POST)
        #project_name_input = str(request.session['project_name'])
        admin_password_input = str(request.POST['admin_password'])
        project_Qset = Projects.objects.filter(project_name=project_name)

        if len(project_Qset) != 0:
            password_saved = str(project_Qset.values('admin_password')[0]['admin_password'])
            print(password_saved)

            if admin_password_input == password_saved:  # 입력비밀번호 == DB에 저장된 비밀번호
                return redirect(reverse('setBranch', kwargs={'project_name': project_name}))
            else:
                messages.error(request, 'Wrong admin password')
                return redirect(reverse('branchAdminCertification', kwargs={'project_name': project_name}))

    else:
        form = AdminCertificationForm()
        return render(request, 'Project/projectAdminCertification.html', {'project_name': project_name, 'check':check, 'form': form})


"""
def logout(request):
    del request.session['project_name']
    del request.session['user_name']  # 세션 삭제
    return redirect('moduMain')
    """
